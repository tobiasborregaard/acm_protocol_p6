"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr, analog


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, samples_per_symbol=4):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='FSK Modulation',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        samples_per_symbol = int(samples_per_symbol)
        self._samples_per_symbol = samples_per_symbol
        self.freqDeviation = (np.pi / 2) / samples_per_symbol 
        

    def work(self, input_items, output_items):
        fmmod = analog.frequency_modulator_fc(self.freqDeviation)
        print(fmmod)
        # output_items[0][:] = fmmod.modulate(input_items[0])
        return len(output_items[0])
