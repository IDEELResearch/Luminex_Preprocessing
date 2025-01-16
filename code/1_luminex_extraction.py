import os
import pandas as pd
from io import StringIO
from config import BASE_FOLDER  # Import BASE_FOLDER from config.py

# Enhanced function to extract any dataframe (like bead count) based on data type
def extract_dataframe_by_type(raw_lines, data_type):
    """
    Extracts a specific dataframe (like bead count) based on its data type from the raw file.
    """
    start_idx = None
    for i, line in enumerate(raw_lines):
        # Check for both formats of "DataType"
        if f'DataType:,{data_type}' in line or f'"DataType:","{data_type}"' in line:
            start_idx = i + 1  # Start after the identified data type line
            break
    if start_idx is None:
        print(f"Data type '{data_type}' not found in the file.")
        return None  # Return None if no matching data type was found

    # Extracting rows until a blank line or the start of the next data type
    dataframe_lines = []
    for line in raw_lines[start_idx:]:
        if line.strip() == "" or line.startswith("DataType:"):
            break
        dataframe_lines.append(line)

    if not dataframe_lines:  # Check if data is found
        print(f"No data found under '{data_type}' section.")
        return None

    # Convert the extracted lines into a dataframe
    data_str = "".join(dataframe_lines)
    try:
        data_df = pd.read_csv(StringIO(data_str))
    except Exception as e:
        print(f"Failed to parse data under '{data_type}': {e}")
        return None

    return data_df

# Function to save extracted dataframe into a specific folder based on its type
def save_extracted_dataframe(data_df, filename, output_folder, data_type):
    """
    Saves the extracted dataframe to a CSV file in the designated output folder.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate output filename
    output_filename = f"{os.path.splitext(filename)[0]}_{data_type.lower()}.csv"
    output_path = os.path.join(output_folder, output_filename)

    # Save the dataframe to CSV
    data_df.to_csv(output_path, index=False)
    print(f"{data_type} data saved to {output_path}")

# Main function to extract and save bead count and median MFI dataframes separately
def extract_and_save_dataframes(base_folder):
    """
    Extracts bead count and median MFI dataframes from raw files and saves them separately.
    """
    folder_path = os.path.join(base_folder, 'data/raw')
    output_folder_bead_count = os.path.join(base_folder, 'data/extraction/bead_count')
    output_folder_median_mfi = os.path.join(base_folder, 'data/extraction/median_mfi')

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.csv'):  # Process only CSV files
            with open(file_path, 'r') as f:
                raw_lines = f.readlines()

            # Extract and save the bead count dataframe
            bead_count_df = extract_dataframe_by_type(raw_lines, "Count")
            if bead_count_df is not None:
                save_extracted_dataframe(bead_count_df, filename, output_folder_bead_count, "bead_count")

            # Extract and save the Median MFI dataframe
            median_mfi_df = extract_dataframe_by_type(raw_lines, "Median")
            if median_mfi_df is not None:
                save_extracted_dataframe(median_mfi_df, filename, output_folder_median_mfi, "median_mfi")

# Run the extraction process
if __name__ == "__main__":
    extract_and_save_dataframes(BASE_FOLDER)
