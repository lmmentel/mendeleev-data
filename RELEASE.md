# Release Process

This document describes how the automated release pipeline works for `mendeleev-data`.

## Overview

`mendeleev-data` is automatically updated whenever a new version of [mendeleev](https://github.com/lmmentel/mendeleev) is released. The pipeline exports data from mendeleev's SQLite database, formats it, and creates a matching release in this repository.

## Automated Flow

```
mendeleev: tag push (vX.Y.Z)
  └─ main.yml: tests (3 OS × 5 Python versions)
      └─ pypi-publish: publish to PyPI
          └─ create-draft-release: create draft GitHub release with auto-generated notes

mendeleev: draft release created
  └─ notify-data.yml: repository_dispatch → mendeleev-data

mendeleev-data: receives dispatch (mendeleev_created)
  └─ data-sync.yml:
      1. Checkout both repos (mendeleev at tag, mendeleev-data main)
      2. Run `inv export` to generate data files
      3. Run `format-data` to normalize JSON/CSV/Markdown
      4. Update README with version info
      5. Update pyproject.toml version pins
      6. Create branch `data/vX.Y.Z` and open PR

mendeleev-data: PR created
  └─ ci.yml: ruff lint check on PR

mendeleev: user reviews release notes and publishes release
  └─ notify-data.yml: repository_dispatch → mendeleev-data

mendeleev-data: receives dispatch (mendeleev_published)
  └─ merge-and-release.yml: find PR, enable auto-merge (squash)

mendeleev-data: PR merged to main
  └─ release.yml: create GitHub release with matching tag
```

## What the Maintainer Does

1. **Run bump2version** locally to bump version, commit, and tag
2. **Push the tag** — everything else is automated
3. **Review the draft release** on GitHub (optionally edit release notes)
4. **Click "Publish release"** — triggers the mendeleev-data PR merge and release

## Workflows

### mendeleev repo

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `main.yml` | tag push `v*` | Tests, PyPI publish, draft GitHub release |
| `notify-data.yml` | release created/published | Dispatches events to mendeleev-data |

### mendeleev-data repo

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `data-sync.yml` | `repository_dispatch` or `workflow_dispatch` | Creates PR with data export |
| `ci.yml` | pull_request | Ruff lint check |
| `merge-and-release.yml` | `repository_dispatch` | Merges PR when mendeleev release is published |
| `release.yml` | push to main | Creates GitHub release after PR merge |

## Data Formatting

Exported data is formatted for clean diffs and consistent presentation:

- **JSON**: Pretty-printed with 4-space indent, keys sorted alphabetically
- **CSV**: Header row added from database column names
- **Markdown**: Header row and separator added from database column names
- **SQL**: Raw `sqlite3 .dump` output (no formatting needed)

### Running format scripts locally

```bash
# Install the package (editable mode)
pip install -e .

# Format all data files
poetry run format-data

# Or format individual formats
poetry run format-json
poetry run format-csv
poetry run format-md

# With custom data directory
poetry run format-data --data-dir ./my-data

# With explicit database path
poetry run format-data --db-path /path/to/elements.db
```

### Running export + format locally

```bash
# From mendeleev repo
poetry run inv export --dest ../mendeleev-data/data

# From mendeleev-data repo
poetry run format-data
```

## Retroactive Releases

To create data releases for past mendeleev versions, use `workflow_dispatch`:

```bash
# Single version
gh workflow run data-sync.yml -f version=v1.0.0 -R lmmentel/mendeleev-data

# Multiple versions
for VERSION in v0.19.0 v0.20.0 v1.0.0; do
  gh workflow run data-sync.yml -f version=$VERSION -R lmmentel/mendeleev-data
done
```

Or use the GitHub UI: Actions → Sync data on release → Run workflow.

Each run creates a PR. After CI passes, merge the PR. The release workflow fires automatically on merge.

## Setup Requirements

### PAT Token

A fine-grained Personal Access Token is needed for cross-repo dispatch:

1. Go to https://github.com/settings/tokens?type=beta
2. Generate new token with `contents: write` on `lmmentel/mendeleev-data`
3. Store as `MENDELEEV_DATA_TOKEN` in **mendeleev** repo secrets

### Repository Settings

- **mendeleev-data**: Enable "Allow auto-merge" in Settings → General → Pull Requests
- **mendeleev-data**: Set workflow permissions to "Read and write" in Settings → Actions → General

### Auto-merge Label

The `auto-merge` label must exist on mendeleev-data. The `data-sync.yml` workflow creates it automatically if missing.

## Troubleshooting

### PR creation fails with "Permission denied"

The `GITHUB_TOKEN` lacks write access. Ensure workflow permissions are set to "Read and write" in repo settings, and the `permissions:` block is present in `data-sync.yml`.

### "auto-merge label not found"

The label doesn't exist yet. The workflow creates it automatically on the next run. For immediate fix, create it manually: Labels → New label → name: `auto-merge`.

### PR not found when publishing release

The PR may have been merged or closed already. Check the PR list. If the PR was merged, the release should have been created automatically.

### Format scripts fail locally

Ensure `jq` and `sqlite3` are installed:
```bash
# macOS
brew install jq sqlite3

# Ubuntu/Debian
apt install jq sqlite3
```
