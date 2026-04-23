def generate_signal(df, metrics):
    score = 0
    reasons = []

    if metrics["institutional_score"] > 0.25:
        score += 40
        reasons.append("High institutional activity detected")

    if metrics["signed_volume"] > 0:
        score += 20
        reasons.append("Accumulation bias (positive signed volume)")
    else:
        score -= 20
        reasons.append("Distribution pressure detected")

    if metrics["autocorr"] > 0.2:
        score += 15
        reasons.append("Order flow persistence (smart money likely)")

    if score > 50:
        signal = "BUY"
    elif score < 20:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    return {
        "signal": signal,
        "confidence": min(100, abs(score)),
        "reasons": reasons
    }


def price_levels(df):
    entry = df["close"].iloc[-1]
    sl = df["low"].min()
    t1 = entry + (entry - sl)
    t2 = entry + 2 * (entry - sl)

    return {
        "entry": entry,
        "stop_loss": sl,
        "target_1": t1,
        "target_2": t2
    }
