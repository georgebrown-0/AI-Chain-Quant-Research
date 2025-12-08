import yfinance as yf
import pandas as pd

def get_price_data(symbols, start, end):
    df = yf.download(symbols, start=start, end=end, auto_adjust=True)
    # We only want the adjusted close prices
    # When we use auto_adjust=True, the 'Close' column is already adjusted
    adj = df["Close"]
    adj.columns = adj.columns.get_level_values(0) 
    
    return adj.dropna()