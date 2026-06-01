import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path(__file__).parent / "amc_problems.db"

TOPICS_EXCEL  = Path(__file__).parent / "AMC10 Problem Topics.xlsx"
TOPICS_SHEET  = "Mstr Prblms"
TOPICS_TABLE  = "problems"

AMC2025_EXCEL = Path(__file__).parent / "2025_AMC_10A.xlsx"
AMC2025_SHEET = "Sheet1"
AMC2025_TABLE = "problem_content"


# ── loaders ──────────────────────────────────────────────────────────────────

def load_topics() -> pd.DataFrame:
    df = pd.read_excel(TOPICS_EXCEL, sheet_name=TOPICS_SHEET)
    df.columns = ["year", "version", "question_num", "level_1", "level_2", "level_3"]
    df["year"]         = df["year"].astype(int)
    df["question_num"] = df["question_num"].astype(int)
    return df


def load_2025() -> pd.DataFrame:
    df = pd.read_excel(AMC2025_EXCEL, sheet_name=AMC2025_SHEET)
    df.columns = ["question_num", "problem", "solution", "version", "year"]
    df["year"]         = df["year"].astype(int)
    df["question_num"] = df["question_num"].astype(int)
    return df[["year", "version", "question_num", "problem", "solution"]]


# ── uploaders ─────────────────────────────────────────────────────────────────

def upload_topics(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    # Drop 4 fully duplicate rows before inserting
    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    if dropped:
        print(f"  Dropped {dropped} duplicate rows from source data.")

    conn.execute(f"DROP TABLE IF EXISTS {TOPICS_TABLE}")
    conn.execute(f"""
        CREATE TABLE {TOPICS_TABLE} (
            year         INTEGER NOT NULL,
            version      TEXT    NOT NULL,
            question_num INTEGER NOT NULL,
            level_1      TEXT    NOT NULL,
            level_2      TEXT    NOT NULL,
            level_3      TEXT    NOT NULL,
            PRIMARY KEY (year, version, question_num, level_1, level_2, level_3)
        )
    """)
    df.to_sql(TOPICS_TABLE, conn, if_exists="append", index=False)
    count = conn.execute(f"SELECT COUNT(*) FROM {TOPICS_TABLE}").fetchone()[0]
    print(f"  '{TOPICS_TABLE}': {count} rows uploaded.")


def upload_2025(df: pd.DataFrame, conn: sqlite3.Connection) -> None:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {AMC2025_TABLE} (
            year         INTEGER NOT NULL,
            version      TEXT    NOT NULL,
            question_num INTEGER NOT NULL,
            problem      TEXT,
            solution     TEXT,
            PRIMARY KEY (year, version, question_num)
        )
    """)
    conn.execute(f"DELETE FROM {AMC2025_TABLE} WHERE year = 2025 AND version = 'A'")
    df.to_sql(AMC2025_TABLE, conn, if_exists="append", index=False)
    count = conn.execute(f"SELECT COUNT(*) FROM {AMC2025_TABLE}").fetchone()[0]
    print(f"  '{AMC2025_TABLE}': {count} rows total.")


# ── verification ──────────────────────────────────────────────────────────────

def verify(conn: sqlite3.Connection) -> None:
    print(f"\n--- {TOPICS_TABLE} sample ---")
    for row in conn.execute(f"SELECT year, version, question_num, level_1, level_2, level_3 FROM {TOPICS_TABLE} LIMIT 4"):
        print(" ", row)

    print(f"\n--- {TOPICS_TABLE} top Level 1 topics ---")
    for row in conn.execute(f"""
        SELECT level_1, COUNT(*) AS cnt FROM {TOPICS_TABLE}
        GROUP BY level_1 ORDER BY cnt DESC
    """):
        print(f"  {row[0]:<25} {row[1]}")

    print(f"\n--- {AMC2025_TABLE} sample (truncated problem text) ---")
    for row in conn.execute(f"""
        SELECT year, version, question_num, SUBSTR(problem, 1, 60) FROM {AMC2025_TABLE} LIMIT 4
    """):
        print(" ", row)

    print(f"\n--- {AMC2025_TABLE} row count by year/version ---")
    for row in conn.execute(f"""
        SELECT year, version, COUNT(*) FROM {AMC2025_TABLE}
        GROUP BY year, version ORDER BY year
    """):
        print(" ", row)


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading Excel files...")
    topics_df = load_topics()
    amc2025_df = load_2025()
    print(f"  Topics rows:  {len(topics_df)}")
    print(f"  2025 rows:    {len(amc2025_df)}")

    print("\nUploading to database...")
    with sqlite3.connect(DB_FILE) as conn:
        upload_topics(topics_df, conn)
        upload_2025(amc2025_df, conn)
        verify(conn)

    print(f"\nDone. Database: {DB_FILE.name}")
