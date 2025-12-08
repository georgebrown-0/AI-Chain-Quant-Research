import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

def get_hedge_ratio(y, x):
    x_const = sm.add_constant(x)
    model = OLS(y, x_const).fit()
    return model.params[1]
