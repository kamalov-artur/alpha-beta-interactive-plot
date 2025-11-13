import numpy as np
from scipy.stats import norm

def errors(mu0, mu1, sigma, c, tail):
    if tail == "right":
        alpha = 1 - norm.cdf(c, loc=mu0, scale=sigma)
        beta  = norm.cdf(c, loc=mu1, scale=sigma)
        power = 1 - beta
        return float(alpha), float(beta), float(power), None, float(c)

    if tail == "left":
        alpha = norm.cdf(c, loc=mu0, scale=sigma)
        beta  = 1 - norm.cdf(c, loc=mu1, scale=sigma)
        power = 1 - beta
        return float(alpha), float(beta), float(power), float(c), None

    # two-sided
    cR = float(c)
    cL = float(2*mu0 - cR)
    alpha = (1 - norm.cdf(cR, loc=mu0, scale=sigma)) + norm.cdf(cL, loc=mu0, scale=sigma)
    beta  = norm.cdf(cR, loc=mu1, scale=sigma) - norm.cdf(cL, loc=mu1, scale=sigma)
    power = 1 - beta
    return float(alpha), float(beta), float(power), cL, cR
