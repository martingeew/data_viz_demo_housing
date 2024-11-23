import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.lines import Line2D # for the legend

import matplotlib.patches as patches # for the legend


### Facet plot

### Main plot
# Todo:
# Make axes value in k
# Fonts - choose a font and stick to it for the future (casual modern minimalist)
# update NZ data
# title: Who's filling the gap?

# load data
data = pd.read_csv(
    "../data/processed/nz_migration_facet_data_202312.csv", parse_dates=["Month"]
)

### Constants

BLUE = '#2166ACFF'
BLUE_LIGHT = '#4393C3FF'
RED = '#B2182BFF'
RED_LIGHT = '#D6604DFF'
GREY40 = "#666666"
GREY25 = "#404040"
GREY20 = "#333333"
CHARCOAL = "#333333"

font = "Consolas"  # techy feel

def single_plot(x, y1, y2, name, ax):

    ax.plot(x, y1, color=BLUE)
    ax.plot(x, y2, color=RED)

    ax.fill_between(
        x, y1, y2, where=(y1 > y2), interpolate=True, color=BLUE_LIGHT, alpha=0.3
    )

    ax.fill_between(
        x, y1, y2, where=(y1 <= y2), interpolate=True, color=RED_LIGHT, alpha=0.3
    )

    ax.tick_params(axis="x", colors=GREY40, size=10)

    # yticks = [0, 10, 20]
    # ax.set_yticks(yticks)
    # ax.set_yticks([5, 15, 25], minor=True)
    # added a 'size' argument
    # ax.set_yticklabels(yticks, color=GREY40, size=10)
    # ax.set_ylim((-1, 26))

    ax.tick_params(axis="y", colors=GREY40)

    ax.grid(which="minor", lw=0.4, alpha=0.4)
    ax.grid(which="major", lw=0.8, alpha=0.4)

    ax.yaxis.set_tick_params(which="both", length=0)
    ax.xaxis.set_tick_params(which="both", length=0)

    ax.spines["left"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    # added a 'size' argument
    ax.set_title(name, weight="bold", size=9, color=CHARCOAL)




NROW = 3
NCOL = 3
NAMES = ["New Zealand"] + list(
    data[(data["Month"] == "2023-12-01") & (data["Citizenship"] != "New Zealand")]
    .sort_values(by="net_sum", ascending=False)["Citizenship"]
    .unique()
)

### Plot

df_plot = data[["Month", "Citizenship", "arrivals_sum", "departures_sum"]]

# Create the figure and axes for subplots
fig, axes = plt.subplots(NROW, NCOL, figsize=(12, 10), sharex=True, sharey=True)

# Flatten axes for easy iteration
axes_flat = axes.flatten()

for i, name in enumerate(NAMES):
    # Select data for the citizenship in 'name'
    df_subset = df_plot[df_plot["Citizenship"] == name]

    # Take the corresponding axis
    ax = axes_flat[i]

    # Take values for x, y1, and y2
    MONTH = df_subset["Month"].values
    ARRIVALS = df_subset["arrivals_sum"].values
    DEPARTURES = df_subset["departures_sum"].values

    # Plot it using the single_plot function
    single_plot(MONTH, DEPARTURES, ARRIVALS, name, ax)

# Remove any unused subplots
for j in range(len(NAMES), len(axes_flat)):
    fig.delaxes(axes_flat[j])
    

# Create handles for lines.
handles = [
    Line2D([], [], c=color, lw=1.2, label=label)
    for label, color in zip(["Departures", "Arrivals"], [BLUE, RED])
]

# Add legend for the lines
fig.legend(
    handles=handles,
    loc=(0.75, 0.95), # This coord is bottom-left corner
    ncol=2,           # 1 row, 2 columns layout
    columnspacing=1,  # Space between columns
    handlelength=1.2, # Line length
    frameon=False     # No frame
)


# Create handles for the area fill with `patches.Patch()`
outflow = patches.Patch(facecolor=BLUE_LIGHT, alpha=0.3, label="Net outflow")
inflow = patches.Patch(facecolor=RED_LIGHT, alpha=0.3, label="Net inflow")

fig.legend(
    handles=[outflow, inflow],
    loc=(0.75, 0.92), # This coord is top-right corner
    ncol=2,          # 1 row, 2 columns layout
    columnspacing=1, # Space between columns
    handlelength=2,  # Area length
    handleheight=2,  # Area height
    frameon=False,   # No frame
)

# Title
fig.text(
    s="Who are filling the gaps in migration",
    x=0.05,
    y=0.98,
    color=CHARCOAL,
    fontsize=26,
    font=font,
    ha="left",
    va="top",
)

# Adjust layout and show the plot
plt.tight_layout()
plt.subplots_adjust(top=0.85)
# fig.suptitle("Arrivals vs Departures for Different Countries")
plt.show()
