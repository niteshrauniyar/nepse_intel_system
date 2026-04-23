import pandas as pd
import numpy as np
import random

# =========================
# GUARANTEED STRUCTURE ENGINE
# =========================
def _make_structured(symbols):
    data = []

    for s in symbols:
        base = random.randint(300, 1200)

        for _ in range(40):
            open_p = base + random.randint(-8, 8)
            close = open_p + random.randint(-12, 12)

            high = max(open_p, close) + random.randint(1, 6)
            low = min(open_p, close) - random.randint(1, 6)

            volume = random.randint(1000, 40000)

            data.append({
                "symbol": s,
                "open": float(open_p),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": float(volume)
            })

    return pd.DataFrame(data)


# =========================
# SAFE FETCH ENTRY POINT
# =========================
def fetch_all():

    # IMPORTANT: ALWAYS SAME SCHEMA
    symbols = [
        "NABIL",
        "NICA",
        "GBIME",
        "SCB",
        "ADBL",
        "HBL",
        "NRIC"
    ]

    df = _make_structured(symbols)

    # FINAL SAFETY CHECK
    required = ["symbol", "open", "high", "low", "close", "volume"]

    for r in required:
        if r not in df.columns:
            raise ValueError(f"Missing column: {r}")

    return df
