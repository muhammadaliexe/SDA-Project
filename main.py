import data_loader

def main():
    config = data_loader.load_config('config.json')
    
    if config is None:
        return

    print("Loading data...")
    raw_data = data_loader.load_and_clean_data(config['file_path'])
    
    if raw_data is None:
        return
    
 #   print(raw_data)
    
main()
    