import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def amihud_illiquidity(df):
    df = df.copy()
    df["return"] = df["close"].pct_change().abs()
    df["illiquidity"] = df["return"] / (df["volume"] + 1)
    return df["illiquidity"].mean()


def signed_volume(df):
    df = df.copy()
    df["direction"] = np.sign(df["close"] - df["open"])
    df["signed_volume"] = df["direction"] * df["volume"]
    return df["signed_volume"].sum()


def order_flow_autocorr(df):
    df = df.copy()
    df["flow"] = np.sign(df["close"].diff())
    return df["flow"].autocorr()


def kmeans_anomaly(df):
    features = df[["open", "high", "low", "close", "volume"]].fillna(0)
    model = KMeans(n_clusters=3, n_init=10, random_state=42)
    df["cluster"] = model.fit_predict(features)
    return df


def liquidity_zones(df):
    high = df["high"].max()
    low = df["low"].min()
    poc = df.groupby("close")["volume"].sum().idxmax()

    return {
        "VAH": high,
        "VAL": low,
        "POC": poc
    }


def institutional_score(df):
    vol_mean = df["volume"].mean()
    big_volume = df[df["volume"] > vol_mean * 1.5]
    return len(big_volume) / len(df)
