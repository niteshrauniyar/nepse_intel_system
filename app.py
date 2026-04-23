import streamlit as st

from data_fetcher import fetch_all
from data_cleaner import standardize
from analysis import (
    amihud_illiquidity,
    signed_volume,
    order_flow_autocorr,
    kmeans_anomaly,
    liquidity_zones,
    institutional_score
)
from signals import generate_signal, price_levels
from charts import plot_chart

st.set_page_config(page_title="NEPSE Institutional Intelligence", layout="wide")

st.title("📊 NEPSE Institutional Intelligence System")

df = fetch_all()
df = standardize(df)

df = kmeans_anomaly(df)

metrics = {
    "illiquidity": amihud_illiquidity(df),
    "signed_volume": signed_volume(df),
    "autocorr": order_flow_autocorr(df),
    "institutional_score": institutional_score(df)
}

signal = generate_signal(df, metrics)
levels = price_levels(df)
zones = liquidity_zones(df)

tab1, tab2, tab3, tab4 = st.tabs([
    "Market Overview",
    "Institutional Analysis",
    "Signals",
    "Broker Activity"
])

with tab1:
    st.subheader("Price Chart")
    st.plotly_chart(plot_chart(df, levels), use_container_width=True)

with tab2:
    st.write("### Liquidity Zones")
    st.json(zones)

    st.write("### Metrics")
    st.json(metrics)

with tab3:
    st.write("### Trading Signal")
    st.metric("Signal", signal["signal"])
    st.metric("Confidence", f"{signal['confidence']}%")

    st.write("### Reasons")
    for r in signal["reasons"]:
        st.write("•", r)

    st.write("### Price Levels")
    st.json(levels)

with tab4:
    st.info("Broker-level data depends on external NEPSE feeds. Currently using proxy institutional flow model.")
