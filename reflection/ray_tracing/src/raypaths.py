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