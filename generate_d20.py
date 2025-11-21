# generate_d20.py
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Golden ratio
phi = (1 + np.sqrt(5)) / 2

# Canonical icosahedron vertices (12 total)
vertices = np.array([
    [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
    [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
    [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
])

# Normalize to unit sphere
vertices = vertices / np.linalg.norm(vertices[0])

# Rotate so that top vertex is at (0,0,1)
# Align [0, 1, phi] to z-axis
v = np.array([0, 1, phi])
v = v / np.linalg.norm(v)
z_axis = np.array([0, 0, 1])
if not np.allclose(v, z_axis):
    axis = np.cross(v, z_axis)
    axis_norm = np.linalg.norm(axis)
    if axis_norm > 1e-6:
        axis = axis / axis_norm
        angle = np.arccos(np.clip(np.dot(v, z_axis), -1.0, 1.0))
        K = np.array([[0, -axis[2], axis[1]],
                      [axis[2], 0, -axis[0]],
                      [-axis[1], axis[0], 0]])
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        vertices = vertices @ R.T

# Sort by z-coordinate (descending)
z = vertices[:, 2]
order = np.argsort(-z)
apex_idx = order[0]
base_indices = order[1:11]  # 10 vertices

# Order base vertices by angle around z-axis
base_pts = vertices[base_indices]
angles = np.arctan2(base_pts[:, 1], base_pts[:, 0])
base_indices = base_indices[np.argsort(angles)]

# Build faces: [apex, base[i], base[i+1]]
faces = []
for i in range(10):
    faces.append([apex_idx, base_indices[i], base_indices[(i + 1) % 10]])
faces = np.array(faces)

# Extract coordinates
x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]

# Create mesh
mesh = go.Mesh3d(
    x=x, y=y, z=z,
    i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
    color='steelblue',
    opacity=0.9,
    flatshading=True
)

# Add edge lines for clarity (optional)
edge_traces = []
for face in faces:
    tri = vertices[face]
    # Close the triangle
    tri_loop = np.vstack([tri, tri[0]])
    edge_traces.append(go.Scatter3d(
        x=tri_loop[:, 0], y=tri_loop[:, 1], z=tri_loop[:, 2],
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False
    ))

# Final figure
fig = go.Figure(data=[mesh] + edge_traces)
fig.update_layout(
    title="Half of a D20 Die (Icosahedron) with Decagonal Base",
    scene=dict(
        xaxis_visible=False,
        yaxis_visible=False,
        zaxis_visible=False,
        aspectmode='data',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    paper_bgcolor='white'
)

# Export to standalone HTML
pio.write_html(fig, file="index.html", auto_open=False, include_plotlyjs='cdn')
print("✅ index.html generated! Open it in your browser.")