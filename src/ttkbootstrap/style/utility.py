from colorsys import hls_to_rgb, rgb_to_hls
from pathlib import Path
from typing import Tuple, cast

from PIL import Image, ImageColor, ImageOps
from PIL.ImageTk import PhotoImage

from ttkbootstrap.style.types import ColorModel
from ttkbootstrap.utility import clamp

image_cache = []

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "widgets"

HUE = 360
SAT = 100
LUM = 100


def color_to_rgb(color, model: ColorModel = 'hex'):
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


def color_to_hex(color, model: ColorModel = 'rgb'):
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


def color_to_hsl(color, model: ColorModel = 'hex'):
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
        in_model: ColorModel = 'hsl',
        out_model: ColorModel = 'hsl'):
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
        color, model: ColorModel, dark_color='#000',
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


def conform_color_model(color, model: ColorModel):
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


def open_image(name: str) -> Image.Image:
    """
    Load a white-layout image from file.

    Args:
        name: The asset name without extension (e.g. "add" loads "add.png")

    Returns:
        A Pillow RGBA Image object.
    """
    path = ASSETS_DIR / f"{name}.png"
    return Image.open(path).convert("RGBA")


def recolor_image(
        name: str,
        white_color: str,
        black_color: str = "#ffffff",
        magenta_color: str | None = None,
        transparent_color: str | None = None,
        *,
        scale: float = 0.43,
) -> PhotoImage:
    """
    Recolor a white-layout PNG image using luminance interpolation.

    Args:
        name: Asset name without `.png` (e.g., "add")
        white_color: Replace white with this color (hex string)
        black_color: Replace black with this color (hex string)
        magenta_color: Replace magenta (#ff00ff) with this color, if provided
        scale: Optional scaling factor for output image
        transparent_color: Fill fully transparent areas with this color

    Returns:
        A ChromaTk-compatible PhotoImage object.
    """
    img = open_image(name)
    gray = ImageOps.grayscale(img)

    fg_rgb = color_to_rgb(white_color)
    bg_rgb = color_to_rgb(black_color)
    mag_rgb = color_to_rgb(magenta_color) if magenta_color else None
    trans_rgb = color_to_rgb(transparent_color) if transparent_color else None

    result = Image.new("RGBA", img.size)
    src_pixels = img.load()
    dst_pixels = result.load()

    for y in range(img.height):
        for x in range(img.width):
            r_src, g_src, b_src, a = src_pixels[x, y]

            if a == 0:
                if trans_rgb:
                    dst_pixels[x, y] = (*trans_rgb, 255)
                else:
                    dst_pixels[x, y] = (0, 0, 0, 0)
                continue

            alpha_frac = a / 255.0

            if mag_rgb and (r_src, g_src, b_src) == (255, 0, 255):
                r, g, b = mag_rgb
            else:
                lum = gray.getpixel((x, y)) / 255.0
                r = round(bg_rgb[0] + (fg_rgb[0] - bg_rgb[0]) * lum)
                g = round(bg_rgb[1] + (fg_rgb[1] - bg_rgb[1]) * lum)
                b = round(bg_rgb[2] + (fg_rgb[2] - bg_rgb[2]) * lum)

            if trans_rgb:
                r_final = round(trans_rgb[0] * (1 - alpha_frac) + r * alpha_frac)
                g_final = round(trans_rgb[1] * (1 - alpha_frac) + g * alpha_frac)
                b_final = round(trans_rgb[2] * (1 - alpha_frac) + b * alpha_frac)
                dst_pixels[x, y] = (r_final, g_final, b_final, 255)
            else:
                dst_pixels[x, y] = (r, g, b, a)

    if scale != 1.0:
        new_size = (
            max(1, int(result.width * scale)),
            max(1, int(result.height * scale))
        )
        result = result.resize(new_size, Image.Resampling.LANCZOS)

    img = PhotoImage(image=result)
    global image_cache
    image_cache.append(img)
    return img


def should_darken(bg_hex: str) -> bool:
    """Determine whether to darken or lighten based on luminance and saturation."""
    r, g, b = [v / 255.0 for v in ImageColor.getrgb(bg_hex)]
    h, l, s = rgb_to_hls(r, g, b)

    # If the color is light and saturated, lighten it (like warning/info)
    # If the color is already very light (lightness > 0.9), darken it to gain contrast
    if l > 0.8:
        return True  # Darken very light colors (like `light`)
    if l < 0.3:
        return False  # Lighten very dark colors (like `dark`)
    if s > 0.6 and l > 0.6:
        return False  # Lighten vibrant, light colors (e.g. warning/info)
    return True  # Default: darken


def darken_color(hex_color: str, percent: float) -> str:
    """Darken a hex color by reducing lightness in HLS color space."""
    r, g, b = [v / 255.0 for v in ImageColor.getrgb(hex_color)]
    h, l, s = rgb_to_hls(r, g, b)
    l = max(0.0, l * (1 - percent))
    r, g, b = hls_to_rgb(h, l, s)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def lighten_color(hex_color: str, percent: float) -> str:
    """Lighten a hex color by increasing lightness in HLS color space."""
    r, g, b = [v / 255.0 for v in ImageColor.getrgb(hex_color)]
    h, l, s = rgb_to_hls(r, g, b)
    l = min(1.0, l + (1 - l) * percent)
    r, g, b = hls_to_rgb(h, l, s)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def mix_colors(color1: str, color2: str, weight: float) -> str:
    """Mix two colors by weight.

    Args:
        color1: The foreground color in hex format (e.g., '#FF0000').
        color2: The background color in hex format.
        weight: A float from 0 to 1, where 1 favors color1 and 0 favors color2.

    Returns:
        A hex color string representing the mixed result.
    """
    r1, g1, b1 = ImageColor.getrgb(color1)
    r2, g2, b2 = ImageColor.getrgb(color2)

    r = round(r1 * weight + r2 * (1 - weight))
    g = round(g1 * weight + g2 * (1 - weight))
    b = round(b1 * weight + b2 * (1 - weight))

    return f"#{r:02X}{g:02X}{b:02X}"


def tint_color(color: str, base_weight: float) -> str:
    """Tint a color by mixing it with white.

    Args:
        color: The base color in hex.
        base_weight: Amount of base color to retain (0–1).

    Returns:
        A tinted hex color string.
    """
    return mix_colors(color, "#ffffff", 1 - base_weight)


def shade_color(color: str, base_weight: float) -> str:
    """Shade a color by mixing it with black.

    Args:
        color: The base color in hex.
        base_weight: Amount of base color to retain (0–1).

    Returns:
        A shaded hex color string.
    """
    return mix_colors(color, "#000000", 1 - base_weight)


def relative_luminance(hex_color: str) -> float:
    """Calculate the relative luminance of a color.

    Args:
        hex_color: A hex color string.

    Returns:
        The luminance value from 0 (black) to 1 (white).
    """
    r, g, b = [x / 255 for x in ImageColor.getrgb(hex_color)]

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    def rel_luminance(r: int, g: int, b: int) -> float:
        def channel(c): return (c / 255.0) ** 2.2

        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    lum1 = rel_luminance(*rgb1)
    lum2 = rel_luminance(*rgb2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """Convert a hex color string to an RGB tuple."""
    value = value.lstrip("#")
    lv = len(value)
    result = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return cast(tuple[int, int, int], result)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert an RGB tuple to a hex color string."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def best_foreground(bg_color: str, candidates: list[str] = None) -> str:
    """Return the color with the highest contrast against the background."""
    if candidates is None:
        candidates = ["#000000", "#ffffff"]

    bg_rgb = hex_to_rgb(bg_color)

    def contrast(c: str) -> float:
        fg_rgb = hex_to_rgb(c)
        return contrast_ratio(bg_rgb, fg_rgb)

    return max(candidates, key=contrast)
