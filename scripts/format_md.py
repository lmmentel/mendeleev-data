"""Format Markdown files: add header row and separator from PRAGMA table_info."""

import argparse
import sqlite3
import sys
from pathlib import Path


def get_column_names(db_path: Path, table: str) -> list[str]:
    """Get column names for a table using PRAGMA table_info."""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.execute(f"PRAGMA table_info({table});")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns


def format_md_file(path: Path, columns: list[str]) -> None:
    """Prepend a header row and separator to a markdown table file."""
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    content = path.read_text()

    with open(path, "w") as f:
        f.write(header + "\n")
        f.write(separator + "\n")
        f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format Markdown files in a data directory."
    )
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

    md_dir = args.data_dir / "markdown"
    if not md_dir.is_dir():
        print(f"Directory not found: {md_dir}", file=sys.stderr)
        sys.exit(1)

    # Find the database
    if args.db_path:
        db_path = args.db_path
    else:
        candidates = [
            Path("mendeleev/elements.db"),
            Path("../mendeleev/elements.db"),
            Path.home() / "projects/mendeleev/mendeleev/elements.db",
        ]
        db_path = None
        for candidate in candidates:
            if candidate.is_file():
                db_path = candidate
                break
        if db_path is None:
            print(
                "Could not find elements.db. Use --db-path to specify.",
                file=sys.stderr,
            )
            sys.exit(1)

    for path in sorted(md_dir.glob("*.md")):
        table = path.stem
        print(f"Formatting {path} ... ", end="")
        columns = get_column_names(db_path, table)
        if not columns:
            print(f"skipped (table {table} not found)")
            continue
        format_md_file(path, columns)
        print("done")


if __name__ == "__main__":
    main()
