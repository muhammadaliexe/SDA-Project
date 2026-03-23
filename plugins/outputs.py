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


class GraphicsChartWriter:
    def write_data(self, data, config):

        names = list(map(lambda item: item['Country Name'], data))
        values = list(map(lambda item: item['Value'], data))
        
        op = config['operation']

        plt.figure(figsize=(12, 6))
        
        if op == "continent_contribution":

            plt.pie(values, labels=names, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            plt.title("Continent Contribution to Global GDP (" + str(config['year'][0]) + " to " + str(config['year'][1]) + ")")
            
        elif op == "fastest_growing_continent":
            plt.bar(names, values, color='lightgreen')
            plt.title("Continent GDP Growth Rate (" + str(config['year'][0]) + " to " + str(config['year'][1]) + ")")
            plt.ylabel("Growth Rate (%)")
            plt.xlabel("Continent")
            plt.xticks(rotation=45, ha='right')

        elif op == "global_trend":
            plt.plot(names, values, marker='s', color='orange', linewidth=2)
            plt.fill_between(names, values, color='orange', alpha=0.3)
            plt.title("Total Global GDP Trend (" + str(config['year'][0]) + " to " + str(config['year'][1]) + ")")
            plt.ylabel("Global GDP (USD)")
            plt.xlabel("Year")
            plt.xticks(rotation=45)    
        
        elif op == "growth_rate":
            plt.plot(names, values, marker='o', color='green', linestyle='-', linewidth=2)
            plt.title("GDP Growth Rate in " + config['region'] + " (" + str(config['year'][0]) + " to " + str(config['year'][1]) + ")")
            plt.ylabel("Growth Rate (%)")
            plt.xlabel("Country")
            plt.xticks(rotation=90, ha='center', fontsize=8)
            
        elif op == "continent_average":
            plt.bar(names, values, color='purple')
            plt.title("Average GDP by Continent (" + str(config['year'][0]) + " to " + str(config['year'][1]) + ")")
            plt.ylabel("Average GDP (USD)")
            plt.xlabel("Continent")
            plt.xticks(rotation=45, ha='right')
            
        elif op in ["top", "bottom"]:
            plt.bar(names, values, color='skyblue')
            if op == "top":
                plt.title("Top 10 GDP in " + config['region'] + " (" + str(config['year']) + ")")
            else:
                plt.title("Bottom 10 GDP in " + config['region'] + " (" + str(config['year']) + ")")
            plt.ylabel("GDP (USD)")
            plt.xlabel("Country")
            plt.xticks(rotation=90, ha='center', fontsize=8)
            
        plt.tight_layout()
        plt.show()