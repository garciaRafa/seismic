import numpy as np
import matplotlib.pyplot as plt

def plot_wave_types():
    """
    Plots P-wave (longitudinal) and S-wave (transversal) representations.
    """
    x = np.linspace(0, 4*np.pi, 100)
    t = np.linspace(0, 2*np.pi, 5)

    fig = plt.figure(figsize=(12, 8))

    # P-wave
    ax1 = fig.add_subplot(2, 1, 1)
    for ti in t:
        displacement = 0.5 * np.sin(x - ti)
        particle_positions = x + displacement
        ax1.plot(particle_positions, np.zeros_like(x) + ti/5, 'bo-', alpha=0.5)
        ax1.plot(x, np.zeros_like(x) + ti/5, 'k--', alpha=0.2)
    ax1.set_ylabel('Time progression')
    ax1.set_xlabel('Propagation direction')
    ax1.grid(True)
    ax1.set_title('P-wave (Longitudinal)')

    # S-wave
    
    ax2 = fig.add_subplot(2, 1, 2)
    for ti in t:
        displacement = 0.5 * np.sin(x - ti)
        ax2.plot(x, displacement + ti/5, 'go-', alpha=0.5)
        ax2.plot(x, np.zeros_like(x) + ti/5, 'k--', alpha=0.2)
    ax2.set_ylabel('Vertical displacement')
    ax2.set_xlabel('Propagation direction')
    ax2.grid(True)
    ax2.set_title('S-wave (Transverse)')

    plt.tight_layout()
    plt.show()