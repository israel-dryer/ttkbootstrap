"""Color model and theme definitions for ttkbootstrap.

Holds `Colors` (the color scheme plus color math), `ThemeDefinition` (the
name/colors/light-or-dark container the style engine consumes), and `Theme`
(a semantic-anchor theme family that generates light/dark `ThemeDefinition`s
from a handful of accent colors). Lowest layer of the `style` package.
"""
import colorsys
from collections.abc import Mapping
from dataclasses import dataclass, fields, replace
from functools import lru_cache
from types import MappingProxyType

from PIL import ImageColor

from ttkbootstrap import colorutils
from ttkbootstrap.constants import *


_TINT_WEIGHTS = {
    50: 0.90,
    100: 0.80,
    150: 0.70,
    200: 0.60,
    250: 0.50,
    300: 0.40,
    350: 0.30,
    400: 0.20,
    450: 0.10,
}
_SHADE_WEIGHTS = {
    550: 0.10,
    600: 0.20,
    650: 0.30,
    700: 0.40,
    750: 0.50,
    800: 0.60,
    850: 0.70,
    900: 0.80,
    950: 0.90,
}


def _normalize_color(color: str) -> str:
    """Return a Pillow-supported color as canonical lowercase hex."""
    r, g, b = ImageColor.getrgb(color)
    return f'#{r:02x}{g:02x}{b:02x}'


def _mix_colors(color1: str, color2: str, weight: float) -> str:
    """Mix two colors; weight is the fraction of color1."""
    r1, g1, b1 = ImageColor.getrgb(color1)
    r2, g2, b2 = ImageColor.getrgb(color2)
    channels = (
        round(r1 * weight + r2 * (1 - weight)),
        round(g1 * weight + g2 * (1 - weight)),
        round(b1 * weight + b2 * (1 - weight)),
    )
    return f'#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}'


def _tint(color: str, weight: float) -> str:
    """Mix `weight` of white into `color` (a lighter highlight)."""
    return _mix_colors('#ffffff', color, weight)


def _shade(color: str, weight: float) -> str:
    """Mix `weight` of black into `color` (a darker shade)."""
    return _mix_colors('#000000', color, weight)


@lru_cache(maxsize=256)
def _cached_color_ramp(anchor: str) -> Mapping[int, str]:
    """Build one immutable Bootstrap-compatible 50–950 color ramp."""
    ramp = {
        stop: _mix_colors(anchor, '#ffffff', 1 - target)
        for stop, target in _TINT_WEIGHTS.items()
    }
    ramp[500] = anchor
    ramp.update(
        {
            stop: _mix_colors(anchor, '#000000', 1 - target)
            for stop, target in _SHADE_WEIGHTS.items()
        }
    )
    return MappingProxyType(ramp)


def _color_ramp(color: str) -> Mapping[int, str]:
    """Return the cached private ramp for color."""
    return _cached_color_ramp(_normalize_color(color))


# The valid 50-950 ramp stops, in 50-step increments. Every stop is >= 50, and
# no hex/named color string is that long, so an int index of this magnitude is
# unambiguously a ramp request and never collides with ordinary str indexing
# (char indices 0-6, slices) -- which `RampColor` delegates to `str` untouched.
_RAMP_STOPS = frozenset(range(50, 1000, 50))


class RampColor(str):
    """A hex color string that also addresses its own 50-950 tint/shade ramp.

    Behaves as the plain color string everywhere it is used today
    (`str.__eq__`, formatting, `color[1:]` slicing, char indexing), so it is a
    drop-in for the previous `str` color values. Additionally, indexing with a
    ramp stop returns that step of the color's ramp, treating the color itself
    as the `[500]` anchor:

        c.primary          # '#2780e3'  (a str)
        c.primary[500]     # '#2780e3'  (the anchor, normalized)
        c.primary[300]     # a lighter tint
        c.primary[700]     # a darker shade
        c.primary[1:]      # '2780e3'   (ordinary str slicing, unchanged)

    Only int keys that are valid ramp stops (multiples of 50 in 50-950) are
    intercepted; every other key falls through to `str.__getitem__`.
    """

    __slots__ = ()

    def __getitem__(self, key):
        if isinstance(key, int) and key in _RAMP_STOPS:
            return _color_ramp(self)[key]
        return super().__getitem__(key)


def _as_ramp_color(value):
    """Wrap a color string as a `RampColor`; pass through non-strings/None."""
    if isinstance(value, str) and not isinstance(value, RampColor):
        return RampColor(value)
    return value


def _relative_luminance(color: str) -> float:
    """Return WCAG relative luminance for a Pillow-supported color."""
    channels = [value / 255 for value in ImageColor.getrgb(color)]

    def linearize(value: float) -> float:
        if value <= 0.03928:
            return value / 12.92
        return ((value + 0.055) / 1.055) ** 2.4

    r, g, b = (linearize(value) for value in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast_ratio(color1: str, color2: str) -> float:
    """Return the WCAG contrast ratio between two colors."""
    lum1 = _relative_luminance(color1)
    lum2 = _relative_luminance(color2)
    lighter, darker = max(lum1, lum2), min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def _color_to_hsl(color: str) -> tuple[int, int, int]:
    """Return hue, saturation, and lightness on 360/100/100 scales."""
    r, g, b = (value / 255 for value in ImageColor.getrgb(color))
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return int(hue * 360), int(saturation * 100), int(lightness * 100)


# On-color (filled-surface foreground) tuning. White is the conventional and
# perceptually better label on vivid accents, so it is preferred; black is used
# only where it is genuinely more readable. Two floors + a saturation gate,
# because WCAG relative luminance is not perceptual: it under-weights red/blue,
# so a raw max-contrast rule wrongly picks black on saturated blues/greens/reds
# (e.g. sandstone info #29abe0: black scores 8.0 vs white 2.6, yet white reads
# far better). Saturation separates a vivid accent from a light gray; the warm
# hue band keeps perceptually-light yellow/orange/lime on black.
_ON_COLOR_MIN_CONTRAST = 3.0   # white always wins at or above this ratio
_ON_COLOR_WHITE_FLOOR = 2.3    # marginal white still preferred for vivid accents
_ON_COLOR_SAT_FLOOR = 45       # below this a fill is near-neutral: use real contrast


def _accent_on_color(surface: str) -> str:
    """Return a readable filled-surface foreground, white-preferred.

    White wins whenever it clears the bold-text floor. When it is marginal,
    white is still chosen for vivid, non-warm accents (saturated blues, greens,
    and reds), where WCAG contrast understates its readability; otherwise black
    is used. Mode-independent — the choice depends only on the fill.
    """
    if _contrast_ratio('#ffffff', surface) >= _ON_COLOR_MIN_CONTRAST:
        return '#ffffff'
    hue, saturation, _ = _color_to_hsl(surface)
    warm = 20 <= hue <= 100  # orange/yellow/lime read light -> keep black
    if (
        saturation >= _ON_COLOR_SAT_FLOOR
        and not warm
        and _contrast_ratio('#ffffff', surface) >= _ON_COLOR_WHITE_FLOOR
    ):
        return '#ffffff'
    return '#000000'


def _border_color(surface: str) -> str:
    """Derive a neutral border by mixing a surface toward its on-color.

    The dedicated border derivation (bootstack parity): 84% surface + 16% of the
    surface's readable on-color, so a border is a subtle, mode-correct step off
    the surface -- never the accent, and desaturated toward the on-color rather
    than a raw lightness move that keeps a saturated surface saturated. This is
    the same formula as the `StyleBuilderTTK.border()` helper.
    """
    return _mix_colors(surface, _accent_on_color(surface), 0.84)


def _darken_color(color: str, percent: float) -> str:
    """Darken a color by reducing HLS lightness."""
    r, g, b = (value / 255 for value in ImageColor.getrgb(color))
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    lightness = max(0.0, lightness * (1 - percent))
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


def _lighten_color(color: str, percent: float) -> str:
    """Lighten a color by increasing HLS lightness."""
    r, g, b = (value / 255 for value in ImageColor.getrgb(color))
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    lightness = min(1.0, lightness + (1 - lightness) * percent)
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


def _state_color(color: str, state: str) -> str:
    """Port bootstack's luminance-directed active/pressed derivation."""
    delta = {'active': 0.08, 'pressed': 0.12}[state]
    if _relative_luminance(color) < 0.5:
        return _lighten_color(color, delta)
    return _darken_color(color, delta)


class Colors:
    """A class that defines the color scheme for a theme as well as
    provides several static methods for manipulating colors.

    A `Colors` object is attached to a `ThemeDefinition` and can also
    be accessed through the `Style.colors` property for the
    current theme.

    Examples:

        ```python
        style = Style()

        # dot-notation
        style.colors.primary

        # get method
        style.colors.get('primary')
        ```

        This class is an iterator, so you can iterate over the main
        style color labels (primary, secondary, success, info, warning,
        danger, light, dark):

        ```python
        for color_label in style.colors:
            color = style.colors.get(color_label)
            print(color_label, color)
        ```

        If, for some reason, you need to iterate over all theme color
        labels, then you can use the `Colors.label_iter` method. This
        will include all theme colors.

        ```python
        for color_label in style.colors.label_iter():
            color = style.colors.get(color_label)
            print(color_label, color)
        ```

        If you want to adjust the hsv values of an existing color by a
        specific percentage (delta), you can use the `Colors.update_hsv`
        method, which is static. In the example below, the "value delta"
        or `vd` is increased by 15%, which will lighten the color:

        ```python
        Colors.update_hsv("#9954bb", vd=0.15)
        ```
    """

    def __init__(
            self,
            primary,
            secondary,
            success,
            info,
            warning,
            danger,
            light,
            dark,
            bg,
            fg,
            selectbg,
            selectfg,
            border,
            inputfg,
            inputbg,
            active,
    ):
        """
        Parameters:

            primary (str):
                The primary theme color; used by default for all widgets.

            secondary (str):
                An accent color; commonly of a `grey` hue.

            success (str):
                An accent color; commonly of a `green` hue.

            info (str):
                An accent color; commonly of a `blue` hue.

            warning (str):
                An accent color; commonly of an `orange` hue.

            danger (str):
                An accent color; commonly of a `red` hue.

            light (str):
                An accent color.

            dark (str):
                An accent color.

            bg (str):
                Background color.

            fg (str):
                Default text color.

            selectfg (str):
                The color of selected text.

            selectbg (str):
                The background color of selected text.

            border (str):
                The color used for widget borders.

            inputfg (str):
                The text color for input widgets.

            inputbg (str):
                The text background color for input widgets.

            active (str):
                An accent color.
        """
        # Colors are stored as RampColor -- a str subclass that additionally
        # ramp-addresses (c.primary[300]); a no-op for every existing str use.
        self.primary = _as_ramp_color(primary)
        self.secondary = _as_ramp_color(secondary)
        self.success = _as_ramp_color(success)
        self.info = _as_ramp_color(info)
        self.warning = _as_ramp_color(warning)
        self.danger = _as_ramp_color(danger)
        self.light = _as_ramp_color(light)
        self.dark = _as_ramp_color(dark)
        self.bg = _as_ramp_color(bg)
        self.fg = _as_ramp_color(fg)
        self.selectbg = _as_ramp_color(selectbg)
        self.selectfg = _as_ramp_color(selectfg)
        self.border = _as_ramp_color(border)
        self.inputfg = _as_ramp_color(inputfg)
        self.inputbg = _as_ramp_color(inputbg)
        self.active = _as_ramp_color(active)

    @staticmethod
    def make_transparent(alpha, foreground, background='#ffffff'):
        """Simulate color transparency.
        
        Parameters:

            alpha (float):
                The amount of transparency; a number between 0 and 1.

            foreground (str):
                The foreground color.

            background (str):
                The background color.

        Returns:

            str:
                A hexadecimal color representing the "transparent" 
                version of the foreground color against the background 
                color.
        """
        fg = ImageColor.getrgb(foreground)
        bg = ImageColor.getrgb(background)
        rgb_float = [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(fg, bg)]
        rgb_int = [int(x) for x in rgb_float]
        return '#{:02x}{:02x}{:02x}'.format(*rgb_int)

    @staticmethod
    def rgb_to_hsv(r, g, b):
        """Convert an rgb to hsv color value.

        Parameters:
            r (float):
                red
            g (float):
                green
            b (float):
                blue

        Returns:
            tuple[float, float, float]: The hsv color value.
        """
        return colorsys.rgb_to_hsv(r, g, b)

    def get_luminance(self, color):
        """Calculate the luminance of a color.

        Parameters:
            color (str):
                A hexadecimal color value.
        Returns:
            float:
                The luminance value of the color.
        """
        r, g, b = self.hex_to_rgb(color)

        # Convert RGB to linear RGB
        r = self._get_luminance_value(r)
        g = self._get_luminance_value(g)
        b = self._get_luminance_value(b)

        # Calculate luminance using the WCAG formula
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _get_luminance_value(self, value):
        if value <= 0.03928:
            return value / 12.92
        else:
            return ((value + 0.055) / 1.055) ** 2.4

    def get_contrast_ration(self, lum1, lum2):
        """Calculate the contrast ratio between two luminance values.

        Parameters:
            lum1 (float):
                The first luminance value.
            lum2 (float):
                The second luminance value.

        Returns:
            float:
                The contrast ratio.
        """
        if lum1 > lum2:
            return (lum1 + 0.05) / (lum2 + 0.05)
        else:
            return (lum2 + 0.05) / (lum1 + 0.05)

    def get_foreground(self, color_label):
        """Return the appropriate foreground color for the specified
        color_label.

        Parameters:
            color_label (str):
                A color label corresponding to a class property

        Returns:
            str:
                A hexadecimal color value for the foreground color.

        Raises:
            TypeError: If the color_label is not a valid color property.
        """
        if color_label == LIGHT:
            return self.dark
        elif color_label == DARK:
            return self.light

        # local import breaks the theme<-engine cycle (engine imports theme)
        from ttkbootstrap.style.engine import Style

        if not Style().dynamic_foreground:
            return self.selectfg

        # dynamic foreground selection
        contrast_with_fg = self.get_contrast_ration(
            self.get_luminance(self.get(color_label)), self.get_luminance(self.fg)
        )
        contrast_with_selectfg = self.get_contrast_ration(
            self.get_luminance(self.get(color_label)), self.get_luminance(self.selectfg)
        )

        if contrast_with_fg > contrast_with_selectfg:
            return self.fg
        return self.selectfg

    def get(self, color_label: str):
        """Lookup a color value from the color name

        Parameters:

            color_label (str):
                A color label corresponding to a class property

        Returns:

            str:
                A hexadecimal color value.
        """
        return self.__dict__.get(color_label)

    def ramp(self, color_label: str) -> Mapping[int, str]:
        """Return the full immutable 50-950 tint/shade ramp for a color role.

        The role's current value is treated as the `[500]` anchor. Equivalent
        to reading each stop off the addressable color (`self.get(label)[stop]`)
        but returns the whole mapping at once.

        Parameters:

            color_label (str):
                A color label corresponding to a class property.

        Returns:

            Mapping[int, str]:
                An immutable mapping of ramp stop (50-950) to hex color.
        """
        return _color_ramp(self.get(color_label))

    def set(self, color_label: str, color_value: str):
        """Set a color property value. This does not update any existing
        widgets. Can also be used to create on-demand color properties
        that can be used in your program after creation.

        Parameters:

            color_label (str):
                The name of the color to be set (key)

            color_value (str):
                A hexadecimal color value
        """
        self.__dict__[color_label] = _as_ramp_color(color_value)

    def __iter__(self):
        return iter(
            [
                "primary",
                "secondary",
                "success",
                "info",
                "warning",
                "danger",
                "light",
                "dark",
            ]
        )

    def __repr__(self):
        out = tuple(zip(self.__dict__.keys(), self.__dict__.values()))
        return str(out)

    @staticmethod
    def label_iter():
        """Iterate over all color label properties in the Color class

        Returns:

            iter:
                An iterator for color label names
        """
        return iter(
            [
                "primary",
                "secondary",
                "success",
                "info",
                "warning",
                "danger",
                "light",
                "dark",
                "bg",
                "fg",
                "selectbg",
                "selectfg",
                "border",
                "inputfg",
                "inputbg",
                "active",
            ]
        )

    @staticmethod
    def hex_to_rgb(color: str):
        """Convert hexadecimal color to rgb color value

        Parameters:

            color (str):
                A hexadecimal color value

        Returns:

            tuple[float, float, float]:
                The rgb color value, each channel normalized to 0-1.
        """
        r, g, b = colorutils.color_to_rgb(color)
        return r / 255, g / 255, b / 255

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int):
        """Convert rgb to hexadecimal color value

        Parameters:

            r (int):
                red

            g (int):
                green

            b (int):
                blue

        Returns:

            str:
                A hexadecimal color value
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return colorutils.color_to_hex((r_, g_, b_))

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex
        color value by specifying the _delta_.

        Parameters:

            color (str):
                A hexadecimal color value to adjust.

            hd (float):
                % change in hue, _hue delta_.

            sd (float):
                % change in saturation, _saturation delta_.

            vd (float):
                % change in value, _value delta_.

        Returns:

            str:
                The resulting hexadecimal color value
        """
        r, g, b = Colors.hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # hue
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= 1 + hd

        # saturation
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= 1 + sd

        # value
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= 1 + vd

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Colors.rgb_to_hex(r, g, b)


class ThemeDefinition:
    """Encapsulates the name, color palette, and metadata for a
    ttkbootstrap theme.

    A ThemeDefinition is a lightweight container that pairs a theme name
    with its Colors object and whether it is a light or dark theme. The
    Style engine consumes ThemeDefinition instances to build widget
    styles and images for the active theme.
    """

    def __init__(self, name, colors, themetype=LIGHT):
        """
        Parameters:

            name (str):
                The name of the theme.

            colors (Colors or dict):
                A Colors instance or a dict of color values.

            themetype (str):
                Specifies whether the theme is **light** or **dark**.
        """
        self.name = name
        self.colors = colors if isinstance(colors, Colors) else Colors(**colors)
        self.type = themetype

    def __repr__(self):
        return " ".join(
            [
                f"name={self.name},",
                f"type={self.type},",
                f"colors={self.colors}",
            ]
        )


# --- Semantic-anchor theme model (Workstream E, PR E2) ----------------------
#
# A `Theme` family declares its accent colors once (as `[500]` ramp anchors)
# plus a light/dark {background, foreground} block, and generates a resolved
# `ThemeDefinition` per mode. The 16 legacy `Colors` fields are *derived* here
# from the anchors + surface, so the builders are untouched -- only how `Colors`
# is populated changes. Mechanism ported from bootstack; the ramp/surface math
# is the in-repo color-helper code above.

_ACCENT_ROLES = ("primary", "success", "info", "warning", "danger")

# Which ramp step a SOLID fill uses per mode. On light a darker step reads
# against a light bg; on dark a brighter step reads against a dark bg.
# warning/info stay at [500] on light -- they carry dark on-color at any shade,
# so darkening only mutes them.
_SOLID_STOP = {
    "light": {"primary": 600, "success": 600, "danger": 600, "info": 500, "warning": 500},
    "dark":  {"primary": 400, "success": 400, "danger": 400, "info": 400, "warning": 400},
}
_SECONDARY_STOP = {"light": 700, "dark": 400}  # neutral step for an uncolored secondary
_LIGHT_ACCENT_STOP = 100  # the pale-gray `light` accent role (both modes)
_DARK_ACCENT_STOP = 800   # the dark-gray `dark` accent role (both modes)

# Surface-derivation knobs. Hue/saturation-preserving lightness moves off the
# authored background (NOT a tint toward white -- that would desaturate a
# themed dark field, the regression Workstream E was chartered to fix). Initial
# values; confirmed/tuned in the human visual gate. `border` is not a lightness
# move: it uses the dedicated `_border_color` (mix toward the on-color).
_INPUT_LIFT = 0.03    # dark inputbg lift off bg
_ACTIVE_MIX = 0.06    # light active/hover darken
_ACTIVE_MIX_D = 0.09  # dark active/hover lighten

_DEFAULT_NEUTRAL = "#adb5bd"  # gray anchor when a family omits `neutral`


def _generate_colors(mode, anchors, neutral, background, foreground, secondary=None):
    """Derive the 16 `Colors` fields for one mode from semantic anchors.

    Parameters:
        mode: ``"light"`` or ``"dark"``.
        anchors: mapping of accent role -> `[500]` anchor hex (the 5 accents).
        neutral: gray anchor hex for the neutral ramp.
        background/foreground: the authored surface block, hex.
        secondary: optional colored secondary anchor; when None, `secondary`
            derives from the neutral ramp.

    Returns:
        Colors: the resolved per-mode color scheme.
    """
    solid = _SOLID_STOP[mode]

    def step(color, stop):
        return _color_ramp(color)[stop]

    primary = step(anchors["primary"], solid["primary"])
    if secondary:
        secondary_c = step(secondary, solid["primary"])
    else:
        secondary_c = step(neutral, _SECONDARY_STOP[mode])

    bg = _normalize_color(background)
    fg = _normalize_color(foreground)
    border = _border_color(bg)
    if mode == "dark":
        inputbg = _lighten_color(bg, _INPUT_LIFT)
        active = _lighten_color(bg, _ACTIVE_MIX_D)
    else:
        inputbg = bg
        active = _darken_color(bg, _ACTIVE_MIX)

    # selectbg is NOT just the selection highlight: the builders reuse it as a
    # neutral surface for dark-mode borders and for scale/progress/label troughs
    # (`shade(selectbg)`). It must stay neutral, or the accent bleeds into every
    # trough and border -- so derive it from the neutral ramp, decoupled from a
    # colored `secondary`.
    selectbg = step(neutral, _SECONDARY_STOP[mode])
    return Colors(
        primary=primary,
        secondary=secondary_c,
        success=step(anchors["success"], solid["success"]),
        info=step(anchors["info"], solid["info"]),
        warning=step(anchors["warning"], solid["warning"]),
        danger=step(anchors["danger"], solid["danger"]),
        light=step(neutral, _LIGHT_ACCENT_STOP),
        dark=step(neutral, _DARK_ACCENT_STOP),
        bg=bg,
        fg=fg,
        selectbg=selectbg,
        selectfg=_accent_on_color(selectbg),
        border=border,
        inputfg=fg,
        inputbg=inputbg,
        active=active,
    )


@dataclass
class Theme:
    """A semantic-anchor color theme *family* declared in code.

    Declare the accent colors once (as the `[500]` midpoint of each ramp) plus a
    `light` and/or `dark` `{background, foreground}` block; the family generates
    a well-contrasted `ThemeDefinition` per mode (`<name>-light` /
    `<name>-dark`). The per-mode ramp step for solids, borders, and inputs is
    chosen automatically -- there is no per-mode shade boilerplate.

    Examples:

        ```python
        Theme(
            name="pulse",
            primary="#593196", success="#13b955", info="#009cdc",
            warning="#efa31d", danger="#fc3939",
            light=dict(background="#ffffff", foreground="#17141f"),
            dark=dict(background="#17141f", foreground="#e9ecef"),
        ).register()   # registers pulse-light + pulse-dark on the live Style
        ```

    Parameters:

        name (str):
            Family name; generated variants are ``<name>-light`` /
            ``<name>-dark``.
        primary, success, info, warning, danger (str):
            Accent `[500]` anchor colors (hex).
        secondary (str):
            Optional colored secondary accent (hex). When omitted, `secondary`
            derives from the neutral ramp.
        neutral (str):
            Gray base for the neutral ramp (secondary, the light/dark accents).
        light, dark (dict):
            ``{'background': ..., 'foreground': ...}`` for that variant, or None
            to skip it.
    """

    name: str
    primary: str = None
    success: str = None
    info: str = None
    warning: str = None
    danger: str = None
    secondary: str = None
    neutral: str = _DEFAULT_NEUTRAL
    light: dict = None
    dark: dict = None

    def _definition(self, mode):
        block = self.light if mode == "light" else self.dark
        if block is None:
            return None
        if "background" not in block or "foreground" not in block:
            raise ValueError(
                f"Theme {self.name!r} {mode} block must define both "
                f"'background' and 'foreground'."
            )
        anchors = {role: getattr(self, role) for role in _ACCENT_ROLES}
        missing = [role for role, value in anchors.items() if not value]
        if missing:
            raise ValueError(
                f"Theme {self.name!r} is missing accent anchor(s): "
                f"{', '.join(missing)}."
            )
        colors = _generate_colors(
            mode, anchors, self.neutral,
            block["background"], block["foreground"], self.secondary,
        )
        return ThemeDefinition(name=f"{self.name}-{mode}", colors=colors, themetype=mode)

    def to_definitions(self):
        """Return the generated per-mode `ThemeDefinition`s (light, then dark).

        A family that declares only one block yields a single definition.
        """
        return [d for d in (self._definition("light"), self._definition("dark")) if d]

    def register(self):
        """Register the generated variants on the live `Style` singleton.

        Returns this theme so ``theme = Theme(...).register()`` reads cleanly.
        Raises `RuntimeError` if no `Style` has been created yet.
        """
        # local import breaks the theme<-engine cycle (engine imports theme)
        from ttkbootstrap.style.engine import Style

        style = Style.get_instance()
        if style is None:
            raise RuntimeError(
                "No Style instance yet; create a Window/Style before registering "
                "a Theme, or add it to the built-in catalog."
            )
        definitions = self.to_definitions()
        if not definitions:
            raise ValueError(
                f"Theme {self.name!r} defines neither a 'light' nor a 'dark' block."
            )
        for definition in definitions:
            style.register_theme(definition)
        return self

    @classmethod
    def from_existing(cls, base: "Theme", *, name: str, **overrides) -> "Theme":
        """Derive a new family from an existing `Theme`, overriding some tokens.

        Every token not overridden is inherited from `base`, so a built-in can
        be re-branded by changing just its `primary` (and anything else).

        Examples:

            ```python
            Theme.from_existing(BOOTSTRAP, name="acme", primary="#ff5722")
            ```
        """
        unknown = set(overrides) - {f.name for f in fields(cls)}
        if unknown:
            raise ValueError(f"Unknown Theme token(s): {', '.join(sorted(unknown))}.")
        return replace(base, name=name, **overrides)
