import pandas as pd

# Load employment data
data = pd.read_csv(
    "https://github.com/jgleeson/PublicHouse/raw/main/dataset.csv"
)

### Data wrangling

# Create city dataset - Add city states
# Choose a common year across countries or interpolate if no data
# add persons per dwelling
# add Auckland

df_city=data[data['area_level'].isin([ 'city-region', 'city-state'])].copy()


df_country=data[data['area_level'].isin([ 'country'])].copy() # add hong kong and Singapore

df_dwellings_country=df_country[df_country['variable']=="dwellings"][["year","value","area_name","grouping"]].copy()
df_dwellings_country=df_dwellings_country.rename(columns={"value":"dwellings"})

df_pop_country=df_country[df_country['variable']=="population"][["year","value","area_name","grouping"]].copy()
df_pop_country=df_pop_country.rename(columns={"value":"population"})

merged_df = pd.merge(df_dwellings_country, df_pop_country, on=['year', 'area_name','grouping'])

merged_df.sort_values(by=['area_name', 'year']).reset_index(drop=True)

merged_df['min_year_by_area'] = merged_df.groupby('area_name')['year'].transform('min')

merged_df=merged_df[merged_df['min_year_by_area'] <= 1995].copy()
merged_df=merged_df[merged_df['year'] >= 1990].copy()

merged_df['size'] = merged_df.groupby('area_name').transform('size')

merged_df['pop_per_dwelling'] = merged_df['population'] / merged_df['dwellings']

merged_df['pop_per_dwelling_mean'] = merged_df.groupby('area_name')['pop_per_dwelling'].transform('mean')

merged_df['pop_per_dwelling_min'] = merged_df.groupby('area_name')['pop_per_dwelling'].transform('min')

merged_df['pop_per_dwelling_max'] = merged_df.groupby('area_name')['pop_per_dwelling'].transform('max')

merged_df['pop_per_dwelling_last'] = merged_df.groupby('area_name')['pop_per_dwelling'].transform('last')


# data needed for lollipop plot (persons per dwelling by city): index: index: 
summary_df = merged_df[['area_name','grouping', 'pop_per_dwelling_mean', 'pop_per_dwelling_min','pop_per_dwelling_max', 'pop_per_dwelling_last']].drop_duplicates(['area_name','grouping'])

summary_df = summary_df.sort_values(by='pop_per_dwelling_last')

# The horizontal plot is made using the hline function
import matplotlib.pyplot as plt
df=summary_df
my_range=range(1,len(df.index)+1)
plt.hlines(y=my_range, xmin=df['pop_per_dwelling_min'], xmax=df['pop_per_dwelling_max'], color='grey', alpha=0.4, zorder=1)
plt.scatter(df['pop_per_dwelling_min'], my_range, color='skyblue', alpha=1, label='pop_per_dwelling_min')
plt.scatter(df['pop_per_dwelling_max'], my_range, color='lightgreen', alpha=1 , label='pop_per_dwelling_max')
plt.scatter(df['pop_per_dwelling_last'], my_range, color='red', alpha=1 , label='pop_per_dwelling_last')
plt.legend()
 
# Add title and axis names
plt.yticks(my_range, df['area_name'])
plt.title("Comparison of the value 1 and the value 2", loc='left')
plt.xlabel('Value of the variables')

# Show the graph
plt.show()

# # Sanity checks
# merged_df.groupby('area_name')['year'].min()
# merged_df.groupby('area_name')['year'].max()
# merged_df['year'].min()
# merged_df.groupby('area_name').size()
merged_df[merged_df['area_name']=='South Korea']

# data needed for facet plot of migration by citizenship in NZ or internationally long form: index: [country, year], columns: ['net', 'departures','arrivals]


migration_data = pd.read_csv("../data/raw/df_citizenship_direction_202312.csv")

df=migration_data[migration_data['Citizenship'].isin([
    'New Zealand',
    'Australia', 
    'Fiji', 
    "China, People's Republic of",
    'India',
    'Korea, Republic of',
    'South Africa',
     'United Kingdom',
    ])]

df = df.pivot(
    index=["Month", "Citizenship"], 
    columns="Direction", 
    values="Count"
).reset_index()

df['arrivals_sum'] = df.groupby('Citizenship')['Arrivals'].transform(lambda x: x.rolling(window=12, min_periods=12).sum())
df['departures_sum'] = df.groupby('Citizenship')['Departures'].transform(lambda x: x.rolling(window=12, min_periods=12).sum())

df['Month'] = pd.to_datetime(df['Month'])

df=df[df['Month']>='2001-12-01']

# save df to csv
df.to_csv('../data/processed/nz_migration_facet_data_202312.csv', index=False) 




