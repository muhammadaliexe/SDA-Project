REGION_MAPPING = {
    "Europe & Central Asia": ["Europe", "Asia"],
    "East Asia & Pacific": ["Asia", "Oceania"],
    "South Asia": ["Asia"],
    "Middle East & North Africa": ["Africa", "Asia"],
    "Sub-Saharan Africa": ["Africa"],
    "North America": ["North America"],
    "Latin America & Caribbean": ["South America", "North America"]
}

def filter_by_region(data, region_name):
    if region_name in REGION_MAPPING:
        target_values = REGION_MAPPING[region_name]
    else:
        target_values = [region_name]
    
    # filter() takes the items that match the condition
    return list(filter(lambda item: item['Region'] in target_values, data))

def filter_by_year(data, year):
    # filter() checks the year for every row instantly
    return list(filter(lambda item: item['Year'] == int(year), data))

def aggregate_stats(filtered_data, operation):
    if len(filtered_data) == 0:
        return 0
    
    # map() extracts just the 'Value' from every row into a simple list
    gdp_values = list(map(lambda item: item['Value'], filtered_data))
    
    total = sum(gdp_values)
        
    if operation == "sum":
        return total
        
    if operation == "average":
        return total / len(filtered_data)
    
    return 0