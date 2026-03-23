import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core.engine import AvgCalc

class SysTracker:
    def __init__(self, in_q, out_q, mx_size):
        self.in_q = in_q
        self.out_q = out_q
        self.mx_size = mx_size
        self.viewers = []

    def add_viewer(self, v):
        self.viewers.append(v)

    def alert_viewers(self):
        in_sz = self.in_q.qsize()
        out_sz = self.out_q.qsize()

        in_stat = self.pick_color(in_sz)
        out_stat = self.pick_color(out_sz)

        list(map(lambda v: v.update_colors(in_stat, out_stat), self.viewers))

    def pick_color(self, sz):
        pct = (sz / self.mx_size) * 100
        if pct < 50: return "green"
        if pct < 80: return "yellow"
        return "red"

class LiveScreen:
    def __init__(self, cfg, out_q, tracker):
        self.cfg = cfg
        self.out_q = out_q
        self.tracker = tracker
        self.tracker.add_viewer(self)

        w_size = cfg["processing"]["stateful_tasks"]["running_average_window_size"]
        self.math_guy = AvgCalc(w_size)

        self.x_times = []
        self.y_raw = []
        self.y_avg = []
        self.color1 = "gray"
        self.color2 = "gray"

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [3, 1]})
        self.fig.canvas.manager.set_window_title('Phase 3 Real-Time Dashboard')

    def update_colors(self, stat1, stat2):
        self.color1 = stat1
        self.color2 = stat2

    def empty_q_func(self):
        if not self.out_q.empty():
            pkt = self.out_q.get_nowait()
            done_pkt = self.math_guy.add_new_val(pkt)
            
            self.x_times.append(done_pkt['time_period'])
            self.y_raw.append(done_pkt['metric_value'])
            self.y_avg.append(done_pkt['computed_metric'])
            
            self.empty_q_func()

    def draw_frame(self, frame_num):
        self.empty_q_func()

        self.tracker.alert_viewers()

        self.ax1.clear()
        self.ax1.plot(self.x_times[-20:], self.y_raw[-20:], label='Authentic Raw', marker='o', color='blue')
        self.ax1.plot(self.x_times[-20:], self.y_avg[-20:], label='Running Avg', marker='x', color='orange')
        self.ax1.set_title("Live Sensor Data & Averages")
        self.ax1.legend()

        self.ax2.clear()
        self.ax2.bar(["Raw Stream", "Processed Stream"], [1, 1], color=[self.color1, self.color2])
        self.ax2.set_ylim(0, 1)
        self.ax2.set_title("Pipeline Telemetry")
        self.ax2.set_yticks([])

    def run(self):
        print("Starting Dashboard...")
        self.ani = animation.FuncAnimation(self.fig, self.draw_frame, interval=500, cache_frame_data=False)
        plt.tight_layout()
        plt.show()