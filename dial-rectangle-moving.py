import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sin, cos, radians, sqrt

#-----------------------------------#
W, H = 8, 4              # Rectangle width and height
r = 1                    # Moving circle radius
rect_cx, rect_cy = 1, 1  # Rectangle center (delta_x, delta_y)
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
    return max(valid_d) if valid_d else None

# Pre-calculate trace points for animation
angles = np.arange(0, 361, 1)
trace_x = []
trace_y = []
for a in angles:
    d = get_rectangle_contact(a)
    if d is not None:
        trace_x.append(d * cos(radians(a)))
        trace_y.append(d * sin(radians(a)))

# --- Setup Animation ---
fig, ax = plt.subplots(figsize=(8, 8))

# Static: Fixed rectangle
rectangle = plt.Rectangle((rect_cx - W/2, rect_cy - H/2), W, H, 
                          fill=False, color='blue', linewidth=2, label='Fixed Rectangle')
ax.add_patch(rectangle)

# Dynamic: Trace line, moving circle, and ray
trace_line, = ax.plot([], [], 'r-', linewidth=2, label='Trace of Center r')
moving_circle = plt.Circle((0, 0), r, color='green', alpha=0.4, label='Moving Circle r')
ax.add_artist(moving_circle)
ray_line, = ax.plot([], [], 'k--', alpha=0.3)

def init():
    trace_line.set_data([], [])
    moving_circle.center = (0, 0)
    ray_line.set_data([], [])
    return trace_line, moving_circle, ray_line

def update(frame):
    # Current point
    cx, cy = trace_x[frame], trace_y[frame]
    
    # Update trace
    trace_line.set_data(trace_x[:frame+1], trace_y[:frame+1])
    
    # Update moving circle
    moving_circle.center = (cx, cy)
    
    # Update ray line
    ray_line.set_data([0, cx], [0, cy])
    
    return trace_line, moving_circle, ray_line

limit = max(W, H) + r + sqrt(rect_cx**2 + rect_cy**2) + 1
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
plt.grid(True, linestyle='--', alpha=0.6)
plt.title(f'Animation: Trace of Circle r contacting Rectangle')
plt.legend(loc='upper right')

ani = FuncAnimation(fig, update, frames=len(trace_x), init_func=init, 
                    interval=20, blit=True)

plt.show()
