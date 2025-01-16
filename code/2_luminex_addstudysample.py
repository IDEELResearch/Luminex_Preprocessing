import os
import pandas as pd
from config import BASE_FOLDER  # Import BASE_FOLDER from config.py

# Function to convert the "Key" sheet from Excel to CSV
def excel_to_csv(excel_file, csv_file, sheet_name='Key'):
    """Converts the specified Excel sheet to a CSV file."""
    print(f"Attempting to read '{sheet_name}' sheet from {excel_file}")
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df.to_csv(csv_file, index=False)
        print(f"Saved CSV to {csv_file}")
    except Exception as e:
        print(f"Error reading '{sheet_name}' sheet from {excel_file}: {e}")

# Function to refine the parsing of the 'Location' column to extract the 'Well' value
def parse_location_to_well(data_df, location_column='Location'):
    """
    Refines the parsing of the 'Location' column to extract the 'Well' value.
    """
    if location_column in data_df.columns:
        data_df['Well'] = data_df[location_column].str.extract(r'[,\(]([A-H]\d{1,2})\)')
    else:
        print(f"Column '{location_column}' not found in the dataset.")
    return data_df

# Function to add Study_sample, Subclass, and Well columns based on the Key file
def add_study_sample(key_file, data_file, output_file):
    """Adds the Study_sample, Subclass, and Well columns to a data file based on matching the Well."""
    key_df = pd.read_csv(key_file)
    data_df = pd.read_csv(data_file)

    # Refine Well extraction from the 'Location' column
    data_df = parse_location_to_well(data_df)

    # Merge Study_sample and Subclass based on matching Well
    merged_df = pd.merge(data_df, key_df[['Well', 'Study_sample', 'Subclass']], how='left', on='Well')

    # Reorder columns to make Well, Study_sample, and Subclass the first three columns
    cols = merged_df.columns.tolist()
    well_col = cols.pop(-3)  # Remove Well column from end
    study_sample_col = cols.pop(-2)  # Remove Study_sample column from end
    subclass_col = cols.pop(-1)  # Remove Subclass column from end
    cols.insert(0, well_col)  # Insert Well as the first column
    cols.insert(1, study_sample_col)  # Insert Study_sample as the second column
    cols.insert(2, subclass_col)  # Insert Subclass as the third column
    merged_df = merged_df[cols]

    # Save the updated dataframe to a new CSV
    merged_df.to_csv(output_file, index=False)
    print(f"Saved updated file with Study_sample, Subclass, and Well columns to {output_file}")

if __name__ == "__main__":
    # Define all necessary folders relative to the BASE_FOLDER
    input_folder = os.path.join(BASE_FOLDER, 'data/plate_layout/input_layouts')
    key_folder = os.path.join(BASE_FOLDER, 'data/plate_layout/keys')
    bead_count_folder = os.path.join(BASE_FOLDER, 'data/extraction/bead_count')
    median_mfi_folder = os.path.join(BASE_FOLDER, 'data/extraction/median_mfi')

    # Step 1: Extract Key sheets from Excel files in input_layouts and save as CSVs in keys
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
        print(f"Created output folder for keys: {key_folder}")
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx') and not filename.startswith('~$'):  # Skip temp files
            excel_file = os.path.join(input_folder, filename)
            clean_name = filename.replace("_layout.xlsx", "")  # Remove only "_layout.xlsx"
            csv_file = os.path.join(key_folder, f"{clean_name}_key.csv")
            
            # Convert the "Key" sheet to CSV
            try:
                excel_to_csv(excel_file, csv_file, sheet_name="Key")
            except Exception as e:
                print(f"Error processing {excel_file}: {e}")

    # Step 2: Process each file in bead_count and median_mfi folders to add Study_sample, Subclass, and Well
    for folder, suffix in [(bead_count_folder, '_bead_count'), (median_mfi_folder, '_median_mfi')]:
        for filename in os.listdir(folder):
            if filename.endswith('.csv'):
                clean_name = filename.replace(f"{suffix}.csv", '')  # Correctly remove suffix
                key_file = os.path.join(key_folder, f"{clean_name}_key.csv")
                data_file = os.path.join(folder, filename)
                output_file = os.path.join(folder, f"{clean_name}{suffix}.csv")
                
                # Add Study_sample, Subclass, and Well columns if the corresponding Key file exists
                if os.path.exists(key_file):
                    try:
                        add_study_sample(key_file, data_file, output_file)
                    except Exception as e:
                        print(f"Error processing {data_file} with {key_file}: {e}")
                else:
                    print(f"Key file not found for {filename}: {key_file}")



