import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, radians, sqrt

#-----------------------------------#
R = 5
r = 1
delta_x, delta_y = [0.5, 0.5] # displacement of fixed circle R center
#-----------------------------------#

def get_contact_point(angle_deg):
    """
    Finds the center (x, y) of circle r that is in contact with circle R,
    such that (x, y) lies on a ray from the origin at angle_deg.
    
    The center (x,y) satisfies:
    1) x = d * cos(theta)
    2) y = d * sin(theta)
    3) (x - delta_x)^2 + (y - delta_y)^2 = (R + r)^2
    
    Substituting (1) and (2) into (3) yields a quadratic equation for d:
    d^2 - 2*d*(delta_x*cos(theta) + delta_y*sin(theta)) + delta_x^2 + delta_y^2 - (R+r)^2 = 0
    """
    theta = radians(angle_deg)
    
    # Quadratic coefficients: ad^2 + bd + c = 0 (a=1)
    b = -2 * (delta_x * cos(theta) + delta_y * sin(theta))
    c = delta_x**2 + delta_y**2 - (R + r)**2
    
    discriminant = b**2 - 4*c
    if discriminant < 0:
        return None, None
        
    # We take the positive root for the distance along the ray from origin
    # Since c < 0 (origin is inside R+r circle), one root is positive and one is negative.
    d = (-b + sqrt(discriminant)) / 2
    
    x = d * cos(theta)
    y = d * sin(theta)
    return x, y

def get_trace():
    '''get trace of center of circle r contacting with circle R for 0-360 degrees'''
    x_pos = []
    y_pos = []
    for angle in range(0, 361):
        x, y = get_contact_point(angle)
        if x is not None:
            x_pos.append(x)
            y_pos.append(y)
    return x_pos, y_pos

x_pos, y_pos = get_trace()

fig, ax = plt.subplots(figsize=(8,8))

# 1. Fixed circle R centered at (delta_x, delta_y)
fixed_circle = plt.Circle((delta_x, delta_y), R, color='blue', fill=False, label=f'Fixed Circle R (center at {delta_x}, {delta_y})')
ax.add_artist(fixed_circle)

# 2. Trace of the center of moving circle r
ax.plot(x_pos, y_pos, 'r-', linewidth=2, label=f'Trace of Center r (radius={r})')

# 3. Example of circle r at 45 degrees to show contact
ex_x, ex_y = get_contact_point(45)
if ex_x is not None:
    example_circle = plt.Circle((ex_x, ex_y), r, color='green', alpha=0.3, label='Example position at 45°')
    ax.add_artist(example_circle)
    ax.plot([0, ex_x], [0, ex_y], 'g--', alpha=0.5) # Ray from origin

limit = R + r + sqrt(delta_x**2 + delta_y**2) + 1
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Trace of Contacting Circle Center\nFixed R={R} at ({delta_x}, {delta_y}), Moving r={r}')
plt.legend()
plt.show()
