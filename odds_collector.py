import requests
import pandas as pd
from datetime import datetime

API_KEY = "YOUR_ODDS_API_KEY"

def collect_odds():
    url = "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "totals",
        "oddsFormat": "american"
    }

    data = requests.get(url, params=params).json()
    rows = []

    for g in data:
        for b in g.get("bookmakers", []):
            for m in b.get("markets", []):
                if m["key"] == "totals":
                    for o in m.get("outcomes", []):
                        rows.append({
                            "game": f"{g['away_team']} @ {g['home_team']}",
                            "book": b["title"],
                            "side": o["name"],
                            "total": o["point"],
                            "timestamp": datetime.utcnow()
                        })

    df = pd.DataFrame(rows)
    df.to_csv(
        "data/odds_history.csv",
        mode="a",
        index=False,
        header=not pd.io.common.file_exists("data/odds_history.csv")
    )

    print("✔ odds_history.csv updated")

if __name__ == "__main__":
    collect_odds()
def run():
    collect_odds()

if __name__ == "__main__":
    run()
