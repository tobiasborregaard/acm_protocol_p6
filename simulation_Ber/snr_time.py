import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import re

def fspl(dist):
    freq = 437e6
    wavelen = 3e8/freq

    loss = np.power(((4*np.pi*dist)/wavelen),2)

    loss_db = -10*np.log10(loss)
    return loss_db

def calc_dist(angle):
    r_orbit = 6921e3
    r_earth = 6371e3
    if angle > 90:
        angle = 180 - angle
    angle = (np.pi*angle)/180 # Convert to radians

    dist_nominator = -r_earth*np.tan(angle) + np.sqrt(r_orbit**2*np.tan(angle)**2 + r_orbit**2 - r_earth**2)
    dist_denom = (np.tan(angle)**2 + 1)*np.cos(angle)

    return dist_nominator / dist_denom

def load_thr_from_json():
    with open('MODCOD.json', 'r') as f:
        json_data = json.load(f)
    return [json_data[key]['THR'] for key in sorted(json_data.keys(), key=int)]

def plot(stepsize):
    y = []
    passLen = 5555583.25 # m
    satVelocity = 7.38e3 # m/s
    passTime = passLen / satVelocity 
    alpha = 180/passTime 
   
    x = range(int(passTime))
    for i in x:
        y.append(fspl(calc_dist(i*alpha)))
    x = np.array(x)
    y = np.array(y)
    y = y - y.max()
    
    # Redefine y-axis to channel SNR
    transmitPower = 16 # Transmit power offset (0 dB = 1W) 
    recvPower = -108.16 - transmitPower # dB
    bandwidth = 25e3 # Hz
    noisePower = 10*np.log10(10**(-187/10)*bandwidth) # dB
    y = y + recvPower - noisePower

    # Load THR values from JSON
    threshold = load_thr_from_json()

    # Create a stepwise vector from threshold values
    stepArr = []
    iter = 0
    margin = 2 # 3 dB to avoid exceeding
    for i in range(len(y)):
        if iter + 1 < len(threshold) and threshold[iter + 1] <= y[i] - margin:
            iter += 1
            stepArr.append(threshold[iter])
        elif iter < len(threshold) and threshold[iter] <= y[i] - margin:
            stepArr.append(threshold[iter])
        else:
            stepArr.append(None)  # Append None if the threshold is unusable
   
    # SNR optimum plot with stepwise
    plt.plot(x, y, label='Channel SNR')
    plt.step(x, stepArr, where='mid', label='MODCOD quantization')
    plt.xlabel('Time [sec]')
    plt.ylabel('SNR [dB]')
    plt.legend()
    plt.grid()
    plt.xticks(np.arange(0, x.max()+1, 60))
    plt.tight_layout()
    plt.xlim(0, max(x)/2)
    plt.show()
    return

        
#create MODCOD.json with data and store coloumns in json
def modcodJSON():
    file_path = 'thrTab.csv'
    # Load the CSV file, assuming it has headers and you are skipping the first row from your description
    data = pd.read_csv(file_path, skiprows=1, header=None, names=['MODCOD', 'RS', 'CONV', 'GP', 'TP', 'SPECT', 'THR'])
    
    # Sort data by 'THR' and 'GP', both ascending
    data = data.sort_values(by=['THR', 'GP'], ascending=[True, True])
    
    # Initialize variables to keep track of the best GP and corresponding threshold
    best_gp = -1
    best_thr = -1
    result_indices = []

    # Iterate over the DataFrame
    for index, row in data.iterrows():
        current_gp = row['GP']
        current_thr = row['THR']
        current_spec = row['SPECT']
        current_thr = current_thr + 10*np.log10(current_spec)

        # Check if the current threshold is higher than the last best threshold with a higher GP
        if current_thr > best_thr and current_gp > best_gp:
            best_gp = current_gp
            best_thr = current_thr
            result_indices.append(index)

    # Create a new DataFrame from the filtered indices
    filtered_data = data.loc[result_indices].reset_index(drop=True)
        # Initialize a dictionary to hold the JSON structure
       # Initialize a dictionary to hold the JSON structure
    json_data = {}

    # Regex patterns for extracting numbers from RS and CONV
    rs_pattern = re.compile(r'\[(\d{3})(\d{3})\]')
    conv_pattern = re.compile(r'(\d+)/(\d+)')

    # Iterate over DataFrame rows to populate the dictionary
    for index, row in filtered_data.iterrows():
        # Parsing MODCOD to extract the MOD type and other potential data
        mod = row['MODCOD'].split()[0]  # Extracts the first part, e.g., 'GMSK', 'gMSK'
        mod2 = row['MODCOD'].split()[1]  # Extracts the second part, e.g., '1/2', '3/4'
        if mod2 == 'Uncoded':
            rs_k, rs_n = "Uncoded", "Uncoded"
            conv_k, conv_n = "Uncoded", "Uncoded"
        else:
            # Extract RS using regex
            rs_match = rs_pattern.search(row['RS'])
            if rs_match:
                rs_k, rs_n = map(int, rs_match.groups())
            else:
                rs_n, rs_k = None, None  # Default or handle error

            # Extract CONV using regex
            conv_match = conv_pattern.search(row['CONV'])
            if conv_match:
                conv_k, conv_n = map(int, conv_match.groups())
            else:
                conv_n, conv_k = None, None  # Default or handle error
        threshold = row['THR']+10*np.log10(row['SPECT'])
        # Construct JSON data structure
        json_data[str(index + 1)] = {
            "reed": {
                "n": rs_k,
                "k": rs_n
            },
            "conv": {
                "n": conv_n,
                "k": conv_k
            },
            "SPECT": row['SPECT'],
            "MOD": mod,
            "THR": threshold

        }
        GP = row['GP']
        
        print(f"{index+1} & {mod}[{rs_k} {rs_n}] {conv_k}/{conv_n} & {GP:.0f} & {threshold:.2f} \\\ \hline")

    # Convert dictionary to JSON string and print
    json_output = json.dumps(json_data, indent=4)
    # Optionally, save to a JSON file
    with open('MODCOD.json', 'w') as json_file:
        json_file.write(json_output)


    
   
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the fspl, for a given angle of the AAU GND station.\n No arugments give a plot over the whole pass.")
    parser.add_argument("-a", metavar="angle", help="Get fspl for given angle of the GND statoin", type=float)
    parser.add_argument("-r", metavar="resolution", help="Step step size for plot", type=float, default=1)

    args = parser.parse_args()
    if args.a != None:
        print(fspl(calc_dist(args.a)))
    else:
        plot(args.r)
    modcodJSON()

