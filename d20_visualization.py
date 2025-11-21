import numpy as np
import plotly.graph_objects as go

def create_icosahedron():
    """
    Create vertices and faces of a regular icosahedron (d20)
    """
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Vertices of icosahedron
    vertices = np.array([
        [0, 1, phi],
        [0, -1, phi],
        [0, 1, -phi],
        [0, -1, -phi],
        [1, phi, 0],
        [-1, phi, 0],
        [1, -phi, 0],
        [-1, -phi, 0],
        [phi, 0, 1],
        [-phi, 0, 1],
        [phi, 0, -1],
        [-phi, 0, -1]
    ])
    
    # Normalize vertices to unit sphere
    vertices = vertices / np.linalg.norm(vertices, axis=1)[:, np.newaxis]
    
    # Faces of icosahedron (20 triangular faces)
    faces = np.array([
        [0, 8, 4], [0, 5, 9], [0, 9, 8], [0, 4, 5],
        [1, 6, 8], [1, 9, 6], [1, 5, 9], [1, 4, 8],
        [2, 4, 10], [2, 11, 4], [2, 5, 11], [2, 10, 5],
        [3, 6, 10], [3, 10, 11], [3, 11, 7], [3, 7, 6],
        [8, 6, 10], [8, 10, 4], [9, 5, 11], [9, 11, 7], [9, 7, 6], [9, 6, 8]
    ])
    
    return vertices, faces

def visualize_d20():
    """
    Create and show the 3D d20 visualization
    """
    vertices, faces = create_icosahedron()
    
    # Extract coordinates
    x = vertices[:, 0]
    y = vertices[:, 1]
    z = vertices[:, 2]
    
    # Create 3D mesh
    fig = go.Figure(data=[
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color='lightblue',
            opacity=0.8,
            flatshading=True
        )
    ])
    
    # Update layout
    fig.update_layout(
        title='3D D20 (Icosahedron)',
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        width=800,
        height=800
    )
    
    return fig

# Create and show the visualization
fig = visualize_d20()
fig.show()