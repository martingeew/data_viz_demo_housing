import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from highlight_text import fig_text, ax_text
from pyfonts import load_font
from matplotlib.animation import FuncAnimation

# parameters
background_color = '#282a36'
text_color = 'white'
line_color_1 = "#B6E880"
line_color_2="#636EFA"
dpi = 300

# Load the fonts
font = load_font(
    "https://github.com/dharmatype/Bebas-Neue/blob/master/fonts/BebasNeue(2018)ByDhamraType/ttf/BebasNeue-Regular.ttf?raw=true"
)
other_font = load_font(
    "https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Light.ttf?raw=true"
)
other_bold_font = load_font(
    "https://github.com/bBoxType/FiraSans/blob/master/Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Normal/Roman/FiraSans-Medium.ttf?raw=true"
)

# Load plot data
plot_data = pd.read_csv("../data/processed/homeownership_state_processed_full_20241124.csv")

df=plot_data[plot_data["state"].isin(['NY','CA'])]
df = df.pivot(index='year', columns='state', values='home_ownership').reset_index()
df.columns.name = None
df.rename(columns={'CA': 'home_ownership_ca', 'NY': 'home_ownership_ny'}, inplace=True)
df.set_index('year', inplace=True)

# Setting up the plot
fig, ax = plt.subplots(figsize=(10, 6), dpi=dpi)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)
ax.tick_params(axis='y', colors=text_color)
ax.spines[['left']].set_color(text_color)

# Update function for the animation
def update(frame):

    # skip first frame
    if frame == 0:
        return None

    # initialize subset of data
    subset_df = df.iloc[:frame]
    ax.clear()

    # create the line chart
    ax.plot(subset_df.index, subset_df['home_ownership_ca'], color=line_color_1)
    ax.scatter(subset_df.index[-1], subset_df['home_ownership_ca'].values[-1], color=line_color_1, s=100)
    
    # create the line chart
    ax.plot(subset_df.index, subset_df['home_ownership_ny'], color=line_color_2)
    ax.scatter(subset_df.index[-1], subset_df['home_ownership_ny'].values[-1], color=line_color_2, s=100)
    
    # custom axes
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    y_max = max(subset_df['home_ownership_ca'].max(), subset_df['home_ownership_ny'].max())
    y_min=50
    ax.set_ylim(y_min, y_max*1.05)
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set_xlim(1980, 2023)
    ax.set_xticks([])
    
    # create annotation
    # create annotation next to the last point
    ax.text(
        x=subset_df.index[-1] + 0.5,  # Slightly offset the x position to avoid overlap
        y=subset_df['home_ownership_ca'].values[-1],
        s="CA",
        fontsize=14,
        verticalalignment='center',
        horizontalalignment='left',
        color=line_color_1
    )
    
    # create annotation next to the last point
    ax.text(
        x=subset_df.index[-1] + 0.5,  # Slightly offset the x position to avoid overlap
        y=subset_df['home_ownership_ny'].values[-1],
        s="NY",
        fontsize=14,
        verticalalignment='center',
        horizontalalignment='left',
        color=line_color_2
    )

    # date in the background
    year = df.index[frame]
    fig_text(
        0.15, 0.87,
        '1984 - ' + str(round(year)),
        ha='left', va='top',
        fontsize=30,
        font=font,
        color=text_color,
        fontweight='bold',
        alpha=0.5,
        fig=fig
    )
    
    # Title
    fig.text(
        s="Home Ownership Rate (%): California vs New York",
        x=0.13,
        y=0.95,
        color=text_color,
        fontsize=20,
        font=font,
        ha="left",
        va="top",
        fontweight="bold"
    )

    # credit annotation
    fig.text(
        s="Source: U.S. Census Bureau\nautonomousecon.substack.com",
        x=0.98,
        y=0.02,
        color=text_color,
        fontsize=12,
        font=other_font,
        ha="right",
        va="baseline",
    )

# create and save animation
ani = FuncAnimation(fig, update, frames=len(df))
ani.save('../reports/us_line_home_ownership.gif', fps=5)
plt.show()
