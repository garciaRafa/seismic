"""
Functions to compute ray paths and travel times for hyperbolic analysis.
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_travel_times_horizontal(source_x, receiver_x, depth_at_source, velocity):
    """
    Calculate travel times for reflection from a horizontal interface.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: receiver x coordinates array
    - depth_at_source: depth of reflector below source
    - velocity: wave velocity in m/s
    
    Returns:
    - numpy array of travel times
    """
    dx = receiver_x - source_x
    h = depth_at_source
    v = velocity
    
    # Travel time formula for horizontal reflector
    travel_times = np.sqrt(4 * h**2 + dx**2) / v
    
    return travel_times

def calculate_travel_times_dipping(source_x, receiver_x, depth_at_source, velocity, dip_angle):
    """
    Calculate travel times for reflection from a dipping interface.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: receiver x coordinates array
    - depth_at_source: depth of reflector below source
    - velocity: wave velocity in m/s
    - dip_angle: dip angle of reflector in degrees
    
    Returns:
    - numpy array of travel times
    """
    dx = receiver_x - source_x
    h = depth_at_source
    v = velocity
    theta = np.radians(dip_angle)
    
    # Travel time formula for dipping reflector
    travel_times = np.sqrt(4 * h**2 + dx**2 + 4 * h * dx * np.sin(theta)) / v
    
    return travel_times

def calculate_travel_times_depth_velocity_tradeoff(source_x, receiver_x, depth_velocity_pairs):
    """
    Generate travel times for multiple (depth, velocity) pairs.
    Demonstrates the trade-off: deeper + faster vs shallower + slower.
    
    Returns:
    - dictionary with (depth, velocity) as key and travel times as value
    """
    results = {}
    for depth, velocity in depth_velocity_pairs:
        times = calculate_travel_times_horizontal(source_x, receiver_x, depth, velocity)
        results[(depth, velocity)] = times
    return results

"""
def calculate_travel_times_two_layers(source_x, receiver_x, depth1, depth2, v1, v2):
    
    # Reflection from two horizontal reflectors (layered model).
    # Useful to simulate thin-bed ambiguity vs single deeper reflector.
    
    # Returns:
    # - t1: travel times for first reflector
    # - t2: travel times for second reflector
    
    dx = receiver_x - source_x
    t1 = np.sqrt(4 * depth1**2 + dx**2) / v1
    t2 = np.sqrt(4 * depth2**2 + dx**2) / v2
    return t1, t2
"""

def calculate_travel_times_source_shifted(source_x, receiver_x, depth_at_source, velocity, dip_angle, source_shift):
    """
    Reflection from dipping reflector with shifted source position.
    Shifting the source can mimic a different dip/geometry.
    
    Parameters:
    - source_shift: horizontal displacement of the source
    """
    shifted_source = source_x + source_shift
    return calculate_travel_times_dipping(shifted_source, receiver_x, depth_at_source, velocity, dip_angle)

def generate_hyperbola_curves(source_x, receiver_x, depth_at_source, velocity, dip_angles):
    """
    Generate hyperbola curves for multiple dip angles.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: array of receiver x coordinates
    - depth_at_source: depth of reflector
    - velocity: wave velocity
    - dip_angles: list of dip angles in degrees
    
    Returns:
    - dictionary with dip angles as keys and travel times as values
    """
    hyperbolas = {}
    
    for angle in dip_angles:
        if angle == 0:
            travel_times = calculate_travel_times_horizontal(source_x, receiver_x, depth_at_source, velocity)
        else:
            travel_times = calculate_travel_times_dipping(source_x, receiver_x, depth_at_source, velocity, angle)
        hyperbolas[angle] = travel_times
    
    return hyperbolas

def generate_ambiguous_models(source_x, receiver_x, depth_at_source, velocity):
    """
    Generate a dictionary of different ambiguous scenarios.
    Includes: horizontal, dipping, depth-velocity tradeoff, two layers, source shift.
    
    Returns:
    - dictionary with model name as key and travel times as value
    """
    models = {}

    # Base horizontal
    models["horizontal"] = calculate_travel_times_horizontal(source_x, receiver_x, depth_at_source, velocity)

    # Small dip vs horizontal
    models["dip_10"] = calculate_travel_times_dipping(source_x, receiver_x, depth_at_source+20, velocity, 10)

    # Depth-velocity tradeoff
    models["shallow_slow"] = calculate_travel_times_horizontal(source_x, receiver_x, depth_at_source-50, velocity-400)
    models["deep_fast"] = calculate_travel_times_horizontal(source_x, receiver_x, depth_at_source+100, velocity+500)

    """
    # Two layers
    t1, t2 = calculate_travel_times_two_layers(source_x, receiver_x, depth_at_source-50, depth_at_source+80, velocity, velocity)
    models["two_layers_top"] = t1
    models["two_layers_bottom"] = t2
    """

    # Source shifted + dip
    models["dip_15_shifted"] = calculate_travel_times_source_shifted(source_x, receiver_x, depth_at_source, velocity, 15, source_shift=200)

    return models


def plot_model_horizontal(depth=2.0, x_min=0, x_max=10, n_receivers=100):
    """
    Plot a simple horizontal reflector model with source and receivers.
    """

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(depth + 1, 0) 

    source_x = (x_min + x_max) / 2
    ax.scatter(source_x, 0, c="red", marker="*", s=120, label="source")

    receivers_x = np.linspace(x_min, x_max, n_receivers)
    ax.scatter(receivers_x, np.zeros_like(receivers_x), c="blue", marker="v", label="Receivers")

    ax.hlines(depth, x_min, x_max, colors="black", linestyles="--", label=f"Reflector at z={depth}")

    ax.set_xlabel("Distance (x)")
    ax.set_ylabel("Depth (z)")
    ax.legend()
    ax.set_title("Horizontal Reflector Model")
    plt.show()

def plot_model_dip(depth_at_source=2.0, dip_angle=15, x_min=0, x_max=10, n_receivers=11):
    """
    Plot a dipping reflector model with source and receivers

    Parameters:
    - depth_at_source: Depth of reflector at the source point.
    - dip_angle: Dip angle in degrees(positive = dipping to the right).
    - x_min, x_max: Horizontal range of the model
    - n_receivers: Number of receivers at the surface
    """

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(depth_at_source + 2, 0)

    source_x = (x_min + x_max) / 2
    ax.scatter(source_x, 0, c="red", marker="*", s=120, label="Source")

    receivers_x = np.linspace(x_min, x_max, n_receivers)
    ax.scatter(receivers_x, np.zeros_like(receivers_x), c="blue", marker="v", label="Receivers")

    dip_rad = np.radians(dip_angle)
    reflector_x = np.linspace(x_min, x_max, 200)
    reflector_z = depth_at_source + np.tan(dip_rad) * (reflector_x - source_x)

    ax.plot(reflector_x, reflector_z, color="black", linestyle="--", label=f"Dip {dip_angle}°")

    ax.set_xlabel("Distance (x)")
    ax.set_ylabel("Depth (z)")
    ax.legend()
    ax.set_title("Dipping Reflector Model")
    plt.show()


def plot_model_depth_velocity_tradeoff(depths, velocities, labels=None):
    """
    Plots two reflector models (different depth/velocity) to illustrate the depth-velocity tradeoff ambiguity.
    """

    pass

def plot_model_horizontal_vs_dip(depth_horizontal, depth_dip, dip_angle):
    """
    PLots two reflectors models(horizontal vs dipping layer) to illustrate the source-shifted ambiguity.
    """

    pass

def plot_tradeoff_pair():
    """
    Shows side-by-side the reflectors models and their corresponding hyperbolas / synthetic seismograms 
    for depth-velocity tradeoff.     
    """
    
    pass

def plot_horizontal_vs_dip_pair():
    """
    Shows side-by-side the reflectors models and their corresponding hyperbolas / synthetic seismograms 
    for horizontal and dip ambiguity.     
    """

    pass

