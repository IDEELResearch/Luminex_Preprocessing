import os
import pandas as pd
from datetime import datetime
from config import BASE_FOLDER  # Import BASE_FOLDER from config.py

# Function to clean and process median MFI files
def process_median_mfi_files(base_folder):
    input_folder = os.path.join(base_folder, 'data/extraction/median_mfi')
    output_folder = os.path.join(base_folder, 'data/clean')

    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")

    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(input_folder):
        print(f"Error: Input folder does not exist: {input_folder}")
        return

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            plate_name = filename.replace("_median_mfi.csv", "")

            # Load the median MFI file
            data = pd.read_csv(file_path)

            # Extract antigen columns (between "Sample" and "Total Events")
            start_idx = data.columns.get_loc("Sample")
            end_idx = data.columns.get_loc("Total Events")
            antigen_columns = data.columns[start_idx + 1 : end_idx]

            # Subtract BSA value from all other analyte columns
            bsa_values = data["BSA"]
            for col in antigen_columns:
                if col != "BSA":
                    data[col] = data[col] - bsa_values
                    data[col] = data[col].clip(lower=0)  # Replace negative values with zero

            # Add Plate column
            data["Plate"] = plate_name

            # Keep required columns, including Study_sample and Subclass if present
            metadata_columns = ["Plate", "Sample"]
            if "Study_sample" in data.columns:
                metadata_columns.append("Study_sample")
            if "Subclass" in data.columns:
                metadata_columns.append("Subclass")

            final_columns = metadata_columns + antigen_columns.tolist()
            data = data[final_columns]

            # Save processed file
            processed_filename = f"{plate_name}_processed.csv"
            processed_path = os.path.join(output_folder, processed_filename)
            data.to_csv(processed_path, index=False)
            print(f"Processed file saved to {processed_path}")

# Function to merge all processed files into a single CSV
def merge_cleaned_files(base_folder):
    clean_folder = os.path.join(base_folder, 'data/clean')
    output_folder = os.path.join(base_folder, 'data')
    
    os.makedirs(output_folder, exist_ok=True)
    
    all_data = []
    
    for filename in os.listdir(clean_folder):
        if filename.endswith('_processed.csv'):
            file_path = os.path.join(clean_folder, filename)
            df = pd.read_csv(file_path)

            # Exclude rows where all columns except 'Plate' are empty
            df = df.dropna(how='all', subset=df.columns.difference(['Plate']))

            all_data.append(df)
    
    if all_data:
        merged_data = pd.concat(all_data, ignore_index=True)
    
        # Dynamically generate merged filename based on BASE_FOLDER name
        folder_name = os.path.basename(base_folder.rstrip("/"))
        today_date = datetime.now().strftime('%Y-%m-%d')
        merged_filename = f"{folder_name}_merged_{today_date}.csv"
        merged_path = os.path.join(output_folder, merged_filename)
        
        # Save merged data
        merged_data.to_csv(merged_path, index=False)
        print(f"Merged file saved to {merged_path}")
    else:
        print("No valid data found to merge!")

# Run processing and merging functions
process_median_mfi_files(BASE_FOLDER)
merge_cleaned_files(BASE_FOLDER)
