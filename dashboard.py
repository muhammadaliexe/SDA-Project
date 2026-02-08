import matplotlib.pyplot as plt
import data_processor

def show_results(result, config):
    print("\n" + "="*40)
    print(f"DASHBOARD RESULTS")
    print("="*40)
    print(f"Region:    {config['region']}")
    print(f"Year:      {config['year']}")
    print(f"Operation: {config['operation']}")
    print("-" * 40)
    print(f"Result:    ${result:,.2f}")
    print("="*40 + "\n")

def plot_data(full_region_data, year_data, config):
    
    sorted_data = sorted(year_data, key=lambda x: x['Value'], reverse=True)
    top_10 = sorted_data[:10]
    
    names = data_processor.get_country_names(top_10)
    values = data_processor.get_gdp_values(top_10)

    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.bar(names, values, color='skyblue')
    plt.title(f"Top 10 GDP in {config['region']} ({config['year']})")
    plt.xlabel("Country")
    plt.ylabel("GDP (USD)")
    plt.xticks(rotation=45, ha='right')

    all_years = sorted(list(set(d['Year'] for d in full_region_data)))
    
    yearly_totals = []
    for y in all_years:
        d_year = data_processor.filter_by_year(full_region_data, y)
        total = data_processor.aggregate_stats(d_year, "sum")
        yearly_totals.append(total)

    plt.subplot(1, 2, 2)
    plt.plot(all_years, yearly_totals, marker='o', color='green')
    plt.title(f"GDP Trend: {config['region']}")
    plt.xlabel("Year")
    plt.ylabel("Total GDP")
    plt.grid(True)

    plt.tight_layout()
    plt.show()