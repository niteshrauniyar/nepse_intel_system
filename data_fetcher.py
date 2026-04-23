import pandas as pd
import requests
import random
import time

BASE_URL = "https://pro.sumeru/api"

HEADERS = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120"},
    {"User-Agent": "Safari"}
]


# =========================
# SAFE REQUEST
# =========================
def safe_get(url):
    for _ in range(3):
        try:
            r = requests.get(url, headers=random.choice(HEADERS), timeout=10)
            if r.status_code == 200:
                return r.json()
        except:
            time.sleep(1)
    return None


# =========================
# FETCH FUNCTION (SAFE)
# =========================
def fetch_sumeru():

    url = f"{BASE_URL}/market/today"

    data = safe_get(url)

    # 🔥 CRITICAL FIX: NEVER USE df BEFORE CHECK
    if data is None:
        return None

    try:
        df = pd.DataFrame(data)
        return df
    except:
        return None


# =========================
# NORMALIZER
# =========================
def normalize(df):

    if df is None or df.empty:
        return None

    df = df.copy()

    df.columns = [c.lower().strip() for c in df.columns]

    # safe mapping
    def pick(cols):
        for c in cols:
            if c in df.columns:
                return df[c]
        return None

    out = pd.DataFrame()

    out["symbol"] = pick(["symbol", "ticker", "stock"])
    out["open"] = pick(["open"])
    out["high"] = pick(["high"])
    out["low"] = pick(["low"])
    out["close"] = pick(["close", "ltp"])
    out["volume"] = pick(["volume", "qty"])

    # fill missing safely
    for c in ["symbol", "open", "high", "low", "close", "volume"]:
        if c not in out or out[c] is None:
            out[c] = 0

    # numeric conversion
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)

    return out


# =========================
# SAFE FALLBACK
# =========================
def fallback():

    symbols = ["NABIL", "NICA", "GBIME", "SCB"]

    rows = []

    for s in symbols:
        base = random.randint(300, 1200)

        for _ in range(30):
            open_p = base + random.randint(-5, 5)
            close = open_p + random
