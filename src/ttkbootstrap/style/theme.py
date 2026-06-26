"""Color model and theme definition for ttkbootstrap.

Holds `Colors` (the color scheme plus color math) and `ThemeDefinition` (the
name/colors/light-or-dark container the style engine consumes). Lowest layer of
the `style` package; the semantic-anchor `Theme` model (Workstream E) will grow
here. Split out of the monolithic `style.py` in 2.0.
"""
import colorsys

from PIL import ImageColor

from ttkbootstrap import colorutils
from ttkbootstrap.constants import *


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
        danger):

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
            color = Colors.get(color_label)
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
        self.primary = primary
        self.secondary = secondary
        self.success = success
        self.info = info
        self.warning = warning
        self.danger = danger
        self.light = light
        self.dark = dark
        self.bg = bg
        self.fg = fg
        self.selectbg = selectbg
        self.selectfg = selectfg
        self.border = border
        self.inputfg = inputfg
        self.inputbg = inputbg
        self.active = active

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
                A color label corresponding to a class propery

        Returns:

            str:
                A hexadecimal color value.
        """
        return self.__dict__.get(color_label)

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
        self.__dict__[color_label] = color_value

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

            tuple[int, int, int]:
                An rgb color value.
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
