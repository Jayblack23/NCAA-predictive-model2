import pandas as pd
import os

TORVIK_CSV_URL = "https://barttorvik.com/getdata.php?conlimit=All&year=2025&csv=1"

def scrape_torvik():
    df = pd.read_csv(TORVIK_CSV_URL)

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    required = ["team", "adjoe", "adjde", "tempo"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing required columns: {missing}")

    df = df[required]

    # Force numeric
    for c in ["adjoe", "adjde", "tempo"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/team_stats.csv", index=False)

def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
