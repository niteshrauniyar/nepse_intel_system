import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import random
import time

# =========================
# SAFE HEADERS ROTATION
# =========================
HEADERS = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120.0"},
    {"User-Agent": "Safari/537.36"},
]

def get_headers():
    return random.choice(HEADERS)

# =========================
# SAFE REQUEST (NO CRASH)
# =========================
def safe_request(url, timeout=10, retries=2):
    for _ in range(retries):
        try:
            r = requests.get(url, headers=get_headers(), timeout=timeout)
            if r.status_code == 200:
                return r.text
        except:
            time.sleep(1)
    return None


# =========================
# SCRAPER 1 (NEPSE)
# =========================
def fetch_nepse():
    url = "https://www.nepalstock.com.np/today-price"
    html = safe_request(url)

    try:
        if html:
            tables = pd.read_html(html)
            if tables and len(tables) > 0:
                df = tables[0]
                return df
    except:
        pass

    return None


# =========================
# SCRAPER 2 (SHARESSANSAR)
# =========================
def fetch_sharesansar():
    url = "https://www.sharesansar.com/today-share-price"
    html = safe_request(url)

    try:
        if html:
            tables = pd.read_html(html)
            if
