import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the circle outline
circle = np.load('circle_outline.npy')

# Get the first three white pixels
white_coords = np.argwhere(circle == 1)
if white_coords.shape[0] < 3:
    raise ValueError("Not enough white pixels found to select three origins!")

origins = white_coords[:3]  # (y, x) for first three white pixels
colors = ['blue', 'red', 'green']  # Colors for each origin

# Initialize a 100x100x100 cube (optional if you want to accumulate votes)
cube = np.zeros((100, 100, 100), dtype=int)

# To store color-coded point sets for each origin
points_by_origin = [[] for _ in range(3)]  # List of lists: (x, y, z)

# Vote logic for each origin
for i, (origin_y, origin_x) in enumerate(origins):
    for y in range(100):
        for x in range(100):
            distance = int(round(np.sqrt((x - origin_x)**2 + (y - origin_y)**2)))
            if 0 <= distance < 100:
                cube[y, x, distance] += 1
                points_by_origin[i].append((x, y, distance))

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for i, point_set in enumerate(points_by_origin):
    if point_set:  # If there are any points
        x, y, z = zip(*point_set)
        ax.scatter(x, y, z, color=colors[i], s=2, label=f"Origin {i+1} ({colors[i]})")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Distance (Z)')
ax.set_title("3D Cube: Votes from First Three White Pixels")
ax.legend()
ax.view_init(elev=30, azim=30)

plt.show()
