import streamlit as st
import pandas as pd

# =========================
# SAFE IMPORT (NO CRASH)
# =========================
try:
    from data_fetcher import fetch_all
except Exception as e:
    st.error("❌ data_fetcher import failed")
    st.stop()

from data_cleaner import standardize
from engine import run_full_scan, rank_stocks
from charts import plot_chart

# =========================
# UI CONFIG
# =========================
st.set_page_config(
    page_title="NEPSE Institutional Intelligence",
    layout="wide"
)

st.title("📊 NEPSE Institutional Intelligence System")

# =========================
# LOAD DATA (SAFE)
# =========================
try:
    raw_df = fetch_all()
except Exception as e:
    st.error(f"❌ Data fetch failed: {e}")
    st.stop()

# =========================
# VALIDATION (NO BLANK APP)
# =========================
if raw_df is None or raw_df.empty:
    st.warning("⚠️ No data received. Using fallback engine.")
    st.stop()

df = standardize(raw_df)

if df.empty:
    st.error("❌ Data became empty after cleaning")
    st.stop()

# =========================
# DEBUG PANEL (IMPORTANT)
# =========================
st.write("📦 Data Shape:", df.shape)
st.dataframe(df.head())

# =========================
# RUN ANALYSIS ENGINE
# =========================
results = run_full_scan(df)
ranking = rank_stocks(results)

# =========================
# TABS UI
# =========================
tab1, tab2, tab3 = st.tabs([
    "🏆 Top Signals",
    "📊 Stock Analysis",
    "📈 Rankings"
])

# =========================
# TAB 1: TOP SIGNALS
# =========================
with tab1:
    st.subheader("High Conviction Trades")

    if not results:
        st.warning("No results generated")
    else:
        for r in results:
            sig = r["signal"]

            if sig["confidence"] < 40:
                continue

            st.markdown(f"### {r['symbol']}")
