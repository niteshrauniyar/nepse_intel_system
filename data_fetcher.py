import pandas as pd
import requests
import time
import random

# =========================
# CONFIG (SET YOUR BASE URL HERE)
# =========================
BASE_URL = "https://pro.sumeru/api"  # <-- adjust if needed

HEADERS = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120"},
    {"User-Agent": "Safari"}
]


# =========================
# SAFE REQUEST ENGINE
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
# PRO SUMERU FETCH
# =========================
def fetch_sumeru_market():

    url = f"{BASE_URL}/market/today"  # <-- adjust endpoint if needed

    data = safe_get(url)

    if not data:
        return None

    try:
        df = pd.DataFrame(data)
        return df
    except:
        return None


# =========================
# NORMALIZER (CRITICAL)
# =========================
def normalize(df):

    if df is None or df.empty:
        return None

    df = df.copy()

    # standardize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # flexible mapping (handles API variations)
    rename_map = {
        "symbol": ["symbol", "ticker", "stock"],
        "open": ["open"],
        "high": ["high"],
        "low": ["low"],
        "close": ["close", "ltp"],
        "volume": ["volume", "qty", "traded_volume"]
    }

    out = pd.DataFrame()

    for key, options in rename_map.items():
        for col in options:
            if col in df.columns:
                out[key] = df[col]
                break

    # ensure required columns exist
    required = ["symbol", "open", "high", "low", "close", "volume"]

    for r in required:
        if r not in out.columns:
            out[r] = 0

    # numeric cleanup
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)

    return out


# =========================
# FALLBACK CACHE (NO RANDOM FAKE DATA)
# =========================
def fallback_cache():
    try:
        return pd.read_csv("cache.csv")
    except:
        return None


# =========================
# MAIN ENTRY
# =========================
def fetch_all():

    df
