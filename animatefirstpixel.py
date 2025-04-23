import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Load the circle outline
circle = np.load('circle_outline.npy')

# Find the first white pixel
white_coords = np.argwhere(circle == 1)
first_white_y, first_white_x = white_coords[0]
print(f"First white pixel: ({first_white_y}, {first_white_x})")

# Initialize the vote cube
cube = np.zeros((100, 100, 100), dtype=int)

# Setup plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter([], [], [], c=[], cmap='hot', s=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 100)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Distance (Z)")
ax.set_title("Animated 3D Vote Accumulation")

# Storage for points
x_list, y_list, z_list, c_list = [], [], [], []

# Flatten loop counter over y and x
coords = [(y, x) for y in range(100) for x in range(100)]

def update(frame):
    y, x = coords[frame]
    distance = int(round(np.sqrt((x - first_white_x)**2 + (y - first_white_y)**2)))
    if 0 <= distance < 100:
        cube[y, x, distance] += 1
        x_list.append(x)
        y_list.append(y)
        z_list.append(distance)
        c_list.append(cube[y, x, distance])

        # Update scatter plot
        sc._offsets3d = (x_list, y_list, z_list)
        sc.set_array(np.array(c_list))

    return sc,

# Animate (adjust interval as needed)
ani = animation.FuncAnimation(fig, update, frames=len(coords), interval=1, blit=False)

plt.show()
