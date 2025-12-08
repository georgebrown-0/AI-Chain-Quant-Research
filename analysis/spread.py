import numpy as np

def compute_spread(y, x, hr):
    return y - hr * x

def zscore(series):
    return (series - series.mean()) / np.std(series)
