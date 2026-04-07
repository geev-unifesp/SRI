import os
import pandas as pd

def find_header_row(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        for i, line in enumerate(file):
            print(f"{line}")
            if line.startswith('DATE'):
                return i
    return -1

def smart_detect_delimiter(file_path, header_row=0):
    # Try tab
    try:
        df_tab = pd.read_csv(file_path, delimiter='\t', skiprows=header_row, encoding='latin1')
        if len(df_tab.columns) > 1:
            return '\t'
    except Exception:
        pass

    # Try semicolon
    try:
        df_semi = pd.read_csv(file_path, delimiter=';', skiprows=header_row, encoding='latin1')
        if len(df_semi.columns) > 1:
            return ';'
    except Exception:
        pass

    raise ValueError(f"Could not determine delimiter for {file_path}")

def process_files_in_folder(folder_path):
    # Create a new folder named "CsvFiles" in the user's documents folder
    output_folder = '/Users/juliavallim/Desktop'
    os.makedirs(output_folder, exist_ok=True)
    
    # List all .txt files in the specified folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        
        try:
            # Find the header row dynamically
            header_row = find_header_row(file_path)
            if header_row == -1:
                raise ValueError(f"Header row not found in {txt_file}")
                
            delimiter = smart_detect_delimiter(file_path, header_row)

            # Read the .txt file into a DataFrame, starting from the header row
            df = pd.read_csv(file_path, delimiter=delimiter, skiprows=header_row, encoding='latin1')
            
            # Check if 'DATE' and 'TIME' columns both exist
            if 'DATE' in df.columns and 'TIME' in df.columns:
                # Extract hour and minute from TIME column
                df['HOUR_MINUTE'] = df['TIME'].str[:5]
                
            elif 'DATE/TIME' in df.columns:
                # Split the 'DATE/TIME' column into separate 'DATE' and 'TIME' columns
                df[['DATE', 'TIME']] = df['DATE/TIME'].str.split(' ', expand=True)
                # Extract hour and minute from TIME column
                df['HOUR_MINUTE'] = df['TIME'].str[:5]
                
            else:
                raise ValueError(f"Neither 'DATE'/'TIME' nor 'DATE/TIME' column found in {txt_file}")

            # Check for the presence of 00:00 and 23:59 in the TIME column
            if not df[df['HOUR_MINUTE'] == '00:00'].empty and not df[df['HOUR_MINUTE'] == '23:59'].empty:
                # Filter the DataFrame to start from the first occurrence of 00:00 and end at the last occurrence of 23:59
                start_index = df[df['HOUR_MINUTE'] == '00:00'].index[0]
                end_index = df[df['HOUR_MINUTE'] == '23:59'].index[-1]
                df = df.loc[start_index:end_index].reset_index(drop=True)
            else:
                print(f"TIME 00:00 or 23:59 not found in the dataset for {txt_file}. Proceeding with the entire dataset.")

            # Drop the auxiliary HOUR_MINUTE column
            df = df.drop(columns=['HOUR_MINUTE'])

            # Create the Sleep column based on the STATE column
            df['Sleep'] = df['STATE'].apply(lambda x: 0 if x in [0, 4] else 1 if x in [1, 2] else None)

            # Reorder columns if necessary (optional)
            columns_order = ['DATE', 'TIME', 'Sleep'] + [col for col in df.columns if col not in ['DATE/TIME', 'DATE', 'TIME', 'Sleep']]
            df = df[columns_order]

            # Save the processed DataFrame to a new CSV file in the "LuluCsvFiles" folder
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(txt_file)[0]}_processed.csv")
            df.to_csv(output_file_path, sep=';', index=False)

        except Exception as e:
            print(f"Error processing file {txt_file}: {e}")


process_files_in_folder("'/Users/juliavallim/Library/CloudStorage/OneDrive-Pessoal/Laboratório/Pós-doutorado/Análise dos dados/Análise 3/Arquivos individuais/ArquivosTXT/Padronizado_7 dias")