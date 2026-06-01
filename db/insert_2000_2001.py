"""
Upload 2000 and 2001 AMC 10A problem content into the problem_content table.
Only 10A exists for these years; there is no 10B.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path(__file__).parent / "amc_problems.db"
TABLE = "problem_content"

FILES = [
    Path(__file__).parent / "2000" / "2000_AMC_10A.xlsx",
    Path(__file__).parent / "2001" / "2001_AMC_10A.xlsx",
]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=0)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"question no": "question_num"})
    df["question_num"] = df["question_num"].astype(int)
    df["year"] = df["year"].astype(int)
    df["version"] = df["version"].astype(str).str.strip()
    return df[["year", "version", "question_num", "problem", "solution"]]


def upload(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    for (year, version), _ in df.groupby(["year", "version"]):
        deleted = conn.execute(
            f"DELETE FROM {TABLE} WHERE year = ? AND version = ?", (year, version)
        ).rowcount
        if deleted:
            print(f"  Replaced {deleted} existing rows for {year}-{version}.")
    df.to_sql(TABLE, conn, if_exists="append", index=False)
    return len(df)


if __name__ == "__main__":
    with sqlite3.connect(DB_FILE) as conn:
        total = 0
        for path in FILES:
            if not path.exists():
                print(f"  SKIPPED (not found): {path.name}")
                continue
            print(f"Loading {path.name}...")
            df = load(path)
            year = int(df["year"].iloc[0])
            version = df["version"].iloc[0]
            n = upload(df, conn)
            print(f"  Inserted {n} rows for {year}-{version}.")
            total += n

        print(f"\nDone. Total rows inserted: {total}")
        print("\n--- problem_content row count by year/version ---")
        for row in conn.execute(
            f"SELECT year, version, COUNT(*) FROM {TABLE} GROUP BY year, version ORDER BY year, version"
        ):
            print(f"  {row[0]}  {row[1]}  {row[2]} problems")
