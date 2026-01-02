import pandas as pd
import os

TORVIK_CSV_URL = "https://barttorvik.com/getdata.php?conlimit=All&year=2025&csv=1"

def scrape_torvik():
    df = pd.read_csv(TORVIK_CSV_URL)

    # Normalize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Required fields
    required = {
        "team": "team",
        "adjoe": "adjoe",
        "adjde": "adjde",
        "tempo": "tempo"
    }

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing required columns: {missing}")

    df = df[list(required.values())]

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/team_stats.csv", index=False)

def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
