import pandas as pd

def backtest(spread, z_score):
    # Simple backtest based on period when z-score crosses thresholds
    # Adjust threshold values as needed
    threshold = 2
    long_signal = z_score < -threshold
    short_signal = z_score > threshold
    exit_signal = (z_score > -0.5) & (z_score < 0.5)
    position = 0
    pnl = []

    for i in range(1, len(spread)):
        if position == 0:
            if long_signal.iloc[i]:
                position = 1
            elif short_signal.iloc[i]:
                position = -1
        elif exit_signal.iloc[i]:
            position = 0

        pnl.append(position * (spread.iloc[i] - spread.iloc[i-1]))

    return pd.Series(pnl, index=spread.index[1:])
