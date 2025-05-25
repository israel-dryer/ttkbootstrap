from typing import Literal, Tuple
from colorsys import rgb_to_hls
from PIL import ImageColor
from ttkbootstrap.logger import Logger

logger = Logger(False, True)

HUE = 360
SAT = 100
LUM = 100

COLOR_MODEL = Literal['rgb', 'hsl', 'hex']


def color_to_rgb(color, model: COLOR_MODEL = 'hex'):
    """Convert color value to rgb.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters
    ----------
    color : Any
        The color values for the model being converted.

    model : Literal['rbg', 'hsl', 'hex']
        The color model being converted.

    Returns
    -------
    Tuple[int, int, int]
        The rgb color values.
    """
    conformed = conform_color_model(color, model)
    return ImageColor.getrgb(conformed)


def color_to_hex(color, model: COLOR_MODEL = 'rgb'):
    """Convert color value to hex.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters
    ----------
    color : Any
        The color values for the model being converted.

    model : Literal['rgb', 'hsl', 'hex']
        The color model being converted.

    Returns
    -------
    str
        The hexadecimal color value.
    """
    r, g, b = color_to_rgb(color, model)
    return f'#{r:02x}{g:02x}{b:02x}'


def color_to_hsl(color, model: COLOR_MODEL = 'hex'):
    """Convert color value to hsl.

    The color and model parameters represent the color to be converted.
    The value is expected to be a string for "name" and "hex" models and
    a Tuple or List for "rgb" and "hsl" models.

    Parameters
    ----------
    color : Any
        The color values for the model being converted.

    model : Literal['rgb', 'hsl', 'hex']
        The color model being converted.

    Returns
    -------
    Tuple[int, int, int]
        The hsl color values.
    """
    r, g, b = color_to_rgb(color, model)
    hls = rgb_to_hls(r / 255, g / 255, b / 255)
    hue = int(clamp(hls[0] * HUE, 0, HUE))
    lum = int(clamp(hls[1] * LUM, 0, LUM))
    sat = int(clamp(hls[2] * SAT, 0, SAT))
    return hue, sat, lum


def update_hsl_value(
        color, hue=None, sat=None, lum=None,
        in_model: COLOR_MODEL = 'hsl',
        out_model: COLOR_MODEL = 'hsl'):
    """Change hue, saturation, or luminosity of the color based on the hue,
    sat, lum parameters provided.

    Parameters
    ----------
    color : Any
        The color.

    hue : int, optional
        A number between 0 and 360.

    sat : int, optional
        A number between 0 and 100.

    lum : int, optional
        A number between 0 and 100.

    in_model : Literal['rgb', 'hsl', 'hex']
        The color model of the input color.

    out_model : Literal['rgb', 'hsl', 'hex']
        The color model of the output color.

    Returns
    -------
    Tuple[int, int, int]
       The color value based on the selected color model.
    """
    h, s, l = color_to_hsl(color, in_model)
    if hue is not None:
        h = hue
    if sat is not None:
        s = sat
    if lum is not None:
        l = lum
    if out_model == 'rgb':
        return color_to_rgb([h, s, l], 'hsl')
    elif out_model == 'hex':
        return color_to_hex([h, s, l], 'hsl')
    else:
        return h, s, l


def contrast_color(
        color, model: COLOR_MODEL, dark_color='#000',
        light_color='#fff'):
    """The best matching contrasting light or dark color for the given color.
    https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color

    Parameters
    ----------
    color : str
        The color value to evaluate.

    model : Literal['rgb', 'hsl', 'hex']
        The model of the color value to be evaluated. 'rgb' by default.

    dark_color : str
        The color of the dark contrasting color.

    light_color : str
        The color of the light contrasting color.

    Returns
    -------
    str
        The matching color value.
    """
    if model != 'rgb':
        r, g, b = color_to_rgb(color, model)
    else:
        r, g, b = color

    luminance = ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255
    if luminance > 0.5:
        return dark_color
    else:
        return light_color


def conform_color_model(color, model: COLOR_MODEL):
    """Conform the color values to a string that can be interpreted by the
    `PIL.ImageColor.getrgb method`.

    Parameters
    ----------
    color : Any
        The color value to conform.

    model : Literal['rgb', 'hsl', 'hex']
        The model of the color to evaluate (rgb, hex, hsl).

    Returns
    -------
    str
        A color value string that can be used as a parameter in the
        PIL.ImageColor.getrgb method.
    """
    if model == 'hsl':
        hue = clamp(color[0], 0, HUE)
        sat = clamp(color[1], 0, SAT)
        lum = clamp(color[2], 0, LUM)
        return f'hsl({hue},{sat}%,{lum}%)'
    elif model == 'rgb':
        red = clamp(color[0], 0, 255)
        grn = clamp(color[1], 0, 255)
        blu = clamp(color[2], 0, 255)
        return f'rgb({red},{grn},{blu})'
    else:
        return color


def make_transparent(alpha, foreground, background='#fff'):
    """Simulate color transparency.

    Parameters
    ----------
    alpha : float
        The amount of transparency between 0.0 and 1.0.

    foreground : str
        The foreground color.

    background : str
        The background color.

    Returns
    -------
    str
        A hexadecimal color representing the "transparent" version of the
        foreground color against the background color.
    """
    fg = ImageColor.getrgb(foreground)
    bg = ImageColor.getrgb(background)
    rgb_float = [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(fg, bg)]
    rgb_int = [int(x) for x in rgb_float]
    return '#{:02x}{:02x}{:02x}'.format(*rgb_int)


def clamp(value, min_val, max_val):
    """Return a value that is bounded by a min and max.

    Parameters
    ----------
    value : Any
        The amount of evaluate

    min_val : Any
        The minimum allowed value

    max_val : Any
        The maximum allowed value

    Returns
    -------
    Any
        The bounded value
    """
    return min(max(value, min_val), max_val)
