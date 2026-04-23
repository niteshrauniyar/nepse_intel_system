import plotly.graph_objects as go

def plot_chart(df, levels=None):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price"
    ))

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["volume"],
        name="Volume",
        yaxis="y2"
    ))

    if levels:
        fig.add_hline(y=levels["entry"], line_width=2, line_color="blue")
        fig.add_hline(y=levels["stop_loss"], line_width=2, line_color="red")
        fig.add_hline(y=levels["target_1"], line_width=2, line_color="green")

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=600
    )

    return fig
