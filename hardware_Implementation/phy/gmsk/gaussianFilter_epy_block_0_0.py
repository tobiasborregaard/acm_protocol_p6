"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr, filter


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, samples_per_symbol=4, bt=0.25):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Gaussian filter',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.float32]
        )
        samples_per_symbol = int(samples_per_symbol)
        self._samples_per_symbol = samples_per_symbol
        self._bt = bt
        ntaps = 4 * samples_per_symbol

        # Generate Gaussian filter taps
        gaussian_taps = filter.firdes.gaussian(
        1,                       # gain
        samples_per_symbol,    # symbol_rate
        bt,                       # bandwidth * symbol time
        ntaps                       # number of taps
        )

        taps =  np.convolve(np.array(gaussian_taps), np.ones(samples_per_symbol))
        print(taps)

        self.gaussian_filter = filter.interp_fir_filter_fff(samples_per_symbol, taps)
        print(self.gaussian_filter)
        # self.sqwave = (1,) * samples_per_symbol       # rectangular window
        # self.taps = np.convolve(np.array(gaussian_taps), np.array(self.sqwave))
        # print(self.taps)
        # print(type(self.taps))
        

    def work(self, input_items, output_items):
        data = 2 * input_items[0][:] - 1	# convert to NRZ
        print(type(input_items))
        print(type(input_items[0]))
        output_items[0][:] = data
        return len(output_items[0])
