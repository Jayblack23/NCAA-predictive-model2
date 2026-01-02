import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

URL = "https://barttorvik.com/trank.php?year=2025"

def scrape_torvik():
    html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"id": "ratings-table"})
    rows = []

    for r in table.find_all("tr")[1:]:
        c = [x.text.strip() for x in r.find_all("td")]
        if len(c) < 10:
            continue

        rows.append({
            "team": c[1].lower(),
            "tempo": float(c[4]),
            "adj_oe": float(c[5]),
            "adj_de": float(c[7]),
            "conference": c[3],
            "date": date.today()
        })

    df = pd.DataFrame(rows)
    df.to_csv("data/team_stats.csv", index=False)
    print("✔ team_stats.csv updated")

if __name__ == "__main__":
    scrape_torvik()
def run():
    scrape_torvik()

if __name__ == "__main__":
    run()
