"""
Load AMC problem content into the `problem_content` table.

Usage:
    python insert_2024.py                        # loads 2024_AMC_10A.xlsx
    python insert_2024.py 2025_AMC_10A.xlsx      # loads any other file
    python insert_2024.py path/to/file.xlsx      # full or relative path

Expected Excel columns (Sheet1):
    Question no | Problem | Solution | version | year
"""

import sys
import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE       = Path(__file__).parent / "amc_problems.db"
DEFAULT_EXCEL = Path(__file__).parent / "2024_AMC_10A.xlsx"
TABLE         = "problem_content"

COLUMN_MAP = {
    "Question no": "question_num",
    "Problem":     "problem",
    "Solution":    "solution",
    "version":     "version",
    "year":        "year",
}


def load(excel_path: Path) -> pd.DataFrame:
    df = pd.read_excel(excel_path, sheet_name="Sheet1")
    df = df.rename(columns=COLUMN_MAP)
    df["question_num"] = df["question_num"].astype(int)
    df["year"]         = df["year"].astype(int)
    df["version"]      = df["version"].astype(str).str.strip()
    return df[["year", "version", "question_num", "problem", "solution"]]


def upload(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            year         INTEGER NOT NULL,
            version      TEXT    NOT NULL,
            question_num INTEGER NOT NULL,
            problem      TEXT,
            solution     TEXT,
            PRIMARY KEY (year, version, question_num)
        )
    """)

    # Remove existing rows for each (year, version) pair in the file before reinserting
    for (year, version), group in df.groupby(["year", "version"]):
        deleted = conn.execute(
            f"DELETE FROM {TABLE} WHERE year = ? AND version = ?", (year, version)
        ).rowcount
        if deleted:
            print(f"  Removed {deleted} existing rows for {year}-{version}.")

    df.to_sql(TABLE, conn, if_exists="append", index=False)


def verify(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    print(f"\n--- {TABLE} sample (problem text truncated to 80 chars) ---")
    year = int(df["year"].iloc[0])
    for row in conn.execute(f"""
        SELECT year, version, question_num, SUBSTR(problem, 1, 80)
        FROM {TABLE} WHERE year = ? LIMIT 4
    """, (year,)):
        print(" ", row)

    print(f"\n--- {TABLE} row count by year/version ---")
    for row in conn.execute(f"""
        SELECT year, version, COUNT(*) FROM {TABLE}
        GROUP BY year, version ORDER BY year
    """):
        print(f"  year={row[0]}  version={row[1]}  rows={row[2]}")


if __name__ == "__main__":
    excel_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_EXCEL

    if not excel_path.is_absolute():
        excel_path = Path(__file__).parent / excel_path

    if not excel_path.exists():
        print(f"Error: file not found — {excel_path}")
        sys.exit(1)

    print(f"Loading {excel_path.name}...")
    df = load(excel_path)
    years = df.groupby(["year", "version"]).size().reset_index(name="rows")
    for _, r in years.iterrows():
        print(f"  year={int(r['year'])}  version={r['version']}  rows={r['rows']}")

    print("\nUploading to database...")
    with sqlite3.connect(DB_FILE) as conn:
        upload(df, conn)
        verify(conn, df)

    print(f"\nDone. Database: {DB_FILE.name}")
