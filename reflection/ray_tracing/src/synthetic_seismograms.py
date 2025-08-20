"""
Functions to generate synthetic seismograms.
"""

import numpy as np
import matplotlib.pyplot as plt

def ricker_wavelet(frequency, duration, dt, time_shift=0.1):
    """
    Generate a Ricker wavelet.
    
    Parameters:
    - frequency: central frequency in Hz
    - duration: total duration in seconds
    - dt: time sampling interval
    - time_shift: time shift for wavelet peak
    
    Returns:
    - time array and wavelet array
    """
    t = np.arange(0, duration, dt)
    t_shifted = t - time_shift
    wavelet = (1 - 2 * (np.pi * frequency * t_shifted)**2) * np.exp(-(np.pi * frequency * t_shifted)**2)
    return t, wavelet

def generate_synthetic_seismogram(travel_times, wavelet, duration, dt, noise_level=0.01):
    """
    Generate synthetic seismogram from travel times and wavelet.
    
    Parameters:
    - travel_times: array of travel times for each receiver
    - wavelet: source wavelet
    - duration: total recording duration
    - dt: time sampling interval
    - noise_level: level of random noise to add
    
    Returns:
    - 2D array representing the seismogram
    """
    n_receivers = len(travel_times)
    n_samples = int(duration / dt)
    
    seismogram = np.zeros((n_receivers, n_samples))
    
    for i, t0 in enumerate(travel_times):
        start_idx = int(t0 / dt)
        end_idx = start_idx + len(wavelet)
        
        if end_idx < n_samples:
            seismogram[i, start_idx:end_idx] += wavelet
            
    # Add noise
    noise = noise_level * np.random.randn(*seismogram.shape)
    seismogram += noise
    
    # Normalize
    seismogram /= np.max(np.abs(seismogram))
    
    return seismogram

def plot_hyperbola_curves(receiver_x, hyperbolas, title='Reflection Hyperbolas'):
    """
    Plot hyperbola curves for different dip angles.
    
    Parameters:
    - receiver_x: array of receiver positions
    - hyperbolas: dictionary with dip angles as keys and travel times as values
    - title: plot title
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(hyperbolas)))
    
    for i, (angle, travel_times) in enumerate(hyperbolas.items()):
        ax.plot(receiver_x, travel_times, color=colors[i], linewidth=3, 
                label=f'Dip: {angle}°')
    
    ax.set_xlabel('Receiver Position (m)', fontsize=14)
    ax.set_ylabel('Two-Way Travel Time (s)', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=12)
    ax.invert_yaxis()
    
    return fig, ax

def plot_seismogram(seismogram, receiver_x, duration, title='Synthetic Seismogram'):
    """
    Plot synthetic seismogram using gray scale.
    
    Parameters:
    - seismogram: 2D array of seismic data
    - receiver_x: array of receiver x positions
    - duration: total time duration
    - title: plot title
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    extent = [receiver_x[0], receiver_x[-1], duration, 0]
    im = ax.imshow(seismogram.T, aspect='auto', cmap='gray', extent=extent, 
                  vmin=-1, vmax=1)
    
    ax.set_xlabel('Receiver Position (m)', fontsize=14)
    ax.set_ylabel('Two-Way Time (s)', fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Normalized Amplitude', fontsize=12)
    
    return fig, ax

def plot_comparison_seismograms(seismograms, receiver_x, duration, titles):
    """
    Plot multiple seismograms for comparison.
    
    Parameters:
    - seismograms: list of seismogram arrays
    - receiver_x: array of receiver positions
    - duration: total time duration
    - titles: list of titles for each subplot
    """
    n_plots = len(seismograms)
    fig, axes = plt.subplots(1, n_plots, figsize=(6*n_plots, 8))
    
    if n_plots == 1:
        axes = [axes]
    
    for i, (seismogram, title) in enumerate(zip(seismograms, titles)):
        extent = [receiver_x[0], receiver_x[-1], duration, 0]
        im = axes[i].imshow(seismogram.T, aspect='auto', cmap='gray', extent=extent,
                          vmin=-1, vmax=1)
        
        axes[i].set_xlabel('Receiver Position (m)', fontsize=12)
        axes[i].set_ylabel('Two-Way Time (s)', fontsize=12)
        axes[i].set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig, axes