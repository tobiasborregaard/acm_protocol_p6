import numpy as np
from gnuradio import gr
import pmt
import json


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, addr="modcod"):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='MUX',   # will show up in GRC
            in_sig = [np.complex64, np.complex64, np.complex64],
            out_sig = [np.complex64]
        )
        self.addr = addr
        self.modcod = "1" # default modcod
        
        # read MODCOD from json file
        # file_name = 'MODCOD.json'
        self.filename = "MODCOD.json"
        self.json_data = None

        # message port setup
        self.message_in = 'msg_in'
        self.message_port_register_in(pmt.intern(self.message_in))
        self.set_msg_handler(pmt.intern(self.message_in), self.mailbox)
        self.message_out = 'msg_out'
        self.message_port_register_out(pmt.intern(self.message_out))
        
    def extract_pmt(self, msg):
        try:
            data = pmt.to_python(msg)
        except:
            self.message_port_pub(pmt.intern(self.message_out), pmt.to_pmt("Err: Invalid format"))
        return data

    def unpack(self, msg):
        if msg[0] == self.addr:
            return msg[1:]
        else: return False


    def mailbox(self, msg):
        r = {}
        try:
            data = self.extract_pmt(msg)

            #If address check is active:
            data = self.unpack(data)
            if data == False: return 

            varname = list(data[1].keys())[0]
            if varname not in self.__dict__:
                raise Exception("Err: Unknown variable")
            
            if data[0].lower() == "get":
                r[varname] = self.__dict__[varname]
            elif data[0].lower() == "set":
                if type(data[1][varname]) != type(self.__dict__[varname]):
                    raise Exception("Err: Variable in wrong format")
                else:
                    self.__dict__[varname] = data[1][varname]
                    r[varname] = "ok"
            
            #If address return with SRC
            r = [self.addr, r]

            self.message_port_pub(pmt.intern(self.message_out), pmt.to_pmt(r))
            return

        except Exception as e:
            self.message_port_pub(pmt.intern(self.message_out), pmt.to_pmt(str(e)))

   
    def work(self, input_items, output_items):
        if self.json_data == None:
            with open(self.filename) as json_file:
                self.json_data = json.load(json_file)

         # determine the appropriate modcod
        modcod_idx = self.json_data[self.modcod]["MOD"]
        match modcod_idx:
            case "g4FSK":
                modcod_idx = 0
            case "MSK":
                modcod_idx = 1
            case "gMSK":
                modcod_idx = 2
            case _:
                raise ValueError("Invalid modcod")
        
        output_items[0][:] = input_items[modcod_idx] 
        
        return len(output_items[0])
