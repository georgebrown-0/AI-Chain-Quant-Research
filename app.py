import streamlit as st
import pandas as pd
from data.downloader import get_price_data
from analysis.cointegration import run_cointegration_test
from analysis.hedge_ratio import get_hedge_ratio
from analysis.spread import compute_spread, zscore
from analysis.backtest import backtest
from utilities.plotting import plot_prices, plot_spread_zscore, plot_pnl

st.title("AI Arbitrage Pair Trading Tools")
st.write("Yuyao Xie - Quant Society")

st.sidebar.header("Settings")
# Default tickers for Visa and Mastercard
ticker1 = st.sidebar.text_input("Ticker 1", "V")
ticker2 = st.sidebar.text_input("Ticker 2", "MA")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2014-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))
run_button = st.sidebar.button("Run Analysis")

if run_button:
    prices = get_price_data([ticker1, ticker2], start_date, end_date)
    st.subheader("Price Data")
    st.plotly_chart(plot_prices(prices, ticker1, ticker2))

    pvalue = run_cointegration_test(prices[ticker1], prices[ticker2])
    st.subheader("Cointegration Test Result")
    st.write(f"**p-value:** {pvalue:.4f}")

    if pvalue < 0.05:
        st.success("The pair appears cointegrated (p < 0.05)")
    else:
        st.warning("The pair does not appear strongly cointegrated.")

    y = prices[ticker1]
    x = prices[ticker2]

    hedge_ratio = get_hedge_ratio(y, x)
    spread = compute_spread(y, x, hedge_ratio)
    z_score = zscore(spread)

    st.subheader("Spread & Z-Score")
    st.plotly_chart(plot_spread_zscore(spread, z_score))

    pnl = backtest(spread, z_score)
    st.subheader("Backtest Results")
    st.write("Z-score min:", z_score.min(), "max:", z_score.max())
    st.write("Number of long signals:", sum(z_score < -2))
    st.write("Number of short signals:", sum(z_score > 2))
    st.plotly_chart(plot_pnl(pnl))

    st.success(f"**Total PnL:** {pnl.sum():.2f}")
    sharpe_ratio = pnl.mean() / pnl.std() if pnl.std() != 0 else 0
    st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")


else:
    st.info("Enter ticker symbols, start and end dates then click **Run Analysis**.")
