import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, fft_size=2**15, bandwidth=500, samplerate = 32e3, addr = "snr_meas"):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='SNR Measurement',   
            in_sig = [(np.complex64, fft_size)],
            out_sig = None 
        )
        self.addr = addr
        self.fft_size = fft_size
        self.samplerate = samplerate
        self.bandwidth = bandwidth
        self.snrAvg = 0
        
        self.snr = np.zeros(int((samplerate/fft_size)))
        self.window = int(0.5*(samplerate/fft_size)) # 0.5 s window
        self.kernel = np.ones(self.window) / self.window
        # self.portName = 'print_out'

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
        
        data = input_items[0][0][:]

        fft = np.fft.fft(data) * 1/self.fft_size
        fft_shifted = np.fft.fftshift(fft) 
        magsquared = fft_shifted.real**2 + fft_shifted.imag**2
        # print("fft")
        res = self.samplerate/self.fft_size
        span = int(self.bandwidth/res)
        center = int(self.fft_size/2)
        start =int( center - span/2)
        stop = int(center + span/2)
        sig = magsquared[start:stop]
       
        noise = np.append(magsquared[0:start-int(span/2)], magsquared[stop+int(span/2):])
        noise = span*np.mean(noise)
        # noise = magsquared[:span]

        # print(f"Range %i - %i, Noise %.3f, len: %i" % (start, stop, 10*np.log10(np.mean(sig)), len(sig)))
    
        noise_power = 10*np.log10(noise)
        receive_power = 10*np.log10(np.sum(sig))
        snr = receive_power - noise_power

        # Update the SNR buffer
        self.snr = self.snr[1:]
        self.snr = np.append(self.snr, snr)

        # Calculate the moving average of the SNR with convolution
        self.snrAvg = np.convolve(self.snr, self.kernel, mode='valid')[-1]
        print(self.snrAvg)
        # self.message_port_pub(pmt.intern(self.portName), pmt.to_pmt(self.snrAvg))
        #output_items[0][:] = 10*np.log10(magsquared) # To view the fft in vector sink

        return 1
