#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# User-defined settings
# ----------------------------
xvg_file = "data.xvg"

x_label = "Helix tilt (°)"
y_label = "Normalized fraction"
n_frames = 10000  # Number of simulation frames
n_bins = 50
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
column_labels = None  # e.g. ["WT", "Mutant_1", "Mutant_2"]

# ----------------------------
# Helper: read XVG file
# ----------------------------
def load_xvg(filename):
    rows = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("#", "@", "&")):
                continue
            rows.append([float(v) for v in line.split()])
    return np.array(rows)

def main():
    data = load_xvg(xvg_file)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError("Expected at least 2 columns: 1 X column + 1+ Y columns.")

    y_data = data[:, 1:]
    n_ycols = y_data.shape[1]

    if column_labels is None:
        labels = [f"Y{i+1}" for i in range(n_ycols)]
    else:
        if len(column_labels) != n_ycols:
            raise ValueError("column_labels must have the same length as the number of Y columns.")
        labels = column_labels

    # Common binning
    all_y = y_data.ravel()
    hist_range = (np.min(all_y), np.max(all_y))
    bin_edges = np.linspace(hist_range[0], hist_range[1], n_bins + 1)

    # Convert bins to centers for line plotting
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    fig, ax = plt.subplots(figsize=(8, 5))
    for i in range(n_ycols):
        y = y_data[:, i]
        color = colors[i % len(colors)]

        counts, _ = np.histogram(y, bins=bin_edges)
        norm_counts = counts / n_frames

        # Plot iteratively
        ax.plot(bin_centers, norm_counts, color=color, linewidth=1.5, label=labels[i])
        ax.fill_between(bin_centers, norm_counts, alpha=0.2, color=color)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(frameon=False)
    ax.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
