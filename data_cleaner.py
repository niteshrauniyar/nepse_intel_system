import pandas as pd
from utils import safe_float

def normalize_columns(df):
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    return df


def clean_numeric(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: safe_float(x) if isinstance(x, str) else x)
    return df


def standardize(df):
    df = normalize_columns(df)
    df = clean_numeric(df)

    required = ["open", "high", "low", "close", "volume"]
    for r in required:
        if r not in df.columns:
            df[r] = 0

    return df
