import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, snr=10, addr="awgn"):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='AWGN Channel',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.addr = addr
        self.snr = snr
        window_size = 100
        self.kernel = np.ones(window_size)/window_size

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
        # Calculate the moving average of the signal power to determine the noise power
        data = input_items[0][:]
        signal_power = data.real**2 + data.imag**2 # convert to power
        signal_power_avg = np.convolve(signal_power, self.kernel , mode='same')[-1]
        noise_power = signal_power_avg / 10**(self.snr/10)

        # Debug messages
        # if self.nitems_written(0) % 100 == 0:
        #     print(f"Signal Power Average: {np.sqrt(signal_power_avg)}")
        #     print(f"Noise Power: {np.sqrt(noise_power)}")

        noise_vector = np.sqrt(noise_power) * (np.random.randn(len(input_items[0])) + 1j * np.random.randn(len(input_items[0])))
        output_items[0][:] = input_items[:] + noise_vector
        return len(output_items[0])
