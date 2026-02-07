import pandas as pd
import json
import os

def load_config(config_file):
    
    if not os.path.exists(config_file):
        print(f"Error: The file '{config_file}' does not exist.")
        return None
    
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def load_and_clean_data(csv_file):
    
    if not os.path.exists(csv_file):
        print(f"Error: The data file '{csv_file}' was not found.")
        return None

    df = pd.read_csv(csv_file)

    if 'Continent' not in df.columns:
        print("Error: The CSV is missing the 'Continent' column.")
        return None

    year_columns = [col for col in df.columns if col.isdigit()]

    df2 = df.melt(
        id_vars=['Country Name', 'Continent'], 
        value_vars=year_columns,
        var_name='Year', 
        value_name='Value'
    )

    df2.rename(columns={'Continent': 'Region'}, inplace=True)
    
    df2['Year'] = pd.to_numeric(df2['Year'], errors='coerce')
    df2['Value'] = pd.to_numeric(df2['Value'], errors='coerce')

    df2.dropna(subset=['Value', 'Region'], inplace=True)
    
#    print(df2)

    data_list = df2.to_dict('records')
    
    return data_list