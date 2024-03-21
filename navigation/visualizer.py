
import matplotlib.pyplot as plt 
import navigation
import numpy as np

# Calculate the number of rows and columns
x_bound = len(navigation.grid)
y_bound = len(navigation.grid[0]) if x_bound > 0 else 0



# Take the grid and convert it into a 2D array of booleans which indicate whether a cell has a barrier
grid = [[navigation.grid[row][col].is_barrier() for col in range(y_bound)] for row in range(x_bound)]

# Transpose the grid so that the first index corresponds to the x-coordinate and the second index corresponds to the y-coordinate
grid = np.transpose(grid)

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Display the array with 'True' as black and 'False' as white
cmap = plt.cm.gray
ax.imshow(grid, cmap=cmap, aspect='equal')

# Draw gridlines
ax.set_xticks([x - 0.5 for x in range(1, x_bound)], minor=True)
ax.set_yticks([y - 0.5 for y in range(1, y_bound)], minor=True)
ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
ax.tick_params(which="minor", size=0)

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Show plot
plt.savefig('grid.png')
plt.show()
