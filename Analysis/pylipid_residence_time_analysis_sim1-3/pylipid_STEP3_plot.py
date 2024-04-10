# TEMPLATE PLOTTING SCRIPT
# creating two subplots representing residence times of two lipids

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_inline.backend_inline import set_matplotlib_formats
set_matplotlib_formats('svg')

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(8, 4), layout='tight', sharex=True, sharey=True)


# ----- DATASET 1 -----
# Step 1: Read the data from the file
os.chdir('FULL_PATH')
data = np.loadtxt("file.xvg")

# Step 2: Extract the values from the second, third, and fourth columns
x_ax = data[:, 0]
col2 = data[:, 1]
col3 = data[:, 2]
col4 = data[:, 3]

# Step 3: Calculate the average and standard deviation for each row
average1 = np.mean(np.column_stack((col2, col3, col4)), axis=1)
std_dev1 = np.std(np.column_stack((col2, col3, col4)), axis=1)

# Step 4: Plot avg & std_dev
ax0.plot(x_ax, average1, color='magenta')
ax0.fill_between(x_ax, 
                 average1-std_dev1,
                 average1+std_dev1,
                 color='magenta',
                 alpha=0.15)
ax0.grid(color='gray', linewidth=0.7, alpha=0.5)


# ----- DATASET 2 -----

os.chdir('FULL_PATH')
data = np.loadtxt("file.xvg")

x_ax = data[:, 0]
col2 = data[:, 1]
col3 = data[:, 2]
col4 = data[:, 3]

average2 = np.mean(np.column_stack((col2, col3, col4)), axis=1)
std_dev2 = np.std(np.column_stack((col2, col3, col4)), axis=1)

ax1.plot(x_ax, average2, color='dodgerblue')
ax1.fill_between(x_ax, 
                 average2-std_dev2,
                 average2+std_dev2,
                 color='dodgerblue',
                 alpha=0.15)
ax1.grid(color='gray', linewidth=0.5, alpha=0.5)


# ----- GLOBAL SETTINGS -----

fig.supylabel('Residence time (µs)', fontsize=12)
plt.xlabel('Residue number', fontsize=12)
plt.show()



