import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load full file as numbers
data = np.loadtxt("densmap.dat")

# Extract labels and values
x_labels = data[0, 1:]      # first row, skip first column
y_labels = data[1:, 0]      # first column, skip first row
values   = data[1:, 1:]     # matrix of floats

# Define colormap: white → orange
cmap = LinearSegmentedColormap.from_list("white_orange", ["white", "orange"])

# Plot with pcolormesh (better for labeled axes)
plt.pcolormesh(x_labels, y_labels, values, cmap=cmap, shading="auto")

plt.colorbar(label="Density")
plt.xlabel("X (nm)")
plt.ylabel("Y (nm)")
#plt.title("gmx densmap heatmap")
plt.tight_layout()
plt.show()
