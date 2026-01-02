import os
import subprocess
import streamlit as st
import pandas as pd

from model import projected_total, prob_over
from bet_sizing import kelly
from config import EDGE_THRESHOLD, CONF_THRESHOLD

st.set_page_config(layout="wide")
st.title("🏀 NCAAB Totals Model")

# --------------------------------------------------
# AUTO-GENERATE DATA IF MISSING
# --------------------------------------------------

if not os.path.exists("data/team_stats.csv"):
    st.warning("Team stats not found. Running Torvik scraper...")
    subprocess.run(["python", "torvik_scraper.py"], check=True)

if not os.path.exists("data/odds_history.csv"):
    st.warning("Odds history not found. Collecting odds...")
    subprocess.run(["python", "odds_collector.py"], check=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

teams = (
    pd.read_csv("data/team_stats.csv")
    .set_index("team")
    .to_dict("index")
)

odds = pd.read_csv("data/odds_history.csv")

teams = pd.read_csv("data/team_stats.csv").set_index("team").to_dict("index")
odds = pd.read_csv("data/odds_history.csv")

games = odds.groupby("game")["total"].mean()

rows = []

for game, market in games.items():
    away, home = game.lower().split(" @ ")

    if home not in teams or away not in teams:
        continue

    proj = projected_total(home, away, teams)
    edge = proj - market
    prob = prob_over(proj, market)

    if prob >= CONF_THRESHOLD and abs(edge) >= EDGE_THRESHOLD:
        bet = "OVER" if edge > 0 else "UNDER"
        stake = kelly(prob)
    else:
        bet = "PASS"
        stake = 0

    rows.append({
        "Game": game,
        "Market Total": round(market, 1),
        "Projected Total": proj,
        "Edge": round(edge, 1),
        "Win Prob %": round(prob * 100, 1),
        "Bet": bet,
        "Stake ($)": stake
    })

df = pd.DataFrame(rows).sort_values("Edge", ascending=False)
st.dataframe(df, use_container_width=True)
