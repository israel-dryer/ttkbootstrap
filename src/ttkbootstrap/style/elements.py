"""Manifest-driven recoloring for vendored ttk element raster templates.

Templates use black and white structural channels, an optional magenta fill
channel, and source alpha. Loading is lazy so importing ttkbootstrap does not
read the manifest or PNG files.
"""
from dataclasses import dataclass
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageColor
from PIL.Image import Resampling, Transpose


_ELEMENTS_DIR = Path(__file__).parent.parent / "assets" / "elements"
_TRANSFORMS = {
    None: None,
    "flip-x": Transpose.FLIP_LEFT_RIGHT,
    "rotate-90": Transpose.ROTATE_90,
    "rotate-180": Transpose.ROTATE_180,
    "rotate-270": Transpose.ROTATE_270,
}


@dataclass(frozen=True)
class ElementMeta:
    """Scaled ttk image-element geometry from the asset manifest."""

    width: int
    height: int
    border: int | tuple[int, ...]
    padding: int | tuple[int, ...]


@dataclass(frozen=True)
class RecolorResult:
    """Cached Tcl image name and its scaled element geometry."""

    image: str
    meta: ElementMeta


class RecolorRenderer:
    """Load, recolor, transform, and scale element templates."""

    _manifest = None
    _sources = {}

    @classmethod
    def _load_manifest(cls):
        if cls._manifest is None:
            cls._manifest = json.loads(
                (_ELEMENTS_DIR / "manifest.json").read_text(encoding="utf-8"))
        return cls._manifest

    @classmethod
    def info(cls, name):
        """Return the manifest entry for element `name`."""
        images = cls._load_manifest().get("images", {})
        try:
            return images[name]
        except KeyError:
            raise ValueError(
                f"unknown element asset {name!r}; not in assets/elements/manifest.json"
            ) from None

    @classmethod
    def source_dpi(cls):
        """Return the manifest's default source scale (template DPI multiplier)."""
        return float(cls._load_manifest().get("default_source_scale", 2.0))

    @classmethod
    def _source(cls, name):
        image = cls._sources.get(name)
        if image is None:
            info = cls.info(name)
            path = _ELEMENTS_DIR / info["file"]
            with Image.open(path) as source:
                image = source.convert("RGBA")
            expected = tuple(info.get("source_size", image.size))
            if image.size != expected:
                raise ValueError(
                    f"element asset {name!r} is {image.size}, manifest says {expected}"
                )
            cls._sources[name] = image
        return image

    @staticmethod
    def _validate_transform(transform):
        if transform not in _TRANSFORMS:
            valid = ", ".join(repr(value) for value in _TRANSFORMS)
            raise ValueError(f"unknown element transform {transform!r}; use {valid}")

    @staticmethod
    def _rotate_spec(value, transform):
        """Rotate 2- or 4-side border/padding metadata with the image."""
        if isinstance(value, int):
            return value
        values = tuple(value)
        if transform in ("rotate-90", "rotate-270"):
            if len(values) == 2:
                return (values[1], values[0])
            if len(values) == 4:
                left, top, right, bottom = values
                if transform == "rotate-90":
                    return (top, right, bottom, left)
                return (bottom, left, top, right)
        if transform == "rotate-180" and len(values) == 4:
            left, top, right, bottom = values
            return (right, bottom, left, top)
        if transform == "flip-x" and len(values) == 4:
            left, top, right, bottom = values
            return (right, top, left, bottom)
        return values

    @staticmethod
    def _scale_spec(value, scaling):
        def scaled(item):
            return scaling.logical(item, minimum=1) if item > 0 else 0

        if isinstance(value, int):
            return scaled(value)
        return tuple(scaled(item) for item in value)

    @classmethod
    def metadata(cls, name, scaling, transform=None):
        """Return `ElementMeta` for `name`, scaled and adjusted for `transform`."""
        cls._validate_transform(transform)
        info = cls.info(name)
        width, height = info["size"]
        if transform in ("rotate-90", "rotate-270"):
            width, height = height, width

        border = cls._rotate_spec(info.get("border", 0), transform)
        padding = cls._rotate_spec(info.get("padding", 0), transform)
        return ElementMeta(
            width=scaling.logical(width, minimum=1),
            height=scaling.logical(height, minimum=1),
            border=cls._scale_spec(border, scaling),
            padding=cls._scale_spec(padding, scaling),
        )

    @staticmethod
    def _channel_lut(low, high):
        return [round(low + (high - low) * value / 255) for value in range(256)]

    @classmethod
    def _recolor(cls, source, white, black, magenta):
        """Map source palette channels while retaining the original alpha."""
        black_rgb = ImageColor.getrgb(black)
        white_rgb = ImageColor.getrgb(white)
        gray = source.convert("L")
        channels = [
            gray.point(cls._channel_lut(black_rgb[index], white_rgb[index]))
            for index in range(3)
        ]
        red, green, blue, alpha = source.split()
        result = Image.merge("RGBA", (*channels, alpha))

        # The slider fill uses a magenta-to-white antialiased boundary: red and
        # blue stay 255 while green carries the interpolation amount.
        magenta_mask = red.point(lambda value: 255 if value == 255 else 0)
        blue_mask = blue.point(lambda value: 255 if value == 255 else 0)
        marker_mask = ImageChops.multiply(magenta_mask, blue_mask)
        green_zero = green.point(lambda value: 255 if value == 0 else 0)
        has_magenta = ImageChops.multiply(marker_mask, green_zero).getbbox() is not None
        if has_magenta and magenta is None:
            raise ValueError("element asset contains a magenta channel; provide magenta=")
        if magenta is not None:
            magenta_rgb = ImageColor.getrgb(magenta)
            marker_channels = [
                green.point(cls._channel_lut(magenta_rgb[index], white_rgb[index]))
                for index in range(3)
            ]
            marker = Image.merge("RGBA", (*marker_channels, alpha))
            result = Image.composite(marker, result, marker_mask)
        return result

    @classmethod
    def render(cls, name, size, white, black, magenta=None, transform=None):
        """Return a recolored RGBA image at final pixel `size`."""
        cls._validate_transform(transform)
        image = cls._recolor(cls._source(name), white, black, magenta)
        operation = _TRANSFORMS[transform]
        if operation is not None:
            image = image.transpose(operation)
        if image.size != tuple(size):
            image = image.resize(tuple(size), Resampling.LANCZOS)
        return image
