"""
Closing Line Value (CLV) calculations for betting analysis.
"""
def clv(open_line, close_line):
    return round(close_line - open_line, 2)
