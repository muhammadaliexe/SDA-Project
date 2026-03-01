import pandas as pd
import json
import os
from core.contracts import DataReader

def is_digit_string(text):
    return str(text).isdigit()

class CsvReader:
    def read_data(self, file_path):
        if not os.path.exists(file_path):
            print(f"Error: CSV file '{file_path}' not found.")
            return None
        
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        
        if 'Continent' not in df.columns:
            print("Error: Missing 'Continent' column.")
            return None
            
        year_columns = list(filter(is_digit_string, df.columns))
        df_long = df.melt(id_vars=['Country Name', 'Continent'], value_vars=year_columns, var_name='Year', value_name='Value')
        df_long.rename(columns={'Continent': 'Region'}, inplace=True)
        
        df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
        df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
        df_long.dropna(subset=['Value', 'Region'], inplace=True)
        
        return df_long.to_dict('records')

class JsonReader:
    def read_data(self, file_path):
        if not os.path.exists(file_path):
            print("Error: The JSON file was not found.")
            return None
            
        if os.path.getsize(file_path) == 0:
            print("Error: The JSON file is empty.")
            return None

        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            raw_text = file.read()
            
        clean_text = raw_text.replace('#@$!\\', 'null').replace('NaN', 'null')
        
        data = json.loads(clean_text)
        
        df = pd.DataFrame(data)
        
        if 'Continent' not in df.columns:
            print("Error: The JSON is missing the 'Continent' column.")
            return None
            
        year_columns = list(filter(is_digit_string, df.columns))
                
        df_long = df.melt(id_vars=['Country Name', 'Continent'], value_vars=year_columns, var_name='Year', value_name='Value')
        df_long.rename(columns={'Continent': 'Region'}, inplace=True)
        
        df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
        df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
        df_long.dropna(subset=['Value', 'Region'], inplace=True)
        
        return df_long.to_dict('records')