"""
    A collection of utility functions used to build tk and ttk themes
"""
import colorsys


def hex_to_rgb(color):
    """Convert hexadecimal to rgb color representation"""
    r = round(int(color[1:3], 16) / 255, 2)
    g = round(int(color[3:5], 16) / 255, 2)
    b = round(int(color[5:], 16) / 255, 2)
    return r, g, b


def rgb_to_hex(r, g, b):
    """Convert rgb to hexadecimal color representation"""
    r_ = int(r * 255)
    g_ = int(g * 255)
    b_ = int(b * 255)
    return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)


def brightness(hex_color, pct_change):
    """Adjust the value of a given hexadecimal color. The percent change is expected to be a float. Example: 0.15
    is a 15 percent increase in brightness, whereas -0.15 is a 15 percent decrease in brightness"""
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    v_ = (1 + pct_change) * v
    v_max = max(0, v_)
    v_min = min(1, v_max)
    r_, g_, b_ = colorsys.hsv_to_rgb(h, s, v_min)
    return rgb_to_hex(r_, g_, b_)
