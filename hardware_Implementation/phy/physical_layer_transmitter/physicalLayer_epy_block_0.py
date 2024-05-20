import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, modcod = 0):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='MUX',   # will show up in GRC
            in_sig = [np.byte], 
            out_sig = [np.float32]
            # out_sig = [np.float32, np.float32, np.float32, np.float32, np.float32, np.float32]
        )
        self.modcod = modcod    
    #     Message handling
    #     self.selectPortName = 'modcod'
    #     self.message_port_register_in(pmt.intern(self.selectPortName))
    #     self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)
    #     self.modcod = 0

    # def handle_msg(self, msg):
    #     self.modcod = pmt.to_long(msg)
   
    def work(self, input_items, output_items):
        # MODCOD order from 0-5, 2FSK, 4FSK, MSK, G2FSK, G4FSK, GMSK
        output_items[self.modcod][:] = input_items[0][:] 
        return len(output_items[0])
