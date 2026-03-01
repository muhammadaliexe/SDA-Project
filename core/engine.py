REGION_MAPPING = {
    "Europe & Central Asia": ["Europe", "Asia"],
    "East Asia & Pacific": ["Asia", "Oceania"],
    "South Asia": ["Asia"],
    "Middle East & North Africa": ["Africa", "Asia"],
    "Sub-Saharan Africa": ["Africa"],
    "North America": ["North America"],
    "Latin America & Caribbean": ["South America", "North America"]
}

VALID_CONTINENTS = ["Asia", "Europe", "Africa", "North America", "South America", "Oceania"]

class TransformationEngine:
    def __init__(self, sink, config):
        self.sink = sink
        self.config = config

    def execute(self, raw_data):
        operation = self.config['operation']
        year_setting = self.config['year']

        

        # OPERATION 6: FASTEST GROWING CONTINENT
        if operation == "fastest_growing_continent":
            if type(year_setting) is not list or len(year_setting) != 2:
                print("Error: Year must be a list of two years like [2014, 2020].")
                return
                
            start_year = int(year_setting[0])
            end_year = int(year_setting[1])

            start_data = list(filter(lambda item: item['Year'] == start_year, raw_data))
            end_data = list(filter(lambda item: item['Year'] == end_year, raw_data))
            
            all_regions = list(set(map(lambda item: item['Region'], start_data + end_data)))

            real_continents = list(filter(lambda r: r in VALID_CONTINENTS, all_regions))

            def calc_cont_growth(reg):
                s_items = list(filter(lambda item: item['Region'] == reg, start_data))
                e_items = list(filter(lambda item: item['Region'] == reg, end_data))
                
                s_val = sum(list(map(lambda item: item['Value'], s_items)))
                e_val = sum(list(map(lambda item: item['Value'], e_items)))
                
                if s_val == 0:
                    growth = 0
                else:
                    growth = ((e_val - s_val) / s_val) * 100
                    
                return {'Country Name': reg, 'Value': growth}

            final_data = list(map(calc_cont_growth, real_continents))
            final_data = sorted(final_data, key=lambda x: x['Value'], reverse=True)

            self.sink.write_data(final_data, self.config)
            return

        # OPERATION 5: GLOBAL TREND
        if operation == "global_trend":
            if type(year_setting) is not list or len(year_setting) != 2:
                print("Error: For global_trend, year must be a list of two years like [2010, 2020].")
                return
                
            start_year = int(year_setting[0])
            end_year = int(year_setting[1])

            valid_data = list(filter(lambda item: start_year <= item['Year'] <= end_year, raw_data))
            
            if len(valid_data) == 0:
                print("No data found for this year range.")
                return

            years_list = sorted(list(set(map(lambda item: item['Year'], valid_data))))

            def calc_year_total(yr):
                yr_items = list(filter(lambda item: item['Year'] == yr, valid_data))
                yr_values = list(map(lambda item: item['Value'], yr_items))
                total = sum(yr_values)
                return {'Country Name': str(yr), 'Value': total}

            final_data = list(map(calc_year_total, years_list))
            
            self.sink.write_data(final_data, self.config)
            return

        # OPERATION 4: CONTINENT AVERAGE
        if operation == "continent_average":
            if type(year_setting) is not list or len(year_setting) != 2:
                print("Error: For continent_average, year must be a list of two years like [2014, 2020].")
                return
                
            start_year = int(year_setting[0])
            end_year = int(year_setting[1])

            valid_data = list(filter(lambda item: start_year <= item['Year'] <= end_year, raw_data))
            
            if len(valid_data) == 0:
                print("No data found for this year range.")
                return

            all_regions = list(set(map(lambda item: item['Region'], valid_data)))

            real_continents = list(filter(lambda r: r in VALID_CONTINENTS, all_regions))

            def calc_region_avg(region_name):
                region_items = list(filter(lambda item: item['Region'] == region_name, valid_data))
                region_values = list(map(lambda item: item['Value'], region_items))
                
                if len(region_values) > 0:
                    avg = sum(region_values) / len(region_values)
                else:
                    avg = 0
                    
                return {'Country Name': region_name, 'Value': avg}

            final_data = list(map(calc_region_avg, real_continents))
            final_data = sorted(final_data, key=lambda x: x['Value'], reverse=True)

            self.sink.write_data(final_data, self.config)
            return

        region_name = self.config['region']
        if region_name in REGION_MAPPING:
            target_values = REGION_MAPPING[region_name]
        else:
            target_values = [region_name]
        
        region_data = list(filter(lambda item: item['Region'] in target_values, raw_data))
        
        if len(region_data) == 0:
            print("No data found for this region.")
            return

        # OPERATION 3: GROWTH RATE (Countries)
        if operation == "growth_rate":
            if type(year_setting) is not list or len(year_setting) != 2:
                print("Error: For growth_rate, year must be a list of two years like [2014, 2020].")
                return
                
            start_year = int(year_setting[0])
            end_year = int(year_setting[1])
            
            start_data = list(filter(lambda item: item['Year'] == start_year, region_data))
            end_data = list(filter(lambda item: item['Year'] == end_year, region_data))
            
            start_dict = dict(map(lambda item: (item['Country Name'], item['Value']), start_data))
            
            valid_end_data = list(filter(lambda item: item['Country Name'] in start_dict, end_data))
            
            if len(valid_end_data) == 0:
                print("No matching data found for those years.")
                return

            def calc_growth(item):
                start_val = start_dict[item['Country Name']]
                end_val = item['Value']
                growth = ((end_val - start_val) / start_val) * 100
                return {'Country Name': item['Country Name'], 'Value': growth}

            final_data = list(map(calc_growth, valid_end_data))

        # OPERATION 1 & 2: TOP OR BOTTOM 10
        elif operation in ["top", "bottom"]:
            if type(year_setting) is list:
                target_year = int(year_setting[0])
            else:
                target_year = int(year_setting)
                
            year_data = list(filter(lambda item: item['Year'] == target_year, region_data))
            
            if len(year_data) == 0:
                print("No data found for this year.")
                return

            if operation == "top":
                sorted_data = sorted(year_data, key=lambda x: x['Value'], reverse=True)
            else:
                sorted_data = sorted(year_data, key=lambda x: x['Value'], reverse=False)
                
            final_data = sorted_data[:10]

        if len(final_data) == 0:
            print("No data to show.")
            return

        self.sink.write_data(final_data, self.config)