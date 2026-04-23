import streamlit as st
import pandas as pd

from data_fetcher import fetch_all
from data_cleaner import standardize
from engine import run_full_scan, rank_stocks
from charts import plot_chart

st.set_page_config(page_title="NEPSE Institutional Intelligence V2", layout="wide")

st.title("📊 NEPSE Institutional Intelligence System V2")

# Load data
raw = fetch_all()
df = standardize(raw)

# Run per-stock institutional scan
results = run_full_scan(df)
ranking = rank_stocks(results)

# ======================
# UI TABS
# ======================

tab1, tab2, tab3 = st.tabs([
    "🏆 Top Signals",
    "📊 Stock Deep Dive",
    "🧠 Institutional Rankings"
])

# ----------------------
# TAB 1: TOP SIGNALS
# ----------------------
with tab1:
    st.subheader("High Conviction Trades")

    for r in results:
        sig = r["signal"]

        if sig["confidence"] < 40:
            continue

        st.markdown(f"## {r['symbol']}")

        st.write("Signal:", sig["signal"])
        st.write("Confidence:", sig["confidence"])

        for reason in sig["reasons"]:
            st.write("•", reason)

        st.divider()

# ----------------------
# TAB 2: SINGLE STOCK VIEW
# ----------------------
with tab2:
    symbol = st.selectbox("Select Stock", df["symbol"].unique())

    res = next((r for r in results if r["symbol"] == symbol), None)

    if res:
        st.subheader(symbol)

        st.plotly_chart(
            plot_chart(res["df"], res["levels"]),
            use_container_width=True
        )

        st.write("### Signal")
        st.json(res["signal"])

        st.write("### Metrics")
        st.json(res["metrics"])

        st.write("### Liquidity Zones")
        st.json(res["zones"])

# ----------------------
# TAB 3: RANKING
# ----------------------
with tab3:
    st.subheader("Institutional Stock Ranking")

    for r in ranking:
        st.write(f"🏷 {r['symbol']} | {r['signal']} | Score: {r['confidence']:.2f}")
