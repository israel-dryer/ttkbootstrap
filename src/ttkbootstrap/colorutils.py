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
    
    Parameters:
        
        color (Any):
            The color values for the model being converted.
            
        model (str):
            The color model being converted.
    
    Returns:

        tuple[int, int, int]:
            The rgb color values.
    """
    color_ = conform_color_model(color, model)    
    try:
        return ImageColor.getrgb(color_)
    except:
        print('this')
    
def color_to_hex(color, model=RGB):
    """Convert color value to hex.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.
    
    Parameters:
        
        color (Any):
            The color values for the model being converted.
            
        model (str):
            The color model being converted.
    
    Returns:
    
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
    
    Parameters:
        
        color (Any):
            The color values for the model being converted.
            
        model (str):
            The color model being converted.
    
    Returns:

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
    """Change hue, saturation, or lumenosity of the color based on the
    hue, sat, lum parameters provided.
    
    Parameters:

        color (Any):
            The color

        hue (int):
            A number between 0 and 360.

        sat (int):
            A number between 0 and 100.

        lum (int):
            A number between 0 and 100.

        inmodel (str):
            The color model used by the color to be changed. One of
            hsl, rgb, hex, name.

        outmodel (str):
            The color value model to be returned when the color is
            changed. One of hsl, rgb, hex.

    Returns:

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
    """Returns the best matching contrasting light or dark color for
    the given color.
    
    Parameters:

        color (Any):
            The color value to evaluate.

        model (str):
            The model of the color value to be evaluated. 'rgb' by 
            default.

        darkcolor (Any):
            The color value to be returned when the constrasting color 
            should be dark.

        lightcolor (Any):
            The color value to be returned when the constrasting color
            should be light.

    Returns:

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
    """Conform the color values to a string that can be interpreted
    by the `PIL.ImageColor.getrgb method`.

    Parameters:

        color (Union[tuple[int, int, int], str]):
            The color value to conform.

        model (str):
            One of 'HSL', 'RGB', or 'HEX'

    Returns:

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
