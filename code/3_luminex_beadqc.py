import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from config import BASE_FOLDER  # Import BASE_FOLDER from config.py

# Function to create heatmaps and flag well-antigen combinations based on bead count thresholds
def generate_bead_count_heatmap(bead_count_df, filename, output_folder, warning_threshold=50, fail_threshold=40):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate clean filename by removing "_bead_count.csv" to use as Plate name
    clean_filename = filename.replace("_bead_count.csv", "")

    # Dynamically identify analyte columns (between 'Sample' and 'Total Events')
    sample_index = bead_count_df.columns.get_loc("Sample")
    total_events_index = bead_count_df.columns.get_loc("Total Events")
    analyte_columns = bead_count_df.columns[sample_index + 1 : total_events_index]

    # Convert bead count data to numeric for analyte columns only
    bead_count_df[analyte_columns] = bead_count_df[analyte_columns].apply(pd.to_numeric, errors='coerce')

    # Use 'Study_sample' as row labels if available, otherwise fall back to 'Sample'
    row_labels = bead_count_df['Study_sample'] if 'Study_sample' in bead_count_df.columns else bead_count_df['Sample']

    # Flag wells that meet warning or fail criteria
    flagged_wells = []
    for index, row in bead_count_df.iterrows():
        for analyte in analyte_columns:
            bead_count = row[analyte]
            if pd.notna(bead_count):  # Only consider non-NaN values
                if bead_count < fail_threshold:
                    flagged_wells.append([clean_filename, row['Sample'], row.get('Study_sample', 'N/A'), analyte, bead_count, 'Failed'])
                elif bead_count < warning_threshold:
                    flagged_wells.append([clean_filename, row['Sample'], row.get('Study_sample', 'N/A'), analyte, bead_count, 'Warning'])

    # Define custom colormap and boundaries for fail, warning, and pass
    cmap = mcolors.ListedColormap(['lightcoral', 'lightyellow', 'mediumaquamarine'])
    bounds = [0, fail_threshold, warning_threshold, 200]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.figure(figsize=(10, 20))
    sns.heatmap(bead_count_df[analyte_columns], cmap=cmap, norm=norm,  # Custom colormap and boundaries
                cbar_kws={'label': 'Bead Count'}, linewidths=.5,
                linecolor='black', vmin=0, vmax=200, yticklabels=row_labels)
    plt.title(f"Bead Count Heatmap for {clean_filename}")

    # Save heatmap with clean_filename (without "_bead_count.csv")
    heatmap_path = os.path.join(output_folder, f'{clean_filename}_heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Heatmap saved to {heatmap_path}")

    return flagged_wells

# Function to process all bead count files, generate heatmaps, and save flagged wells
def process_bead_counts_with_qc(base_folder, warning_threshold=50, fail_threshold=40):
    input_folder = os.path.join(base_folder, 'data/extraction/bead_count')
    output_folder_heatmaps = os.path.join(base_folder, 'data/qc/bead_count_heatmaps')
    flagged_output_csv = os.path.join(base_folder, 'data/qc/flagged_wells.csv')

    # Collect all flagged wells across files
    all_flagged_wells = []

    # Loop through all files in the bead count extraction folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.endswith('.csv'):  # Process only CSV files
            # Read bead count data
            bead_count_df = pd.read_csv(file_path)

            # Generate heatmap and gather flagged wells for the current file
            flagged_wells = generate_bead_count_heatmap(
                bead_count_df, filename, output_folder_heatmaps,
                warning_threshold=warning_threshold, fail_threshold=fail_threshold
            )

            # Append flagged wells to the overall list
            all_flagged_wells.extend(flagged_wells)

    # Create a DataFrame for all flagged wells and save as CSV
    flagged_df = pd.DataFrame(all_flagged_wells, columns=['Plate', 'Sample', 'Study_sample', 'Antigen', 'Bead Count', 'Flag'])
    flagged_df.to_csv(flagged_output_csv, index=False)
    print(f"Flagged wells saved to {flagged_output_csv}")

# Define threshold parameters
warning_threshold = 50  # Bead count under this value is a warning
fail_threshold = 40     # Bead count under this value is a fail

# Run the bead count QC process
process_bead_counts_with_qc(BASE_FOLDER, warning_threshold, fail_threshold)

