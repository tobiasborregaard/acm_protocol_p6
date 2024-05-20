import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='NRZ',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.float32]
        )
      

    def work(self, input_items, output_items):
        output_items[0][:] = 2*input_items[0] -1 
        return len(output_items[0])
