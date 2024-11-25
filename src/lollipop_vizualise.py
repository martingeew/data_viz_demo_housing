
# The horizontal plot is made using the hline function
import matplotlib.pyplot as plt
import pandas as pd

# load data
data = pd.read_csv(
    "../data/processed/housing_data_202411.csv",
)


df = data
my_range = range(1, len(df.index) + 1)
plt.hlines(
    y=my_range,
    xmin=df["pop_per_dwelling_min"],
    xmax=df["pop_per_dwelling_max"],
    color="grey",
    alpha=0.4,
    zorder=1,
)
plt.scatter(
    df["pop_per_dwelling_min"],
    my_range,
    color="skyblue",
    alpha=1,
    label="pop_per_dwelling_min",
)
plt.scatter(
    df["pop_per_dwelling_max"],
    my_range,
    color="lightgreen",
    alpha=1,
    label="pop_per_dwelling_max",
)
plt.scatter(
    df["pop_per_dwelling_last"],
    my_range,
    color="red",
    alpha=1,
    label="pop_per_dwelling_last",
)
plt.legend()

# Add title and axis names
plt.yticks(my_range, df["area_name"])
plt.title("Comparison of the value 1 and the value 2", loc="left")
plt.xlabel("Value of the variables")

# Show the graph
plt.show()

# # Sanity checks
# merged_df.groupby('area_name')['year'].min()
# merged_df.groupby('area_name')['year'].max()
# merged_df['year'].min()
# merged_df.groupby('area_name').size()
# merged_df[merged_df["area_name"] == "South Korea"]