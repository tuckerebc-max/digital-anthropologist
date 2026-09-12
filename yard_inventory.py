"""Read-only, explicitly scoped recovery inventory; Python 3.11+, Git required."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit, urlunsplit

SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.next',
        '.cache', 'site-packages', 'target', 'dist', 'vendor', '.tox'}
CODE = {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.ps1', '.sh'}
TOKEN = re.compile(r'(?i)(?:github_pat_|gh[pousr]_|sk[-_]|lr[-_])[a-z0-9_-]{16,}')


def display_path(path):
    value = str(path)
    if value.startswith('\\\\?\\UNC\\'):
        return '\\\\' + value[8:]
    return value.removeprefix('\\\\?\\')


def filesystem_path(path):
    value = os.path.abspath(path)
    if os.name == 'nt' and not value.startswith('\\\\?\\'):
        value = '\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value
    return Path(value)


def redact(value):
    return TOKEN.sub('[REDACTED]', str(value))


def safe_remote(value):
    if '://' in value:
        try:
            parsed = urlsplit(value)
            host = parsed.hostname or ''
            if ':' in host:
                host = '[' + host + ']'
            port = ':' + str(parsed.port) if parsed.port else ''
            return redact(urlunsplit((parsed.scheme, host + port, parsed.path, '', '')))
        except ValueError:
            return '[INVALID_REMOTE]'
    return redact(value.split('?', 1)[0].split('#', 1)[0])


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]


def git(path, *args):
    result = subprocess.run(
        ['git', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false',
         '-c', 'core.longpaths=true', '-C', str(path), *args],
        capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20,
        env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0'},
    )
    return result.returncode, result.stdout


def inspect_repository(path):
    label = redact(display_path(path))
    try:
        status_code, status = git(path, 'status', '--porcelain=v1', '-z', '--untracked-files=normal')
        if status_code:
            return {'path': label, 'error': 'git_status_failed', 'exit_code': status_code}

        def read(*args):
            code, value = git(path, *args)
            return value.strip() if not code else None

        head = read('rev-parse', '--verify', 'HEAD')
        branch = read('symbolic-ref', '--quiet', '--short', 'HEAD')
        common = read('rev-parse', '--path-format=absolute', '--git-common-dir')
        if common is None:
            return {'path': label, 'error': 'git_identity_failed'}
        remote_names = (read('remote') or '').splitlines()
        remotes = []
        for name in remote_names:
            url = read('remote', 'get-url', name) or ''
            kind = 'network' if ('://' in url and not url.startswith('file://')) or re.match(r'^[^/\\]+@[^:]+:', url) else 'local'
            remotes.append({'name': redact(name), 'url': safe_remote(url), 'kind': kind})
        origin = next((r['url'] for r in remotes if r['name'] == 'origin'), '')
        remote_kind = 'network' if any(r['kind'] == 'network' for r in remotes) else 'local' if remotes else 'none'
        upstream = read('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
        ahead = behind = None
        if head and upstream:
            counts = read('rev-list', '--left-right', '--count', 'HEAD...@{u}')
            if counts:
                ahead, behind = map(int, counts.split())
        entries = iter(status.split('\0'))
        tracked = untracked = 0
        for entry in entries:
            if not entry:
                continue
            if entry[:2] == '??':
                untracked += 1
            else:
                tracked += 1
                if 'R' in entry[:2] or 'C' in entry[:2]:
                    next(entries, None)
        reasons = []
        if tracked or untracked:
            reasons.append('working_copy_changes')
        if not remotes:
            reasons.append('no_remote')
        elif remote_kind == 'local':
            reasons.append('local_remote_only')
        if head and not upstream:
            reasons.append('no_upstream')
        if ahead:
            reasons.append('ahead_of_local_upstream')
        state = 'unborn' if not head else 'branch' if branch else 'detached'
        if state != 'branch':
            reasons.append(state)
        safe_origin = safe_remote(origin)
        revision_origin = next((r['url'] for r in remotes if r['kind'] == 'network'), safe_origin)
        return {
            'path': label, 'repository_id': digest(os.path.normcase(display_path(common))),
            'revision_group': digest((revision_origin or 'unassigned') + ':' + (head or common)),
            'head': head, 'branch': redact(branch) if branch else None, 'branch_state': state,
            'head_committed_at': read('show', '-s', '--format=%cI', 'HEAD') if head else None,
            'origin': safe_origin, 'remotes': remotes, 'remote_kind': remote_kind,
            'upstream': redact(upstream) if upstream else None,
            'ahead_of_local_upstream': ahead, 'behind_local_upstream': behind,
            'tracked_changes': tracked, 'untracked_entries': untracked,
            'publication': 'unknown', 'remote_observed_at': None,
            'review_reasons': reasons,
        }
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return {'path': label, 'error': type(exc).__name__}


def scan(roots, *, study_id):
    """Collect metadata only; never fetch, run recovered files, or mutate repositories."""
    if not study_id or not study_id.strip():
        raise ValueError('A study identifier is required')
    roots = list(dict.fromkeys(filesystem_path(p) for p in roots))
    if not roots:
        raise ValueError('At least one explicit root is required')
    errors, repos, loose = [], [], []
    visited = set()
    skipped_links = skipped_bare = 0

    for root in roots:
        if not root.is_dir():
            errors.append({'path': redact(display_path(root)), 'error': 'missing_or_non_directory_root'})
            continue
        try:
            if root.is_symlink() or getattr(root.lstat(), 'st_file_attributes', 0) & 1024:
                skipped_links += 1
                continue
        except OSError as exc:
            errors.append({'path': redact(display_path(root)), 'error': type(exc).__name__})
            continue
        # A scoped subtree can already be inside a repository outside the scope.
        # Avoid classifying its code as unversioned without expanding that scope.
        code, _ = git(root, 'rev-parse', '--show-toplevel')
        stack = [(root, code == 0)]
        while stack:
            path, in_repo = stack.pop()
            identity = os.path.normcase(str(path))
            if identity in visited:
                continue
            visited.add(identity)
            try:
                info = path.lstat()
                if path.is_symlink() or getattr(info, 'st_file_attributes', 0) & 1024:
                    skipped_links += 1
                    continue
                with os.scandir(path) as entries:
                    entries = list(entries)
                names = {e.name for e in entries}
                if '.git' in names:
                    repos.append(path)
                    in_repo = True
                if {'HEAD', 'config', 'objects', 'refs'}.issubset(names):
                    skipped_bare += 1
                    continue
                code_files = [e.name for e in entries if e.is_file(follow_symlinks=False)
                              and Path(e.name).suffix.lower() in CODE]
                if code_files and not in_repo:
                    loose.append({'path': redact(display_path(path)), 'code_files': len(code_files),
                                  'examples': [redact(n) for n in sorted(code_files)[:3]],
                                  'disposition': 'unversioned_review_candidate'})
                for entry in reversed(sorted(entries, key=lambda e: e.name)):
                    if entry.name in SKIP:
                        continue
                    if entry.is_symlink():
                        skipped_links += 1
                    elif entry.is_dir(follow_symlinks=False):
                        stack.append((Path(entry.path), in_repo))
            except OSError as exc:
                errors.append({'path': redact(display_path(path)), 'error': type(exc).__name__})

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(inspect_repository, sorted(repos)))
    for result in results:
        if result.get('error'):
            errors.append(result)
    valid = [r for r in results if not r.get('error')]
    return {
        'schema_version': 1, 'study_id': redact(study_id),
        'observed_at_utc': datetime.now(timezone.utc).isoformat(),
        'roots': [redact(display_path(p)) for p in roots],
        'mode': 'read_only_local_metadata', 'privacy': 'local_private',
        'summary': {'checkouts': len(valid), 'repository_identities': len({r['repository_id'] for r in valid}),
                    'revision_groups': len({r['revision_group'] for r in valid}),
                    'dirty_checkouts': sum(bool(r['tracked_changes'] or r['untracked_entries']) for r in valid),
                    'review_candidates': sum(bool(r['review_reasons']) for r in valid),
                    'unversioned_code_directories': len(loose), 'errors': len(errors),
                    'skipped_links': skipped_links, 'skipped_bare_repositories': skipped_bare},
        'repositories': valid, 'unversioned_code': loose, 'errors': errors,
        'limits': [
            'Remote refs are local cached evidence; publication is unknown until independently checked.',
            'A review candidate may be an intentional fixture, duplicate, scratch script, or already published.',
            'Untracked counts are Git status entries, which may summarize whole directories.',
            'Dependency/build directories, symlinks, Windows reparse directories, and bare repositories are excluded.',
            'The scan is not an atomic snapshot; active work can change during collection.',
            'Redaction covers common token formats and remote URL credentials, not all possible sensitive text. Review before sharing.',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', action='append', required=True, help='Authorized directory; may be repeated')
    parser.add_argument('--study-id', required=True, help='Identifier of an authorized bounded study')
    parser.add_argument('--output', type=Path, required=True, help='Private local JSON destination')
    args = parser.parse_args()
    try:
        report = scan(args.root, study_id=args.study_id)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(2, type(exc).__name__ + ': inventory could not be written\n')
    print(json.dumps(report['summary']))
    return 2 if report['summary']['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
