import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the 2D circle outline
circle = np.load('circle_outline.npy')
white_coords = np.argwhere(circle == 1)

if white_coords.shape[0] < 3:
    raise ValueError("Not enough white pixels to choose three spaced origins!")

# Step 1: Choose three white pixels that are well-separated
min_dist = 40  # Minimum distance between origins

def euclidean(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# Pick the first white pixel
origin1 = white_coords[0]

# Pick second far from first
origin2 = next((pt for pt in white_coords if euclidean(pt, origin1) > min_dist), None)

# Pick third far from both first and second
origin3 = next(
    (pt for pt in white_coords 
     if euclidean(pt, origin1) > min_dist and euclidean(pt, origin2) > min_dist), 
    None
)

if origin2 is None or origin3 is None:
    raise ValueError("Could not find three well-separated white pixels.")

origins = [origin1, origin2, origin3]
colors = ['blue', 'red', 'green']
print(f"Using origins: {origins}")

# Step 2: Vote into the 3D cube
cube = np.zeros((100, 100, 100), dtype=int)
points_by_origin = [[] for _ in range(3)]

for i, (oy, ox) in enumerate(origins):
    for y in range(100):
        for x in range(100):
            d = int(round(np.sqrt((x - ox)**2 + (y - oy)**2)))
            if 0 <= d < 100:
                cube[y, x, d] += 1
                points_by_origin[i].append((x, y, d))

# Step 3: 3D Scatter Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for i, points in enumerate(points_by_origin):
    if points:
        x, y, z = zip(*points)
        ax.scatter(x, y, z, color=colors[i], s=2, label=f"Origin {i+1} ({colors[i]})")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Distance (Z)')
ax.set_title("3D Vote Cube from Spaced White Pixels")
ax.legend()
ax.view_init(elev=30, azim=30)

plt.show()
