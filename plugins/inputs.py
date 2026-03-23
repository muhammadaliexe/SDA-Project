import csv
import time
import os

def fix_type(val, d_type):
    if d_type == "integer": return int(val)
    if d_type == "float": return float(val)
    return str(val)

def read_csv_stuff(cfg, in_q):
    file_path = cfg["dataset_path"]
    wait_time = cfg["pipeline_dynamics"]["input_delay_seconds"]
    cols_cfg = cfg["schema_mapping"]["columns"]
    w_count = cfg["pipeline_dynamics"]["core_parallelism"]

    if not os.path.exists(file_path):
        print(f"Input Error: The dataset file '{file_path}' was not found.")
        list(map(lambda _: in_q.put(None), range(w_count)))
        return

    name_map = dict(map(lambda c: (c["source_name"], c["internal_mapping"]), cols_cfg))
    type_map = dict(map(lambda c: (c["internal_mapping"], c["data_type"]), cols_cfg))

    print(f"Input Stream Started: Reading {file_path}...")
    
    with open(file_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        all_rows = list(csv_reader)

    def handle_row(r):
        good_items = filter(lambda i: i[0] in name_map, r.items())
        
        def make_dict(i):
            int_name = name_map[i[0]]
            d_type = type_map[int_name]
            return (int_name, fix_type(i[1], d_type))
        
        new_pkt = dict(map(make_dict, good_items))
        
        in_q.put(new_pkt)
        time.sleep(wait_time)

    list(map(handle_row, all_rows))
    
    list(map(lambda _: in_q.put(None), range(w_count)))