import base64
from io import BytesIO
from math import ceil
from typing import Union
import platform

from PIL import Image, ImageOps
from PIL.ImageTk import PhotoImage

from PIL.ImageDraw import ImageDraw

from ttkbootstrap.utils import color_utils


def image_draw(size, mode=None, *args):
    im = Image.new(mode or 'RGBA', size, *args)
    return im, ImageDraw(im)


def image_resize(img, size):
    return PhotoImage(image=img.resize(size, Image.Resampling.LANCZOS))


def image_open(data: str):
    return Image.open(BytesIO(base64.b64decode(data))).convert('RGBA')


def downscale_image(image: Image.Image) -> Image.Image:
    from ttkbootstrap.window import get_default_root
    tk = get_default_root()
    scale = float(tk.call('tk', 'scaling')) or 1.0
    factor = 0.5 * scale
    size = (max(1, int(image.width * factor)), max(1, int(image.height * factor)))
    return image.resize(size, Image.Resampling.LANCZOS)


def scale_size(*size):
    from ttkbootstrap.window import get_default_root
    tk = get_default_root()
    baseline = 1.0005 if platform.system() == 'Darwin' else 2.0009
    factor = float(tk.call('tk', 'scaling')) / baseline
    scaled = [ceil(s * factor) for s in size]
    return scaled[0] if len(scaled) == 1 else tuple(scaled)


def image_recolor_map(data: Union[str, Image.Image], white: str, black: str, overlay: Image.Image = None):
    img = image_open(data) if isinstance(data, str) else data
    base_rgb = ImageOps.grayscale(img)
    alpha = img.getchannel("A")
    light = color_utils.color_to_rgb(white)
    dark = color_utils.color_to_rgb(black)
    result = Image.new("RGBA", img.size)
    pixels = result.load()
    for y in range(img.height):
        for x in range(img.width):
            lum = base_rgb.getpixel((x, y)) / 255.0
            a = alpha.getpixel((x, y))
            r = round(dark[0] + (light[0] - dark[0]) * lum)
            g = round(dark[1] + (light[1] - dark[1]) * lum)
            b = round(dark[2] + (light[2] - dark[2]) * lum)
            pixels[x, y] = (r, g, b, a)
    if overlay is not None:
        result = Image.alpha_composite(result, overlay)
    return PhotoImage(downscale_image(result))
