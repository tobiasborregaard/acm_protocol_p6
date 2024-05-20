import json
import numpy as np

file_name = 'MODCOD.json'

data:dict
with open(file_name, 'r') as f:
    data = json.load(f.read())

def interpolation(samp_rate, bw, modcod):
    spectral_eff = data[modcod]["SPECT"]
    throughput = spectral_eff * bw
    baud_rate = samp_rate 
    interp_factor = baud_rate / throughput
    if interp_factor < 1:
        raise ValueError("Interpolation factor is less than 1") 

    return int(np.ceil(interp_factor))
