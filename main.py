import json
import os
from plugins.inputs import CsvReader, JsonReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter
from core import engine

# This dictionary matches the string in config.json to the right class
INPUT_DRIVERS = {
    "csv": CsvReader,
    "json": JsonReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "graphics": GraphicsChartWriter
}

def main():
    config_file = 'config.json'
    
    if not os.path.exists(config_file):
        print("Error: config.json file is missing.")
        return
        
    if os.path.getsize(config_file) == 0:
        print("Error: config.json is empty.")
        return
        
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Check for missing settings
    required_keys = {'input', 'output', 'file_path', 'region', 'year', 'operation'}
    if not required_keys.issubset(config.keys()):
        print("Error: Missing a required setting in config file.")
        return

    input_choice = config['input']
    output_choice = config['output']

    if input_choice not in INPUT_DRIVERS:
        print("Error: Invalid input choice in config.")
        return
        
    if output_choice not in OUTPUT_DRIVERS:
        print("Error: Invalid output choice in config.")
        return

    # Create the reader and writer objects
    reader = INPUT_DRIVERS[input_choice]()
    writer = OUTPUT_DRIVERS[output_choice]()

    print("Reading data...")
    raw_data = reader.read_data(config['file_path'])
    
    if raw_data is None:
        return

    region_data = engine.filter_by_region(raw_data, config['region'])
    if len(region_data) == 0:
        print("No data found for this region.")
        return

    year_data = engine.filter_by_year(region_data, config['year'])
    if len(year_data) == 0:
        print("No data found for this year.")
        return

    result = engine.aggregate_stats(year_data, config['operation'])

    # Send the data to the writer (console or chart)
    writer.write_data(year_data, result, config)

# Start the program
main()