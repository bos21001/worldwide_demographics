import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# wdi_wide.csv openning

wdi = pd.read_csv("wdi_wide.csv")

wdi['region'].replace('', np.nan, inplace=True)
wdi.dropna(subset=['region', 'GNI', 'life_expectancy_female', 'life_expectancy_male', 'internet_use', 'population'],
           inplace=True)

regions = wdi.region.unique()
regions.sort()

# Internet usage session

internet_use = wdi[["region", "internet_use", "population"]]
internet_use = internet_use.sort_values(by="region").reset_index(drop=True)
internet_use_percentage_sum = []
internet_use_by_region = {}

for continent_name in regions:
    internet_use_by_region[continent_name.lower(
    )] = internet_use.loc[internet_use.region == continent_name]

for continent_name in internet_use_by_region:
    internet_use_arr = internet_use_by_region[continent_name].values
    population_internet_result = []
    for internet_use in internet_use_arr:
        population_internet_result.append((internet_use[1] / 100) * internet_use[2])
    
    internet_use_by_region[continent_name]["result_population_internet_use"] = population_internet_result

internet_use_average_by_region = {}

for continent_name in internet_use_by_region:

    internet_use_average_by_region[continent_name] = {}
    for region_column_name_value in internet_use_by_region[continent_name].columns.values:
        if region_column_name_value == "population":
            internet_use_average_by_region[continent_name].update(
                {
                    region_column_name_value: internet_use_by_region[continent_name][region_column_name_value].sum(
                    )
                }
            )
        elif region_column_name_value == "internet_use":
            
            sum_result_population_internet_use = internet_use_by_region[continent_name]["result_population_internet_use"].sum()
            sum_population = internet_use_by_region[continent_name]["population"].sum()
            percentage_population_internet_use = ((sum_result_population_internet_use * 100) / sum_population)
            
            internet_use_average_by_region[continent_name].update(
                {
                    region_column_name_value : percentage_population_internet_use
                }
            )

# GNI life expectancy session

gni_life_expectancy = wdi[["region", "GNI",
                           "life_expectancy_female", "life_expectancy_male"]]
gni_life_expectancy = gni_life_expectancy.sort_values(
    by="region").reset_index(drop=True)
gni_life_expectancy_by_region = {}

for continent_name in regions:
    gni_life_expectancy_by_region[continent_name.lower()] = gni_life_expectancy.loc[
        gni_life_expectancy.region == continent_name
    ]

gni_life_average_expectancy_by_region = {}

for continent_name in gni_life_expectancy_by_region:

    gni_life_average_expectancy_by_region[continent_name] = {}
    for region_column_name_value in gni_life_expectancy_by_region[continent_name].columns.values:
        if region_column_name_value == "GNI":
            gni_life_average_expectancy_by_region[continent_name] \
                .update(
                {
                    region_column_name_value: gni_life_expectancy_by_region[
                        continent_name][region_column_name_value]
                    .sum()
                }
            )
        elif region_column_name_value != "region":
            gni_life_average_expectancy_by_region[continent_name].update(
                {
                    region_column_name_value: gni_life_expectancy_by_region[
                        continent_name][region_column_name_value]
                    .mean()
                }
            )
            
    life_expectancy_people = (gni_life_average_expectancy_by_region[continent_name]['life_expectancy_female'] + gni_life_average_expectancy_by_region[continent_name]['life_expectancy_male']) / 2
    gni_life_average_expectancy_by_region[continent_name].update(
        {
            "life_expectancy_people": life_expectancy_people
        }
    )
    
# Charts generators

internet_use_pd = pd.DataFrame(internet_use_average_by_region)

population_row = pd.DataFrame(internet_use_pd.loc[["population"]])
internet_use_row = pd.DataFrame(internet_use_pd.loc[["internet_use"]])

internet_use_row.plot(kind="bar", rot=9)
population_row.plot(kind="bar", rot=9)
plt.show()

gni_life_expectancy_pd = pd.DataFrame(gni_life_average_expectancy_by_region)

gni_row = pd.DataFrame(gni_life_expectancy_pd.loc[["GNI"]])
life_expectancy_row = pd.DataFrame(gni_life_expectancy_pd.loc[["life_expectancy_people"]])

gni_row.plot(kind="bar", rot=9)
life_expectancy_row.plot(kind="bar", rot=9)

plt.show()
