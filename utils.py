import random
import time
import requests

HEADERS_POOL = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/120.0"},
    {"User-Agent": "Safari/537.36"},
]

def get_headers():
    return random.choice(HEADERS_POOL)

def safe_request(url, retries=3, timeout=10):
    for _ in range(retries):
        try:
            res = requests.get(url, headers=get_headers(), timeout=timeout)
            if res.status_code == 200:
                return res.text
        except Exception:
            time.sleep(1)
    return None


def safe_float(x):
    try:
        return float(str(x).replace(",", "").strip())
    except:
        return None
