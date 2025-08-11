"""
Functions for creating and handling seismic model geometry.
Part of the seismic modeling project using ray tracing.
"""

import numpy as np

def create_source_position(x=0, z=0):
    """
    Create source position coordinates.
    
    Parameters:
    - x: float, x coordinate of the source (default 0)
    - z: float, z coordinate (depth) of the source (default 0)
    
    Returns:
    - tuple (x, z)
    """
    return (x, z)

def create_receiver_array(n_receivers, x_start, x_end, z=0):
    """
    Create receiver coordinates along the surface (z fixed).
    
    Parameters:
    - n_receivers: int, number of receivers
    - x_start: float, starting x position
    - x_end: float, ending x position
    - z: float, depth coordinate (default 0)
    
    Returns:
    - tuple of numpy arrays (x_positions, z_positions)
    """
    x_positions = np.linspace(x_start, x_end, n_receivers)
    z_positions = np.full_like(x_positions, z)
    return x_positions, z_positions

def plot_acquisition_geometry(source_pos, receiver_x, receiver_z, reflection_depth):
    """
    Plot the seismic acquisition geometry with source and receivers.
    
    Parameters:
    - source_pos: tuple (x, z) of source position
    - receiver_x: numpy array of x positions of receivers
    - receiver_z: numpy array of z positions of receivers
    - reflection_depth: float, depth of reflective interface
    
    Returns:
    - matplotlib figure and axes objects (fig, ax)
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(source_pos[0], source_pos[1], 'r*', label='Source')
    ax.plot(receiver_x, receiver_z, 'b^', label='Receivers')
    ax.axhline(y=reflection_depth, color='k', linestyle='--', label='Reflective Interface')
    ax.invert_yaxis()
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig, ax