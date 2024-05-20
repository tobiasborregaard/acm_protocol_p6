import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# Load the CSV file into a DataFrame
file_path = 'output.csv'
data = pd.read_csv(file_path, skiprows=1, header=None, names=['SNR', 'Modulation', 'Range', 'CodingRate', 'BER'])

# Convert BER column to numeric for plotting
data['BER'] = pd.to_numeric(data['BER'], errors='coerce')

modulations = ['2FSK', '4FSK', 'MSK']  # Define the modulation types

# Create a unique list of (Range, CodingRate) combinations and create a color map
unique_combinations = data[['Range', 'CodingRate']].drop_duplicates()
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_combinations)))
color_map = {tuple(row): color for row, color in zip(unique_combinations.to_records(index=False), colors)}

# Define font size multiplier
font_scale = 1.1

for mod in modulations:
    fig, ax = plt.subplots(figsize=(12, 6))  # Create a new figure for each modulation type
    mod_data = data[data['Modulation'] == mod]

    # Determine the maximum SNR for '1' groups
    max_snr_for_one = mod_data[mod_data['CodingRate'] == '1']['SNR'].max()
    
    # Determine the appropriate upper limit for x-axis
    upper_snr_limit = mod_data['SNR'].max() + 5  # you can adjust this margin

    # Filtering groups and plotting
    for (modulation, range_val, coding_rate), group in mod_data.groupby(['Modulation', 'Range', 'CodingRate']):
        group.sort_values('SNR', inplace=True)  # Ensure data is sorted
        if group['SNR'].max() > max_snr_for_one and coding_rate != '1':
            continue  # Skip this group
        
        color = color_map[(range_val, coding_rate)]
        # Apply different styles based on the coding rate
        if coding_rate == "1":
            marker_style = ' '  # No marker
            line_style = '--'  # Dashed line
            color = 'red'  # Special color for specific coding rate
        else:
            marker_style = 'o'  # Circle marker
            line_style = '-'   # Solid line

        ax.plot(group['SNR'], group['BER'], marker=marker_style, linestyle=line_style, color=color,
                label=f"{coding_rate.strip()}, {range_val.strip()}")

    ax.set_xlabel('EB/N0 (dB)', fontsize=12 * font_scale)
    ax.set_ylabel('BER', fontsize=12 * font_scale)
    ax.set_yscale('log')
    ax.set_title(f'BER vs EB/N0 for {mod}', fontsize=14 * font_scale)
    ax.grid(True)
    
    # Set the x-axis limits
    ax.set_xlim([-5, upper_snr_limit])

    # Position legend to avoid overlapping the data
    legend = ax.legend(title="Coding Rate", fontsize=10 * font_scale, loc='upper right', bbox_to_anchor=(1, 0.7))

    # Save the figure
    pdf_filename = f'{mod}_BER_vs_SNR.pdf'
    fig.savefig(pdf_filename, bbox_inches='tight')

    plt.show()
