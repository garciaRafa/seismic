"""
Functions to compute ray paths and travel times for hyperbolic analysis.
"""

import numpy as np

def calculate_travel_times_horizontal(source_x, receiver_x, reflector_depth, velocity):
    """
    Calculate travel times for reflection from a horizontal interface.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: receiver x coordinates array
    - reflector_depth: depth of reflector below source
    - velocity: wave velocity in m/s
    
    Returns:
    - numpy array of travel times
    """
    dx = receiver_x - source_x
    h = reflector_depth
    v = velocity
    
    # Travel time formula for horizontal reflector
    travel_times = np.sqrt((4 * h**2 + dx**2) / v**2)
    
    return travel_times

def calculate_travel_times_dipping(source_x, receiver_x, reflector_depth, velocity, dip_angle):
    """
    Calculate travel times for reflection from a dipping interface.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: receiver x coordinates array
    - reflector_depth: depth of reflector below source
    - velocity: wave velocity in m/s
    - dip_angle: dip angle of reflector in degrees
    
    Returns:
    - numpy array of travel times
    """
    dx = receiver_x - source_x
    h = reflector_depth
    v = velocity
    theta = np.radians(dip_angle)
    
    # Travel time formula for dipping reflector
    travel_times = np.sqrt((4 * h**2 + dx**2 + 4 * h * dx * np.sin(theta)) / v**2)
    
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

def calculate_travel_times_two_layers(source_x, receiver_x, depth1, depth2, v1, v2):
    """
    Reflection from two horizontal reflectors (layered model).
    Useful to simulate thin-bed ambiguity vs single deeper reflector.
    
    Returns:
    - t1: travel times for first reflector
    - t2: travel times for second reflector
    """
    dx = receiver_x - source_x
    t1 = np.sqrt((4 * depth1**2 + dx**2) / v1**2)
    t2 = np.sqrt((4 * depth2**2 + dx**2) / v2**2)
    return t1, t2

def calculate_travel_times_source_shifted(source_x, receiver_x, reflector_depth, velocity, dip_angle, source_shift):
    """
    Reflection from dipping reflector with shifted source position.
    Shifting the source can mimic a different dip/geometry.
    
    Parameters:
    - source_shift: horizontal displacement of the source
    """
    shifted_source = source_x + source_shift
    return calculate_travel_times_dipping(shifted_source, receiver_x, reflector_depth, velocity, dip_angle)

def generate_hyperbola_curves(source_x, receiver_x, reflector_depth, velocity, dip_angles):
    """
    Generate hyperbola curves for multiple dip angles.
    
    Parameters:
    - source_x: source x coordinate
    - receiver_x: array of receiver x coordinates
    - reflector_depth: depth of reflector
    - velocity: wave velocity
    - dip_angles: list of dip angles in degrees
    
    Returns:
    - dictionary with dip angles as keys and travel times as values
    """
    hyperbolas = {}
    
    for angle in dip_angles:
        if angle == 0:
            travel_times = calculate_travel_times_horizontal(source_x, receiver_x, reflector_depth, velocity)
        else:
            travel_times = calculate_travel_times_dipping(source_x, receiver_x, reflector_depth, velocity, angle)
        hyperbolas[angle] = travel_times
    
    return hyperbolas

def generate_ambiguous_models(source_x, receiver_x, reflector_depth, velocity):
    """
    Generate a dictionary of different ambiguous scenarios.
    Includes: horizontal, dipping, depth-velocity tradeoff, two layers, source shift.
    
    Returns:
    - dictionary with model name as key and travel times as value
    """
    models = {}

    # Base horizontal
    models["horizontal"] = calculate_travel_times_horizontal(source_x, receiver_x, reflector_depth, velocity)

    # Small dip vs horizontal
    models["dip_10"] = calculate_travel_times_dipping(source_x, receiver_x, reflector_depth+20, velocity, 10)

    # Depth-velocity tradeoff
    models["shallow_slow"] = calculate_travel_times_horizontal(source_x, receiver_x, reflector_depth-50, velocity-400)
    models["deep_fast"] = calculate_travel_times_horizontal(source_x, receiver_x, reflector_depth+100, velocity+500)

    # Two layers
    t1, t2 = calculate_travel_times_two_layers(source_x, receiver_x, reflector_depth-50, reflector_depth+80, velocity, velocity)
    models["two_layers_top"] = t1
    models["two_layers_bottom"] = t2

    # Source shifted + dip
    models["dip_15_shifted"] = calculate_travel_times_source_shifted(source_x, receiver_x, reflector_depth, velocity, 15, source_shift=200)

    return models