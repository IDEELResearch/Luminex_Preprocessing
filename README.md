## Author
Sahal Thahir, MD  
sahal@med.unc.edu


# Luminex Data Extraction and Quality Control Pipeline

This project processes Luminex Xponent data for quality control, extraction, and visualization. It is designed for flexibility, requiring minimal user input to update configuration files for each dataset.

---

## Folder Architecture

```
Luminex/
├── code/                         # Scripts for processing data
│   ├── 1_luminex_extraction.py   # Extracts raw data from CSV files
│   ├── 2_luminex_addstudysample.py # Adds study/sample metadata
│   ├── 3_luminex_beadqc.py       # Performs bead count QC
│   ├── 4_luminex_processed_mfi(clean).py # Processes cleaned MFI data
│   └── config.py                 # Configuration file for user input
├── data/                         # Data storage
│   ├── raw/                      # Raw input files
│   ├── processed/                # Processed data (code-generated)
│   └── plate_layout/             # Plate layout templates
│       ├── input_layouts/        # User-provided plate layout files
│       ├── keys/        # Study_sample and Subclass Key (code- generated)
│       └── Luminex_p96layout_template.xlsx # 96-well template (input required on two sheets)
│       └── Luminex_p384layout_template.xlsx # 384-well template (input required on two sheets)
├── results/                      # Results and visualizations (optional)
├── .git/                         # Version control (if applicable)
├── README.md                     # This file
```

---

## User Instructions

### 1. Setup

1. Install required dependencies:
    - Python 3.x
    - Required Python libraries (`pandas`, `numpy`, `matplotlib`, etc.)
    - Install using `pip install -r requirements.txt` if provided.

2. Ensure raw Luminex data and plate layouts are correctly placed:
    - Raw data files: Place in `data/raw/`.
    - Plate layout files: Place in `data/plate_layout/input_layouts/`.

### 2. Edit the Configuration File

Update the `code/config.py` file to reflect your data setup:
- Specify the pathname for input and output directories.

### 3. Run the Pipeline

Run the scripts in order:
1. Extract raw data: 
   ```bash
   python code/1_luminex_extraction.py
   ```
2. Add study/sample metadata:
   ```bash
   python code/2_luminex_addstudysample.py
   ```
3. Perform bead count QC:
   ```bash
   python code/3_luminex_beadqc.py
   ```
4. Process cleaned MFI data:
   ```bash
   python code/4_luminex_processed_mfi(clean).py
   ```

### 4. View Results

- Bead count and median mfi dataframes (raw): Store in `data/extraction`
- Processed data: Stored in `data/processed/`.
- Quality control outputs: Stored in `data/qc`.
   - Heatmaps: .png files
   - flagged wells (batch): `flagged_wells.csv`
- Logs for debugging: Found in `logs/`.

---

## Data Display

- **QC Heatmaps**: Visualizes well-analyte combinations with low bead counts. Saved in `results/`.
- **Cleaned MFI Files**: Available in `data/processed/`. Includes BSA subtraction (BSA median MFI maitained)

---

## Troubleshooting

1. **Error Messages**: Check `logs/` for detailed error logs.
2. **Missing Data**: Ensure raw data and plate layouts are correctly placed in `data/raw/` and `data/plate_layout/input_layouts/`.

---


This pipeline was designed to streamline Luminex data processing and enhance reproducibility.
