import os
import numpy as np
from scipy.stats import norm

# Initialize parameters
def initialize_params(data, num):
    np.random.seed(42)
    means = np.random.choice(data, num)
    variances = np.ones(num) * np.nanvar(data)
    weights = np.ones(num) / num
    return means, variances, weights

# Expectation step
def expectation(data, means, variances, weights, num):
    responsibilities = np.zeros((len(data), num))
    for k in range(num):
        responsibilities[:, k] = weights[k] * norm.pdf(data, means[k], np.sqrt(variances[k]))
    responsibilities /= np.nansum(responsibilities, axis=1, keepdims=True)
    return responsibilities

# Maximization step
def maximization(data, responsibilities):
    N_k = np.nansum(responsibilities, axis=0)
    weights = N_k / len(data)
    means = np.nansum(responsibilities * data[:, np.newaxis], axis=0) / N_k
    variances = np.nansum(responsibilities * (data[:, np.newaxis] - means) ** 2, axis=0) / N_k
    return means, variances, weights

# Run EM algorithm
def run_em(data, num=2, iterations=100, tol=1e-6):
    means, variances, weights = initialize_params(data, num)
    
    for i in range(iterations):
        old_means = means.copy()
        
        responsibilities = expectation(data, means, variances, weights, num)
        means, variances, weights = maximization(data, responsibilities)
        
        # Convergence check
        if np.allclose(means, old_means, atol=tol):
            break

    return means, variances, weights

def log_likelihood_diff(data, weights, means_bi, vars_bi, means_mono, vars_mono):
    logP2 = np.log(weights[0] * norm.pdf(data, means_bi[0], np.sqrt(vars_bi[0])) + 
                   weights[1] * norm.pdf(data, means_bi[1], np.sqrt(vars_bi[1])))

    logP1 = np.log(norm.pdf(data, means_mono, np.sqrt(vars_mono)))

    return np.nansum(logP2 - logP1) / data.size

