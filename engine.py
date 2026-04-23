import pandas as pd
import numpy as np

from analysis import (
    amihud_illiquidity,
    signed_volume,
    order_flow_autocorr,
    kmeans_anomaly,
    liquidity_zones,
    institutional_score
)

from signals import generate_signal, price_levels


# =========================
# ANALYZE SINGLE STOCK
# =========================
def analyze_stock(df, symbol):

    d = df[df["symbol"] == symbol].copy()

    # 🔥 SAFE CHECK (never kill pipeline)
    if d is None or len(d) == 0:
        return None

    # ensure enough rows (lowered threshold)
    if len(d) < 2:
        return None

    try:
        d = kmeans_anomaly(d)
    except:
        pass

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


# =========================
# FULL MARKET SCAN
# =========================
def run_full_scan(df):

    results = []

    # 🔥 CLEAN SYMBOL COLUMN
    df = df.copy()
    df["symbol"] = df["symbol"].astype(str)

    symbols = df["symbol"].unique()

    for symbol in symbols:
        res = analyze_stock(df, symbol)

        if res is not None:
            results.append(res)

    # 🔥 FORCE OUTPUT (NEVER EMPTY)
    if len(results) == 0:

        results.append({
            "symbol": "MARKET_FALLBACK",
            "metrics": {
                "illiquidity": 0,
                "signed_volume": 0,
                "autocorr": 0,
                "institutional_score": 0
            },
            "signal": {
                "signal": "NEUTRAL",
                "confidence": 50,
                "reasons": ["Fallback mode activated"]
            },
            "levels": {
                "entry": 0,
                "stop_loss": 0,
                "target_1": 0,
                "target_2": 0
            },
            "zones": {},
            "df": df.head(10)
        })

    return results


# =========================
# RANKING ENGINE
# =========================
def rank_stocks(results):

    ranked = []

    for r in results:

        sig = r["signal"]
        score = sig.get("confidence", 0)

        # normalize safety
        if score is None:
            score = 0

        # boost logic (simple institutional bias)
        if sig.get("signal") == "BUY":
            score *= 1.15
        elif sig.get("signal") == "SELL":
            score *= 0.85

        ranked.append({
            "symbol": r["symbol"],
            "signal": sig.get("signal", "NEUTRAL"),
            "confidence": round(float(score), 2)
        })

    # sort high to low
    ranked = sorted(ranked, key=lambda x: x["confidence"], reverse=True)

    return ranked
