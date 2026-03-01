import matplotlib.pyplot as plt

class ConsoleWriter:
    def write_data(self, data, config):
        print("\n========================================")
        print("DASHBOARD RESULTS")
        print("========================================")
        
        global_ops = ["continent_average", "global_trend", "fastest_growing_continent", "continent_contribution"]
        
        if config['operation'] in global_ops:
            print("Region:    World")
            print("Year:      " + str(config['year'][0]) + " to " + str(config['year'][1]))
        else:
            print("Region:    " + config['region'])
            print("Year:      " + str(config['year']))
            
        print("Operation: " + config['operation'])
        print("----------------------------------------")
        
        is_growth = (config['operation'] in ["growth_rate", "fastest_growing_continent"])
        is_contribution = (config['operation'] == "continent_contribution")
        
        if is_contribution:

            total_val = sum(list(map(lambda x: x['Value'], data)))
            text_lines = list(map(lambda item: item['Country Name'] + ": " + str(round((item['Value']/total_val)*100, 2)) + "%", data))
        elif is_growth:
            text_lines = list(map(lambda item: item['Country Name'] + ": " + str(round(item['Value'], 2)) + "%", data))
        else:
            text_lines = list(map(lambda item: item['Country Name'] + ": $" + str(round(item['Value'], 2)), data))
            
        print('\n'.join(text_lines))
        print("========================================\n")


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