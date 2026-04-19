import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sin, cos, radians, sqrt

#-----------------------------------#
W, H = 5, 4              # Rectangle width and height
r = 1                    # Moving circle radius
rect_cx, rect_cy = 0.5, 0.5  # Rectangle center (delta_x, delta_y)
#-----------------------------------#

def get_rectangle_contact(angle_deg):
    """
    Finds the center (x, y) of circle r that is in contact with the rectangle,
    such that (x, y) lies on a ray from the origin at angle_deg.
    """
    theta = radians(angle_deg)
    ux, uy = cos(theta), sin(theta)
    hw, hh = W/2, H/2
    candidates = []
    
    # 1. Intersection with vertical sides
    for sx in [-1, 1]:
        x_const = rect_cx + sx * (hw + r)
        if abs(ux) > 1e-9:
            d = x_const / ux
            y = d * uy
            if rect_cy - hh <= y <= rect_cy + hh:
                candidates.append(d)
                
    # 2. Intersection with horizontal sides
    for sy in [-1, 1]:
        y_const = rect_cy + sy * (hh + r)
        if abs(uy) > 1e-9:
            d = y_const / uy
            x = d * ux
            if rect_cx - hw <= x <= rect_cx + hw:
                candidates.append(d)
                
    # 3. Intersection with corner arcs
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            cx, cy = rect_cx + sx * hw, rect_cy + sy * hh
            b = -2 * (ux * cx + uy * cy)
            c = cx**2 + cy**2 - r**2
            discriminant = b**2 - 4*c
            if discriminant >= 0:
                d_cand = (-b + sqrt(discriminant)) / 2
                x_cand, y_cand = d_cand * ux, d_cand * uy
                if (sx * (x_cand - cx) > 0) and (sy * (y_cand - cy) > 0):
                    candidates.append(d_cand)

    valid_d = [d for d in candidates if d > 0]
    return max(valid_d) if valid_d else None # np.nan

# Pre-calculate trace points and distances
angles = np.arange(0, 361, 1)
trace_x = []
trace_y = []
distances = []
for a in angles:
    d = get_rectangle_contact(a)
    if d is not None:
        trace_x.append(d * cos(radians(a)))
        trace_y.append(d * sin(radians(a)))
        distances.append(d)

# --- Setup Animation with 2 Subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Subplot 1: Geometry and Trace
rectangle = plt.Rectangle((rect_cx - W/2, rect_cy - H/2), W, H, 
                          fill=False, color='blue', linewidth=2, label='Fixed Rectangle')
ax1.add_patch(rectangle)
trace_line, = ax1.plot([], [], 'r-', linewidth=2, label='Trace of Center r')
moving_circle = plt.Circle((0, 0), r, color='green', alpha=0.4)
ax1.add_artist(moving_circle)
ray_line, = ax1.plot([], [], 'k--', alpha=0.3)

limit = max(W, H) + r + sqrt(rect_cx**2 + rect_cy**2) + 1
ax1.set_xlim(-limit, limit)
ax1.set_ylim(-limit, limit)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_title('Trace of Circle r')
ax1.legend(loc='upper right')

# Subplot 2: Probe Distance vs Angle
dist_plot, = ax2.plot([], [], 'b-', linewidth=2)
ax2.set_xlim(0, 360)
ax2.set_ylim(0, max(distances) + 1)
ax2.set_xticks(45*np.arange(9))
ax2.set_xlabel('Angle (deg)')
ax2.set_ylabel('Distance from Origin')
ax2.set_title('Probe Distance')
ax2.grid(True, linestyle='--', alpha=0.6)

def init():
    trace_line.set_data([], [])
    moving_circle.center = (0, 0)
    ray_line.set_data([], [])
    dist_plot.set_data([], [])
    return trace_line, moving_circle, ray_line, dist_plot

def update(frame):
    # Current point
    cx, cy = trace_x[frame], trace_y[frame]
    
    # Update Subplot 1
    trace_line.set_data(trace_x[:frame+1], trace_y[:frame+1])
    moving_circle.center = (cx, cy)
    ray_line.set_data([0, cx], [0, cy])
    
    # Update Subplot 2
    dist_plot.set_data(angles[:frame+1], distances[:frame+1])
    
    return trace_line, moving_circle, ray_line, dist_plot

ani = FuncAnimation(fig, update, frames=len(trace_x), init_func=init, 
                    interval=20, blit=True)

plt.tight_layout()
plt.show()
