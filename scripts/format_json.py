"""Format JSON files: pretty-print with 4-space indent and sorted keys."""

import argparse
import json
import sys
from pathlib import Path


def format_json_file(path: Path) -> None:
    """Read a JSON file, sort keys, pretty-print, and write back."""
    with open(path) as f:
        data = json.load(f)

    with open(path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Format JSON files in a data directory.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Path to the data directory (default: data/)",
    )
    args = parser.parse_args()

    json_dir = args.data_dir / "json"
    if not json_dir.is_dir():
        print(f"Directory not found: {json_dir}", file=sys.stderr)
        sys.exit(1)

    for path in sorted(json_dir.glob("*.json")):
        print(f"Formatting {path} ... ", end="")
        format_json_file(path)
        print("done")


if __name__ == "__main__":
    main()
