import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import random

DB = "nepse_cache.db"

# =========================
# DATABASE CACHE
# =========================
def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            symbol TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_cache(df):
    conn = sqlite3.connect(DB)
    df.to_sql("market_data", conn, if_exists="replace", index=False)
    conn.close()


def load_cache():
    conn = sqlite3.connect(DB)
    try:
        df = pd.read_sql("SELECT * FROM market_data", conn)
        return df
    except:
        return None
    finally:
        conn.close()


# =========================
# SAFE SCRAPER
# =========================
HEADERS = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120"},
    {"User-Agent": "Safari"}
]


def safe_request(url):
    for _ in range(3):
        try:
            r = requests.get(url, headers=random.choice(HEADERS), timeout=10)
            if r.status_code == 200:
                return r.text
        except:
            time.sleep(1)
    return None


# =========================
# PRIMARY SOURCE (NEPSE)
# =========================
def fetch_nepse():
    url = "https://www.nepalstock.com.np/today-price"
    html = safe_request(url)

    try:
        if html:
            tables = pd.read_html(html)
            if tables:
                df = tables[0]
                return df
    except:
        pass

    return None


# =========================
# NORMALIZER (CRITICAL FIX)
# =========================
def normalize(df):
    if df is None or df.empty:
        return None

    df = df.copy()
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    # map possible columns
    mapping = {
        "symbol": ["symbol", "security", "company_name"],
        "open": ["open", "op"],
        "high": ["high"],
        "low": ["low"],
        "close": ["close", "ltp", "last_traded_price"],
        "volume": ["volume", "traded_quantity"]
    }

    out = pd.DataFrame()

    for key, options in mapping.items():
        for col in options:
            if col in df.columns:
                out[key] = df[col]
                break

    # force numeric
    for c in ["open", "high", "low", "close", "volume"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)

    if "symbol" not in out.columns:
        return None

    return out


# =========================
# MAIN ENGINE
# =========================
def fetch_all():

    init_db()

    df = fetch_nepse()
    df = normalize(df)

    if df is not None and len(df) > 0:
        save_cache(df)
        return df

    # fallback = LAST KNOWN GOOD DATA (NOT RANDOM)
    cached = load_cache()

    if cached is not None and len(cached) > 0:
        return cached

    # last resort safety
    return pd.DataFrame(columns=["symbol","open","high","low","close","volume"])
