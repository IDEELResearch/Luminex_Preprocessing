# RTSS_Kisumu_Schisto

This repository is for the RTS,S AS,01 MVIE subproject evaluating S. mansoni exposure on the function vaccine reponse in the Kisumu cohort. This project is a collaboration between U Mass, UNC, MIT, Harvard, and Brown University.

Sahal Thahir [sahal\@ad.unc.edu](mailto:sahal@ad.unc.edu) (703)344-6153

## Directory Set up

This repository is set up to allow for the extraction of Median MFI data from raw Luminex Xponent .csv files. It is set-up so that if this full repository is downloaded, the system can be used for any luminex study for plate-level quality control, median MFI aggregation, and MFI standardization across multiple plates.

### Repository Folders

#### code

This can be used for study specific R coding. Currently it holds some early code I'll be integrating into the markdown documents

#### data

This is where *data files* (raw and clean) are to be stored. There are three folders are required within this folder for the code to work well. 

  - **data/raw:** This is where raw files should go. data/raw/luminex was placed so other raw files (ex: qPCR) could also be placed in separate folders. *data/raw/luminex* is where the Rmarkdown code will extract csv files. These files will not be changed when running the code 
  
  - **data/clean:** median MFI extracted from each raw file will be within the *data/clean/luminex*. The compiled dataframe is within the main folder after the code is run. 
  
  - **data/qc**: Quality control outputs from [Luminex Xponent_Plate level QC.Rmd]()

#### results

This is for general storage of plots, analysis, for results presentation.

## R Markdown code explanation

### [LuminexCompilation.Rmd]()

**Setup Chunk:** This chunk initializes the R Markdown document and sets options for rendering it as a PDF. It ensures that the document is properly formatted and includes necessary metadata like title, author, and date.

**HTML Comments:** These comments serve as developer notes and include useful links for reference during development. They provide additional context and resources for anyone working on or reviewing the code.

**Library Loads:** This chunk loads required R libraries, namely tidyverse and here, which are essential for data manipulation and file management tasks throughout the document.

1.  **Raw File Extraction:** This section begins by iterating through each raw CSV file in a specified directory. For each file, it reads the contents and performs data extraction, trimming rows to include only relevant information between "Median" and "Net MFI" rows. It then trims columns to include only data between "Location" and "Total.Events" columns. BSA subtraction is performed on numerical columns, with the BSA value subtracted from each value while maintaining the BSA values on the plate. Negative median fluorescence intensity (MFI) values after correction are set to zero to ensure data integrity. Additionally, serology type is extracted from the file name, and it is appended to the numerical column names. A new column named Plate_Serology is created to store the plate identifier and serology type.Finally, the processed data is exported to a clean data directory as a CSV file in *data/clean/luminex*

2.  *Compiling All Plates:* This section combines data from all plates into a single data frame for further analysis.Each CSV file is read and converted into a data frame, and all data frames are combined row-wise. Numeric columns are processed to remove commas and convert them to numeric data types, while NA values are replaced with blanks. Plate-related columns are grouped together, and non-plate columns are moved to the beginning of the data frame. A summary function is applied to serology columns to handle multiple values, taking the mean if necessary. Two new columns are created:

    -   RID: Extracted from the sample IDs to represent the Researcher Identifier.
    -   Timepoint: Extracted from the sample IDs to represent the timepoint of the sample. The compiled data frame, containing information from all plates, is exported to a CSV file for further analysis.

### [Luminex Xponent_Plate level QC.Rmd]()

These code chunks collectively conduct plate-level quality control analysis for Luminex studies, encompassing bead count analysis, background median MFI analysis, and standard curve analysis. Each chunk performs specific tasks, contributing to the overall aim of the document to ensure data quality and reliability for downstream analysis.

**Setup Chunk:** Initializes the R Markdown document and sets options for rendering it as a PDF.

**HTML Comments:** Includes developer notes and useful links for reference during development.

**Library Loads:** Loads required R libraries, tidyverse and here, necessary for data manipulation and file management tasks.

  1. **Required Inputs:**
        Prompts users to specify the working directory, input file, minimum bead count, and output file path.

  2. **Quality Control - Bead count per Antigen:**
        Extracts bead count data from the input file and creates a heatmap visualization.

  3. **Bead Count: per well:**
        Identifies wells with low bead counts and generates a schematic representation of the plate layout.
        Exports a list of wells with low bead counts to a CSV file.

  4. **QC of median MFI data:**
        Extracts median MFI data from the input file and removes values with bead counts below the specified threshold.
        Performs BSA subtraction if necessary.

  5. **Background MFI:**
        Averages the median MFI values for background and non-background samples and visualizes the results with a bar graph.

  6. **Standard curve:**
        Extracts standard curve data from the input file and creates standard curves for each analyte.
        The code runs separately for each analyte and produces individual plots.
        
### [Luminex standardization across multiple plates.Rmd]()

These code chunks collectively aim to standardize MFI values across multiple plates in Luminex experiments.

**Library loads:** This chunk loads necessary R libraries, including tidyverse, here, and ggpubr.

1.  **Generation of standards dataframe**: This chunk extracts standards data from all plates, creates a standards dataframe, calculates dilution factors, categorizes MFI columns, creates an Antigen column, calculates log10(MFI), and selects specific columns. It also prints the unique Plates.

2.  **Standard curves for all antigens:** This chunk plots standard curves for each antigen, calculates correlation and R-squared values for each subclass, and displays the plots.

3.  **Define standard antigen:** This chunk defines the standard antigen of interest.

4.  **Standard Ag plots:** This chunk filters data for the standard antigen, filters out rows with zero dilution factor or NA MFI, calculates correlation and R-squared for each subset, and creates scatterplots with filtered data, facetted by subclass.

5.  **Line of best fit for each plate:** This chunk calculates Pearson correlation coefficient, line of best fit equation, and R-squared values for each plate, and plots with correlation text annotations. It also creates a dataframe to store plate statistics.

6.  **Average line of best fit for each Subclass:** This chunk creates average fit lines for each subclass based on the calculated plate statistics.

7.  **Determine scaling factor:** This chunk joins the average slope and intercept with the plate statistics, calculates the scaling factor using a selected dilution factor, and displays plate statistics with scaling factor.

8.  **Testing scaling on standard antigen:** This chunk tests the scaling factor on the log10 data of the standard antigen, plots corrected and uncorrected log10(MFI) vs. Dilution Factor, and displays the plots.

### [LuminexCompileExperiment_2024_03_07.Rmd]() this is Jeff's original code

**Setup Chunk:** Initializes the R Markdown document and sets options for rendering it as a PDF. It also prints the current working directory.

**HTML Comments:** Includes developer notes and useful links for reference during development.

**Dependencies:** Loads required R libraries (tidyverse and here) for data manipulation and file management tasks.

1.  **Required Inputs:** Specifies project parameters such as the project name, directory paths for raw data files, plate list, and sample list file.

2.  **Data Cleaning:** Provides optional sections for fixing inconsistencies in sample names and deleting specific samples from the dataset.

3.  **Load Sample List:** Reads the sample list file specified in the previous section and checks if it contains essential columns (PlateID and SampleID).

4.  **Output Directory:** Defines the output directory for compiled data files and removes any existing CSV and TSV files in the directory.

5.  **Processing Plate Data:** This is the main processing chunk.The script iterates through each plate specified in the platelist. For each plate, it retrieves a list of associated raw data files from the directory specified in rawdir. It then processes each raw file individually, extracting relevant data, adjusting columns, and cleaning up sample names. The processed data for each file is written to a temporary TSV file. After processing all files for a plate, the script combines the data across conditions/antibodies using a full join operation, creating a single dataset for that plate. This compiled plate dataset is printed and written to a TSV file in the output directory. Once processing is complete for all plates, the script combines the compiled plate datasets across all plates using bind_rows() to create a full compiled dataset encompassing data from all plates. This final compiled dataset is then written to a TSV file in the output directory, completing the compilation process for the Luminex xPONENT output data.

*this documented was made with the assistance of Large Language Models*
