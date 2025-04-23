import numpy as np
import plotly.graph_objects as go

# Load the 2D circle outline
circle = np.load('circle_outline.npy')
white_coords = np.argwhere(circle == 1)

print(f"Total white pixels used as origins: {len(white_coords)}")

# Initialize a 100x100x100 vote cube
cube = np.zeros((100, 100, 100), dtype=int)

# Accumulate votes from all white pixels
for origin_y, origin_x in white_coords:
    for y in range(100):
        for x in range(100):
            d = int(round(np.sqrt((x - origin_x)**2 + (y - origin_y)**2)))
            if 0 <= d < 100:
                cube[y, x, d] += 1

# Save cube
np.save('vote_cube.npy', cube)
print("Cube saved as vote_cube.npy")

# Normalize cube for opacity
cube_normalized = cube / np.max(cube)
threshold = 0.1

# Find hottest voxel
hot_index = np.unravel_index(np.argmax(cube), cube.shape)
hot_y, hot_x, hot_z = hot_index
hot_value = cube[hot_index]
print(f"Hottest point at coordinates: ({hot_x}, {hot_y}, {hot_z}) with {hot_value} votes")

# Prepare Plotly figure
fig = go.Figure()

# Volume rendering
fig.add_trace(go.Volume(
    x=np.repeat(np.arange(100), 100*100),
    y=np.tile(np.repeat(np.arange(100), 100), 100),
    z=np.tile(np.arange(100), 100*100),
    value=cube.flatten(),
    opacity=0.1,
    surface_count=25,
    isomin=int(np.max(cube) * threshold),
    isomax=np.max(cube),
    colorscale='Hot',
    caps=dict(x_show=False, y_show=False, z_show=False)
))

# Add a labeled marker for the hottest point (with coordinates)
fig.add_trace(go.Scatter3d(
    x=[hot_x], y=[hot_y], z=[hot_z],
    mode='markers+text',
    marker=dict(size=6, color='cyan'),
    text=[f"({hot_x}, {hot_y}, {hot_z})"],
    textposition="top center",
    name='Hottest Point'
))

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Distance (Z)',
    ),
    title='3D Vote Density with Coordinates of Hottest Point'
)

fig.show()
