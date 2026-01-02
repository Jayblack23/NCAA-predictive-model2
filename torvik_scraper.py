import pandas as pd
import os

TORVIK_CSV_URL = "https://barttorvik.com/getdata.php?conlimit=All&year=2025&csv=1"

def scrape_torvik():
    df = pd.read_csv(
        TORVIK_CSV_URL,
        engine="python",       # REQUIRED for malformed CSV
        sep=None,              # AUTO-detect delimiter (CRITICAL)
        encoding="utf-8",
        on_bad_lines="skip",
    )

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    required_cols = ["team", "adjoe", "adjde", "tempo"]
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise RuntimeError(f"Missing required Torvik columns: {missing}")

    df = df[required_cols]

    # Force numeric types
    for col in ["adjoe", "adjde", "tempo"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/team_stats.csv", index=False)

def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
