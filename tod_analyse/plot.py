import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.stats import norm

def plot_diagnostics(data, weights, means, variances, means_mono, variances_mono, log_diff, chan, obsid):
    save_path = f"./plots/bimodality_check/{obsid}/"

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    x = np.linspace(min(data), max(data), 1000)

    y1 = weights[0] * norm.pdf(x, means[0], np.sqrt(variances[0]))
    y2 = weights[1] * norm.pdf(x, means[1], np.sqrt(variances[1]))
        
    y_mono = norm.pdf(x, means_mono, np.sqrt(variances_mono))
    #fig, ax = plt.subplots(1,2)
    plt.subplot(2,2,1)
    plt.hist(data, bins=100, density=True)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y1 + y2, c="k", ls="dashed")

    plt.subplot(2,2,2)
    plt.hist(data, bins=100, density=True)
    plt.plot(x, y_mono)
    
    plt.subplot(2,1,2)
    plt.plot(data)

    plt.suptitle(f"chan = {chan}, diff log P = {log_diff}")
    plt.savefig(save_path + f"{chan}.png")
    plt.close()
    plt.cla()
    plt.clf()
