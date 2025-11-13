import numpy as np
from scipy.stats import norm

def se_from_sigma_n(sigma, n):
    return sigma / np.sqrt(n)

def critical_from_alpha(mu0, se, alpha, tail):
    if tail == "right":
        z = norm.ppf(1 - alpha)
        return None, mu0 + z * se
    if tail == "left":
        z = norm.ppf(alpha)
        return mu0 + z * se, None
    z = norm.ppf(1 - alpha / 2.0)
    return mu0 - z * se, mu0 + z * se

def errors_from_c(mu0, mu1, se, cL, cR, tail):
    if tail == "right":
        c = cR
        alpha = 1 - norm.cdf(c, loc=mu0, scale=se)
        beta  = norm.cdf(c, loc=mu1, scale=se)
        power = 1 - beta
        return float(alpha), float(beta), float(power), None, float(c)

    if tail == "left":
        c = cL
        alpha = norm.cdf(c, loc=mu0, scale=se)
        beta  = 1 - norm.cdf(c, loc=mu1, scale=se)
        power = 1 - beta
        return float(alpha), float(beta), float(power), float(c), None

    alpha = (1 - norm.cdf(cR, loc=mu0, scale=se)) + norm.cdf(cL, loc=mu0, scale=se)
    beta  =      norm.cdf(cR, loc=mu1, scale=se)  - norm.cdf(cL, loc=mu1, scale=se)
    power = 1 - beta
    return float(alpha), float(beta), float(power), float(cL), float(cR)
