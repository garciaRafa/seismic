"""
Functions for creating and handling seismic model geometry.
Part of the seismic modeling project using ray tracing.
"""

import numpy as np
import matplotlib.pyplot as plt

def create_source_position(x=0, z=0):
    """
    Create source position coordinates.
    
    Parameters:
    - x: float, x coordinate of the source (default 0)
    - z: float, z coordinate (depth) of the source (default 0)
    
    Returns:
    - tuple (x, z)
    """
    if not isinstance(x, (int, float)) or not isinstance(z, (int, float)):
        raise ValueError("Source coordinates must be numeric values.")
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
    if n_receivers <=0:
        raise ValueError("Number of receivers must be positive.")
    if x_start >= x_end:
        raise ValueError("x_start must be less than x_end.")

    x_positions = np.linspace(x_start, x_end, n_receivers)
    z_positions = np.full_like(x_positions, z)
    return x_positions, z_positions

def plot_acquisition_geometry(sources, receiver_x, receiver_z, reflection_depth, show_rays=False, save_path=None):
    """
    Plot the seismic acquisition geometry with source(s) and receivers, and optionally rays.
    
    Parameters:
    - sources: tuple (x, z) or list of tuples for multiple sources
    - receiver_x: numpy array of x positions of receivers
    - receiver_z: numpy array of z positions of receivers
    - reflection_depth: float, depth of reflective interface
    - show_rays: bool, whether to draw rays from source to receivers via reflection
    - save_path: str, optional path to save the figure
    Returns:
    - matplotlib figure and axes objects (fig, ax)
    """
    
    if isinstance(sources, tuple):
        sources = [sources]
    elif not all(isinstance(s, tuple) and len(s) == 2 for s in sources):
        raise ValueError("Sources must be a tuple(x, z) or a list of such tuples")

    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Plot sources
    for src in sources:
        ax.plot(src[0], src[1], 'r*', markersize=12, label='Source' if src == sources[0] else "")
    
    # Plot receivers
    ax.plot(receiver_x, receiver_z, 'b^', label='Receivers')

    # Reflective INterface
    ax.axhline(y=reflection_depth, color='k', linestyle='--', label='Reflective Interface')

    # Rays
    if show_rays:
        for src in sources:
            for rx, rz in zip(receiver_x, receiver_z):
 
                # Calculate reflection point (midpoint between source and receiver at reflection depth)
                reflection_x = (src[0] + rx) / 2

                # Ray going down (orange) - source to reflection point
                ax.plot([src[0], reflection_x], [src[1], reflection_depth], 'orange', alpha=0.5)
                # Ray coming back (green) - reflection point to receiver
                ax.plot([reflection_x, rx], [reflection_depth, rz], 'green', alpha=0.5)
    
    ax.invert_yaxis()
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Depth (m)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300)

    return fig, ax
