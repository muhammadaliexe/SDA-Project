import json
import os
import multiprocessing
from plugins.inputs import read_csv_stuff
from core.engine import do_work
from plugins.outputs import SysTracker, LiveScreen

def get_cfg(path='config.json'):
    if not os.path.exists(path):
        print(f"Error: Required file '{path}' is missing.")
        return None
        
    with open(path, 'r') as f:
        return json.load(f)

def validate_cfg(cfg):
    if type(cfg) is not dict:
        print("Config Error: Configuration must be a dictionary.")
        return False

    if "pipeline_dynamics" not in cfg:
        print("Config Error: Missing required key 'pipeline_dynamics'.")
        return False

    dynamics = cfg["pipeline_dynamics"]
    if type(dynamics) is not dict:
        print("Config Error: 'pipeline_dynamics' must be a dictionary.")
        return False

    if "input_delay_seconds" not in dynamics or dynamics["input_delay_seconds"] < 0:
        print("Config Error: 'input_delay_seconds' is missing or cannot be negative.")
        return False

    if "core_parallelism" not in dynamics or dynamics["core_parallelism"] < 1:
        print("Config Error: 'core_parallelism' is missing or must be at least 1.")
        return False

    if "stream_queue_max_size" not in dynamics or dynamics["stream_queue_max_size"] < 1:
        print("Config Error: 'stream_queue_max_size' is missing or must be at least 1.")
        return False

    if "processing" not in cfg:
        print("Config Error: Missing required key 'processing'.")
        return False

    processing = cfg["processing"]
    if type(processing) is not dict or "stateful_tasks" not in processing:
        print("Config Error: Missing required key 'stateful_tasks' in processing.")
        return False

    stateful = processing["stateful_tasks"]
    if type(stateful) is not dict or "running_average_window_size" not in stateful or stateful["running_average_window_size"] < 1:
        print("Config Error: 'running_average_window_size' is missing or must be at least 1.")
        return False

    if "dataset_path" not in cfg or type(cfg["dataset_path"]) is not str:
        print("Config Error: 'dataset_path' is missing or must be a valid string path.")
        return False

    return True

if __name__ == '__main__':
    my_cfg = get_cfg()
    if my_cfg is None or not validate_cfg(my_cfg):
        exit(1)
        
    max_q = my_cfg["pipeline_dynamics"]["stream_queue_max_size"]
    w_count = my_cfg["pipeline_dynamics"]["core_parallelism"]

    q1 = multiprocessing.Queue(maxsize=max_q)
    q2 = multiprocessing.Queue(maxsize=max_q)

    p_in = multiprocessing.Process(
        target=read_csv_stuff, 
        args=(my_cfg, q1)
    )
    p_in.start()
    def launch_w(w_id):
        p = multiprocessing.Process(
            target=do_work, 
            args=(my_cfg, q1, q2)
        )
        p.start()
        return p

    w_list = list(map(launch_w, range(w_count)))

    my_tracker = SysTracker(q1, q2, max_q)
    my_ui = LiveScreen(my_cfg, q2, my_tracker)
    
    my_ui.run()

    p_in.terminate()
    list(map(lambda p: p.terminate(), w_list))