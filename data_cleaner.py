import pandas as pd

def standardize(df):

    df = df.copy()

    # normalize column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # force symbol
    if "symbol" not in df.columns:
        df["symbol"] = "UNKNOWN"

    # ensure numeric safety
    for col in ["open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # REMOVE ONLY FULLY INVALID ROWS
    df = df[df["symbol"] != "UNKNOWN"]

    return df
