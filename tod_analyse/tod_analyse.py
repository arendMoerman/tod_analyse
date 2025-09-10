import os
import numpy as np
from scipy.stats import norm
import json

from tqdm import tqdm

from tod_analyse.em import run_em, log_likelihood_diff
from tod_analyse.plot import plot_diagnostics

def bimod(tod, chan, obsid, plot=True):
    log_diff_l = []
    chan_l = []

    for i in tqdm(range(tod.shape[1])):
        data = tod[:,i]
        if np.all(np.isnan(data)):
            print(f"Channel {chan[i]} only has NaN values!")
            continue

        means, variances, weights = run_em(data)
        means_mono, variances_mono, weights_mono = run_em(data, num=1)

        log_diff = log_likelihood_diff(data, weights, means, variances, means_mono, variances_mono)

        log_diff_l.append(log_diff)
        chan_l.append(chan[i])

        if plot:
            plot_diagnostics(data, weights, means, variances, means_mono, variances_mono, log_diff, chan[i], obsid)

    to_write = {int(chan_l[i]) : log_diff_l[i] for i in range(len(chan_l))}

    with open(f"{obsid}_bimod.json", 'w') as file:
        json.dump(to_write, file, indent=4)

    return chan_l, log_diff_l

def nresp(tod, chan, obsid, plot=False):
    """
    Find channels with negative responses by calculating correlation coefficient.
    
    @param da Data array containing DEMS file.
    @param thres_r Threshold for rejection of KID based on correlation coefficient.
        Default is 0, meaning only KIDs with r < 0 get rejected.
    @param verbose Whether to print progress info or not. Default is true.

    @returns Array containing master indices of KIDs with negative responses.
    """

    mat = np.corrcoef(tod.T) 

    meds = np.nanmedian(mat, axis=1)
    to_write = {int(chan[i]) : meds[i] for i in range(len(chan))}

    with open(f"{obsid}_nresp.json", 'w') as file:
        json.dump(to_write, file, indent=4)

    return chan, meds

def flag_chans(tod, chan, obsid, json_type, threshold):
    with open(f"{obsid}_{json_type}.json", 'r') as file:
        flag_dict = json.load(file)

    if json_type == "bimod":
        chan_keep = np.array([x for x, y in flag_dict.items()if y < threshold])
    else:
        chan_keep = np.array([x for x, y in flag_dict.items()if y > threshold])

    _, idx_keep, _ = np.intersect1d(chan, chan_keep, assume_unique=True, return_indices=True)

    return tod[:,idx_keep], chan[idx_keep], idx_keep
