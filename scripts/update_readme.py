"""Update README.md with current version info and previous versions table."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def get_previous_releases(exclude_version: str) -> list[dict[str, str]]:
    """Fetch previous releases from GitHub, excluding the current version."""
    result = subprocess.run(
        [
            "gh", "release", "list",
            "-R", "lmmentel/mendeleev-data",
            "--json", "tagName",
            "-L", "50",
            "--jq", 'sort_by(.tagName) | reverse',
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []

    releases = json.loads(result.stdout)
    return [r for r in releases if r["tagName"] != exclude_version]


def update_readme(readme_path: Path, version: str) -> None:
    """Replace the Current Version and Previous Versions sections in README."""
    content = readme_path.read_text()

    # Update current version section
    content = re.sub(
        r"## Current Version\n.*?(?=\n## )",
        (
            f"## Current Version\n\n"
            f"This repository contains data for **mendeleev {version}**.\n\n"
            f"[View mendeleev {version} release notes]"
            f"(https://github.com/lmmentel/mendeleev/releases/tag/{version})\n\n"
        ),
        content,
        flags=re.DOTALL,
    )

    # Build previous versions table
    releases = get_previous_releases(version)
    rows = []
    for r in releases:
        tag = r["tagName"]
        rows.append(
            f"| [{tag}](https://github.com/lmmentel/mendeleev-data/releases/tag/{tag})"
            f" | [mendeleev {tag}](https://github.com/lmmentel/mendeleev/releases/tag/{tag}) |"
        )
    table = "\n".join(rows) if rows else "_No previous releases._"

    content = re.sub(
        r"## Previous Versions\n.*?(?=\n## |\Z)",
        (
            f"## Previous Versions\n\n"
            f"| Data Release | Mendeleev Release |\n"
            f"|---|---|\n"
            f"{table}\n\n"
        ),
        content,
        flags=re.DOTALL,
    )

    readme_path.write_text(content)
    print(f"README updated for {version}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update README.md with version info."
    )
    parser.add_argument(
        "version",
        help="mendeleev version (e.g. v1.0.0)",
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="Path to README.md (default: README.md)",
    )
    args = parser.parse_args()

    if not args.readme.is_file():
        print(f"File not found: {args.readme}", file=sys.stderr)
        sys.exit(1)

    update_readme(args.readme, args.version)


if __name__ == "__main__":
    main()
