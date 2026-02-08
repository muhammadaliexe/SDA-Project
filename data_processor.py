REGION_MAPPING = {
    "Europe & Central Asia": ["Europe", "Asia"],
    "East Asia & Pacific": ["Asia", "Oceania"],
    "South Asia": ["Asia"],
    "Middle East & North Africa": ["Africa", "Asia"],
    "Sub-Saharan Africa": ["Africa"],
    "North America": ["North America"],
    "Latin America & Caribbean": ["South America", "North America"]
}

def filter_by_region(data, region):
    filtered = list(filter(lambda x: x['Region'] == region, data))
    return filtered

def filter_by_year(data, year):
    filtered = list(filter(lambda x: x['Year'] == int(year), data))
    return filtered

def aggregate_stats(filtered_data, operation):
    if len(filtered_data) == 0:
        return 0

    gdp_values = list(map(lambda x: x['Value'], filtered_data))
    
    total_gdp = sum(gdp_values)
    
    if operation == "sum":
        return total_gdp
    
    if operation == "average":
        return total_gdp / len(gdp_values)
    
    return 0

def get_country_names(filtered_data):
    return list(map(lambda x: x['Country Name'], filtered_data))

def get_gdp_values(filtered_data):
    return list(map(lambda x: x['Value'], filtered_data))