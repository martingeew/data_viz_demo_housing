import matplotlib.pyplot as plt

# List of color hash codes
hash_codes = ['#2166ACFF', '#4393C3FF', '#92C5DEFF', '#D1E5F0FF', '#F7F7F7FF', '#FDDBC7FF', '#F4A582FF', '#D6604DFF', '#B2182BFF']

hash_codes = [ '#F4A582FF', '#FDDBC7FF','#F7F7F7FF', '#D1E5F0FF',  '#92C5DEFF']

hash_codes = ['#4393C3FF', '#92C5DEFF','#FDDBC7FF',  '#F4A582FF', '#D6604DFF']

# Create a figure to display the colors
fig, ax = plt.subplots(figsize=(8, 2))

# Iterate over the hash codes to display each color as a horizontal bar
for i, color in enumerate(hash_codes):
    ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    ax.text(i + 0.5, -0.3, color, ha='center', va='center', fontsize=10)

# Set the x and y limits
ax.set_xlim(0, len(hash_codes))
ax.set_ylim(-1, 1)

# Remove axes
ax.axis('off')

# Show the figure
plt.show()