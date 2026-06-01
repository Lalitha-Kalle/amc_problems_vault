"""
Insert 2024 AMC 10B and 2025 AMC 10B problem content into `problem_content`.

The B-version Excel files use capitalised column headers (Year, Version)
unlike the A-version files. This script normalises them before loading.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path(__file__).parent / "amc_problems.db"
TABLE   = "problem_content"

FILES = [
    Path(__file__).parent / "2024" / "2024_AMC_10B.xlsx",
    Path(__file__).parent / "2025" / "2025_AMC_10B.xlsx",
]

COLUMN_MAP = {
    "question no": "question_num",
    "problem":     "problem",
    "solution":    "solution",
    "version":     "version",
    "year":        "year",
}


def load(excel_path: Path) -> pd.DataFrame:
    df = pd.read_excel(excel_path, sheet_name="Sheet1")
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns=COLUMN_MAP)
    df["question_num"] = pd.to_numeric(df["question_num"], errors="coerce")
    # Fall back to 1-based row position for any non-numeric entries (e.g. typo 's' for 25)
    fallback = pd.Series(range(1, len(df) + 1), index=df.index, dtype="float64")
    df["question_num"] = df["question_num"].fillna(fallback).astype(int)
    df["year"]         = df["year"].astype(int)
    df["version"]      = df["version"].astype(str).str.strip()
    return df[["year", "version", "question_num", "problem", "solution"]]


def upload(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    for (year, version), group in df.groupby(["year", "version"]):
        deleted = conn.execute(
            f"DELETE FROM {TABLE} WHERE year = ? AND version = ?", (year, version)
        ).rowcount
        if deleted:
            print(f"  Removed {deleted} existing rows for {year}-{version}.")

    df.to_sql(TABLE, conn, if_exists="append", index=False)


def verify(conn: sqlite3.Connection) -> None:
    print(f"\n--- {TABLE} row count by year/version ---")
    for row in conn.execute(f"""
        SELECT year, version, COUNT(*) FROM {TABLE}
        GROUP BY year, version ORDER BY year, version
    """):
        print(f"  year={row[0]}  version={row[1]}  rows={row[2]}")


if __name__ == "__main__":
    with sqlite3.connect(DB_FILE) as conn:
        for path in FILES:
            if not path.exists():
                print(f"ERROR: file not found — {path}")
                continue

            print(f"\nLoading {path.name}...")
            df = load(path)
            year    = int(df["year"].iloc[0])
            version = df["version"].iloc[0]
            print(f"  year={year}  version={version}  rows={len(df)}")

            print("  Uploading to database...")
            upload(df, conn)
            print(f"  Done — inserted {len(df)} rows for {year}-{version}.")

        verify(conn)

    print(f"\nDatabase: {DB_FILE.name}")
