"""Run all data formatters: JSON, CSV, and Markdown."""

import argparse
import sys
from pathlib import Path

from .format_csv import main as csv_main
from .format_json import main as json_main
from .format_md import main as md_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Format all exported data files.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Path to the data directory (default: data/)",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Path to elements.db (auto-detected if not specified)",
    )
    args = parser.parse_args()

    json_args = ["format", "--data-dir", str(args.data_dir)]
    db_args = json_args + (
        ["--db-path", str(args.db_path)] if args.db_path else []
    )

    for name, fmt_main, extra_args in [
        ("JSON", json_main, json_args),
        ("CSV", csv_main, db_args),
        ("Markdown", md_main, db_args),
    ]:
        print(f"\n--- Formatting {name} ---")
        sys.argv = extra_args
        try:
            fmt_main()
        except SystemExit as e:
            if e.code != 0:
                print(f"Error formatting {name}", file=sys.stderr)
                sys.exit(1)

    print("\nAll formats complete.")


if __name__ == "__main__":
    main()
