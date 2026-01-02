import math
from config import LEAGUE_AVG_OE, LEAGUE_AVG_DE, STD_TOTAL

def projected_total(home, away, teams):
    h = teams[home]
    a = teams[away]

    possessions = (h["tempo"] + a["tempo"]) / 2

    h_ppp = (h["adj_oe"] / LEAGUE_AVG_OE) * (LEAGUE_AVG_DE / a["adj_de"])
    a_ppp = (a["adj_oe"] / LEAGUE_AVG_OE) * (LEAGUE_AVG_DE / h["adj_de"])

    return round(possessions * (h_ppp + a_ppp), 1)

def prob_over(proj, market):
    z = (proj - market) / STD_TOTAL
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))
