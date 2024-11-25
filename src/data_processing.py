import pandas as pd

# Load public data
data = pd.read_csv("https://github.com/jgleeson/PublicHouse/raw/main/dataset.csv")

################################################################################
# Dataset for lollipop plot

# Create city dataset - Add city states
# Choose a common year across countries or interpolate if no data
# add persons per dwelling
# add Auckland

# df_city = data[data["area_level"].isin(["city-region", "city-state"])].copy()

df_country = data[
    data["area_level"].isin(["country"])
].copy()  # add hong kong and Singapore

df_dwellings_country = df_country[df_country["variable"] == "dwellings"][
    ["year", "value", "area_name", "grouping"]
].copy()
df_dwellings_country = df_dwellings_country.rename(columns={"value": "dwellings"})

df_pop_country = df_country[df_country["variable"] == "population"][
    ["year", "value", "area_name", "grouping"]
].copy()
df_pop_country = df_pop_country.rename(columns={"value": "population"})

merged_df = pd.merge(
    df_dwellings_country, df_pop_country, on=["year", "area_name", "grouping"]
)

merged_df.sort_values(by=["area_name", "year"]).reset_index(drop=True)

merged_df["min_year_by_area"] = merged_df.groupby("area_name")["year"].transform("min")

merged_df = merged_df[merged_df["min_year_by_area"] <= 1995].copy()
merged_df = merged_df[merged_df["year"] >= 1990].copy()

merged_df["size"] = merged_df.groupby("area_name").transform("size")

merged_df["pop_per_dwelling"] = merged_df["population"] / merged_df["dwellings"]

merged_df["pop_per_dwelling_mean"] = merged_df.groupby("area_name")[
    "pop_per_dwelling"
].transform("mean")

merged_df["pop_per_dwelling_min"] = merged_df.groupby("area_name")[
    "pop_per_dwelling"
].transform("min")

merged_df["pop_per_dwelling_max"] = merged_df.groupby("area_name")[
    "pop_per_dwelling"
].transform("max")

merged_df["pop_per_dwelling_last"] = merged_df.groupby("area_name")[
    "pop_per_dwelling"
].transform("last")


# data needed for lollipop plot (persons per dwelling by city): index: index:
summary_df = merged_df[
    [
        "area_name",
        "grouping",
        "pop_per_dwelling_mean",
        "pop_per_dwelling_min",
        "pop_per_dwelling_max",
        "pop_per_dwelling_last",
    ]
].drop_duplicates(["area_name", "grouping"])

summary_df = summary_df.sort_values(by="pop_per_dwelling_last")

summary_df.to_csv("../data/processed/housing_data_202411.csv", index=False)

################################################################################
# data needed for facet plot of migration by citizenship 

migration_data = pd.read_csv("../data/raw/df_citizenship_direction_202312.csv")

# check most important groups
df_rank = migration_data[migration_data["Direction"] == "Net"].copy()
df_rank["net_sum"] = df_rank.groupby("Citizenship")["Count"].transform(
    lambda x: x.rolling(window=12, min_periods=12).sum()
)

# all time
print(df_rank[(df_rank["net_sum"] > 2000)].sort_values(by="net_sum", ascending=False)[
    "Citizenship"
].unique())  # check most important countries

# recent
print(df_rank[(df_rank["net_sum"] > 2000) & (df_rank["Month"] > "2023-06-01")].sort_values(
    by="net_sum", ascending=False
)[
    "Citizenship"
].unique())  # check most important countries

# top inflows by citizenship
top_citizenships = [
    "New Zealand",
    "India",
    "Philippines",
    "China, People's Republic of",
    "Fiji",
    "South Africa",
    "Sri Lanka",
    "Viet Nam",
    "United Kingdom",
    # "United States of America",
    # "Tonga",
    # "Samoa",
    #"Korea, Republic of",
]

# Calculate the total for 'TOTAL ALL CITIZENSHIPS'
total_all = migration_data[migration_data["Citizenship"] == "TOTAL ALL CITIZENSHIPS"]

# Calculate the total for the excluded categories
excluded_total = (
    migration_data[migration_data["Citizenship"].isin(top_citizenships)]
    .groupby(["Month", "Direction"])["Count"]
    .sum()
    .reset_index()
)

# Merge and calculate the new entry for 'Remaining Citizenship'
remaining_total = total_all.merge(
    excluded_total, on=["Month", "Direction"], suffixes=("_total", "_excluded")
)
remaining_total["Count"] = (
    remaining_total["Count_total"] - remaining_total["Count_excluded"]
)
remaining_total["Citizenship"] = "Other Citizenships"

# Select the relevant columns
remaining_total = remaining_total[["Month", "Count", "Direction", "Citizenship"]]

# Append the new entry to the original DataFrame
migration_data = pd.concat([migration_data, remaining_total], ignore_index=True)

# Final dataset for plot in wide format
df = migration_data[migration_data["Citizenship"].isin(top_citizenships)]

df = df.pivot(
    index=["Month", "Citizenship"], columns="Direction", values="Count"
).reset_index()

df["arrivals_sum"] = df.groupby("Citizenship")["Arrivals"].transform(
    lambda x: x.rolling(window=12, min_periods=12).sum()
)
df["departures_sum"] = df.groupby("Citizenship")["Departures"].transform(
    lambda x: x.rolling(window=12, min_periods=12).sum()
)
df["net_sum"] = df.groupby("Citizenship")["Net"].transform(
    lambda x: x.rolling(window=12, min_periods=12).sum()
)

df["Month"] = pd.to_datetime(df["Month"])

df = df[df["Month"] >= "2001-12-01"]

df['Citizenship'] = df['Citizenship'].replace({
    "China, People's Republic of": 'China',
    'Viet Nam': 'Vietnam'
})

# save df to csv
df.to_csv("../data/processed/nz_migration_facet_data_202312.csv", index=False)


################################################################################
# Data for anmiation plot

housing_data = pd.read_csv("../data/raw/homeownership_state_20241124.csv",  index_col=0, parse_dates=True)

housing_data.index = housing_data.index.to_period('Y')

# Convert the DataFrame from wide to long format
df_long = housing_data.reset_index().melt(id_vars='index', var_name='state', value_name='home_ownership')

# Rename the 'index' column to 'year'
df_long.rename(columns={'index': 'year'}, inplace=True)

df_long['year'] = df_long['year'].dt.year

df_long=df_long[df_long['year'].isin([1984, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023])].copy()

df_long.to_csv("../data/processed/homeownership_state_processed_20241124.csv", index=False)