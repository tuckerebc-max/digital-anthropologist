import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import yard_inventory as inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def git(self, path, *args):
        result = subprocess.run(['git', '-C', str(path), *args], capture_output=True,
                                text=True, check=True)
        return result.stdout.strip()

    def repo(self, name='project with spaces', commit=True):
        path = self.root / name
        path.mkdir()
        self.git(path, 'init', '-b', 'main')
        self.git(path, 'config', 'user.name', 'Fixture')
        self.git(path, 'config', 'user.email', 'fixture@example.invalid')
        if commit:
            (path / 'app.py').write_text('print(42)\n')
            self.git(path, 'add', 'app.py')
            self.git(path, 'commit', '-m', 'Initial fixture')
        return path

    def scan(self, root=None):
        return inventory.scan([root or self.root], study_id='TEST-1')

    def test_dirty_no_remote_is_candidate_without_claiming_unpublished(self):
        path = self.repo()
        (path / 'app.py').write_text('print(43)\n')
        (path / 'new.txt').write_text('new')
        before = self.git(path, 'status', '--porcelain=v1')
        item = self.scan()['repositories'][0]
        self.assertEqual(item['publication'], 'unknown')
        self.assertEqual(item['remote_kind'], 'none')
        self.assertEqual(item['tracked_changes'], 1)
        self.assertEqual(item['untracked_entries'], 1)
        self.assertIn('no_remote', item['review_reasons'])
        self.assertEqual(self.git(path, 'status', '--porcelain=v1'), before)

    def test_upstream_ahead_and_stale_remote_are_separate_facts(self):
        path = self.repo()
        remote = self.root / 'remote.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
        self.git(path, 'remote', 'add', 'origin', str(remote))
        self.git(path, 'push', '-u', 'origin', 'main')
        (path / 'app.py').write_text('print(44)\n')
        self.git(path, 'commit', '-am', 'Local work')
        item = next(x for x in self.scan()['repositories'] if x['path'] == str(path))
        self.assertEqual(item['ahead_of_local_upstream'], 1)
        self.assertEqual(item['behind_local_upstream'], 0)
        self.assertEqual(item['publication'], 'unknown')
        self.assertEqual(item['remote_kind'], 'local')
        self.assertIn('ahead_of_local_upstream', item['review_reasons'])

    def test_detached_and_unborn_are_reported(self):
        path = self.repo()
        self.git(path, 'checkout', '--detach')
        self.repo('empty', commit=False)
        found = {Path(x['path']).name: x for x in self.scan()['repositories']}
        self.assertEqual(found['project with spaces']['branch_state'], 'detached')
        self.assertEqual(found['empty']['branch_state'], 'unborn')
        self.assertIsNone(found['empty']['head'])

    def test_worktrees_share_identity_and_keep_working_copy_state(self):
        path = self.repo()
        worktree = self.root / 'linked'
        self.git(path, 'worktree', 'add', '-b', 'feature', str(worktree))
        (worktree / 'app.py').write_text('print(99)\n')
        items = self.scan()['repositories']
        self.assertEqual(len(items), 2)
        self.assertEqual(len({x['repository_id'] for x in items}), 1)
        self.assertEqual(sorted(x['tracked_changes'] for x in items), [0, 1])

    def test_skips_dependency_trees_and_reports_unversioned_code(self):
        path = self.root / 'scratch'
        path.mkdir()
        (path / 'recover.py').write_text('do not execute this file')
        dependency = path / 'node_modules'
        dependency.mkdir()
        (dependency / 'library.js').write_text('ignored')
        report = self.scan()
        self.assertEqual(len(report['unversioned_code']), 1)
        self.assertEqual(report['unversioned_code'][0]['code_files'], 1)
        self.assertEqual(report['repositories'], [])

    def test_redacts_remote_credentials_query_and_token_paths(self):
        secret = 'ghp_' + 'a' * 36
        path = self.repo('project-' + secret)
        self.git(path, 'remote', 'add', 'origin',
                 'https://user:' + secret + '@github.com/example/project.git?key=QUERY_SECRET_SENTINEL#part')
        report = self.scan()
        encoded = json.dumps(report)
        self.assertNotIn(secret, encoded)
        self.assertNotIn('QUERY_SECRET_SENTINEL', encoded)
        self.assertEqual(report['repositories'][0]['origin'], 'https://github.com/example/project.git')

    def test_non_origin_remote_is_not_misreported_as_missing(self):
        path = self.repo()
        self.git(path, 'remote', 'add', 'upstream', 'https://github.com/example/project.git')
        item = self.scan()['repositories'][0]
        self.assertEqual(item['remote_kind'], 'network')
        self.assertNotIn('no_remote', item['review_reasons'])

    @unittest.skipUnless(os.name == 'nt', 'Windows long-path behavior')
    def test_long_windows_directory_is_scanned(self):
        path = inventory.filesystem_path(self.root)
        for i in range(7):
            path = path / ('component' + str(i) + 'x' * 30)
        path.mkdir(parents=True)
        (path / 'recover.py').write_text('print(1)')
        def remove_long_fixture():
            (path / 'recover.py').unlink(missing_ok=True)
            cursor = path
            for _ in range(7):
                cursor.rmdir()
                cursor = cursor.parent
        self.addCleanup(remove_long_fixture)
        report = self.scan()
        self.assertEqual(report['summary']['errors'], 0)
        self.assertEqual(report['unversioned_code'][0]['code_files'], 1)

    @unittest.skipUnless(os.name == 'nt', 'Windows junction behavior')
    def test_windows_junction_does_not_expand_scope(self):
        path = self.repo()
        scope = self.root / 'scope'
        scope.mkdir()
        junction = scope / 'outside'
        quoted = lambda p: "'" + str(p).replace("'", "''") + "'"
        command = 'New-Item -ItemType Junction -Path ' + quoted(junction) + ' -Target ' + quoted(path)
        result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = self.scan(scope)
        self.assertEqual(report['repositories'], [])
        self.assertEqual(report['summary']['skipped_links'], 1)

    def test_network_remote_remains_visible_beside_local_origin(self):
        path = self.repo()
        self.git(path, 'remote', 'add', 'origin', str(self.root / 'local.git'))
        self.git(path, 'remote', 'add', 'upstream', 'https://github.com/example/project.git')
        item = self.scan()['repositories'][0]
        self.assertEqual(item['remote_kind'], 'network')
        self.assertNotIn('local_remote_only', item['review_reasons'])

    def test_configured_clean_filter_is_never_executed(self):
        path = self.repo()
        (path / '.gitattributes').write_text('tracked.txt filter=review_probe\n')
        tracked = path / 'tracked.txt'
        tracked.write_text('before\n')
        self.git(path, 'add', '.gitattributes', 'tracked.txt')
        self.git(path, 'commit', '-m', 'Filter fixture')
        marker = self.root / 'executed.txt'
        probe = self.root / 'probe.py'
        probe.write_text('import pathlib,sys\npathlib.Path(' + repr(str(marker)) +
                         ').write_text("EXECUTED")\nsys.stdout.write(sys.stdin.read())\n')
        self.git(path, 'config', 'filter.review_probe.clean',
                 '"' + sys.executable.replace('\\', '/') + '" "' + str(probe).replace('\\', '/') + '"')
        tracked.write_text('after!\n')
        info = tracked.stat()
        os.utime(tracked, (info.st_atime, info.st_mtime + 2))
        report = self.scan(path)
        self.assertFalse(marker.exists(), 'A repository filter executed during the metadata scan')
        self.assertEqual(report['summary']['errors'], 0)
        self.assertEqual(report['repositories'][0]['tracked_changes'], 1)

    def test_corrupt_upstream_is_a_coverage_error(self):
        path = self.repo()
        self.git(path, 'remote', 'add', 'origin', 'https://github.com/example/project.git')
        self.git(path, 'config', 'branch.main.remote', 'origin')
        self.git(path, 'config', 'branch.main.merge', 'refs/heads/main')
        remote_ref = path / '.git/refs/remotes/origin/main'
        remote_ref.parent.mkdir(parents=True)
        remote_ref.write_text('invalid-reference\n')
        report = self.scan(path)
        self.assertGreater(report['summary']['errors'], 0)
        self.assertIn('upstream', json.dumps(report['errors']))

    def test_inherited_git_routing_cannot_escape_the_selected_root(self):
        allowed = self.repo('allowed')
        outside = self.repo('outside')
        (outside / 'app.py').write_text('outside')
        self.git(outside, 'commit', '-am', 'Different history')
        expected = self.git(allowed, 'rev-parse', 'HEAD')
        with patch.dict(os.environ, {'GIT_DIR': str(outside / '.git'), 'GIT_WORK_TREE': str(outside)}):
            report = self.scan(allowed)
        self.assertEqual(report['repositories'][0]['head'], expected)
        self.assertEqual(report['summary']['errors'], 0)

    def test_canonical_origin_groups_revisions_even_with_an_extra_remote(self):
        first = self.repo('first')
        second = self.root / 'second'
        subprocess.run(['git', 'clone', str(first), str(second)], check=True, capture_output=True)
        self.git(first, 'remote', 'add', 'origin', 'https://github.com/example/project.git')
        self.git(second, 'remote', 'set-url', 'origin', 'https://github.com/example/project.git')
        self.git(second, 'remote', 'add', 'backup', 'https://github.com/example/backup.git')
        report = self.scan()
        self.assertEqual(report['summary']['revision_groups'], 1)
        self.assertEqual(report['summary']['checkouts'], 2)

    def test_scp_remote_without_username_is_network(self):
        path = self.repo()
        self.git(path, 'remote', 'add', 'origin', 'github.com:example/project.git')
        self.assertEqual(self.scan()['repositories'][0]['remote_kind'], 'network')

    def test_file_url_remote_is_local(self):
        path = self.repo()
        self.git(path, 'remote', 'add', 'origin', (self.root / 'remote.git').as_uri())
        item = self.scan()['repositories'][0]
        self.assertEqual(item['remote_kind'], 'local')
        self.assertIn('local_remote_only', item['review_reasons'])

    def test_root_timeout_keeps_other_root_evidence(self):
        good = self.repo()
        bad = self.root / 'timeout-root'
        bad.mkdir()
        real_git = inventory.git
        def timeout_one_root(path, *args):
            if inventory.display_path(path) == str(bad):
                raise subprocess.TimeoutExpired('git', 20)
            return real_git(path, *args)
        with patch.object(inventory, 'git', side_effect=timeout_one_root):
            report = inventory.scan([good, bad], study_id='TEST-1')
        self.assertEqual(report['summary']['checkouts'], 1)
        self.assertEqual(report['summary']['errors'], 1)
        self.assertEqual(report['errors'][0]['error'], 'TimeoutExpired')

    def test_missing_root_is_visible_coverage_error(self):
        report = self.scan(self.root / 'does-not-exist')
        self.assertEqual(report['summary']['errors'], 1)
        self.assertEqual(report['repositories'], [])

    def test_duplicate_and_overlapping_roots_do_not_double_count(self):
        path = self.repo()
        report = inventory.scan([self.root, path, self.root], study_id='TEST-1')
        self.assertEqual(len(report['repositories']), 1)

    def test_scanner_does_not_follow_directory_symlink(self):
        path = self.repo()
        other = self.root / 'scope'
        other.mkdir()
        try:
            (other / 'outside').symlink_to(path, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks requires privileges on this host')
        report = self.scan(other)
        self.assertEqual(report['repositories'], [])
        self.assertEqual(report['summary']['skipped_links'], 1)

    def test_cli_produces_report_and_nonzero_for_incomplete_coverage(self):
        self.repo()
        out = self.root / 'result.json'
        command = [sys.executable, str(Path(inventory.__file__)), '--study-id', 'TEST-CLI',
                   '--root', str(self.root), '--output', str(out)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(out.read_text())['study_id'], 'TEST-CLI')
        result = subprocess.run(command + ['--root', str(self.root / 'missing')],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
