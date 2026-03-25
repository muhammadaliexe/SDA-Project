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

if __name__ == '__main__':
    my_cfg = get_cfg()
    if my_cfg is None:
        exit()
        
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