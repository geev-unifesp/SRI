# SRI
Sleep Regularity Index calculation (actimetry)
markdown
# Sleep Data Processor

This script processes raw `.txt` files containing physiological or behavioral state data (e.g., sleep/wake states), extracts datetime information, filters full-day records (00:00–23:59), adds a binary `Sleep` column, and exports cleaned data as `.csv` files.

## Features

- Automatically detects header row containing `DATE/TIME`
- Handles files with `;` delimiter and `latin1` encoding
- Splits `DATE/TIME` into separate `DATE` and `TIME` columns
- Extracts hour and minute to identify full-day records (00:00 to 23:59)
- Creates a `Sleep` column based on the `STATE` column:
  - `0` or `4` → `0` (awake or other)
  - `1` or `2` → `1` (sleep)
- Saves processed data as semicolon-separated `.csv` files in a dedicated output folder

## Requirements

Install the required Python package:

```bash
pip install pandas
Folder Structure
text
.
├── process_sleep_data.py   # Main script
└── README.md
Input Format
The script expects .txt files with:

A header row starting with DATE/TIME

Columns separated by ;

A STATE column containing integer codes (0, 1, 2, 4)

Encoding: latin1

Example:

text
DATE/TIME;STATE;OTHER
2023-01-01 00:00;0;...
2023-01-01 00:01;1;...
Output
Processed files are saved in:

text
/Users/luisalopes/desktop/LuluCsvFiles/
Each output file is named: [original_name]_processed.csv

Output columns order:

text
DATE, TIME, Sleep, [remaining original columns]
Usage
Update the folder_path variable inside the script to point to your folder containing .txt files.

Run the script:

bash
python process_sleep_data.py
Customization
To change the output folder location, modify the output_folder variable.

To alter sleep classification rules, edit the lambda function in:

python
df['Sleep'] = df['STATE'].apply(lambda x: 0 if x in [0, 4] else 1 if x in [1, 2] else None)
Error Handling
The script will:

Skip files without a DATE/TIME header

Skip files missing 00:00 or 23:59 timestamps (and process the full file instead)

Print an error message for any file that fails to process

Limitations
Assumes data are recorded in chronological order

Only the first 00:00 and last 23:59 are used for filtering

Does not handle time zones or daylight saving transitions

Author
Developed for processing actigraphy/sleep diary exports from systems using STATE codes.

License
Feel free to use and modify as needed.

text

## Agora faça exatamente isso:

1. **Clique no ícone de copiar** no canto superior direito deste bloco
2. Abra seu arquivo `README.md` no GitHub
3. **Selecione tudo** que está lá (Ctrl+A ou Cmd+A)
4. **Delete** ou **Cole por cima** (Ctrl+V ou Cmd+V)
5. **Salve** o arquivo

Pronto! Seu README vai ficar completo e correto. 🎯
create_csv_files_atualizado.py
PY 4.1KB
sri_from_csv.py
PY 3.03KB
Eu tenho esses dois codigos e tambem quero criar o readme
Aqui está o README completo para os dois scripts (o processador de dados e o calculador de SRI), em um único bloco para você copiar:

markdown
# Sleep Data Processing & SRI Analysis

This repository contains two Python scripts for processing actigraphy/sleep diary data and calculating the **Sleep Regularity Index (SRI)** — a measure of sleep-wake consistency across days.

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `create_csv_files_atualizado.py` | Processes raw `.txt` files, cleans sleep/wake data, and exports structured `.csv` files |
| `sri_from_csv.py` | Calculates the Sleep Regularity Index from processed sleep data |

---

## Script 1: `create_csv_files_atualizado.py`

### Features

- Automatically detects header row containing `DATE`
- Intelligently detects delimiter (`;` or `\t`)
- Handles both `DATE/TIME` combined column or separate `DATE` and `TIME` columns
- Extracts hour/minute to identify full-day records (00:00 to 23:59)
- Creates a `Sleep` column based on the `STATE` column:
  - `0` or `4` → `0` (awake or other)
  - `1` or `2` → `1` (sleep)
- Saves processed data as semicolon-separated `.csv` files

### Requirements

```bash
pip install pandas
Input Format
The script expects .txt files with:

A header row containing DATE (or DATE/TIME)

A STATE column with integer codes (0, 1, 2, 4)

Delimiter: ; or \t

Encoding: latin1

Example:

text
DATE;TIME;STATE;OTHER
2023-01-01;00:00;0;...
2023-01-01;00:01;1;...
Output
Processed files are saved to:

text
/Users/juliavallim/Desktop/
Each output file is named: [original_name]_processed.csv

Output columns order:

text
DATE, TIME, Sleep, [remaining original columns]
Customization
To change the output folder, modify the output_folder variable

To alter sleep classification rules, edit the lambda function:

python
df['Sleep'] = df['STATE'].apply(lambda x: 0 if x in [0, 4] else 1 if x in [1, 2] else None)
Usage
python
# Update the folder path inside the script
process_files_in_folder("/path/to/your/txt/files")
Then run:

bash
python create_csv_files_atualizado.py
Script 2: sri_from_csv.py
Features
Calculates the Sleep Regularity Index (SRI) from sleep/wake time series

SRI ranges from -100 (completely irregular) to +100 (perfectly regular)

Handles missing values gracefully

Supports custom epochs per day (default: 1440, i.e., 1-minute epochs)

Requirements
bash
pip install numpy pandas
Usage (Command Line)
bash
python sri_from_csv.py [-h] [-e EPOCHS] [-c COLUMN] filename.csv
Arguments
Argument	Description
fn	CSV file containing sleep data (positional argument)
-e, --epochs	Number of epochs per day (default: 1440)
-c, --column	Column name containing sleep values (default: sleep)
Example
bash
# Using default 1440 epochs per day and 'sleep' column
python sri_from_csv.py data_processed.csv

# Custom epochs (e.g., 2880 for 30-second epochs) and custom column name
python sri_from_csv.py -e 2880 -c Sleep data_processed.csv
Output Example
text
Calculating SRI values from the sleep column of data_processed.csv based on 1440 epochs per day
Found 10080 epochs and 7 complete days. Discarding 0 trailing epochs
Found 0 missing sleep values, which will be ignored during SRI calculation

The calculated SRI is 72.3456
How SRI Works
The SRI measures the probability that sleep/wake state at any time of day matches the state exactly 24 hours later. The formula used is:

text
SRI = 200 × mean(match24) - 100
Where match24 is the proportion of matching states between consecutive days (ignoring missing values).

Complete Workflow Example
Process raw .txt files:

python
# In create_csv_files_atualizado.py, update the folder path
process_files_in_folder("/path/to/raw/txt/files")
Run the processor:

bash
python create_csv_files_atualizado.py
Calculate SRI for a processed file:

bash
python sri_from_csv.py -c Sleep /Users/juliavallim/Desktop/participant_processed.csv
Error Handling
Script 1 (create_csv_files_atualizado.py)
Skips files without a DATE or DATE/TIME header

Skips files missing 00:00 or 23:59 timestamps (processes entire file instead)

Automatically detects delimiter (; or \t)

Prints error messages for any file that fails to process

Script 2 (sri_from_csv.py)
Handles missing values (NaNs) by ignoring them during calculation

Discards incomplete trailing epochs

Warns if file contains only one column (which may prevent missing value detection)

Limitations
Script 1
Assumes data are recorded in chronological order

Only the first 00:00 and last 23:59 are used for filtering

Does not handle time zones or daylight saving transitions

Output folder is hardcoded (modify manually)

Script 2
Assumes data are regularly sampled (constant epoch length)

Discards incomplete final days

Requires at least 2 days of data for meaningful SRI calculation

Author
Script 1: Luisa da Costa Lopes

Script 2: Matthew Engelhard (Copyright 2018, MIT License)

License
create_csv_files_atualizado.py: Free to use and modify

sri_from_csv.py: MIT License (see copyright notice in script)
