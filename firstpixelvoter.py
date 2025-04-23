import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the 2D circle outline
circle = np.load('circle_outline.npy')

# Find the first white pixel
white_coords = np.argwhere(circle == 1)
if white_coords.size == 0:
    raise ValueError("No white pixels found in the input image!")

first_white_y, first_white_x = white_coords[0]
print(f"First white pixel found at: ({first_white_y}, {first_white_x})")

# Initialize 100x100x100 cube
cube = np.zeros((100, 100, 100), dtype=int)

# Vote logic
for y in range(100):
    for x in range(100):
        distance = int(round(np.sqrt((x - first_white_x)**2 + (y - first_white_y)**2)))
        if 0 <= distance < 100:
            cube[y, x, distance] += 1

# Get voxel coordinates where votes occurred
y_coords, x_coords, z_coords = np.nonzero(cube)

# Plot just the plane structure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_coords, y_coords, z_coords, color='blue', s=2)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Distance (Z)')
ax.set_title('Plane Formed by Distance from First White Pixel')
ax.view_init(elev=30, azim=30)  # Optional: nice default view

plt.show()
