from scipy.stats import norm
import numpy as np

def calculate_gamma(S, K, T, r, sigma):
    
    T = max(T, 0.0001) 
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma
