"""
Upload AMC 10A/B problem content for years 2002-2018 into problem_content.
(2019 and 2020 are already in the database; 2000-2001 files don't exist.)
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path(__file__).parent / "amc_problems.db"
TABLE = "problem_content"

BASE = Path(__file__).parent

FILES = [
    BASE / "2002" / "2002_AMC_10A.xlsx",
    BASE / "2002" / "2002_AMC_10B.xlsx",
    BASE / "2003" / "2003_AMC_10A.xlsx",
    BASE / "2003" / "2003_AMC_10B.xlsx",
    BASE / "2004" / "2004_AMC_10A.xlsx",
    BASE / "2004" / "2004_AMC_10B.xlsx",
    BASE / "2005" / "2005_AMC_10A.xlsx",
    BASE / "2005" / "2005_AMC_10B.xlsx",
    BASE / "2006" / "2006_AMC_10A.xlsx",
    BASE / "2006" / "2006_AMC_10B.xlsx",
    BASE / "2007" / "2007_AMC_10A.xlsx",
    BASE / "2007" / "2007_AMC_10B.xlsx",
    BASE / "2008" / "2008_AMC_10A.xlsx",
    BASE / "2008" / "2008_AMC_10B.xlsx",
    BASE / "2009" / "2009_AMC_10A.xlsx",
    BASE / "2009" / "2009_AMC_10B.xlsx",
    BASE / "2010" / "2010_AMC_10A.xlsx",
    BASE / "2010" / "2010_AMC_10B.xlsx",
    BASE / "2011" / "2011_AMC_10A.xlsx",
    BASE / "2011" / "2011_AMC_10B.xlsx",
    BASE / "2012" / "2012_amc_10A.xlsx",
    BASE / "2012" / "2012_AMC_10B.xlsx",
    BASE / "2013" / "2013_AMC_10A.xlsx",
    BASE / "2013" / "2013_AMC_10B.xlsx",
    BASE / "2014" / "2014_AMC_10A.xlsx",
    BASE / "2014" / "2014_amc_10B.xlsx",
    BASE / "2015" / "2015_AMC_10A.xlsx",
    BASE / "2015" / "2015_AMC_10B.xlsx",
    BASE / "2016" / "2016_AMC_10A.xlsx",
    BASE / "2016" / "2016_AMC_10B.xlsx",
    BASE / "2017" / "2017_AMC_10A.xlsx",
    BASE / "2017" / "2017_AMC_10B.xlsx",
    BASE / "2018" / "2018_AMC_10A.xlsx",
    BASE / "2018" / "2018_AMC_10B.xlsx",
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
        skipped = []
        for path in FILES:
            if not path.exists():
                print(f"  SKIPPED (not found): {path.name}")
                skipped.append(path.name)
                continue
            print(f"Loading {path.name}...")
            df = load(path)
            year = int(df["year"].iloc[0])
            version = df["version"].iloc[0]
            n = upload(df, conn)
            print(f"  Inserted {n} rows for {year}-{version}.")
            total += n

        print(f"\nDone. Total rows inserted: {total}")
        if skipped:
            print(f"Files not found: {skipped}")

        print("\n--- problem_content row count by year/version ---")
        for row in conn.execute(
            f"SELECT year, version, COUNT(*) FROM {TABLE} GROUP BY year, version ORDER BY year, version"
        ):
            print(f"  {row[0]}  {row[1]}  {row[2]} problems")
