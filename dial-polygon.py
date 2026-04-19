import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

#---------------------------------------------------------#
# Parameters
#---------------------------------------------------------#
csv_path = 'probe_data_test1.csv'
r = 1.0  # Radius of the gauge ball (must match the source data)

#---------------------------------------------------------#
# 1. Load the probe data [angles, dist1]
#---------------------------------------------------------#
try:
    # Attempt to read the provided CSV file
    # Format expected: columns 'angle' and 'distance'
    data = pd.read_csv(csv_path)
    angles = data['angle'].values
    dists = data['distance'].values
except Exception as e:
    print(f"Error loading CSV: {e}")
    print("Ensure 'lab/dialgauge/line_d1.csv' exists with 'angle' and 'distance' columns.")
    # Fallback to dummy data if file is missing for demonstration
    angles = np.linspace(0, 360, 361)
    dists = 5 + 0.5 * np.sin(np.radians(4 * angles)) # example clover shape
    print("Using fallback dummy data.")

#---------------------------------------------------------#
# 2. Reconstruct the center path of the probe
#---------------------------------------------------------#
angles_rad = np.radians(angles)
xc = dists * np.cos(angles_rad)
yc = dists * np.sin(angles_rad)

#---------------------------------------------------------#
# 3. Calculate the inner envelope (the contacting shape)
#---------------------------------------------------------#
# The envelope of a family of circles (x - xc(t))^2 + (y - yc(t))^2 = r^2
# is given by P(t) = C(t) ± r * N(t), where N is the unit normal to the path.

# Use np.gradient for numerical derivatives
dxc = np.gradient(xc, angles_rad)
dyc = np.gradient(yc, angles_rad)

# Magnitude of the tangent vector
mag = np.sqrt(dxc**2 + dyc**2)

# Unit normal vector (pointing inward towards the origin/object)
# For a counter-clockwise path, (-dy, dx) is the left-hand normal.
# Since the probe is outside the object, this normal points toward the object.
nx = -dyc / mag
ny = dxc / mag

# Reconstructed shape points
px = xc + r * nx
py = yc + r * ny

#---------------------------------------------------------#
# 4. Visualization and Animation
#---------------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Subplot 1: Geometry Reconstruction
limit = np.max(dists)
ax1.set_xlim(-limit, limit)
ax1.set_ylim(-limit, limit)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_title('Reconstructed Shape (Inner Envelope)')

# Plot center path and reconstructed outline
ax1.plot(xc, yc, 'g--', alpha=0.3, label='Probe Center Path')
ax1.plot(px, py, 'r-', linewidth=2, label='Reconstructed Shape')

# Animation elements
circle = plt.Circle((xc[0], yc[0]), r, color='blue', alpha=0.2, fill=True)
contact_point, = ax1.plot([], [], 'ro', markersize=4, label='Contact Point')
probe_ray, = ax1.plot([], [], 'k:', alpha=0.4)
ax1.add_patch(circle)
ax1.legend(loc='upper right', fontsize='small')
# ax1.add_patch(plt.Circle((xc[0], yc[0]), r, color='blue', alpha=0.2, fill=True))
# ax1.add_patch(plt.Circle((xc[30], yc[30]), r, color='blue', alpha=0.2, fill=True))
# ax1.add_patch(plt.Circle((xc[50], yc[50]), r, color='blue', alpha=0.2, fill=True))

# Subplot 2: Distance Data
ax2.plot(angles, dists, 'g-', label='Probe Distance (d1)')
ax2.set_xlim(0, 360)
ax2.set_xlabel('Angle (deg)')
ax2.set_ylabel('Distance')
ax2.set_title('Input Data from CSV File')
ax2.grid(True, linestyle='--', alpha=0.6)
curr_dist_marker, = ax2.plot([], [], 'ro')

def init():
    circle.center = (xc[0], yc[0])
    contact_point.set_data([], [])
    probe_ray.set_data([], [])
    curr_dist_marker.set_data([], [])
    return circle, contact_point, probe_ray, curr_dist_marker

def update(frame):
    # Update Subplot 1
    circle.center = (xc[frame], yc[frame])
    contact_point.set_data([px[frame]], [py[frame]])
    probe_ray.set_data([0, xc[frame]], [0, yc[frame]])
    
    # Update Subplot 2
    curr_dist_marker.set_data([angles[frame]], [dists[frame]])
    
    return circle, contact_point, probe_ray, curr_dist_marker

ani = FuncAnimation(fig, update, frames=len(angles), init_func=init, interval=20, blit=True)

plt.tight_layout()
plt.show()
