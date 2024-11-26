import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from drawarrow import fig_arrow
from highlight_text import fig_text, ax_text
from pyfonts import load_font


# Function to annotate states
def annotate_states(geo_df, ax, value_col, color_text, other_font, other_bold_font):
    """
    Annotates states on a geographic plot with their respective values.

    Parameters:
    - geo_df: GeoDataFrame containing geographic data, including centroids and state codes.
    - ax: Matplotlib axis on which the annotations will be plotted.
    - value_col: Column name containing the values to be displayed for each state.

    The function adds state annotations with custom positioning and color based on the value.
    """
    states_to_annotate = list(geo_df["STUSPS"].unique())

    for state in states_to_annotate:
        # Get the centroid coordinates and rate for each state
        centroid = geo_df.loc[geo_df["STUSPS"] == state, "centroid"].values[0]
        x, y = centroid.coords[0]
        rate = geo_df.loc[geo_df["STUSPS"] == state, value_col].values[0]
        # Make small adjustments to annotation locations
        try:
            x += adjustments[state][0]
            y += adjustments[state][1]
        except KeyError:
            pass

        # Determine text color based on rate value
        color_text = (
            "white" if rate <= 35 or rate >= 75 else text_color
        )  # e.g., 'black'

        # Set annotation text format based on state condition
        if state in ["NC", "VA", "TN", "KY", "NY", "HI"]:
            text = f"<{state.upper()}>: {rate:.1f}"
        else:
            text = f"<{state.upper()}>\n{rate:.1f}"

        # Add the annotation
        ax_text(
            x=x,
            y=y,
            s=text,
            fontsize=8.5,
            ha="center",
            va="center",
            font=other_font,
            color=color_text,
            ax=ax,
            highlight_textprops=[{"font": other_bold_font}],
        )


def annotate_state_with_arrows(
    data,
    ax,
    state_code,
    column_name,
    tail_position,
    head_position,
    radius,
    text_color,
    other_font,
):
    """
    Annotates a state on a plot with an arrow and text label.

    Parameters:
    - data: DataFrame containing the data for states.
    - fig: Plotly or matplotlib figure object.
    - state_code: str, the two-letter code for the state to annotate (e.g., 'NJ').
    - column_name: str, the column in the data containing the value to plot.
    - tail_position: tuple, (x, y) starting position of the arrow.
    - head_position: tuple, (x, y) end position of the arrow head.
    """
    # Define arrow properties
    arrow_props = dict(
        width=0.5, head_width=2, head_length=4, color="#666666", fill_head=False
    )

    # Draw the arrow
    fig_arrow(
        tail_position=tail_position,
        head_position=head_position,
        radius=radius,
        **arrow_props,
    )

    # Get the centroid coordinates and rate for each state
    centroid = data.loc[data["STUSPS"] == state_code, "centroid"].values[0]
    x, y = centroid.coords[0]
    state_value = data.loc[data["STUSPS"] == state_code, column_name].values[0]
    # Make small adjustments to annotation locations
    try:
        x += adjustments[state_code][0]
        y += adjustments[state_code][1]
    except KeyError:
        pass

    # Add the text annotation
    ax_text(
        s=f"<{state_code}>: {state_value:.1f}",
        x=x,
        y=y,
        highlight_textprops=[{"font": other_bold_font}],
        color=text_color,
        fontsize=9,
        font=other_font,
        ha="center",
        va="center",
        ax=ax,
    )


def plot_with_legend(data, ax, xlim, ylim):
    """
    Plots the data on the provided axis with optional legend.

    Parameters:
    - data: GeoDataFrame to plot.
    - ax: Matplotlib axis to plot on.
    - xlim: Tuple for x-axis limits.
    - ylim: Tuple for y-axis limits.
    """
    # Plot data with custom color mapping
    data.plot(
        ax=ax,
        column="binned",
        color=data["binned"].map(color_mapping),
        edgecolor="white",
        linewidth=0.5,
        legend=False,  # Disable automatic legend
    )
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


# Load the fonts
text_color = "#333333" # charcoal

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

# Offsets for individual state annotations
adjustments = {
    "HI": (+0.5, +1.5),
    "AK": (0, +0.5),
    "SC": (+0.3, -0.28),
    "LA": (-0.5, 0),
    "VA": (0, -0.5),
    "MI": (+0.5, 0),
    "FL": (+0.75, 0),
    "WV": (-0.13, -0.2),
    "KY": (0, -0.2),
    "NJ": (+7.5, -3.7),
    "DE": (+6.5, -4.9),
    "MD": (+2, -6.5),
    "VT": (-5.4, +1.6),
    "NH": (-0.8, +4),
    "MA": (+5, +1),
    "CT": (+6.6, -2.5),
    "RI": (+5.75, -1),
    "DC": (+4.3, -2.6),
}

# Define custom colors for each bin
labels = ["35-45%", "45-55%", "55-65%", "65-75%", "75%+"]
colors = ["#D6604DFF", "#F4A582FF", "#FDDBC7FF", "#92C5DEFF", "#4393C3FF"]
color_mapping = dict(zip(labels, colors))

# List of state codes to annotate
state_codes_arrows = ["MA", "RI", "CT", "NJ", "DE", "MD", "VT", "NH", "DC"]

# Define arrow parameters for each state
arrow_parameters = {
    "MA": {
        "tail_position": (0.853, 0.65),
        "head_position": (0.815, 0.63),
        "radius": 0.2,
    },
    "RI": {
        "tail_position": (0.863, 0.6),
        "head_position": (0.815, 0.62),
        "radius": -0.18,
    },
    "NJ": {
        "tail_position": (0.86, 0.525),
        "head_position": (0.775, 0.58),
        "radius": 0.3,
    },
    "CT": {"tail_position": (0.86, 0.57), "head_position": (0.8, 0.62), "radius": -0.2},
    "DE": {
        "tail_position": (0.843, 0.48),
        "head_position": (0.7675, 0.565),
        "radius": 0.5,
    },
    "MD": {
        "tail_position": (0.77, 0.45),
        "head_position": (0.76, 0.56),
        "radius": 0.23,
    },
    "VT": {
        "tail_position": (0.76, 0.70),
        "head_position": (0.803, 0.67),
        "radius": -0.2,
    },
    "NH": {
        "tail_position": (0.8, 0.73),
        "head_position": (0.815, 0.65),
        "radius": -0.25,
    },
    "DC": {
        "tail_position": (0.8, 0.525),
        "head_position": (0.75, 0.565),
        "radius": 0.25,
    },
}

# Load employment data
plot_data = pd.read_csv("../data/processed/homeownership_state_processed_20241124.csv")
plot_data = plot_data[plot_data["year"] == 2023]

# Read the shapefile
shapefile_path = "../data/raw/us_map_data/tl_2023_us_state.shp"
gdf = gpd.read_file(shapefile_path)

# Project the data to EPSG:5070 and calculate centroids.
# A projection is a way to represent the 3D surface of the Earth on a 2D map.
# A centroid is the geometric center or “average” point of a shape.
data_projected = gdf.to_crs(epsg=5070)
data_projected["centroid"] = data_projected.geometry.centroid

# Project centroids back to original CRS
gdf["centroid"] = data_projected["centroid"].to_crs(gdf.crs)

# Merge data
data = gdf.merge(plot_data, how="inner", left_on="STUSPS", right_on="state")
print(len(data), len(plot_data), len(gdf))

# Get the set of states from both DataFrames
states_in_df1 = set(gdf["STUSPS"])
states_in_df2 = set(plot_data["state"])

# Print states in df1 but not in df2
states_not_in_intersect = states_in_df1.symmetric_difference(states_in_df2)
print(states_not_in_intersect)

# Choropleth

# Define column for plotting
column_to_plot = "home_ownership"

# Add a binned column based on specified ranges
data["binned"] = pd.cut(
    data["home_ownership"],
    bins=[35, 45, 55, 65, 75, float("inf")],
    labels=["35-45%", "45-55%", "55-65%", "65-75%", "75%+"],
)


# Separate Alaska, Hawaii, and the contiguous U.S.
alaska = data[data["NAME"] == "Alaska"]
hawaii = data[data["NAME"] == "Hawaii"]
contiguous_us = data[(data["NAME"] != "Alaska") & (data["NAME"] != "Hawaii")]

# Set up a 2x2 grid layout with custom size ratios
new_width = 20 * 0.5
new_height = 15 * 0.5
fig, ax = plt.subplots(
    2,
    2,
    figsize=(new_width, new_height),
    dpi=300,
    gridspec_kw={"height_ratios": [4, 1], "width_ratios": [1, 1]},
)

# Plot contiguous U.S. on the main subplot (spanning both columns in the first row)
ax_main = plt.subplot2grid((2, 2), (0, 0), colspan=2, fig=fig)
plot_with_legend(contiguous_us, ax_main, xlim=(-130, -65), ylim=(24, 55))

# Alaska plot in the second row, first column
ax_alaska = plt.subplot2grid((2, 2), (1, 0), fig=fig)
plot_with_legend(alaska, ax_alaska, xlim=(-200, -100), ylim=(50, 73))

# Hawaii plot in the second row, second column
ax_hawaii = plt.subplot2grid((2, 2), (1, 1), fig=fig)
plot_with_legend(hawaii, ax_hawaii, xlim=(-162, -152), ylim=(18, 24))

# Loop through state codes and annotate each one
for state_code in state_codes_arrows:
    params = arrow_parameters.get(state_code, {})
    annotate_state_with_arrows(
        data,
        ax=ax_main,
        state_code=state_code,
        column_name=column_to_plot,
        tail_position=params.get("tail_position"),
        head_position=params.get("head_position"),
        radius=params.get("radius"),
        text_color=text_color,
        other_font=other_font,
    )

# Annotate the states
annotate_states(
    contiguous_us[~contiguous_us["STUSPS"].isin(state_codes_arrows)],
    ax_main,
    value_col=column_to_plot,
    color_text=text_color,
    other_font=other_font,
    other_bold_font=other_bold_font,
)
annotate_states(
    alaska,
    ax_alaska,
    value_col=column_to_plot,
    color_text=text_color,
    other_font=other_font,
    other_bold_font=other_bold_font,
)
annotate_states(
    hawaii,
    ax_hawaii,
    value_col=column_to_plot,
    color_text=text_color,
    other_font=other_font,
    other_bold_font=other_bold_font,
)

for ax in fig.axes:
    ax.set_axis_off()

legend_handles = [
    mpatches.Patch(color=color, label=label) for label, color in color_mapping.items()
]

fig.legend(
    handles=legend_handles,
    loc="lower center",
    bbox_to_anchor=(
        0.5,
        0.79,
    ),  # Position the legend at the bottom center of the figure
    ncol=len(color_mapping),  # Arrange items in a single row
    frameon=False,
    prop=other_font
)

# title
fig_text(
    s="Home Ownership Rate by State: 2023",
    x=0.18,
    y=0.9,
    color=text_color,
    fontsize=24,
    font=font,
    ha="left",
    va="top",
    ax=ax,
)

# caption
fig_text(
    s="Source: U.S. Census Bureau",
    x=0.93,
    y=0.035,
    color=text_color,
    fontsize=8,
    font=other_font,
    ha="right",
    va="top",
    ax=ax,
)

# caption
fig_text(
    s="autonomousecon.substack.com",
    x=0.93,
    y=0.055,
    color=text_color,
    fontsize=8,
    font=other_font,
    ha="right",
    va="top",
    ax=ax,
)

# Adjust plot layout
plt.subplots_adjust(hspace=0.04)
plt.savefig("../reports/home_ownership_map_2023", dpi=300, bbox_inches="tight")
plt.show()
