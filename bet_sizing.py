def kelly(prob, odds=-110, bankroll=1000, fraction=0.5):
    b = abs(odds) / 100
    k = (prob * (b + 1) - 1) / b
    return round(max(k, 0) * bankroll * fraction, 2)
