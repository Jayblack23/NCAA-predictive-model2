import os
import streamlit as st
import pandas as pd

from torvik_scraper import run as run_torvik
from odds_collector import run as run_odds
from model import projected_total, prob_over
from bet_sizing import kelly
from config import EDGE_THRESHOLD, CONF_THRESHOLD

st.set_page_config(layout="wide")
st.title("🏀 NCAAB Totals Model")

# --------------------------------------------------
# ENSURE DATA DIRECTORY
# --------------------------------------------------

os.makedirs("data", exist_ok=True)

# --------------------------------------------------
# ENSURE DATA FILES EXIST (NO SUBPROCESS)
# --------------------------------------------------

if not os.path.exists("data/team_stats.csv"):
    st.info("Fetching team efficiency data (Bart Torvik)...")
    run_torvik()

if not os.path.exists("data/odds_history.csv"):
    st.info("Fetching market totals (Odds API)...")
    run_odds()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

teams = (
    pd.read_csv("data/team_stats.csv")
    .set_index("team")
    .to_dict("index")
)

odds = pd.read_csv("data/odds_history.csv")

games = odds.groupby("game")["total"].mean()

rows = []

# --------------------------------------------------
# MODEL LOOP
# --------------------------------------------------

for game, market in games.items():
    try:
        away, home = game.lower().split(" @ ")
    except ValueError:
        continue

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
