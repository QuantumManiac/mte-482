import navigation
import matplotlib.pyplot as plt 

array = []
for x in range(len(navigation.GRID)):
    row = []
    for y in range(len(navigation.GRID[x])):
        row.append(navigation.GRID[x][y].barrier)
    array.append(row)

print(array)

# Calculate the number of rows and columns
num_rows = len(array)
num_cols = len(array[0]) if num_rows > 0 else 0

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Display the array with 'True' as black and 'False' as white
cmap = plt.cm.gray
ax.imshow(array, cmap=cmap, aspect='equal')

# Draw gridlines
ax.set_xticks([x - 0.5 for x in range(1, num_cols)], minor=True)
ax.set_yticks([y - 0.5 for y in range(1, num_rows)], minor=True)
ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
ax.tick_params(which="minor", size=0)

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Show plot
plt.savefig('grid.png')
plt.show()
