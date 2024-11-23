import pandas as pd

import matplotlib.pyplot as plt


### Facet plot

### Main plot
#Todo:
# Add all countries
# Gridlines - add and colour (use ramen plot)
# Splines
# have axes on bnoth sides
# Make axes value in k
# Fonts - choose a font and stick to it for the future (casual modern minimalist)
# Colour pallete
# axis labels and ticks with a font and colour sames as grid lines
# have same axes y values
# Annotations
# try different countries or update NZ data

# load data
data = pd.read_csv("../data/processed/nz_migration_facet_data_202312.csv")

BLUE = "#3D85F7"
BLUE_LIGHT = "#5490FF"
PINK = "#C32E5A"
PINK_LIGHT = "#D34068"
GREY40 = "#666666"
GREY25 = "#404040"
GREY20 = "#333333"
# BACKGROUND = "#F5F4EF"
CHARCOAL = "#333333"

font = "Consolas"  # techy feel
arrivals_colour_1=PINK
arrivals_colour_2=PINK_LIGHT
departures_colour_1=BLUE
arrivals_colour_2=BLUE_LIGHT

tick_colour=GREY40
text_colour=CHARCOAL

def single_plot(x, y1, y2, name, ax):
    
    ax.plot(x, y1, color=BLUE)
    ax.plot(x, y2, color=PINK)

    ax.fill_between(
        x, y1, y2, where=(y1 > y2), 
        interpolate=True, color=BLUE_LIGHT, alpha=0.3
    )

    ax.fill_between(
        x, y1, y2, where=(y1 <= y2),
        interpolate=True, color=PINK_LIGHT, alpha=0.3
    );

    # xticks = [2010, 2015, 2020]
    # ax.set_xticks(xticks)
    # ax.set_xticks([2012.5, 2017.5], minor=True)
    # added a 'size' argument
    # ax.set_xticklabels(xticks, color=GREY40, size=10)
    
    ax.tick_params(axis="x", colors=GREY40)

    # yticks = [0, 10, 20]
    # ax.set_yticks(yticks)
    # ax.set_yticks([5, 15, 25], minor=True)
    # added a 'size' argument
    # ax.set_yticklabels(yticks, color=GREY40, size=10)
    # ax.set_ylim((-1, 26))
    
    ax.tick_params(axis="y", colors=GREY40)

    ax.grid(which="minor", lw=0.4, alpha=0.4)
    ax.grid(which="major", lw=0.8, alpha=0.4)
    
    # ax.yaxis.set_tick_params(which="both", length=0)
    # ax.xaxis.set_tick_params(which="both", length=0)
    
    ax.spines["left"].set_color("none")
    ax.spines["bottom"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    # added a 'size' argument
    ax.set_title(name, weight="bold", size=9, color=CHARCOAL)
    
df_plot=data[['Month','Citizenship','arrivals_sum','departures_sum']]

NROW = 3
NCOL = 3
NAMES=list(df_plot['Citizenship'].unique())
 
# Create the figure and axes for subplots
fig, axes = plt.subplots(NROW, NCOL, figsize=(12, 10), sharex=True, sharey=True)

# Flatten axes for easy iteration
axes_flat = axes.flatten()

for i, name in enumerate(NAMES):
    # Select data for the citizenship in 'name'
    df_subset = df[df["Citizenship"] == name]
    
    # Take the corresponding axis
    ax = axes_flat[i]
    
    # Take values for x, y1, and y2
    MONTH = df_subset["Month"].values
    ARRIVALS = df_subset["arrivals_sum"].values
    DEPARTURES = df_subset["departures_sum"].values
    
    # Plot it using the single_plot function
    single_plot(MONTH, ARRIVALS, DEPARTURES, name, ax)
    
# Remove any unused subplots
for j in range(len(NAMES), len(axes_flat)):
    fig.delaxes(axes_flat[j])

# Adjust layout and show the plot
plt.tight_layout()
plt.subplots_adjust(top=0.9)
fig.suptitle('Arrivals vs Departures for Different Countries')
plt.show()

