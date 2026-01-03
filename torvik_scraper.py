import pandas as pd
import requests
import os
from io import StringIO

TORVIK_CSV_URL = "https://barttorvik.com/getdata.php?conlimit=All&year=2025&csv=1"

def scrape_torvik():
    resp = requests.get(TORVIK_CSV_URL, timeout=30)
    resp.raise_for_status()

    lines = resp.text.splitlines()

    # Find the real CSV header
    header_idx = None
    for i, line in enumerate(lines):
        if line.lower().startswith("team,"):
            header_idx = i
            break

    if header_idx is None:
        raise RuntimeError("Could not locate CSV header in Torvik data")

    csv_text = "\n".join(lines[header_idx:])

    df = pd.read_csv(StringIO(csv_text))

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    required = ["team", "adjoe", "adjde", "tempo"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing required columns: {missing}")

    df = df[required]

    # Convert to numeric
    for col in ["adjoe", "adjde", "tempo"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/team_stats.csv", index=False)

def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
