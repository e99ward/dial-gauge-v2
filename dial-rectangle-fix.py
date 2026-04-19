import numpy as np
import matplotlib.pyplot as plt
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
    
    The 'contact boundary' for the center of circle r is a rectangle with 
    rounded corners (Minkowski sum of rectangle and circle r).
    """
    theta = radians(angle_deg)
    ux, uy = cos(theta), sin(theta)
    
    # Half-dimensions
    hw, hh = W/2, H/2
    
    candidates = []
    
    # 1. Intersection with vertical sides (straight sections)
    # x = rect_cx +/- (hw + r)
    for sx in [-1, 1]:
        x_const = rect_cx + sx * (hw + r)
        if abs(ux) > 1e-9:
            d = x_const / ux
            y = d * uy
            # Check if y is within the straight segment bounds
            if rect_cy - hh <= y <= rect_cy + hh:
                candidates.append(d)
                
    # 2. Intersection with horizontal sides (straight sections)
    # y = rect_cy +/- (hh + r)
    for sy in [-1, 1]:
        y_const = rect_cy + sy * (hh + r)
        if abs(uy) > 1e-9:
            d = y_const / uy
            x = d * ux
            # Check if x is within the straight segment bounds
            if rect_cx - hw <= x <= rect_cx + hw:
                candidates.append(d)
                
    # 3. Intersection with corner arcs (rounded corners)
    # (x - corner_x)^2 + (y - corner_y)^2 = r^2
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            cx, cy = rect_cx + sx * hw, rect_cy + sy * hh
            # Solve quadratic: (d*ux - cx)^2 + (d*uy - cy)^2 = r^2
            # d^2 - 2*d*(ux*cx + uy*cy) + (cx^2 + cy^2 - r^2) = 0
            b = -2 * (ux * cx + uy * cy)
            c = cx**2 + cy**2 - r**2
            discriminant = b**2 - 4*c
            if discriminant >= 0:
                # We want the intersection on the 'outside' of the corner
                d_cand = (-b + sqrt(discriminant)) / 2
                x_cand, y_cand = d_cand * ux, d_cand * uy
                # Verify point is actually in the exterior quadrant of this corner
                if (sx * (x_cand - cx) > 0) and (sy * (y_cand - cy) > 0):
                    candidates.append(d_cand)

    # Return the furthest positive intersection (exterior contact)
    valid_d = [d for d in candidates if d > 0]
    return max(valid_d) if valid_d else None

def get_trace():
    '''Calculate trace for 0 to 360 degrees'''
    x_pos, y_pos = [], []
    for angle in range(361):
        d = get_rectangle_contact(angle)
        if d is not None:
            x_pos.append(d * cos(radians(angle)))
            y_pos.append(d * sin(radians(angle)))
    return x_pos, y_pos

# --- Execution and Visualization ---
x_trace, y_trace = get_trace()

fig, ax = plt.subplots(figsize=(8, 8))

# 1. Draw the fixed rectangle
rectangle = plt.Rectangle((rect_cx - W/2, rect_cy - H/2), W, H, 
                          fill=False, color='blue', linewidth=2, label='Fixed Rectangle')
ax.add_patch(rectangle)

# 2. Draw the trace of circle r's center
ax.plot(x_trace, y_trace, 'r-', linewidth=2, label='Trace of Center r')

# 3. Draw example contact at 45, 135, 225, 315 degrees
for a in [45, 135, 225, 315]:
    d = get_rectangle_contact(a)
    if d:
        ex_x, ex_y = d * cos(radians(a)), d * sin(radians(a))
        circ = plt.Circle((ex_x, ex_y), r, color='green', alpha=0.2)
        ax.add_artist(circ)
        ax.plot([0, ex_x], [0, ex_y], 'k--', alpha=0.3)

limit = max(W, H) + r + sqrt(rect_cx**2 + rect_cy**2) + 1
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
plt.grid(True, linestyle='--', alpha=0.6)
plt.title(f'Trace of Circle r (radius={r}) contacting Rectangle ({W}x{H})')
plt.legend()
plt.show()
