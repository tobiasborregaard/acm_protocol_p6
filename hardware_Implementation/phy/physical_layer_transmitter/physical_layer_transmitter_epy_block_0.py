import numpy as np
from gnuradio import gr
import pmt
import json

class blk(gr.interp_block):  # other base classes are basic_block, decim_block, interp_block
    
    def __init__(self, addr = "modcod", interpolation = 10, samp_rate=32000, bandwidth = 25000):  # only default arguments here
        gr.interp_block.__init__(
            self,
            name='DEMUX',   # will show up in GRC
            in_sig = [np.byte], 
            out_sig = [np.byte, np.byte, np.byte],
            interp = interpolation
        )
        self.addr = addr
        self._modcod = "1" # default modcod
        self.samp_rate = samp_rate
        self.bandwidth = bandwidth
        self.repack = 1
    
        # read MODCOD from json file      
        #file_name = r"C:\Users\chri0\Documents\GitHub\SDR_Ground_Station\hardwareImplementation\phy\physical_layer_transmitter\MODCOD.json"
        self.filename = "MODCOD.json"
        self.json_data = None
        
        
        # message port setup
        self.message_in = 'msg_in'
        self.message_port_register_in(pmt.intern(self.message_in))
        self.set_msg_handler(pmt.intern(self.message_in), self.mailbox)
        self.message_out = 'msg_out'
        self.message_port_register_out(pmt.intern(self.message_out))

        self.message_out2 = 'repack_out'
        self.message_port_register_out(pmt.intern(self.message_out2))

        self.message_out3 = 'interp_out'
        self.message_port_register_out(pmt.intern(self.message_out3))


        
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

    @property
    def modcod(self):
        return self._modcod
    
    @modcod.setter
    def modcod(self, value: str):
        self._modcod = value
        repack = 1
        
        modcod_spect = self.json_data[self.modcod]["SPECT"]           
        throughput = modcod_spect*self.bandwidth
        if self.json_data[self.modcod]["MOD"] == "g4FSK":
            repack = 2
            throughput = 0.5*throughput # symbol rate conversion

        self._interp = int(np.ceil(self.samp_rate/throughput)) 

        # Define the interpolation rate globally using msg output
        interp = pmt.from_long(self._interp)
        interp_msg = pmt.cons(pmt.string_to_symbol("repack_size"), interp)
        self.message_port_pub(pmt.intern(self.message_out3), interp_msg)

        # Define the repack size globally using msg output
        if self.repack != repack:
            self.repack = repack
            repack = pmt.from_long(repack)
            msg = pmt.cons(pmt.string_to_symbol("repack_size"), repack)
            self.message_port_pub(pmt.intern(self.message_out2), msg)

    def mailbox(self, msg):
        r = {}
        try:
            data = self.extract_pmt(msg)

            #If address check is active:
            data = self.unpack(data)
            if data == False: return 

            varname = list(data[1].keys())[0]
            if varname == "modcod":
                pass
            elif varname not in self.__dict__:
                raise Exception("Err: Unknown variable")
            
            if data[0].lower() == "get":
                if varname == "modcod":
                    r[varname] = self.modcod
                else:
                    r[varname] = self.__dict__[varname]
            elif data[0].lower() == "set":
                if varname == "modcod":
                    self.modcod = data[1][varname]
                    r[varname] = "ok"
                elif type(data[1][varname]) != type(self.__dict__[varname]):
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

        # Apply interpolation rate according to desired bitrate, if the modcod is g4FSK
        # the interpolation is doubled to account for repacking of bits       
        for i in range(len(input_items[0])):
            for j in range(self._interp):
                output_items[modcod_idx][i*self._interp + j] = input_items[0][i]
            

        return len(output_items[0])