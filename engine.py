from analysis import (
    amihud_illiquidity,
    signed_volume,
    order_flow_autocorr,
    kmeans_anomaly,
    liquidity_zones,
    institutional_score
)

from signals import generate_signal, price_levels


def analyze_stock(df, symbol):

    d = df[df["symbol"] == symbol].copy()

    if len(d) < 2:
        return None

    d = kmeans_anomaly(d)

    metrics = {
        "symbol": symbol,
        "illiquidity": amihud_illiquidity(d),
        "signed_volume": signed_volume(d),
        "autocorr": order_flow_autocorr(d),
        "institutional_score": institutional_score(d),
    }

    signal = generate_signal(d, metrics)
    levels = price_levels(d)
    zones = liquidity_zones(d)

    return {
        "symbol": symbol,
        "metrics": metrics,
        "signal": signal,
        "levels": levels,
        "zones": zones,
        "df": d
    }


def run_full_scan(df):

    results = []

    df = df.copy()
    df["symbol"] = df["symbol"].astype(str)

    for symbol in df["symbol"].unique():
        res = analyze_stock(df, symbol)
        if res:
            results.append(res)

    return results


def rank_stocks(results):

    ranked = []

    for r in results:
        score = r["signal"]["confidence"]

        if r["signal"]["signal"] == "BUY":
            score *= 1.2
        elif r["signal"]["signal"] == "SELL":
            score *= 0.8

        ranked.append({
            "symbol": r["symbol"],
            "signal": r["signal"]["signal"],
            "confidence": round(score, 2)
        })

    return sorted(ranked, key=lambda x: x["confidence"], reverse=True)
