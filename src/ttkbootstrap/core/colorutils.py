"""Color utility functions for ttkbootstrap.

This module provides utilities for converting between different color models
and manipulating colors (adjusting hue, saturation, luminance).

Supported color models:
    - RGB: Red, Green, Blue tuple (0-255)
    - HSL: Hue (0-360), Saturation (0-100), Luminance (0-100)
    - HEX: Hexadecimal color string (#RRGGBB)
    - NAME: Named colors (e.g., 'red', 'blue')

Functions:
    color_to_rgb: Convert any color model to RGB
    color_to_hex: Convert any color model to HEX
    color_to_hsl: Convert any color model to HSL
    update_color: Modify HSL values of a color
    contrast_color: Get contrasting foreground color for readability

Example:
    ```python
    from ttkbootstrap.colorutils import *

    # Convert hex to RGB
    rgb = color_to_rgb('#FF5733', model=HEX)  # (255, 87, 51)

    # Adjust color lightness
    lighter = update_color('#FF5733', lum=80, inmodel=HEX, outmodel=HEX)

    # Get contrasting text color
    fg_color = contrast_color('#FF5733')  # Returns 'white' or 'black'
    ```

"""
from PIL import ImageColor
from colorsys import rgb_to_hls

RGB = 'rgb'
HSL = 'hsl'
HEX = 'hex'
NAME = 'name'

HUE = 360
SAT = 100
LUM = 100


def color_to_rgb(color, model=HEX):
    """Convert color value to rgb.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.
    
    Args:
        color: The color value to convert.
        model: The color model of the input value.

    Returns:
    -------
        tuple[int, int, int]:
            The rgb color values.

    """
    color_ = conform_color_model(color, model)
    return ImageColor.getrgb(color_)


def color_to_hex(color, model=RGB):
    """Convert color value to hex.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.
    
    Args:
        color: The color value to convert.
        model: The color model of the input value.

    Returns:
    -------
        str:
            The hexadecimal color value.

    """
    r, g, b = color_to_rgb(color, model)
    return f'#{r:02x}{g:02x}{b:02x}'

def color_to_hsl(color, model=HEX):
    """Convert color value to hsl.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.
    
    Args:
        color: The color value to convert.
        model: The color model of the input value.

    Returns:
    -------
        tuple[int, int, int]:
            The hsl color values.

    """
    r, g, b = color_to_rgb(color, model)
    hls = rgb_to_hls(r/255, g/255, b/255)
    h = int(hls[0]*HUE)
    l = int(hls[1]*LUM)
    s = int(hls[2]*SAT)
    return h, s, l

def update_hsl_value(color, hue=None, sat=None, lum=None, inmodel=HSL, outmodel=HSL):
    """Change the hue, saturation, or luminosity of a color.

    Args:
        color: The color value.
        hue: Hue (0-360).
        sat: Saturation (0-100).
        lum: Luminosity (0-100).
        inmodel: Color model of the input. One of hsl, rgb, hex, name.
        outmodel: Color model for the output. One of hsl, rgb, hex.

    Returns:
    -------
        Union[tuple[int, int, int], str]:
            The color value based on the selected color model.

    """
    h, s, l = color_to_hsl(color, inmodel)
    if hue is not None:
        h = hue
    if sat is not None:
        s = sat
    if lum is not None:
        l = lum
    if outmodel == RGB:
        return color_to_rgb([h, s, l], HSL)
    elif outmodel == HEX:
        return color_to_hex([h, s, l], HSL)
    else:
        return h, s, l


"""
https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color

"""

def contrast_color(color, model=RGB, darkcolor='#000', lightcolor='#fff'):
    """Return the best contrasting light or dark color for the given color.

    Args:
        color: The color value to evaluate.
        model: The color model of the input.
        darkcolor: The dark contrast color to return.
        lightcolor: The light contrast color to return.

    Returns:
    -------
        str:
            The matching color value.

    """
    if model != RGB:
        r, g, b = color_to_rgb(color, model)
    else:
        r, g, b = color

    luminance = ((0.299 * r) + (0.587 * g) + (0.114 * b))/255
    if luminance > 0.5:
        return darkcolor
    else:
        return lightcolor


def conform_color_model(color, model):
    """Conform a color value to a string interpretable by PIL.ImageColor.getrgb.

    Args:
        color: The color value to conform.
        model: One of 'HSL', 'RGB', or 'HEX'.

    Returns:
    -------
        str:
            A color value string that can be used as a parameter in the
            PIL.ImageColor.getrgb method.

    """    
    if model == HSL:
        h, s, l = color
        return f'hsl({h},{s}%,{l}%)'
    elif model == RGB:
        r, g, b = color
        return f'rgb({r},{g},{b})'
    else:
        return color
