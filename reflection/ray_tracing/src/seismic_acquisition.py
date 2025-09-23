import numpy as np
import matplotlib.pyplot as plt

def plot_seismic_acquisition(n_receivers, spacing, source_x, layer_depths, x_min, x_max):
    """
    Plots seismic acquisition geometries with configurable parameters.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(min(layer_depths) - 0.5, 1.0)

    # Surface
    ax.hlines(0, x_min, x_max, color='black', linewidth=2)
    ax.text(x_min+0.2, 0.1, 'Surface', fontsize=10, va='bottom')

    # Source
    ax.plot(source_x, 0, 'ro', markersize=10)
    ax.text(source_x, 0.4, 'Source', color='r', ha='center', fontsize=10, weight='bold')

    # Receivers
    receivers = np.arange(source_x + spacing, source_x + spacing*(n_receivers+1), spacing)
    for i, rx in enumerate(receivers, 1):
        ax.plot(rx, 0, 's', color='darkgreen', markersize=8)
        ax.text(rx, 0.2, f'G{i}', ha='center', fontsize=9, color='darkgreen')
    
    # Layers
    for d in layer_depths:
        ax.hlines(d, x_min, x_max, linestyles='dashed', colors='gray', linewidth=1)
    colors = ['bisque', 'tan', 'peru']
    for i in range(len(layer_depths)):
        ax.fill_between([x_min, x_max], layer_depths[i], layer_depths[i-1] if i > 0 else 0, 
                        color=colors[i % len(colors)], alpha=0.3)

    # Rays
    for i, rx in enumerate(receivers, 1):
        reflex_point = (source_x + rx) / 2
        ax.plot([source_x, rx], [0, 0], ':', color='gray', alpha=0.5) # direto
        ax.plot([source_x, reflex_point, rx], [0, layer_depths[0], 0], '-', linewidth=1.5)
    
    ax.axis('off')
    plt.tight_layout()
    plt.show()

