import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.lines import Line2D  # for the legend

import matplotlib.patches as patches  # for the legend
from pyfonts import load_font
from matplotlib.ticker import FuncFormatter
import numpy as np

### Constants

BLUE = "#2166ACFF"
BLUE_LIGHT = "#4393C3FF"
RED = "#B2182BFF"
RED_LIGHT = "#D6604DFF"
GREY40 = "#666666"
GREY25 = "#404040"
GREY20 = "#333333"
CHARCOAL = "#333333"

# Load the fonts
font = load_font(
    "https://github.com/google/fonts/blob/main/ofl/cabincondensed/CabinCondensed-SemiBold.ttf?raw=true"
)
other_font = load_font(
    "https://github.com/google/fonts/blob/main/ofl/cabincondensed/CabinCondensed-Regular.ttf?raw=true"
)
other_bold_font = load_font(
    "https://github.com/google/fonts/blob/main/ofl/cabincondensed/CabinCondensed-Medium.ttf?raw=true"
)


# Custom function to convert y-tick values to 'k' format
def thousands_formatter(x, pos):
    if x >= 1000:
        return f"{int(x / 1000)}k"
    else:
        return f"{int(x)}"


# Function for a single plot
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
    ax.tick_params(axis="y", colors=GREY40)

    ax.grid(which="minor", lw=0.4, alpha=0.4)
    ax.grid(which="major", lw=0.8, alpha=0.4)

    ax.yaxis.set_tick_params(which="both", length=0)
    ax.xaxis.set_tick_params(which="both", length=0)

    # Customize the start, end, and frequency of the horizontal grid lines
    y_start = 0.0
    y_end = 70000
    y_frequency = 10000
    y_ticks = np.arange(y_start, y_end + y_frequency, y_frequency)
    y_ticks = np.round(y_ticks).astype(int)
    # Set the y-ticks
    ax.set_yticks(y_ticks)
    # Apply the custom formatter to y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

    ax.spines["left"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.set_title(
        name, weight="bold", size=12, color=CHARCOAL, font=other_bold_font, fontsize=12
    )


# load data
data = pd.read_csv(
    "../data/processed/nz_migration_facet_data_202312.csv", parse_dates=["Month"]
)

NROW = 3
NCOL = 3
NAMES = ["New Zealand"] + list(
    data[(data["Month"] == "2023-12-01") & (data["Citizenship"] != "New Zealand")]
    .sort_values(by="net_sum", ascending=False)["Citizenship"]
    .unique()
)
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
    loc=(0.75, 0.81),  # This coord is bottom-left corner
    ncol=2,  # 1 row, 2 columns layout
    columnspacing=1,  # Space between columns
    handlelength=1.2,  # Line length
    frameon=False,  # No frame
    prop=other_font,
    fontsize=14,
)


# Create handles for the area fill with `patches.Patch()`
outflow = patches.Patch(facecolor=BLUE_LIGHT, alpha=0.3, label="Net outflow")
inflow = patches.Patch(facecolor=RED_LIGHT, alpha=0.3, label="Net inflow")

fig.legend(
    handles=[outflow, inflow],
    loc=(0.75, 0.78),  # This coord is top-right corner
    ncol=2,  # 1 row, 2 columns layout
    columnspacing=1,  # Space between columns
    handlelength=2,  # Area length
    handleheight=2,  # Area height
    frameon=False,  # No frame
    prop=other_font,
    fontsize=14,
)

# Title
fig.text(
    s="Which migrants are replacing the New Zealand citizens who leave?",
    x=0.05,
    y=1.025,
    color=CHARCOAL,
    fontsize=30,
    font=font,
    ha="left",
    va="top",
    fontweight="bold",
)

# subtitle
fig.text(
    s="Long-term migration in New Zealand by citizenship (12-month rolling sum, top 9 citizenships)",
    x=0.05,
    y=0.97,
    color=CHARCOAL,
    fontsize=17,
    font=other_bold_font,
    ha="left",
    va="top",
)

# Caption
fig.text(
    s="Source: Statistics NZ\nautonomousecon.substack.com",
    x=0.98,
    y=-0.05,
    color=CHARCOAL,
    fontsize=12,
    font=other_font,
    ha="right",
    va="baseline",
)

# Adjust layout and show the plot
plt.tight_layout()
plt.subplots_adjust(top=0.89, bottom=0.04)
plt.savefig("../reports/facet_migration", dpi=300, bbox_inches="tight")
plt.show()
