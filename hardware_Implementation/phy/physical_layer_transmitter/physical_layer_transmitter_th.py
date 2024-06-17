import json
import numpy as np


file_name = r"C:\Users\chri0\Documents\GitHub\acm_protocol_p6\hardware_Implementation\phy\physical_layer_transmitter\MODCOD.json"
# file_name = "MODCOD.json"
data:dict
with open(file_name, 'r') as f:
    data = json.load(f)

def modcod(bw, modcod):
    spectral_eff = data[modcod]["SPECT"]
    throughput = spectral_eff * bw
    return throughput
