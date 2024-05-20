import numpy as np
from gnuradio import filter

def generate_taps(samples_per_symbol, bt):
    samples_per_symbol = int(samples_per_symbol)
    ntaps = 4 * samples_per_symbol

    # Generate Gaussian filter taps
    gaussian_taps = filter.firdes.gaussian(
        1,                       # gain
        samples_per_symbol,      # symbol_rate
        bt,                      # bandwidth * symbol time
        ntaps                    # number of taps
    )

    taps = np.convolve(np.array(gaussian_taps), np.ones(samples_per_symbol))
    return taps