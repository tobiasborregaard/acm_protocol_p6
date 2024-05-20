import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, snr=10):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='AWGN Channel',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.snr = snr
        window_size = 100
        self.kernel = np.ones(window_size)/window_size

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
        output_items[0][:] = input_items[0][:] + noise_vector
        return len(output_items[0])
