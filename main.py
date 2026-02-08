import data_loader
import data_processor

def main():
    config = data_loader.load_config('config.json')
    
    if config is None:
        return

    print("Loading data...")
    raw_data = data_loader.load_and_clean_data(config['file_path'])
    
    if raw_data is None:
        return
    
#    print(raw_data)

    region_data = data_processor.filter_by_region(raw_data, config['region'])
    
    if len(region_data) == 0:
        print(f"No data found for region: {config['region']}")
        return
    print(region_data)

    target_year_data = data_processor.filter_by_year(region_data, config['year'])

    if len(target_year_data) == 0:
        print(f"No data found for year: {config['year']}")
        return
    print(target_year_data)

    result_value = data_processor.aggregate_stats(target_year_data, config['operation'])
    print(result_value)
    
main()
    