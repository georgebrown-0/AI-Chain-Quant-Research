import pandas as pd
import numpy as np

def half_life(spread):
    s = spread.dropna()
    s_lag = s.shift(1).dropna()
    s_curr = s.loc[s_lag.index]

    x = s_lag.values
    y = s_curr.values

    b, a = np.polyfit(x, y, 1)

    if b<=0 or b>=1:
        return np.nan

    hl = -np.log(2)/np.log(b)
    return float(hl)

def z_band_from_hl(spread, HL0 = 20.0, B0 = 2.0, hl_max = 120):
    hl = half_life(spread)
    if np.isnan(hl):
        return hl, B0
    hl_clamped = min(hl, hl_max)
    band = (B0 * (hl_clamped / HL0)) ** 0.5
    return hl, float(band)

                      
    

def backtest(spread, z_score, threshold = 2.0, alpha = 0.25):
    # Simple backtest based on period when z-score crosses thresholds
    # Adjust threshold values as needed
    exit_band = alpha * threshold
    long_signal = z_score < -threshold
    short_signal = z_score > threshold
    exit_signal = (z_score > -exit_band) & (z_score < exit_band)
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
    
