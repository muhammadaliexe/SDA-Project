import json
import os
from plugins.inputs import CsvReader, JsonReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter
from core.engine import TransformationEngine

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
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print("Error: config.json contains invalid JSON.")
            return

    required_keys = {'input', 'output', 'file_path', 'region', 'year', 'operation'}
    if not required_keys.issubset(config.keys()):
        print("Error: Missing a required setting in config file.")
        return

    input_choice = config['input']
    output_choice = config['output']
    operation_choice = config['operation']

    if input_choice not in INPUT_DRIVERS:
        print("Error: Invalid input choice in config.")
        return
        
    if output_choice not in OUTPUT_DRIVERS:
        print("Error: Invalid output choice in config.")
        return
        
    valid_operations = [
        'top', 'bottom', 'growth_rate', 'continent_average', 
        'global_trend', 'fastest_growing_continent', 'continent_contribution'
    ]
    if operation_choice not in valid_operations:
        print("Error: Invalid operation in config file.")
        return

    reader = INPUT_DRIVERS[input_choice]()
    writer = OUTPUT_DRIVERS[output_choice]()

    engine = TransformationEngine(writer, config)

    print("\nReading data...")
    raw_data = reader.read_data(config['file_path'])
    
    if raw_data is None:
        return

    engine.execute(raw_data)

if __name__ == '__main__':
    main()