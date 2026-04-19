import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sin, cos, radians, sqrt

#-----------------------------------#
W, H = 4, 4              # Rectangle width and height
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
    return max(valid_d) if valid_d else np.nan # None

# Pre-calculate points and distances for both sides
angles = np.arange(0, 361, 1)
trace1_x, trace1_y, dists1 = [], [], []
trace2_x, trace2_y, dists2 = [], [], []
sum_dists = []

for a in angles:
    # Circle 1 at angle 'a'
    d1 = get_rectangle_contact(a)
    trace1_x.append(d1 * cos(radians(a)))
    trace1_y.append(d1 * sin(radians(a)))
    dists1.append(d1)
    
    # Circle 2 at angle 'a + 180'
    d2 = get_rectangle_contact(a + 180)
    trace2_x.append(d2 * cos(radians(a + 180)))
    trace2_y.append(d2 * sin(radians(a + 180)))
    dists2.append(d2)
    
    sum_dists.append(d1 + d2)

# --- Setup Animation with 2 Subplots ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6))

# Subplot 1: Geometry and Trace
rectangle = plt.Rectangle((rect_cx - W/2, rect_cy - H/2), W, H, 
                          fill=False, color='blue', linewidth=2, label='Fixed Rectangle')
ax1.add_patch(rectangle)

# Trace lines for both circles
trace_line1, = ax1.plot([], [], 'r-', linewidth=1.5, alpha=0.6, label='Trace 1 (0°)')
trace_line2, = ax1.plot([], [], 'm-', linewidth=1.5, alpha=0.6, label='Trace 2 (180°)')

# Moving circles
circle1 = plt.Circle((0, 0), r, color='green', alpha=0.4)
circle2 = plt.Circle((0, 0), r, color='orange', alpha=0.4)
ax1.add_artist(circle1)
ax1.add_artist(circle2)

# Ray lines
ray1, = ax1.plot([], [], 'g--', alpha=0.5)
ray2, = ax1.plot([], [], 'orange', linestyle='--', alpha=0.5)

limit = max(W, H) + r + sqrt(rect_cx**2 + rect_cy**2) + 2
ax1.set_xlim(-limit, limit)
ax1.set_ylim(-limit, limit)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.set_title('Opposing Contacting Circles')
ax1.legend(loc='upper right', fontsize='small')

# Subplot 2: Individual Probe Distances
line_d1, = ax2.plot([], [], 'g-', label='d1 (0°)')
line_d2, = ax2.plot([], [], 'orange', linestyle='-', label='d2 (180°)')
ax2.set_xlim(0, 360)
ax2.set_ylim(min(min(dists1), min(dists2)) - 1, max(max(dists1), max(dists2)) + 1)
ax2.set_xticks(45*np.arange(9))
ax2.set_xlabel('Angle (deg)')
ax2.set_ylabel('Distance')
ax2.set_title('Individual (d1, d2)')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

# Subplot 3: Sum of Probe Distances
sum_plot, = ax3.plot([], [], 'b-', linewidth=2, label='Sum (d1 + d2)')
ax3.set_xlim(0, 360)
ax3.set_ylim(min(sum_dists) - 1, max(sum_dists) + 1)
ax3.set_xticks(45*np.arange(9))
ax3.set_xlabel('Angle (deg)')
ax3.set_ylabel('Total Distance')
ax3.set_title('Sum of Probe Distances')
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.legend()

def init():
    trace_line1.set_data([], [])
    trace_line2.set_data([], [])
    circle1.center = (0, 0)
    circle2.center = (0, 0)
    ray1.set_data([], [])
    ray2.set_data([], [])
    line_d1.set_data([], [])
    line_d2.set_data([], [])
    sum_plot.set_data([], [])
    return trace_line1, trace_line2, circle1, circle2, ray1, ray2, line_d1, line_d2, sum_plot

def update(frame):
    # Update Subplot 1 (Geometry)
    trace_line1.set_data(trace1_x[:frame+1], trace1_y[:frame+1])
    trace_line2.set_data(trace2_x[:frame+1], trace2_y[:frame+1])
    
    circle1.center = (trace1_x[frame], trace1_y[frame])
    circle2.center = (trace2_x[frame], trace2_y[frame])
    
    ray1.set_data([0, trace1_x[frame]], [0, trace1_y[frame]])
    ray2.set_data([0, trace2_x[frame]], [0, trace2_y[frame]])
    
    # Update Subplot 2
    line_d1.set_data(angles[:frame+1], dists1[:frame+1])
    line_d2.set_data(angles[:frame+1], dists2[:frame+1])
    
    # Update Subplot 3 (Sum Graph)
    sum_plot.set_data(angles[:frame+1], sum_dists[:frame+1])
    
    return trace_line1, trace_line2, circle1, circle2, ray1, ray2, line_d1, line_d2, sum_plot

ani = FuncAnimation(fig, update, frames=len(angles), init_func=init, 
                    interval=20, blit=True)

plt.tight_layout()
plt.show()
