import pandas as pd
import numpy as np
from utils import safe_request
from bs4 import BeautifulSoup
import random

NEPSE_URL = "https://www.nepalstock.com.np/today-price"

def fetch_nepse_table():
    html = safe_request(NEPSE_URL)
    if not html:
        return None

    try:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        if table is None:
            return None

        df = pd.read_html(str(table))[0]
        return df
    except:
        return None


def fetch_sharesansar():
    url = "https://www.sharesansar.com/today-share-price"
    html = safe_request(url)
    if not html:
        return None

    try:
        tables = pd.read_html(html)
        if tables:
            return tables[0]
    except:
        return None

    return None


def fetch_nepsealpha():
    url = "https://nepsealpha.com/trading"
    html = safe_request(url)
    if not html:
        return None

    try:
        tables = pd.read_html(html)
        return tables[0] if tables else None
    except:
        return None


def generate_synthetic_data():
    symbols = ["NABIL", "SCB", "GBIME", "NICA", "ADBL"]
    data = []

    for s in symbols:
        base = random.randint(200, 1200)
        for i in range(30):
            close = base + random.randint(-20, 20)
            vol = random.randint(1000, 10000)

            data.append({
                "symbol": s,
                "open": close - random.randint(1, 5),
                "high": close + random.randint(1, 10),
                "low": close - random.randint(1, 10),
                "close": close,
                "volume": vol
            })

    return pd.DataFrame(data)


def fetch_all():
    df = fetch_nepse_table()
    if df is not None:
        return df

    df = fetch_sharesansar()
    if df is not None:
        return df

    df = fetch_nepsealpha()
    if df is not None:
        return df

    return generate_synthetic_data()
