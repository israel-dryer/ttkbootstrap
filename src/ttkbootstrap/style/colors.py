import colorsys
from ttkbootstrap.constants import *

class Colors:
    """A class that contains the theme colors as well as several
    helper methods for manipulating colors.
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
    ):
        """This class is attached to the ``Style`` object at run-time
        for the selected theme, and so is available to use with
        ``Style.colors``. The colors can be accessed via dot notation
        or get method:

        .. code-block:: python

            # dot-notation
            Colors.primary

            # get method
            Colors.get('primary')

        This class is an iterator, so you can iterate over the main
        style color labels (primary, secondary, success, info, warning,
        danger):

        .. code-block:: python

            for color_label in Colors:
                color = Colors.get(color_label)
                print(color_label, color)

        If, for some reason, you need to iterate over all theme color
        labels, then you can use the ``Colors.label_iter`` method. This
        will include all theme colors.

        .. code-block:: python

            for color_label in Colors.label_iter():
                color = Colors.get(color_label)
                print(color_label, color)

        Parameters
        ----------
        primary : str
            The primary theme color; used by default for all widgets.

        secondary : str
            An accent color; commonly of a `grey` hue.

        success : str
            An accent color; commonly of a `green` hue.

        info : str
            An accent color; commonly of a `blue` hue.

        warning : str
            An accent color; commonly of an `orange` hue.

        danger : str
            An accent color; commonly of a `red` hue.

        light : str
            An accent color.

        dark : str
            An accent color.

        bg : str
            Background color.

        fg : str
            Default text color.

        selectfg : str
            The color of selected text.

        selectbg : str
            The background color of selected text.

        border : str
            The color used for widget borders.

        inputfg : str
            The text color for input widgets.

        inputbg : str
            The text background color for input widgets.
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

    def rgb_to_hsv(r, g, b):
        return colorsys.rgb_to_hsv(r, g, b)

    def get_foreground(self, color_label: str):
        """Return the appropriate foreground color for the specified
        color_label.

        Parameters
        ----------
        color_label : str
            A color label corresponding to a class property
        """
        if color_label == LIGHT:
            return self.dark
        elif color_label == DARK:
            return self.light
        else:
            return self.selectfg

    def get(self, color_label):
        """Lookup a color property

        Parameters
        ----------
        color_label : str
            A color label corresponding to a class propery

        Returns
        -------
        str
            A hexadecimal color value.
        """
        return self.__dict__.get(color_label)

    def set(self, color_label, color_value):
        """Set a color property

        Parameters
        ----------
        color_label : str
            The name of the color to be set (key)

        color_value : str
            A hexadecimal color value
        """
        self.__dict__[color_label] = color_value

    def __iter__(self):
        return iter(
            ["primary", "secondary", "success", "info", "warning", "danger",
             "light", "dark"]
        )

    def __repr__(self):
        out = tuple(zip(self.__dict__.keys(), self.__dict__.values()))
        return str(out)

    @staticmethod
    def label_iter():
        """Iterate over all color label properties in the Color class

        Returns
        -------
        iter
            An iterator representing the name of the color properties
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
            ]
        )

    @staticmethod
    def hex_to_rgb(color):
        """Convert hexadecimal color to rgb color value

        Parameters
        ----------
        color : str
            A hexadecimal color value

        Returns
        -------
        tuple[int, int, int]
            An rgb color value.
        """
        if len(color) == 4:
            # 3 digit hexadecimal colors
            r = round(int(color[1], 16) / 255, 2)
            g = round(int(color[2], 16) / 255, 2)
            b = round(int(color[3], 16) / 255, 2)
        else:
            # 6 digit hexadecimal colors
            r = round(int(color[1:3], 16) / 255, 2)
            g = round(int(color[3:5], 16) / 255, 2)
            b = round(int(color[5:], 16) / 255, 2)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r, g, b):
        """Convert rgb to hexadecimal color value

        Parameters
        ----------
        r : int
            red

        g : int
            green

        b : int
            blue

        Returns:
            str: a hexadecimal colorl value
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return "#{:02x}{:02x}{:02x}".format(r_, g_, b_)

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex
        color value.

        Parameters
        ----------
        color : str
            A hexadecimal color value to adjust.

        hd : float
            % change in hue

        sd : float
            % change in saturation

        vd : float
            % change in value

        Returns
        -------
        str
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