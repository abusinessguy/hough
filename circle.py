import numpy as np
import matplotlib.pyplot as plt

# Grid size
width, height = 100, 100

# Circle parameters
center_x, center_y = width // 2.5, height // 2.5
radius = 30

# Create the grid (start with all black)
grid = np.zeros((height, width))

# Compute distance from center
y_indices, x_indices = np.indices((height, width))
distance = np.sqrt((x_indices - center_x)**2 + (y_indices - center_y)**2)

# Mark the outline (only where rounded distance equals radius)
grid[np.round(distance) == radius] = 1

# Display the result
plt.imshow(grid, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.title("1-Pixel Circle Outline in 100x100 Grid")
plt.show()

np.save('circle_outline.npy', grid)
print("Circle grid saved to 'circle_outline.npy'")