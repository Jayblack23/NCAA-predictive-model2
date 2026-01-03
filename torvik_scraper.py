import pandas as pd
import requests
import os
from io import StringIO

TORVIK_URL = "https://barttorvik.com/getdata.php?conlimit=All&year=2025&csv=1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def scrape_torvik():
    r = requests.get(TORVIK_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    text = r.text.strip()

    # ❌ Torvik blocked us (HTML page)
    if text.lower().startswith("<!doctype html") or "<html" in text.lower():
        raise RuntimeError("Torvik blocked automated access (HTML returned)")

    # Identify delimiter
    delimiter = "," if "," in text.splitlines()[0] else "\t"

    df = pd.read_csv(StringIO(text), sep=delimiter)

    df.columns = df.columns.str.lower().str.strip()

    required = ["team", "adjoe", "adjde", "tempo"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Required columns missing: {missing}")

    df = df[required]

    for c in ["adjoe", "adjde", "tempo"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna()

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/team_stats.csv", index=False)

def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
