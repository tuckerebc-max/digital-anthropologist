# Center for Digital Anthropology

## Navy Yard design specification

This package defines the proposed Center for Digital Anthropology and the Head of the Center for Digital Anthropology (the Digital Anthropologist) within the Navy Yard architecture.

The central design decision is simple:

> The Center studies bounded work episodes in context. It may observe, ask, interpret, and propose; it may not score people, capture sensitive material by default, or change production authority without a separate governance gate.

The package is designed to be GitHub-native and pilot-ready. It separates:

- the Center’s charter and the Head’s accountable role;
- the observation method and evidence vocabulary;
- interfaces with Superpowers, Kata, Hermes, Linear, Notion, GitHub, ATS, Learning Experience Design, and Behavioral Design;
- a first pilot and success criteria; and
- a small machine-readable observation record.

## Files

- [`CENTER_FOR_DIGITAL_ANTHROPOLOGY_DESIGN_SPECIFICATION.md`](CENTER_FOR_DIGITAL_ANTHROPOLOGY_DESIGN_SPECIFICATION.md) — full charter, role language, method, boundaries, interfaces, and pilot.
- [`observation-record.schema.json`](observation-record.schema.json) — starter schema for a bounded observation record.
- [`RESEARCH_NOTES.md`](RESEARCH_NOTES.md) — original research and GitHub exemplars that informed the design.

## Run a bounded recovery inventory

The Center now includes a read-only instrument for finding work that needs a delivery decision. It accepts explicit authorized folders, reads local Git metadata, and reports unversioned code directories. It never fetches, pushes, runs discovered scripts, or reads conversation history. Git may read working-tree bytes to determine status; no file contents enter the report. Configured clean/process filters and filesystem monitors are disabled, and inherited Git routing variables are removed for each command.

Requires Python 3.11+ and Git on PATH; no Python packages are needed. First establish the study scope using [OPERATIONS.md](OPERATIONS.md), then run:

```powershell
python -B yard_inventory.py --study-id STUDY-001 --root 'C:\Projects' --output '.local/inventory.json'
python -B -m unittest discover -s tests -v
```

Repeat `--root` to include another authorized folder. Linux and macOS use the same command with their native paths. The JSON report is private local evidence; `.local/` is ignored by Git. Exit code 2 means coverage or writing failed; inspect the errors before making a completeness claim.

The report separates working-copy changes, missing/local remotes, branches ahead of cached upstream refs, detached heads, and empty repositories. It groups revisions while retaining each checkout's changes. **Publication remains unknown:** cached refs cannot prove that code is absent from GitHub. Check the current remote and open/merged pull requests before recovery.

Review candidates can be deliberate scratch work, duplicate snapshots, mutation-test fixtures, or already published code. Directory and checkout counts are not project counts. No maturity score or personnel score is produced. Common token formats and remote URL credentials/query strings are redacted, but a human must review any report before sharing it.

## Status

Proposed architecture. The Center should not be activated as a broad observer until its authority, identity and visibility boundaries, notice/consent, retention, correction/withdrawal/deletion, review standard, and first study are ratified.
