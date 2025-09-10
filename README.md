# Installation
Either clone this repo and install locally:
```
git clone https://github.com/arendMoerman/tod_analyse.git
cd tod_analyse
pip install .
```
or install directly from github:
```
pip install git+https://github.com/arendMoerman/tod_analyse.git
```

# Usage
Assume you have loaded a DEMS file, corresponding to some `obsid`, into a DataArray called `da`.
It is important that the negative response checking is performed **BEFORE** atmospheric baseline subtraction, otherwise anti-correlating temporal trends cannot be seen. 
Similarly, bimodality checking must be applied **AFTER** baseline subtraction, otherwise the binned TODs are not Gaussian.
A minimum example for bimodality and negative response checking would be the following.
```
from tod_analyse.tod_analyse import bimod, nresp

chan = da.chan.data
tods = da.to_numpy()

chan_nresp, median_corrcoef = nresp(tods, chan, obsid)

# Apply baseline subtraction here...

chan_bimod, log_diff = bimod(tods_baseline_subtracted, chan, obsid)
```

Here, `nresp` returns the channels, unchanged from the input `chan` argument, and corresponding median correlation coefficient. 
This way, the user can set their own threshold and can do their own selecting. 
The `bimod` function also returns the channels, which are unchanged as well, and returns corresponding logarithmic likelihood differences.
It uses the EM algorithm on both the mixture model and single Gaussian.

Aside from returning channel and statistic, these two functions also write a dictionary, named either `<obsid>_bimod.json` or `<obsid>_nresp.json`, to disk.
These can be stored for later usage so that you don't have to run these checks all the time.
