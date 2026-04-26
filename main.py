import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import plotly.io as pio
import argparse

# --- Synthetic Data Generation ---
def generate_synthetic_options_data(num_strikes=30, num_expiries=20):
    strikes = np.linspace(80, 120, num_strikes)
    expiries = np.linspace(1, 60, num_expiries)  # days to expiry
    S, T = np.meshgrid(strikes, expiries)
    # Simulate gamma/vega surfaces (smooth, realistic shapes)
    gamma = np.exp(-((S-100)**2)/100) * np.exp(-T/40) * (np.sin(S/8) + 1.5)
    vega = np.exp(-((S-100)**2)/200) * np.exp(-T/50) * (np.cos(S/10) + 1.2)
    return S, T, gamma, vega

# --- Matplotlib 3D Plot ---
def plot_surface_matplotlib(S, T, Z, exposure_type='Gamma', cmap='plasma', animate=False):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(S, T, Z, cmap=cmap, edgecolor='none', alpha=0.95)
    ax.set_xlabel('Strike')
    ax.set_ylabel('Days to Expiry')
    ax.set_zlabel(f'{exposure_type} Exposure')
    ax.set_title(f'Options {exposure_type} Surface')
    fig.colorbar(surf, shrink=0.5, aspect=10)
    # Contour projections
    ax.contour(S, T, Z, zdir='z', offset=Z.min(), cmap=cmap, alpha=0.5)
    if animate:
        for angle in range(0, 360, 2):
            ax.view_init(elev=30, azim=angle)
            plt.draw()
            plt.pause(0.01)
    plt.show()

# --- Plotly Interactive 3D Plot ---
def plot_surface_plotly(S, T, Z, exposure_type='Gamma', cmap='plasma'):
    color_map = {'plasma': 'Plasma', 'viridis': 'Viridis'}
    fig = go.Figure(data=[go.Surface(z=Z, x=S, y=T, colorscale=color_map.get(cmap, 'Plasma'))])
    fig.update_layout(
        title=f'Options {exposure_type} Surface',
        scene=dict(
            xaxis_title='Strike',
            yaxis_title='Days to Expiry',
            zaxis_title=f'{exposure_type} Exposure',
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        coloraxis_colorbar=dict(title=f'{exposure_type}'),
        updatemenus=[
            dict(
                type='buttons',
                showactive=True,
                buttons=[
                    dict(label='Rotate', method='animate', args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]),
                ],
                x=0.1, y=1.15
            )
        ]
    )
    # Animation frames for rotation
    frames = [go.Frame(layout=dict(scene_camera_eye=dict(x=np.cos(np.radians(angle))*2, y=np.sin(np.radians(angle))*2, z=0.7))) for angle in range(0, 360, 5)]
    fig.frames = frames
    fig.show()

# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(description='Options Flow Surface Engine')
    parser.add_argument('--exposure', choices=['gamma', 'vega'], default='gamma', help='Exposure type to plot')
    parser.add_argument('--backend', choices=['matplotlib', 'plotly'], default='plotly', help='Plotting backend')
    parser.add_argument('--cmap', choices=['plasma', 'viridis'], default='plasma', help='Colormap')
    parser.add_argument('--animate', action='store_true', help='Animate surface rotation (matplotlib only)')
    args = parser.parse_args()

    S, T, gamma, vega = generate_synthetic_options_data()
    Z = gamma if args.exposure == 'gamma' else vega
    exposure_type = 'Gamma' if args.exposure == 'gamma' else 'Vega'

    if args.backend == 'matplotlib':
        plot_surface_matplotlib(S, T, Z, exposure_type, cmap=args.cmap, animate=args.animate)
    else:
        plot_surface_plotly(S, T, Z, exposure_type, cmap=args.cmap)

if __name__ == '__main__':
    main()
