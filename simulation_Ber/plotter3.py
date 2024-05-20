import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'output.csv'
# file_path = 'TheUltrimateCSV.csv'
data = pd.read_csv(file_path, skiprows=1, header=None, names=['SNR', 'Modulation', 'Range', 'CodingRate', 'BER'])

# Convert BER column to numeric for plotting
data['BER'] = pd.to_numeric(data['BER'], errors='coerce')

# Create a figure with three subplots, one for each modulation type
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 18), sharex=True, constrained_layout=True)

# Plotting
modulations = ['2FSK', '4FSK', 'MSK']  # Define the modulation types
for ax, mod in zip(axs, modulations):
    for (modulation, range_val, coding_rate), group in data[data['Modulation'] == mod].groupby(['Modulation', 'Range', 'CodingRate']):
        group.sort_values('SNR', inplace=True)
        if coding_rate == "1":
            ax.plot(group['SNR'], group['BER'], marker=' ', linestyle='--', label=f"{coding_rate.strip()}, {range_val.strip()}")
        else:
            ax.plot(group['SNR'], group['BER'], marker='o', linestyle='-', label=f"{coding_rate.strip()}, {range_val.strip()}")

    ax.set_xlabel('SNR (dB)')
    ax.set_ylabel('BER')
    ax.set_yscale('log')
    ax.set_title(f'BER vs SNR for {mod}')
    ax.legend()
    ax.grid(True)

# Show plot
plt.show()
