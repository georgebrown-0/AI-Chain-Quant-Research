import plotly.graph_objects as go

def plot_prices(prices, t1, t2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices.index, y=prices[t1], name=t1))
    fig.add_trace(go.Scatter(x=prices.index, y=prices[t2], name=t2))
    fig.update_layout(title="Price History", xaxis_title="Date", yaxis_title="Price")
    return fig

def plot_spread_zscore(spread, zs, entry_z = 2.0):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread"))
    fig.add_trace(go.Scatter(x=zs.index, y=zs, name="Z-Score"))
    fig.add_hline(y=entry_z, line_dash="dash")
    fig.add_hline(y=-entry_z, line_dash="dash")
    fig.update_layout(title="Spread & Z-Score")
    return fig

def plot_pnl(pnl):
    cum = pnl.cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cum.index, y=cum, name="Cumulative PnL"))
    fig.update_layout(title="Cumulative PnL", xaxis_title="Date", yaxis_title="PnL")
    return fig
