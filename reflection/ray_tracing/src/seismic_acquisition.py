import numpy as np
import matplotlib.pyplot as plt

def plot_seismic_acquisition():
    """
    Plots a didactic seismic acquisition setup with source, receivers, geological layers, and seismic rays.
    """

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-2, 12)
    ax.set_ylim(-2.5, 1.0)

    # Surface
    ax.hlines(0, -2, 12, color='black', linewidth=2)
    ax.text(-1.8, 0.1, 'Surface', fontsize=10, va='bottom')

    # Source
    ax.plot(1, 0, 'ro', markersize=10)
    ax.text(1, 0.4, 'Seismic Source', color='r', ha='center', fontsize=10, weight='bold')

    # Receivers
    for i in range(3, 11, 2):
        ax.plot(i, 0, 's', color='darkgreen', markersize=8)
        ax.text(i, 0.2, f'Geophone {i//2}', ha='center', fontsize=9, color='darkgreen')
    
    # Layers
    ax.hlines(-1, -2, 12, linestyles='dashed', colors='gray', linewidth=1)
    ax.hlines(-2, -2, 12, linestyles='dashed', colors='gray', linewidth=1)
    ax.fill_between([-2, 12], -1, 0, color='bisque', alpha=0.3)
    ax.fill_between([-2, 12], -2, 0, color='tan', alpha=0.3)
    ax.fill_between([-2, 12], -2.5, 0, color='peru', alpha=0.3)
    
    # Layer labels
    ax.text(-1.8, -0.5, 'Sediments\n(0-1 km)', fontsize=8, va='center')
    ax.text(-1.8, -1.5, 'Basement Rock\n(1-2 km)', fontsize=8, va='center')
    ax.text(-1.8, -2.25, 'Substrate\n(>2 km)', fontsize=8, va='center')

    # Seismic rays
    colors = plt.cm.tab10(np.linspace(0, 1, 5))
    for i, (x, c) in enumerate(zip(range(3, 11, 2), colors)):
        reflex_point = (1 + x) / 2
        ax.plot([1, x], [0, 0], ':', color=c, alpha=0.5) # direct ray
        ax.plot([1, reflex_point, x], [0, -1, 0], '-', color=c, linewidth=1.5) # reflected
        ax.annotate('', xy=(reflex_point, -0.5), xytext=(1, 0),
                    arrowprops=dict(arrowstyle="->", color=c))
        ax.annotate('', xy=(x, 0), xytext=(reflex_point, -0.5),
                    arrowprops=dict(arrowstyle="->", color=c))
    
    ax.text(6, -1.2, 'Seismic Interface', fontsize=9, ha='center',
            bbox=dict(facecolor='white', alpha=0.8))
    
    ax.axis('off')
    plt.tight_layout()
    plt.show()
    # fig.savefig("seismic_acquisition.png")
