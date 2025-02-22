
# The horizontal plot is made using the hline function
import matplotlib.pyplot as plt
import pandas as pd

# load data
data = pd.read_csv(
    "../data/processed/housing_data_202411.csv",
)


df = data
# # Sanity checks
# merged_df.groupby('area_name')['year'].min()
# merged_df.groupby('area_name')['year'].max()
# merged_df['year'].min()
# merged_df.groupby('area_name').size()
# merged_df[merged_df["area_name"] == "South Korea"]

# Create a new figure and axes object
fig, ax = plt.subplots(figsize=(8, 6))

# Define range for y-axis
y_range = range(1, len(df.index) + 1)

# Plot horizontal lines
ax.hlines(y=y_range, xmin=df['pop_per_dwelling_min'], xmax=df['pop_per_dwelling_max'], color='grey', alpha=0.4, zorder=1)

# Plot scatter points
ax.scatter(df['pop_per_dwelling_min'], y_range, color='skyblue', alpha=1, label='pop_per_dwelling_min', zorder=2)
ax.scatter(df['pop_per_dwelling_max'], y_range, color='lightgreen', alpha=1, label='pop_per_dwelling_max', zorder=2)
ax.scatter(df['pop_per_dwelling_last'], y_range, color='red', alpha=1, label='pop_per_dwelling_last', zorder=3)

# Add legend
ax.legend()

# Add title and axis labels
title = "Comparison of Population per Dwelling Values"
ax.set_title(title, loc='left')
ax.set_xlabel("Value of the variables")
ax.set_yticks(y_range)
ax.set_yticklabels(df['area_name'])

# Show the plot
plt.show()