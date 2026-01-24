import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Define the number of steps in the gradient
num_steps = 256
gradient_values = np.linspace(0, 1, num_steps)

# Create a figure and axes
fig, ax = plt.subplots(figsize=(8, 2))

# Use the 'gray' colormap with a linear normalization
# This maps the 0-1 data range uniformly from black to white.
cmap = plt.get_cmap('gray')
norm = Normalize(vmin=0, vmax=1)

# Reshape the gradient values for plotting (e.g., a horizontal bar)
# We need a 2D array: (1 row, num_steps columns)
gradient_bar = gradient_values.reshape(1, num_steps)

# Display the gradient using imshow
ax.imshow(gradient_bar, cmap=cmap, norm=norm, aspect='auto')

# Customize the plot to remove axes ticks and labels for a cleaner gradient view
ax.set_xticks([])
ax.set_yticks([])
plt.title("Visually Uniform Black to White Gradient")

# Display the plot
plt.show()
