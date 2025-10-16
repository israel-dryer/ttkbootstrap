import colorsys
import json
import re
import tkinter as tk
from math import ceil
from tkinter import TclError, font, ttk
from typing import Any, Callable

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageTk
from PIL.Image import Resampling, Transpose

from ttkbootstrap import colorutils, utility as util
from ttkbootstrap.constants import *
from ttkbootstrap.publisher import Channel, Publisher
from ttkbootstrap.themes.standard import STANDARD_THEMES

try:
    # prevent app from failing if user.py gets corrupted
    from ttkbootstrap.themes.user import USER_THEMES
except (ImportError, ModuleNotFoundError):
    USER_THEMES = {}


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
            Tuple[float, float, float]: The hsv color value.
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
    """A class to provide defined name, colors, and font settings for a
    ttkbootstrap theme."""

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


class Style(ttk.Style):
    """A singleton class for creating and managing the application
    theme and widget styles.

    This class is meant to be a drop-in replacement for `ttk.Style` and
    inherits all of it's methods and properties. However, in
    ttkbootstrap, this class is implemented as a singleton. Subclassing
    is not recommended and may have unintended consequences.

    Examples:

        ```python
        # instantiate the style with default theme
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='superhero')

        # check all available themes
        for theme in style.theme_names():
            print(theme)
        ```

    See the [Python documentation](https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Style)
    on this class for more details.
    """

    instance = None

    def __new__(cls, theme=None):
        if Style.instance is None:
            return object.__new__(cls)
        else:
            return Style.instance

    def __init__(self, theme=DEFAULT_THEME):
        """
        Parameters:

            theme (str):
                The name of the theme to use when styling the widget.
        """
        if Style.instance is not None:
            if theme != DEFAULT_THEME:
                Style.instance.theme_use(theme)
            return
        self._theme_objects = {}
        self._theme_definitions = {}
        self._style_registry = set()  # all styles used
        self._theme_styles = {}  # styles used in theme
        self._theme_names = set()
        self._load_themes()
        self._dynamic_foreground = False
        super().__init__()

        Style.instance = self
        self.theme_use(theme)

        # apply localization
        from ttkbootstrap import localization
        localization.initialize_localities()

    @property
    def colors(self):
        """An object that contains the colors used for the current
        theme.

        Returns:

            Colors:
                The colors object for the current theme.
        """
        theme = self.theme.name
        if theme in list(self._theme_names):
            definition = self._theme_definitions.get(theme)
            if not definition:
                return []  # TODO refactor this
            else:
                return definition.colors
        else:
            return []  # TODO refactor this

    def configure(self, style, query_opt: Any = None, **kw):
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

        if not self.style_exists_in_theme(style):
            ttkstyle = Bootstyle.update_ttk_widget_style(None, style)
        else:
            ttkstyle = style

        if ttkstyle == style:
            # configure an existing ttkbootrap theme
            return super().configure(style, query_opt=query_opt, **kw)
        else:
            # subclass a ttkbootstrap theme
            result = super().configure(style, query_opt=query_opt, **kw)
            self._register_ttkstyle(style)
            return result

    def theme_names(self):
        """Return a list of all ttkbootstrap themes.

        Returns:

            List[str, ...]:
                A list of theme names.
        """
        return list(self._theme_definitions.keys())

    def register_theme(self, definition):
        """Register a theme definition for use by the `Style`
        object. This makes the definition and name available at
        run-time so that the assets and styles can be created when
        needed.

        Parameters:

            definition (ThemeDefinition):
                A `ThemeDefinition` object.
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during*
        runtime. Otherwise, pass the theme name into the Style
        constructor to instantiate the style with a theme.

        Parameters:

            themename (str):
                The name of the theme to apply when creating new widgets

        Returns:

            Union[str, None]:
                The name of the current theme if `themename` is None
                otherwise, `None`.
        """
        if not themename:
            # return current theme
            return super().theme_use()

        # change to an existing theme
        existing_themes = super().theme_names()
        if themename in existing_themes:
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        # setup a new theme
        elif themename in self._theme_names:
            self.theme = self._theme_definitions.get(themename)
            self._theme_objects[themename] = StyleBuilderTTK()
            self._create_ttk_styles_on_theme_change()
            Publisher.publish_message(Channel.STD)
        else:
            raise TclError(themename, "is not a valid theme.")

    def theme_create(self, themename: str, parent: str = None, settings: dict = None) -> None:
        """
        Create a new theme in the Tcl interpreter. If the parent is a registered
        ttkbootstrap theme, the new theme will be registered with a copied
        ThemeDefinition and builder. Duplicate registration is avoided.

        Parameters:

            themename (str):
                The name of the new theme.

            parent (str):
                The name of the parent theme to inherit from.

            settings (dict):
                A dictionary of style settings (Tcl-style).
        """
        from tkinter.ttk import _script_from_settings  # type: ignore[attr-defined]

        script = _script_from_settings(settings) if settings else ''

        # Lazy-load parent if it's a known bootstrap theme
        if parent:
            if parent not in super().theme_names():
                if parent in self._theme_names:
                    self.theme_use(parent)
                else:
                    raise TclError(f"{parent!r} is not a valid theme name or parent theme.")

        # Create the Tcl-level theme
        if parent:
            self.tk.call(
                self._name, "theme", "create", themename,
                "-parent", parent, "-settings", script)
        else:
            self.tk.call(
                self._name, "theme", "create", themename,
                "-settings", script)

        # Register the new theme if copying from a ttkbootstrap theme
        if parent in self._theme_definitions and themename not in self._theme_definitions:
            parent_def = self._theme_definitions[parent]
            copied_def = ThemeDefinition(
                name=themename,
                colors=parent_def.colors,
                themetype=parent_def.type
            )
            self._theme_definitions[themename] = copied_def
            self._theme_names.add(themename)
            self._theme_styles[themename] = set()

            if themename not in self._theme_objects:
                self._theme_objects[themename] = StyleBuilderTTK(build=False)

    def style_exists_in_theme(self, ttkstyle: str):
        """Check if a style exists in the current theme.

        Parameters:

            ttkstyle (str):
                The ttk style to check.

        Returns:

            bool:
                `True` if the style exists, otherwise `False`.
        """
        if self.theme is None:
            return False

        theme_styles = self._theme_styles.get(self.theme.name)
        if theme_styles is None:
            return False

        exists_in_theme = ttkstyle in theme_styles
        exists_in_registry = ttkstyle in self._style_registry
        return exists_in_theme and exists_in_registry

    def use_dynamic_foreground(self, enable: bool = True):
        """Enable or disable dynamic foreground color selection.

        When enabled, the foreground color of widgets will be decided
        between the `fg` and `selectfg` colors based on the
        contrast ratio with the widget's background color.
        At default, this is disabled.

        Parameters:

            enable (bool):
                If `True`, dynamic foreground selection is enabled.
                Otherwise, it is disabled.
        """
        self._dynamic_foreground = enable

    @property
    def dynamic_foreground(self):
        """Returns `True` if dynamic foreground selection is enabled,
        otherwise `False`.
        """
        return self._dynamic_foreground

    @staticmethod
    def get_instance():
        """Returns and instance of the style class"""
        return Style.instance

    @staticmethod
    def _get_builder():
        """Get the object that builds the widget styles for the current
        theme.

        Returns:

            ThemeBuilderTTK:
                The theme builder object that builds the ttk styles for
                the current theme.
        """
        style: Style = Style.get_instance()
        theme_name = style.theme.name
        return style._theme_objects[theme_name]

    @staticmethod
    def _get_builder_tk():
        """Get the object that builds the widget styles for the current
        theme.

        Returns:

            ThemeBuilderTK:
                The theme builder object that builds the ttk styles for
                the current theme.
        """
        builder = Style._get_builder()
        return builder.builder_tk

    def _build_configure(self, style, **kw):
        """Calls configure of superclass; used by style builder classes."""
        super().configure(style, **kw)

    def _load_themes(self, EXTERNAL_THEMES=None):
        """Load all ttkbootstrap defined themes"""
        # create a theme definition object for each theme, this will be
        # used to generate the theme in tkinter along with any assets
        # at run-time
        if USER_THEMES:
            STANDARD_THEMES.update(USER_THEMES)

        if EXTERNAL_THEMES:
            STANDARD_THEMES.update(EXTERNAL_THEMES)

        theme_settings = {"themes": STANDARD_THEMES}
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    colors=definition["colors"],
                )
            )

    def _register_ttkstyle(self, ttkstyle):
        """Register that a ttk style name. This ensures that the
        builder will not attempt to build a style that has already
        been created.

        Parameters:

            ttkstyle (str):
                The name of the ttk style to register.
        """
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)

    def _create_ttk_styles_on_theme_change(self):
        """Create existing styles when the theme changes"""
        for ttkstyle in self._style_registry:
            if not self.style_exists_in_theme(ttkstyle):
                color = Bootstyle.ttkstyle_widget_color(ttkstyle)
                method_name = Bootstyle.ttkstyle_method_name(string=ttkstyle)
                builder: StyleBuilderTTK = self._get_builder()
                method: Callable = builder.name_to_method(method_name)
                method(builder, color)

    def load_user_theme(self, theme: ThemeDefinition):
        """Load a user theme definition"""
        self.register_theme(theme)

    def load_user_themes(self, file):
        """Load user themes saved in json format"""
        with open(file, encoding='utf-8') as f:
            data = json.load(f)
            themes = data['themes']
        for theme in themes:
            for name, definition in theme.items():
                self.register_theme(
                    ThemeDefinition(
                        name=name,
                        themetype=definition["type"],
                        colors=definition["colors"],
                    )
                )


class StyleBuilderTK:
    """A class for styling legacy tkinter widgets (not ttk).

    The methods in this classed are used internally to update tk widget
    style configurations and are not intended to be called by the end
    user.

    All legacy tkinter widgets are updated with a callback whenever the
    theme is changed. The color configuration of the widget is updated
    to match the current theme. Legacy ttk widgets are not the primary
    focus of this library, however, an attempt was made to make sure they
    did not stick out amongst ttk widgets if used.

    Some ttk widgets contain legacy components that must be updated
    such as the Combobox popdown, so this ensures they are styled
    completely to match the current theme.
    """

    def __init__(self):
        self.style = Style.get_instance()
        self.master = self.style.master

    @property
    def theme(self) -> ThemeDefinition:
        """A reference to the `ThemeDefinition` object for the current
        theme."""
        return self.style.theme

    @property
    def colors(self) -> Colors:
        """A reference to the `Colors` object for the current theme."""
        return self.style.colors

    @property
    def is_light_theme(self) -> bool:
        """Returns `True` if the theme is _light_, otherwise `False`."""
        return self.style.theme.type == LIGHT

    def update_tk_style(self, widget: tk.Tk):
        """Update the window style.

        Parameters:

            widget (tkinter.Tk):
                The tk object to update.
        """
        widget.configure(background=self.colors.bg)
        # add default initial font for text widget
        widget.option_add('*Text*Font', 'TkDefaultFont')

    def update_toplevel_style(self, widget: tk.Toplevel):
        """Update the toplevel style.

        Parameters:

            widget (tkinter.Toplevel):
                The toplevel object to update.
        """
        widget.configure(background=self.colors.bg)

    def update_canvas_style(self, widget: tk.Canvas):
        """Update the canvas style.

        Parameters:

            widget (tkinter.Canvas):
                The canvas object to update.
        """
        # if self.is_light_theme:
        #     bordercolor = self.colors.border
        # else:
        #     bordercolor = self.colors.selectbg

        widget.configure(
            background=self.colors.bg,
            highlightthickness=0,
            # highlightbackground=bordercolor,
        )

    def update_button_style(self, widget: tk.Button):
        """Update the button style.

        Parameters:

            widget (tkinter.Button):
                The button object to update.
        """
        background = self.colors.primary
        foreground = self.colors.selectfg
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)

        widget.configure(
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=activebackground,
            highlightbackground=self.colors.selectfg,
        )

    def update_label_style(self, widget: tk.Label):
        """Update the label style.

        Parameters:

            widget (tkinter.Label):
                The label object to update.
        """
        widget.configure(foreground=self.colors.fg, background=self.colors.bg)

    def update_frame_style(self, widget: tk.Frame):
        """Update the frame style.

        Parameters:

            widget (tkinter.Frame):
                The frame object to update.
        """
        widget.configure(background=self.colors.bg)

    def update_checkbutton_style(self, widget: tk.Checkbutton):
        """Update the checkbutton style.

        Parameters:

            widget (tkinter.Checkbutton):
                The checkbutton object to update.
        """
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg,
        )

    def update_radiobutton_style(self, widget: tk.Radiobutton):
        """Update the radiobutton style.

        Parameters:

            widget (tkinter.Radiobutton):
                The radiobutton object to update.
        """
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg,
        )

    def update_entry_style(self, widget: tk.Entry):
        """Update the entry style.

        Parameters:

            widget (tkinter.Entry):
                The entry object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            relief=tk.FLAT,
            highlightthickness=1,
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=1,
        )

    def update_scale_style(self, widget: tk.Scale):
        """Update the scale style.

        Parameters:

            widget (tkinter.scale):
                The scale object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        activecolor = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            showvalue=False,
            sliderrelief=tk.FLAT,
            borderwidth=0,
            activebackground=activecolor,
            highlightthickness=1,
            highlightcolor=bordercolor,
            highlightbackground=bordercolor,
            troughcolor=self.colors.inputbg,
        )

    def update_spinbox_style(self, widget: tk.Spinbox):
        """Update the spinbox style.

        Parameters:

            widget (tkinter.Spinbox):
                THe spinbox object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            relief=tk.FLAT,
            highlightthickness=1,
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            buttonbackground=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=1,
            # these options should work, but do not have any affect
            buttonuprelief=tk.FLAT,
            buttondownrelief=tk.SUNKEN,
        )

    def update_listbox_style(self, widget: tk.Listbox):
        """Update the listbox style.

        Parameters:

            widget (tkinter.Listbox):
                The listbox object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            foreground=self.colors.inputfg,
            background=self.colors.inputbg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            highlightcolor=self.colors.primary,
            highlightbackground=bordercolor,
            highlightthickness=1,
            activestyle="none",
            relief=tk.FLAT,
        )

    def update_menubutton_style(self, widget: tk.Menubutton):
        """Update the menubutton style.

        Parameters:

            widget (tkinter.Menubutton):
                The menubutton object to update.
        """
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            foreground=self.colors.selectfg,
            activebackground=activebackground,
            activeforeground=self.colors.selectfg,
            borderwidth=0,
        )

    def update_menu_style(self, widget: tk.Menu):
        """Update the menu style.

        Parameters:

            widget (tkinter.Menu):
                The menu object to update.
        """
        widget.configure(
            tearoff=False,
            activebackground=self.colors.selectbg,
            activeforeground=self.colors.selectfg,
            foreground=self.colors.fg,
            selectcolor=self.colors.primary,
            background=self.colors.bg,
            relief=tk.FLAT,
            borderwidth=0,
        )

    def update_labelframe_style(self, widget: tk.LabelFrame):
        """Update the labelframe style.

        Parameters:

            widget (tkinter.LabelFrame):
                The labelframe object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            highlightcolor=bordercolor,
            foreground=self.colors.fg,
            borderwidth=1,
            highlightthickness=0,
            background=self.colors.bg,
        )

    def update_text_style(self, widget: tk.Text):
        """Update the text style.

        Parameters:

            widget (tkinter.Text):
                The text object to update.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        focuscolor = widget.cget("highlightbackground")

        if focuscolor in ["SystemButtonFace", bordercolor]:
            focuscolor = bordercolor

        widget.configure(
            background=self.colors.inputbg,
            foreground=self.colors.inputfg,
            highlightcolor=focuscolor,
            highlightbackground=bordercolor,
            insertbackground=self.colors.inputfg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            insertwidth=1,
            highlightthickness=1,
            relief=tk.FLAT,
            padx=5,
            pady=5,
            # font="TkDefaultFont",
        )


class StyleBuilderTTK:
    """A class containing methods for building new ttk widget styles on
    demand.

    The methods in this classed are used internally to generate ttk
    widget styles on-demand and are not intended to be called by the end
    user.
    """

    def __init__(self, build: bool = True):
        self.style: Style = Style.get_instance()
        self.theme_images = {}
        self.builder_tk = StyleBuilderTK()

        if build:
            self.create_theme()

    @staticmethod
    def name_to_method(method_name):
        """Get a method by name.

        Parameters:

            method_name (str):
                The name of the style builder method.

        Returns:

            Callable:
                The method that is named by `method_name`
        """
        func = getattr(StyleBuilderTTK, method_name)
        return func

    @property
    def colors(self) -> Colors:
        """A reference to the `Colors` object of the current theme."""
        return self.style.theme.colors

    @property
    def theme(self) -> ThemeDefinition:
        """A reference to the `ThemeDefinition` object for the current
        theme."""
        return self.style.theme

    @property
    def is_light_theme(self) -> bool:
        """If the current theme is _light_, returns `True`, otherwise
        returns `False`."""
        return self.style.theme.type == LIGHT

    def scale_size(self, size):
        """Scale the size of images and other assets based on the
        scaling factor of ttk to ensure that the image matches the
        screen resolution.

        Parameters:

            size (Union[int, List, Tuple]):
                A single integer or an iterable of integers
        """
        winsys = self.style.master.tk.call("tk", "windowingsystem")
        if winsys == "aqua":
            BASELINE = 1.000492368291482
        else:
            BASELINE = 1.33398982438864281
        scaling = self.style.master.tk.call("tk", "scaling")
        factor = scaling / BASELINE

        if isinstance(size, int) or isinstance(size, float):
            return ceil(size * factor)
        elif isinstance(size, tuple) or isinstance(size, list):
            return [ceil(x * factor) for x in size]

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal
        style methods.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self):
        """This method is called internally every time the theme is
        changed to update various components included in the body of
        the method."""
        self.create_default_style()

    def create_default_style(self):
        """Setup the default widget style configuration for the root
        ttk style "."; these defaults are applied to any widget that
        contains the configuration options updated by this style. This
        method should be called *first* before any other style is applied
        during theme creation.
        """
        self.style._build_configure(
            style=".",
            background=self.colors.bg,
            darkcolor=self.colors.border,
            foreground=self.colors.fg,
            troughcolor=self.colors.bg,
            selectbg=self.colors.selectbg,
            selectfg=self.colors.selectfg,
            selectforeground=self.colors.selectfg,
            selectbackground=self.colors.selectbg,
            fieldbg="white",
            borderwidth=1,
            focuscolor="",
        )
        # this is general style applied to the tableview
        self.create_link_button_style()
        self.style.configure("symbol.Link.TButton", font="-size 16")

        # this is the general style applied to the tooltip
        self.create_label_style()
        self.style.configure(
            style="tooltip.TLabel",
            background="#fffddd",
            foreground="#333",
            bordercolor="#888",
            borderwidth=1,
            darkcolor="#fffddd",
            lightcolor="#fffddd",
            relief=RAISED,
        )

    def create_combobox_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Combobox widget.

        Parameters:

            colorname (str):
                The color label to use as the primary widget color.
        """
        STYLE = "TCombobox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.get(colorname)

        # Create custom arrow assets since the default ones don't work with Tcl/Tk bundled in python 3.13
        arrow_images = self.create_simple_arrow_assets(
            self.colors.inputfg,
            disabled_fg,
            focuscolor,
        )
        downarrow_image = arrow_images[0][1]
        downarrow_disabled_image = arrow_images[1][1]
        downarrow_focused_image = arrow_images[2][1]
        self.style.element_create(
            f"{element}.downarrow",
            "image",
            downarrow_image,
            ("disabled", downarrow_disabled_image),
            ("pressed !disabled", downarrow_focused_image),
            ("focus !disabled", downarrow_focused_image),
            ("hover !disabled", downarrow_focused_image),
        )
        #  self.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # doesn't work in python 3.13
        self.style.element_create(f"{element}.padding", "from", TTK_CLAM)
        self.style.element_create(f"{element}.textarea", "from", TTK_CLAM)

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        self.style._build_configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            foreground=self.colors.inputfg,
            fieldbackground=self.colors.inputbg,
            background=self.colors.inputbg,
            insertcolor=self.colors.inputfg,
            relief=tk.FLAT,
            padding=5,
        )
        self.style.map(
            ttkstyle,
            background=[("readonly", readonly)],
            fieldbackground=[("readonly", readonly)],
            foreground=[("disabled", disabled_fg)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly),
            ],
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    "combo.Spinbox.field",
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            (
                                "Combobox.downarrow",
                                {"side": tk.RIGHT, "sticky": tk.S},
                            ),
                            (
                                "Combobox.padding",
                                {
                                    "expand": "1",
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Combobox.textarea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._register_ttkstyle(ttkstyle)
        try:
            self.create_scrollbar_style()
        except Exception:
            # style already created
            pass

    def create_separator_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Separator widget.

        Parameters:

            colorname (str):
                The primary widget color.
        """
        HSTYLE = "Horizontal.TSeparator"
        VSTYLE = "Vertical.TSeparator"

        hsize = [40, 1]
        vsize = [1, 40]

        # style colors
        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            background = default_color
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

        # horizontal separator
        h_element = h_ttkstyle.replace(".TS", ".S")
        h_img = ImageTk.PhotoImage(Image.new("RGB", hsize, background))
        h_name = util.get_image_name(h_img)
        self.theme_images[h_name] = h_img

        self.style.element_create(f"{h_element}.separator", "image", h_name)
        self.style.layout(
            h_ttkstyle, [(f"{h_element}.separator", {"sticky": tk.EW})]
        )

        # vertical separator
        v_element = v_ttkstyle.replace(".TS", ".S")
        v_img = ImageTk.PhotoImage(Image.new("RGB", vsize, background))
        v_name = util.get_image_name(v_img)
        self.theme_images[v_name] = v_img
        self.style.element_create(f"{v_element}.separator", "image", v_name)
        self.style.layout(
            v_ttkstyle, [(f"{v_element}.separator", {"sticky": tk.NS})]
        )
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_striped_progressbar_assets(self, thickness, colorname=DEFAULT):
        """Create the striped progressbar image and return as a
        `PhotoImage`

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A list of photoimage names.
        """
        if any([colorname == DEFAULT, colorname == ""]):
            barcolor = self.colors.primary
        else:
            barcolor = self.colors.get(colorname)

        # calculate value of the light color
        brightness = Colors.rgb_to_hsv(*Colors.hex_to_rgb(barcolor))[2]
        if brightness < 0.4:
            value_delta = 0.3
        elif brightness > 0.8:
            value_delta = 0
        else:
            value_delta = 0.1

        barcolor_light = Colors.update_hsv(barcolor, sd=-0.2, vd=value_delta)

        # horizontal progressbar
        img = Image.new("RGBA", (100, 100), barcolor_light)
        draw = ImageDraw.Draw(img)
        draw.polygon(
            xy=[(0, 0), (48, 0), (100, 52), (100, 100)],
            fill=barcolor,
        )
        draw.polygon(xy=[(0, 52), (48, 100), (0, 100)], fill=barcolor)

        _resized = img.resize((thickness, thickness), Resampling.LANCZOS)
        h_img = ImageTk.PhotoImage(_resized)
        h_name = h_img._PhotoImage__photo.name
        v_img = ImageTk.PhotoImage(_resized.rotate(90))
        v_name = v_img._PhotoImage__photo.name

        self.theme_images[h_name] = h_img
        self.theme_images[v_name] = v_img
        return h_name, v_name

    def create_striped_progressbar_style(self, colorname=DEFAULT):
        """Create a striped style for the ttk.Progressbar widget.

        Parameters:

            colorname (str):
                The primary widget color label.
        """
        HSTYLE = "Striped.Horizontal.TProgressbar"
        VSTYLE = "Striped.Vertical.TProgressbar"

        thickness = self.scale_size(12)

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            bordercolor = troughcolor

        # ( horizontal, vertical )
        images = self.create_striped_progressbar_assets(thickness, colorname)

        # horizontal progressbar
        h_element = h_ttkstyle.replace(".TP", ".P")
        self.style.element_create(
            f"{h_element}.pbar",
            "image",
            images[0],
            width=thickness,
            sticky=tk.EW,
        )
        self.style.layout(
            h_ttkstyle,
            [
                (
                    f"{h_element}.trough",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                f"{h_element}.pbar",
                                {"side": tk.LEFT, "sticky": tk.NS},
                            )
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            thickness=thickness,
            bordercolor=bordercolor,
            borderwidth=1,
        )

        # vertical progressbar
        v_element = v_ttkstyle.replace(".TP", ".P")
        self.style.element_create(
            f"{v_element}.pbar",
            "image",
            images[1],
            width=thickness,
            sticky=tk.NS,
        )
        self.style.layout(
            v_ttkstyle,
            [
                (
                    f"{v_element}.trough",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                f"{v_element}.pbar",
                                {"side": tk.BOTTOM, "sticky": tk.EW},
                            )
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            bordercolor=bordercolor,
            thickness=thickness,
            borderwidth=1,
        )
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_progressbar_style(self, colorname=DEFAULT):
        """Create a solid ttk style for the ttk.Progressbar widget.

        Parameters:

            colorname (str):
                The primary widget color.
        """
        H_STYLE = "Horizontal.TProgressbar"
        V_STYLE = "Vertical.TProgressbar"

        thickness = self.scale_size(10)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            bordercolor = troughcolor

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.primary
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{H_STYLE}"
            v_ttkstyle = f"{colorname}.{V_STYLE}"

        self.style._build_configure(
            h_ttkstyle,
            thickness=thickness,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
        )
        existing_elements = self.style.element_names()

        self.style._build_configure(
            v_ttkstyle,
            thickness=thickness,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
        )
        existing_elements = self.style.element_names()

        # horizontal progressbar
        h_element = h_ttkstyle.replace(".TP", ".P")
        trough_element = f"{h_element}.trough"
        pbar_element = f"{h_element}.pbar"
        if trough_element not in existing_elements:
            self.style.element_create(trough_element, "from", TTK_CLAM)
            self.style.element_create(pbar_element, "from", TTK_DEFAULT)

        self.style.layout(
            h_ttkstyle,
            [
                (
                    trough_element,
                    {
                        "sticky": "nswe",
                        "children": [
                            (pbar_element, {"side": "left", "sticky": "ns"})
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(h_ttkstyle, background=background)

        # vertical progressbar
        v_element = v_ttkstyle.replace(".TP", ".P")
        trough_element = f"{v_element}.trough"
        pbar_element = f"{v_element}.pbar"
        if trough_element not in existing_elements:
            self.style.element_create(trough_element, "from", TTK_CLAM)
            self.style.element_create(pbar_element, "from", TTK_DEFAULT)
            self.style._build_configure(v_ttkstyle, background=background)
        self.style.layout(
            v_ttkstyle,
            [
                (
                    trough_element,
                    {
                        "sticky": "nswe",
                        "children": [
                            (pbar_element, {"side": "bottom", "sticky": "we"})
                        ],
                    },
                )
            ],
        )

        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_scale_assets(self, colorname=DEFAULT, size=14):
        """Create the assets used for the ttk.Scale widget.

        The slider handle is automatically adjusted to fit the
        screen resolution.

        Parameters:

            colorname (str):
                The color label.

            size (int):
                The size diameter of the slider circle; default=16.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names to be used in the image
                layout when building the style.
        """
        size = self.scale_size(size)
        if self.is_light_theme:
            disabled_color = self.colors.border
            if colorname == LIGHT:
                track_color = self.colors.bg
            else:
                track_color = self.colors.light
        else:
            disabled_color = self.colors.selectbg
            track_color = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        if any([colorname == DEFAULT, colorname == ""]):
            normal_color = self.colors.primary
        else:
            normal_color = self.colors.get(colorname)

        pressed_color = Colors.update_hsv(normal_color, vd=-0.1)
        hover_color = Colors.update_hsv(normal_color, vd=0.1)

        # normal state
        _normal = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_normal)
        draw.ellipse((0, 0, 95, 95), fill=normal_color)
        normal_img = ImageTk.PhotoImage(
            _normal.resize((size, size), Resampling.LANCZOS)
        )
        normal_name = util.get_image_name(normal_img)
        self.theme_images[normal_name] = normal_img

        # pressed state
        _pressed = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_pressed)
        draw.ellipse((0, 0, 95, 95), fill=pressed_color)
        pressed_img = ImageTk.PhotoImage(
            _pressed.resize((size, size), Resampling.LANCZOS)
        )
        pressed_name = util.get_image_name(pressed_img)
        self.theme_images[pressed_name] = pressed_img

        # hover state
        _hover = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_hover)
        draw.ellipse((0, 0, 95, 95), fill=hover_color)
        hover_img = ImageTk.PhotoImage(
            _hover.resize((size, size), Resampling.LANCZOS)
        )
        hover_name = util.get_image_name(hover_img)
        self.theme_images[hover_name] = hover_img

        # disabled state
        _disabled = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse((0, 0, 95, 95), fill=disabled_color)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((size, size), Resampling.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        # vertical track
        h_track_img = ImageTk.PhotoImage(
            Image.new("RGB", self.scale_size((40, 5)), track_color)
        )
        h_track_name = util.get_image_name(h_track_img)
        self.theme_images[h_track_name] = h_track_img

        # horizontal track
        v_track_img = ImageTk.PhotoImage(
            Image.new("RGB", self.scale_size((5, 40)), track_color)
        )
        v_track_name = util.get_image_name(v_track_img)
        self.theme_images[v_track_name] = v_track_img

        return (
            normal_name,
            pressed_name,
            hover_name,
            disabled_name,
            h_track_name,
            v_track_name,
        )

    def create_scale_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Scale widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScale"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = f"Horizontal.{STYLE}"
            v_ttkstyle = f"Vertical.{STYLE}"
        else:
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"

        # ( normal, pressed, hover, disabled, htrack, vtrack )
        images = self.create_scale_assets(colorname)

        # horizontal scale
        h_element = h_ttkstyle.replace(".TS", ".S")
        self.style.element_create(
            f"{h_element}.slider",
            "image",
            images[0],
            ("disabled", images[3]),
            ("pressed", images[1]),
            ("hover", images[2]),
        )
        self.style.element_create(f"{h_element}.track", "image", images[4])
        self.style.layout(
            h_ttkstyle,
            [
                (
                    f"{h_element}.focus",
                    {
                        "expand": "1",
                        "sticky": tk.NSEW,
                        "children": [
                            (f"{h_element}.track", {"sticky": tk.EW}),
                            (
                                f"{h_element}.slider",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        )
        # vertical scale
        v_element = v_ttkstyle.replace(".TS", ".S")
        self.style.element_create(
            f"{v_element}.slider",
            "image",
            images[0],
            ("disabled", images[3]),
            ("pressed", images[1]),
            ("hover", images[2]),
        )
        self.style.element_create(f"{v_element}.track", "image", images[5])
        self.style.layout(
            v_ttkstyle,
            [
                (
                    f"{v_element}.focus",
                    {
                        "expand": "1",
                        "sticky": tk.NSEW,
                        "children": [
                            (f"{v_element}.track", {"sticky": tk.NS}),
                            (
                                f"{v_element}.slider",
                                {"side": tk.TOP, "sticky": ""},
                            ),
                        ],
                    },
                )
            ],
        )
        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_floodgauge_style(self, colorname=DEFAULT):
        """Create a ttk style for the ttkbootstrap.widgets.Floodgauge
        widget. This is a custom widget style that uses components of
        the progressbar and label.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        HSTYLE = "Horizontal.TFloodgauge"
        VSTYLE = "Vertical.TFloodgauge"
        FLOOD_FONT = "-size 14"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
            background = self.colors.primary
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"
            background = self.colors.get(colorname)

        if colorname == LIGHT:
            foreground = self.colors.fg
            troughcolor = self.colors.bg
        else:
            troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)
            foreground = self.colors.selectfg

        # horizontal floodgauge
        h_element = h_ttkstyle.replace(".TF", ".F")
        self.style.element_create(f"{h_element}.trough", "from", TTK_CLAM)
        self.style.element_create(f"{h_element}.pbar", "from", TTK_DEFAULT)
        self.style.layout(
            h_ttkstyle,
            [
                (
                    f"{h_element}.trough",
                    {
                        "children": [
                            (f"{h_element}.pbar", {"sticky": tk.NS}),
                            ("Floodgauge.label", {"sticky": ""}),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        )
        self.style._build_configure(
            h_ttkstyle,
            thickness=50,
            borderwidth=1,
            bordercolor=background,
            lightcolor=background,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
            background=background,
            foreground=foreground,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            font=FLOOD_FONT,
        )
        # vertical floodgauge
        v_element = v_ttkstyle.replace(".TF", ".F")
        self.style.element_create(f"{v_element}.trough", "from", TTK_CLAM)
        self.style.element_create(f"{v_element}.pbar", "from", TTK_DEFAULT)
        self.style.layout(
            v_ttkstyle,
            [
                (
                    f"{v_element}.trough",
                    {
                        "children": [
                            (f"{v_element}.pbar", {"sticky": tk.EW}),
                            ("Floodgauge.label", {"sticky": ""}),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        )
        self.style._build_configure(
            v_ttkstyle,
            thickness=50,
            borderwidth=1,
            bordercolor=background,
            lightcolor=background,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
            background=background,
            foreground=foreground,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            font=FLOOD_FONT,
        )
        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_simple_arrow_assets(self, arrowcolor: str, disabledcolor: str, activecolor: str, y_offset: int = 0):
        """
        Create simple arrow assets (small triangles) that can be used for various widgets.
        Originally created to replace Combobox.downarrow to fix layout issues in python 3.13.
        Also used for the Spinbox widget.

        Args:
            arrowcolor: The color value to use as the arrow fill color.
            disabledcolor: A second color value to use when the arrow is disabled.
            activecolor: A third color value to use when the arrow has focus.
            y_offset: (optional) The vertical padding to apply to the arrow images (useful in spinnboxes).
        Returns:
            A nested tuple containing the names of the created arrow images in the order (up, down, left, right)
            for each color.
        """

        def draw_simple_arrow(color: str, y_offset: int = 0):
            img = Image.new("RGBA", (13, 11))
            draw = ImageDraw.Draw(img)
            size = self.scale_size([13, 11])

            # Draw the arrow shape (triangle) pointing upwards, offset by the specified y_offset
            draw.polygon([(3, 6 + y_offset), (9, 6 + y_offset), (6, 3 + y_offset)], fill=color)

            img = img.resize(size, Resampling.BICUBIC)

            up_img = ImageTk.PhotoImage(img)
            up_name = util.get_image_name(up_img)
            self.theme_images[up_name] = up_img

            down_img = ImageTk.PhotoImage(img.rotate(180))
            down_name = util.get_image_name(down_img)
            self.theme_images[down_name] = down_img

            left_img = ImageTk.PhotoImage(img.rotate(90))
            left_name = util.get_image_name(left_img)
            self.theme_images[left_name] = left_img

            right_img = ImageTk.PhotoImage(img.rotate(-90))
            right_name = util.get_image_name(right_img)
            self.theme_images[right_name] = right_img

            return up_name, down_name, left_name, right_name

        normal_names = draw_simple_arrow(arrowcolor, y_offset=y_offset)
        pressed_names = draw_simple_arrow(disabledcolor, y_offset=y_offset)
        active_names = draw_simple_arrow(activecolor, y_offset=y_offset)

        return normal_names, pressed_names, active_names

    def create_arrow_assets(self, arrowcolor, pressed, active):
        """Create arrow assets used for various widget buttons.

        !!! note
            This method is currently not being utilized.

        Parameters:

            arrowcolor (str):
                The color value to use as the arrow fill color.

            pressed (str):
                The color value to use when the arrow is pressed.

            active (str):
                The color value to use when the arrow is active or
                hovered.
        """

        def draw_arrow(color: str):
            img = Image.new("RGBA", (11, 11))
            draw = ImageDraw.Draw(img)
            size = self.scale_size([11, 11])

            draw.line([2, 6, 2, 9], fill=color)
            draw.line([3, 5, 3, 8], fill=color)
            draw.line([4, 4, 4, 7], fill=color)
            draw.line([5, 3, 5, 6], fill=color)
            draw.line([6, 4, 6, 7], fill=color)
            draw.line([7, 5, 7, 8], fill=color)
            draw.line([8, 6, 8, 9], fill=color)

            img = img.resize(size, Resampling.BICUBIC)

            up_img = ImageTk.PhotoImage(img)
            up_name = util.get_image_name(up_img)
            self.theme_images[up_name] = up_img

            down_img = ImageTk.PhotoImage(img.rotate(180))
            down_name = util.get_image_name(down_img)
            self.theme_images[down_name] = down_img

            left_img = ImageTk.PhotoImage(img.rotate(90))
            left_name = util.get_image_name(left_img)
            self.theme_images[left_name] = left_img

            right_img = ImageTk.PhotoImage(img.rotate(-90))
            right_name = util.get_image_name(right_img)
            self.theme_images[right_name] = right_img

            return up_name, down_name, left_name, right_name

        normal_names = draw_arrow(arrowcolor)
        pressed_names = draw_arrow(pressed)
        active_names = draw_arrow(active)

        return normal_names, pressed_names, active_names

    def create_round_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create image assets to be used when building the round
        scrollbar style.

        Parameters:

            thumbcolor (str):
                The color value of the thumb in normal state.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        vsize = self.scale_size([9, 28])
        hsize = self.scale_size([28, 9])

        def rounded_rect(size, fill):
            x = size[0] * 10
            y = size[1] * 10
            img = Image.new("RGBA", (x, y))
            draw = ImageDraw.Draw(img)
            radius = min([x, y]) // 2
            draw.rounded_rectangle([0, 0, x - 1, y - 1], radius, fill)
            image = ImageTk.PhotoImage(img.resize(size, Resampling.BICUBIC))
            name = util.get_image_name(image)
            self.theme_images[name] = image
            return name

        # create images
        h_normal_img = rounded_rect(hsize, thumbcolor)
        h_pressed_img = rounded_rect(hsize, pressed)
        h_active_img = rounded_rect(hsize, active)

        v_normal_img = rounded_rect(vsize, thumbcolor)
        v_pressed_img = rounded_rect(vsize, pressed)
        v_active_img = rounded_rect(vsize, active)

        return (
            h_normal_img,
            h_pressed_img,
            h_active_img,
            v_normal_img,
            v_pressed_img,
            v_active_img,
        )

    def create_round_scrollbar_style(self, colorname=DEFAULT):
        """Create a round style for the ttk.Scrollbar widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScrollbar"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = f"Round.Horizontal.{STYLE}"
            v_ttkstyle = f"Round.Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Round.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Round.Vertical.{STYLE}"
            background = self.colors.get(colorname)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_round_scrollbar_assets(
            background, pressed, active
        )

        # horizontal scrollbar
        self.style._build_configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.style.element_create(
            f"{h_ttkstyle}.thumb",
            "image",
            scroll_images[0],
            ("pressed", scroll_images[1]),
            ("active", scroll_images[2]),
            border=self.scale_size(9),
            padding=0,
            sticky=tk.EW,
        )
        self.style.layout(
            h_ttkstyle,
            [
                (
                    "Horizontal.Scrollbar.trough",
                    {
                        "sticky": "we",
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(h_ttkstyle, arrowcolor=background)
        self.style.map(
            h_ttkstyle, arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # vertical scrollbar
        self.style._build_configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
        )
        self.style.element_create(
            f"{v_ttkstyle}.thumb",
            "image",
            scroll_images[3],
            ("pressed", scroll_images[4]),
            ("active", scroll_images[5]),
            border=self.scale_size(9),
            padding=0,
            sticky=tk.NS,
        )
        self.style.layout(
            v_ttkstyle,
            [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(v_ttkstyle, arrowcolor=background)
        self.style.map(
            v_ttkstyle, arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create the image assets used to build the standard scrollbar
        style.

        Parameters:

            thumbcolor (str):
                The primary color value used to color the thumb.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        vsize = self.scale_size([9, 28])
        hsize = self.scale_size([28, 9])

        def draw_rect(size, fill):
            x = size[0] * 10
            y = size[1] * 10
            img = Image.new("RGBA", (x, y), fill)
            image = ImageTk.PhotoImage(img.resize(size), Resampling.BICUBIC)
            name = util.get_image_name(image)
            self.theme_images[name] = image
            return name

        # create images
        h_normal_img = draw_rect(hsize, thumbcolor)
        h_pressed_img = draw_rect(hsize, pressed)
        h_active_img = draw_rect(hsize, active)

        v_normal_img = draw_rect(vsize, thumbcolor)
        v_pressed_img = draw_rect(vsize, pressed)
        v_active_img = draw_rect(vsize, active)

        return (
            h_normal_img,
            h_pressed_img,
            h_active_img,
            v_normal_img,
            v_pressed_img,
            v_active_img,
        )

    def create_scrollbar_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Scrollbar widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScrollbar"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = f"Horizontal.{STYLE}"
            v_ttkstyle = f"Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"
            background = self.colors.get(colorname)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_scrollbar_assets(
            background, pressed, active
        )

        # horizontal scrollbar
        self.style._build_configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.style.element_create(
            f"{h_ttkstyle}.thumb",
            "image",
            scroll_images[0],
            ("pressed", scroll_images[1]),
            ("active", scroll_images[2]),
            border=(3, 0),
            sticky=tk.NSEW,
        )
        self.style.layout(
            h_ttkstyle,
            [
                (
                    "Horizontal.Scrollbar.trough",
                    {
                        "sticky": "we",
                        "children": [
                            (
                                "Horizontal.Scrollbar.leftarrow",
                                {"side": "left", "sticky": ""},
                            ),
                            (
                                "Horizontal.Scrollbar.rightarrow",
                                {"side": "right", "sticky": ""},
                            ),
                            (
                                f"{h_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(h_ttkstyle, arrowcolor=background)
        self.style.map(
            h_ttkstyle, arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # vertical scrollbar
        self.style._build_configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.style.element_create(
            f"{v_ttkstyle}.thumb",
            "image",
            scroll_images[3],
            ("pressed", scroll_images[4]),
            ("active", scroll_images[5]),
            border=(0, 3),
            sticky=tk.NSEW,
        )
        self.style.layout(
            v_ttkstyle,
            [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            (
                                "Vertical.Scrollbar.uparrow",
                                {"side": "top", "sticky": ""},
                            ),
                            (
                                "Vertical.Scrollbar.downarrow",
                                {"side": "bottom", "sticky": ""},
                            ),
                            (
                                f"{v_ttkstyle}.thumb",
                                {"expand": "1", "sticky": "nswe"},
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(v_ttkstyle, arrowcolor=background)
        self.style.map(
            v_ttkstyle, arrowcolor=[("pressed", pressed), ("active", active)]
        )

        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_spinbox_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Spinbox widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TSpinbox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get(colorname)

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        if colorname == "light":
            arrowfocus = self.colors.fg
        else:
            arrowfocus = focuscolor

        element = ttkstyle.replace(".TS", ".S")
        arrow_images = self.create_simple_arrow_assets(
            self.colors.inputfg, disabled_fg, arrowfocus, y_offset=2
        )
        uparrow_image = arrow_images[0][0]
        uparrow_disabled_image = arrow_images[1][0]
        uparrow_focus_image = arrow_images[2][0]
        downarrow_image = arrow_images[0][1]
        downarrow_disabled_image = arrow_images[1][1]
        downarrow_focus_image = arrow_images[2][1]

        self.style.element_create(
            f"{element}.uparrow",
            "image",
            uparrow_image,
            ("disabled", uparrow_disabled_image),
            ("pressed !disabled", uparrow_focus_image),
            ("hover !disabled", uparrow_focus_image),
        )
        self.style.element_create(
            f"{element}.downarrow",
            "image",
            downarrow_image,
            ("disabled", downarrow_disabled_image),
            ("pressed !disabled", downarrow_focus_image),
            ("hover !disabled", downarrow_focus_image),
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    f"{element}.field",
                    {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            (
                                "null",
                                {
                                    "side": tk.RIGHT,
                                    "sticky": "",
                                    "children": [
                                        (
                                            f"{element}.uparrow",
                                            {"side": tk.TOP, "sticky": tk.E},
                                        ),
                                        (
                                            f"{element}.downarrow",
                                            {
                                                "side": tk.BOTTOM,
                                                "sticky": tk.E,
                                            },
                                        ),
                                    ],
                                },
                            ),
                            (
                                f"{element}.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{element}.textarea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            ),
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            borderwidth=0,
            background=self.colors.inputbg,
            relief=tk.FLAT,
            insertcolor=self.colors.inputfg,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            fieldbackground=[("readonly", readonly)],
            background=[("readonly", readonly)],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
        )
        # register ttkstyles
        self.style._register_ttkstyle(ttkstyle)

    def create_table_treeview_style(self, colorname=DEFAULT):
        """Create a style for the Tableview widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Table.Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
            hover = Colors.update_hsv(self.colors.light, vd=-0.1)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg
            hover = Colors.update_hsv(self.colors.dark, vd=0.1)

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = Colors.update_hsv(background, vd=-0.1)
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = Colors.update_hsv(background, vd=0.1)

        # treeview header
        self.style._build_configure(
            header_style,
            background=background,
            foreground=foreground,
            relief=RAISED,
            borderwidth=1,
            darkcolor=background,
            bordercolor=bordercolor,
            lightcolor=background,
            padding=5,
        )
        self.style.map(
            header_style,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("active !disabled", hover),
            ],
            darkcolor=[
                ("active !disabled", hover),
            ],
            lightcolor=[
                ("active !disabled", hover),
            ],
        )
        self.style._build_configure(
            body_style,
            background=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            bordercolor=bordercolor,
            lightcolor=self.colors.inputbg,
            darkcolor=self.colors.inputbg,
            borderwidth=2,
            padding=0,
            rowheight=rowheight,
            relief=tk.RAISED,
        )
        self.style.map(
            body_style,
            background=[("selected", self.colors.selectbg)],
            foreground=[
                ("disabled", disabled_fg),
                ("selected", self.colors.selectfg),
            ],
        )
        self.style.layout(
            body_style,
            [
                (
                    "Button.border",
                    {
                        "sticky": tk.NSEW,
                        "border": "1",
                        "children": [
                            (
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        # register ttkstyles
        self.style._register_ttkstyle(body_style)

    def create_treeview_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Treeview widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
            focuscolor = self.colors.primary
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor

        # treeview header
        self.style._build_configure(
            header_style,
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            padding=5,
        )
        self.style.map(
            header_style,
            foreground=[("disabled", disabled_fg)],
            bordercolor=[("focus !disabled", background)],
        )
        # treeview body
        self.style._build_configure(
            body_style,
            background=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            bordercolor=bordercolor,
            lightcolor=self.colors.inputbg,
            darkcolor=self.colors.inputbg,
            borderwidth=2,
            padding=0,
            rowheight=rowheight,
            relief=tk.RAISED,
        )
        self.style.map(
            body_style,
            background=[("selected", self.colors.selectbg)],
            foreground=[
                ("disabled", disabled_fg),
                ("selected", self.colors.selectfg),
            ],
            bordercolor=[
                ("disabled", bordercolor),
                ("focus", focuscolor),
                ("pressed", focuscolor),
                ("hover", focuscolor),
            ],
            lightcolor=[("focus", focuscolor)],
            darkcolor=[("focus", focuscolor)],
        )
        self.style.layout(
            body_style,
            [
                (
                    "Button.border",
                    {
                        "sticky": tk.NSEW,
                        "border": "1",
                        "children": [
                            (
                                "Treeview.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Treeview.treearea",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        try:
            self.style.element_create("Treeitem.indicator", "from", TTK_ALT)
        except:
            pass

        # register ttkstyles
        self.style._register_ttkstyle(body_style)

    def create_frame_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Frame widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TFrame"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get(colorname)

        self.style._build_configure(ttkstyle, background=background)

        # register style
        self.style._register_ttkstyle(ttkstyle)

    def create_button_style(self, colorname=DEFAULT):
        """Create a solid style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TButton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)

        bordercolor = background
        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            focuscolor=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[("disabled", disabled_bg)],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_button_style(self, colorname=DEFAULT):
        """Create an outline style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.TButton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=bordercolor,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            focuscolor=[
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_link_button_style(self, colorname=DEFAULT):
        """Create a link button style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Link.TButton"

        pressed = self.colors.info
        hover = self.colors.info

        if any([colorname == DEFAULT, colorname == ""]):
            foreground = self.colors.fg
            ttkstyle = STYLE
        elif colorname == LIGHT:
            foreground = self.colors.fg
            ttkstyle = f"{colorname}.{STYLE}"
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            anchor=tk.CENTER,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            shiftrelief=[("pressed !disabled", -1)],
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            focuscolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            background=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            bordercolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_square_toggle_assets(self, colorname=DEFAULT):
        """Create the image assets used to build a square toggle
        style.

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """
        size = self.scale_size([24, 15])
        if any([colorname == DEFAULT, colorname == ""]):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg
        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)
        off_indicator = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

        # toggle off
        _off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_off)
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=off_border, width=6, fill=off_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=off_indicator)

        off_img = ImageTk.PhotoImage(_off.resize(size, Resampling.LANCZOS))
        off_name = util.get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # toggle on
        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=on_border, width=6, fill=on_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=on_indicator)
        _on = toggle_on.transpose(Transpose.ROTATE_180)
        on_img = ImageTk.PhotoImage(_on.resize(size, Resampling.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # toggle disabled
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Resampling.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        # toggle on / disabled
        toggle_on_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on_disabled)
        draw.rectangle(
            xy=[1, 1, 225, 129], outline=disabled_fg, width=6, fill=off_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        _on_disabled = toggle_on_disabled.transpose(Transpose.ROTATE_180)
        on_dis_img = ImageTk.PhotoImage(_on_disabled.resize(size, Resampling.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        return off_name, on_name, disabled_name, on_disabled_name

    def create_toggle_style(self, colorname=DEFAULT):
        """Create a round toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
        """
        self.create_round_toggle_style(colorname)

    def create_round_toggle_assets(self, colorname=DEFAULT):
        """Create image assets for the round toggle style.

        Parameters:

            colorname (str):
                The color label assigned to the colors property.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """
        size = self.scale_size([24, 15])

        if any([colorname == DEFAULT, colorname == ""]):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg

        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)
        off_indicator = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

        # toggle off
        _off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_off)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=off_border,
            width=6,
            fill=off_fill,
        )
        draw.ellipse([20, 18, 112, 110], fill=off_indicator)
        off_img = ImageTk.PhotoImage(_off.resize(size, Resampling.LANCZOS))
        off_name = util.get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # toggle on
        _on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_on)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=on_border,
            width=6,
            fill=on_fill,
        )
        draw.ellipse([20, 18, 112, 110], fill=on_indicator)
        _on = _on.transpose(Transpose.ROTATE_180)
        on_img = ImageTk.PhotoImage(_on.resize(size, Resampling.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # toggle on / disabled
        _on_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_on_disabled)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=disabled_fg,
            width=6,
            fill=off_fill,
        )
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)
        _on_disabled = _on_disabled.transpose(Transpose.ROTATE_180)
        on_dis_img = ImageTk.PhotoImage(_on_disabled.resize(size, Resampling.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        # toggle disabled
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129], radius=(128 / 2), outline=disabled_fg, width=6
        )
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Resampling.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name, on_disabled_name

    def create_round_toggle_style(self, colorname=DEFAULT):
        """Create a round toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Round.Toggle"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.create_round_toggle_assets(colorname)

        try:
            width = self.scale_size(28)
            borderpad = self.scale_size(4)
            self.style.element_create(
                f"{ttkstyle}.indicator",
                "image",
                images[1],
                ("disabled selected", images[3]),
                ("disabled", images[2]),
                ("!selected", images[0]),
                width=width,
                border=borderpad,
                sticky=tk.W,
            )
        except:
            """This method is used as the default Toggle style, so it
            is neccessary to catch Tcl Errors when it tries to create
            and element that was already created by the Toggle or
            Round Toggle style"""
            pass

        self.style._build_configure(
            ttkstyle,
            relief=tk.FLAT,
            borderwidth=0,
            padding=0,
            foreground=self.colors.fg,
            background=self.colors.bg,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[("selected", self.colors.bg)],
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},
                                        ),
                                        (
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_square_toggle_style(self, colorname=DEFAULT):
        """Create a square toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "Square.Toggle"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.create_square_toggle_assets(colorname)

        width = self.scale_size(28)
        borderpad = self.scale_size(4)

        self.style.element_create(
            f"{ttkstyle}.indicator",
            "image",
            images[1],
            ("disabled selected", images[3]),
            ("disabled", images[2]),
            ("!selected", images[0]),
            width=width,
            border=borderpad,
            sticky=tk.W,
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                "Toolbutton.padding",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            f"{ttkstyle}.indicator",
                                            {"side": tk.LEFT},
                                        ),
                                        (
                                            "Toolbutton.label",
                                            {"side": tk.LEFT},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        self.style._build_configure(
            ttkstyle, relief=tk.FLAT, borderwidth=0, foreground=self.colors.fg
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("selected", self.colors.bg),
                ("!selected", self.colors.bg),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_toolbutton_style(self, colorname=DEFAULT):
        """Create a solid toolbutton style for the ttk.Checkbutton
        and ttk.Radiobutton widgets.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Toolbutton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            toggle_on = self.colors.get(colorname)

        foreground = self.colors.get_foreground(colorname)

        if self.is_light_theme:
            toggle_off = self.colors.border
        else:
            toggle_off = self.colors.selectbg

        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        self.style._build_configure(
            ttkstyle,
            foreground=self.colors.selectfg,
            background=toggle_off,
            bordercolor=toggle_off,
            darkcolor=toggle_off,
            lightcolor=toggle_off,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("hover", foreground),
                ("selected", foreground),
            ],
            focuscolor=[
                ("disabled", disabled_fg),
                ("hover", foreground),
                ("selected", foreground),
            ],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_toolbutton_style(self, colorname=DEFAULT):
        """Create an outline toolbutton style for the ttk.Checkbutton
        and ttk.Radiobutton widgets.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.Toolbutton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=bordercolor,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            arrowsize=3,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("selected !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_entry_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Entry widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TEntry"

        # general default colors
        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, not colorname]):
            # default style
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            # colored style
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get(colorname)
            bordercolor = focuscolor

        self.style._build_configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            insertcolor=self.colors.inputfg,
            padding=5,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            fieldbackground=[("readonly", readonly)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_radiobutton_assets(self, colorname=DEFAULT):
        """Create the image assets used to build the radiobutton style.

        Parameters:

            colorname (str):

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names
        """
        prime_color = self.colors.get(colorname)
        on_fill = prime_color
        off_fill = self.colors.bg
        on_indicator = self.colors.selectfg
        size = self.scale_size([14, 14])
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)
        disabled = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        if self.is_light_theme:
            if colorname == LIGHT:
                on_indicator = self.colors.dark

        # radio off
        _off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_off)
        draw.ellipse(
            xy=[1, 1, 133, 133], outline=off_border, width=6, fill=off_fill
        )
        off_img = ImageTk.PhotoImage(_off.resize(size, Resampling.LANCZOS))
        off_name = util.get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # radio on
        _on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on)
        if colorname == LIGHT and self.is_light_theme:
            draw.ellipse(xy=[1, 1, 133, 133], outline=off_border, width=6)
        else:
            draw.ellipse(xy=[1, 1, 133, 133], fill=on_fill)
        draw.ellipse([40, 40, 94, 94], fill=on_indicator)
        on_img = ImageTk.PhotoImage(_on.resize(size, Resampling.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # radio on/disabled
        _on_dis = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on_dis)
        if colorname == LIGHT and self.is_light_theme:
            draw.ellipse(xy=[1, 1, 133, 133], outline=off_border, width=6)
        else:
            draw.ellipse(xy=[1, 1, 133, 133], fill=disabled)
        draw.ellipse([40, 40, 94, 94], fill=off_fill)
        on_dis_img = ImageTk.PhotoImage(_on_dis.resize(size, Resampling.LANCZOS))
        on_disabled_name = util.get_image_name(on_dis_img)
        self.theme_images[on_disabled_name] = on_dis_img

        # radio disabled
        _disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse(
            xy=[1, 1, 133, 133], outline=disabled, width=3, fill=off_fill
        )
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Resampling.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name, on_disabled_name

    def create_radiobutton_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Radiobutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "TRadiobutton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.create_radiobutton_assets(colorname)
        width = self.scale_size(20)
        borderpad = self.scale_size(4)
        self.style.element_create(
            f"{ttkstyle}.indicator",
            "image",
            images[1],
            ("disabled selected", images[3]),
            ("disabled", images[2]),
            ("!selected", images[0]),
            width=width,
            border=borderpad,
            sticky=tk.W,
        )
        self.style.map(ttkstyle, foreground=[("disabled", disabled_fg)])
        self.style._build_configure(ttkstyle)
        self.style.layout(
            ttkstyle,
            [
                (
                    "Radiobutton.padding",
                    {
                        "children": [
                            (
                                f"{ttkstyle}.indicator",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                            (
                                "Radiobutton.focus",
                                {
                                    "children": [
                                        (
                                            "Radiobutton.label",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                    "side": tk.LEFT,
                                    "sticky": "",
                                },
                            ),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_date_button_assets(self, foreground):
        """Create the image assets used to build the date button
        style. This button style applied to the button in the
        ttkbootstrap.widgets.DateEntry.

        Parameters:

            foreground (str):
                The color value used to draw the calendar image.

        Returns:

            str:
                The PhotoImage name.
        """
        fill = foreground
        image = Image.new("RGBA", (210, 220))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [10, 30, 200, 210], radius=20, outline=fill, width=10
        )

        calendar_image_coordinates = [
            # page spirals
            [40, 10, 50, 50],
            [100, 10, 110, 50],
            [160, 10, 170, 50],
            # row 1
            [70, 90, 90, 110],
            [110, 90, 130, 110],
            [150, 90, 170, 110],
            # row 2
            [30, 130, 50, 150],
            [70, 130, 90, 150],
            [110, 130, 130, 150],
            [150, 130, 170, 150],
            # row 3
            [30, 170, 50, 190],
            [70, 170, 90, 190],
            [110, 170, 130, 190],
        ]
        for xy in calendar_image_coordinates:
            draw.rectangle(xy=xy, fill=fill)

        size = self.scale_size([21, 22])
        tk_img = ImageTk.PhotoImage(image.resize(size, Resampling.LANCZOS))
        tk_name = util.get_image_name(tk_img)
        self.theme_images[tk_name] = tk_img
        return tk_name

    def create_date_button_style(self, colorname=DEFAULT):
        """Create a date button style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style widget.
        """
        STYLE = "Date.TButton"

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
            btn_foreground = Colors.get_foreground(self.colors, PRIMARY)
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)
            btn_foreground = Colors.get_foreground(self.colors, colorname)

        img_normal = self.create_date_button_assets(btn_foreground)

        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.10)

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(2, 2),
            anchor=tk.CENTER,
            image=img_normal,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[("disabled", disabled_fg)],
            darkcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )

        self.style._register_ttkstyle(ttkstyle)

    def create_calendar_style(self, colorname=DEFAULT):
        """Create a style for the
        ttkbootstrap.dialogs.DatePickerPopup widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "TCalendar"

        if any([colorname == DEFAULT, colorname == ""]):
            prime_color = self.colors.primary
            ttkstyle = STYLE
            chevron_style = "Chevron.TButton"
        else:
            prime_color = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"
            chevron_style = f"Chevron.{colorname}.TButton"

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            pressed = Colors.update_hsv(prime_color, vd=-0.1)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            pressed = Colors.update_hsv(prime_color, vd=0.1)

        self.style._build_configure(
            ttkstyle,
            foreground=self.colors.fg,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=self.colors.fg,
            borderwidth=1,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    "Toolbutton.border",
                    {
                        "sticky": tk.NSEW,
                        "children": [
                            (
                                "Toolbutton.focus",
                                {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Toolbutton.padding",
                                            {
                                                "sticky": tk.NSEW,
                                                "children": [
                                                    ("Toolbutton.label", {"sticky": tk.NSEW})
                                                ],
                                            },
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            focuscolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg),
            ]
        )
        self.style._build_configure(chevron_style, font="-size 14")

        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)
        self.style._register_ttkstyle(chevron_style)

    def create_metersubtxt_label_style(self, colorname=DEFAULT):
        """Create a subtext label style for the
        ttkbootstrap.widgets.Meter widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Metersubtxt.TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            if self.is_light_theme:
                foreground = self.colors.secondary
            else:
                foreground = self.colors.light
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get(colorname)

        background = self.colors.bg

        self.style._build_configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_meter_label_style(self, colorname=DEFAULT):
        """Create a label style for the
        ttkbootstrap.widgets.Meter widget. This style also stores some
        metadata that is called by the Meter class to lookup relevant
        colors for the trough and bar when the new image is drawn.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "Meter.TLabel"

        # text color = `foreground`
        # trough color = `space`

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.bg
            textcolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            textcolor = self.colors.get(colorname)
            background = self.colors.bg

        self.style._build_configure(
            ttkstyle,
            foreground=textcolor,
            background=background,
            space=troughcolor,
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_label_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Label widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.fg
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get(colorname)
            background = self.colors.bg

        # standard label
        self.style._build_configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_inverse_label_style(self, colorname=DEFAULT):
        """Create an inverted style for the ttk.Label.

        The foreground and background are inverted versions of that
        used in the standard label style.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE_INVERSE = "Inverse.TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE_INVERSE
            background = self.colors.fg
            foreground = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE_INVERSE}"
            background = self.colors.get(colorname)
            foreground = self.colors.get_foreground(colorname)

        self.style._build_configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_labelframe_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Labelframe widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TLabelframe"

        background = self.colors.bg

        if any([colorname == DEFAULT, colorname == ""]):
            foreground = self.colors.fg
            ttkstyle = STYLE

            if self.is_light_theme:
                bordercolor = self.colors.border
            else:
                bordercolor = self.colors.selectbg

        else:
            foreground = self.colors.get(colorname)
            bordercolor = foreground
            ttkstyle = f"{colorname}.{STYLE}"

        # create widget style
        self.style._build_configure(
            f"{ttkstyle}.Label",
            foreground=foreground,
            background=background,
        )
        self.style._build_configure(
            ttkstyle,
            relief=tk.RAISED,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=background,
            darkcolor=background,
            background=background,
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_checkbutton_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TCheckbutton"

        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            colorname = PRIMARY
            ttkstyle = STYLE
        else:
            ttkstyle = f"{colorname}.TCheckbutton"

        # ( off, on, disabled )
        images = self.create_checkbutton_assets(colorname)

        element = ttkstyle.replace(".TC", ".C")
        width = self.scale_size(20)
        borderpad = self.scale_size(4)
        self.style.element_create(
            f"{element}.indicator",
            "image",
            images[1],
            ("disabled selected", images[4]),
            ("disabled alternate", images[5]),
            ("disabled", images[2]),
            ("alternate", images[3]),
            ("!selected", images[0]),
            width=width,
            border=borderpad,
            sticky=tk.W,
        )
        self.style._build_configure(ttkstyle, foreground=self.colors.fg)
        self.style.map(ttkstyle, foreground=[("disabled", disabled_fg)])
        self.style.layout(
            ttkstyle,
            [
                (
                    "Checkbutton.padding",
                    {
                        "children": [
                            (
                                f"{element}.indicator",
                                {"side": tk.LEFT, "sticky": ""},
                            ),
                            (
                                "Checkbutton.focus",
                                {
                                    "children": [
                                        (
                                            "Checkbutton.label",
                                            {"sticky": tk.NSEW},
                                        )
                                    ],
                                    "side": tk.LEFT,
                                    "sticky": "",
                                },
                            ),
                        ],
                        "sticky": tk.NSEW,
                    },
                )
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_checkbutton_assets(self, colorname=DEFAULT):
        """Create the image assets used to build the standard
        checkbutton style.

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """
        # set platform specific checkfont
        winsys = self.style.tk.call("tk", "windowingsystem")
        indicator = "✓"
        if winsys == "win32":
            # Windows font
            fnt = ImageFont.truetype("seguisym.ttf", 120)
            font_offset = -20
            # TODO consider using ImageFont.getsize for offsets
        elif winsys == "x11":
            # Linux fonts
            try:
                # this should be available on most Linux distros
                fnt = ImageFont.truetype("FreeSerif.ttf", 130)
                font_offset = 10
            except:
                try:
                    # this should be available as a backup on Linux 
                    # distros that don't have the FreeSerif.ttf file
                    fnt = ImageFont.truetype("DejaVuSans.ttf", 160)
                    font_offset = -15
                except:
                    # If all else fails, use the default ImageFont
                    # this won't actually show anything in practice 
                    # because of how I'm scaling the image, but it 
                    # will prevent the program from crashing. I need 
                    # a better solution for a missing font
                    fnt = ImageFont.load_default()
                    font_offset = 0
                    indicator = "x"
        else:
            # Mac OS font
            fnt = ImageFont.truetype("LucidaGrande.ttc", 120)
            font_offset = -10

        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_fill = prime_color
        off_fill = self.colors.bg
        off_border = self.colors.selectbg
        off_border = Colors.make_transparent(0.4, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.3, self.colors.fg, self.colors.bg)

        if colorname == LIGHT:
            check_color = self.colors.dark
            on_border = check_color
        elif colorname == DARK:
            check_color = self.colors.light
            on_border = check_color
        else:
            check_color = self.colors.selectfg

        size = self.scale_size([14, 14])

        # checkbutton off
        checkbutton_off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_off)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            outline=off_border,
            width=6,
            fill=off_fill,
        )
        off_img = ImageTk.PhotoImage(
            checkbutton_off.resize(size, Resampling.LANCZOS)
        )
        off_name = util.get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # checkbutton on
        checkbutton_on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_on)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            fill=on_fill,
            outline=on_border,
            width=3,
        )

        draw.text((20, font_offset), indicator, font=fnt, fill=check_color)
        on_img = ImageTk.PhotoImage(checkbutton_on.resize(size, Resampling.LANCZOS))
        on_name = util.get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # checkbutton on/disabled
        checkbutton_on_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_on_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            fill=disabled_fg,
            outline=disabled_fg,
            width=3,
        )

        draw.text((20, font_offset), indicator, font=fnt, fill=off_fill)
        on_dis_img = ImageTk.PhotoImage(checkbutton_on_disabled.resize(size, Resampling.LANCZOS))
        on_dis_name = util.get_image_name(on_dis_img)
        self.theme_images[on_dis_name] = on_dis_img

        # checkbutton alt
        checkbutton_alt = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_alt)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            fill=on_fill,
            outline=on_border,
            width=3,
        )
        draw.line([36, 67, 100, 67], fill=check_color, width=12)
        alt_img = ImageTk.PhotoImage(
            checkbutton_alt.resize(size, Resampling.LANCZOS)
        )
        alt_name = util.get_image_name(alt_img)
        self.theme_images[alt_name] = alt_img

        # checkbutton alt/disabled
        checkbutton_alt_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_alt_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            fill=disabled_fg,
            outline=disabled_fg,
            width=3,
        )
        draw.line([36, 67, 100, 67], fill=off_fill, width=12)
        alt_dis_img = ImageTk.PhotoImage(
            checkbutton_alt_disabled.resize(size, Resampling.LANCZOS)
        )
        alt_dis_name = util.get_image_name(alt_dis_img)
        self.theme_images[alt_dis_name] = alt_dis_img

        # checkbutton disabled
        checkbutton_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132], radius=16, outline=disabled_fg, width=3
        )
        disabled_img = ImageTk.PhotoImage(
            checkbutton_disabled.resize(size, Resampling.LANCZOS)
        )
        disabled_name = util.get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name, alt_name, on_dis_name, alt_dis_name

    def create_menubutton_style(self, colorname=DEFAULT):
        """Create a solid style for the ttk.Menubutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TMenubutton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.primary
            foreground = self.colors.get_foreground(PRIMARY)
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get(colorname)
            foreground = self.colors.get_foreground(colorname)

        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            arrowsize=self.scale_size(4),
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=self.colors.selectfg,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            arrowcolor=[("disabled", disabled_fg)],
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_menubutton_style(self, colorname=DEFAULT):
        """Create an outline button style for the ttk.Menubutton widget

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.TMenubutton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.style._build_configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=bordercolor,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            arrowsize=self.scale_size(4),
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed", pressed),
                ("hover", hover),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            arrowcolor=[
                ("disabled", disabled_fg),
                ("pressed", foreground_pressed),
                ("hover", foreground_pressed),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_notebook_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Notebook widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TNotebook"

        if self.is_light_theme:
            bordercolor = self.colors.border
            foreground = self.colors.inputfg
        else:
            bordercolor = self.colors.selectbg
            foreground = self.colors.selectfg

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            selectfg = self.colors.fg
            ttkstyle = STYLE
        else:
            selectfg = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        ttkstyle_tab = f"{ttkstyle}.Tab"

        # create widget style
        self.style._build_configure(
            ttkstyle,
            background=self.colors.bg,
            bordercolor=bordercolor,
            lightcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            tabmargins=(0, 1, 1, 0),
        )
        self.style._build_configure(
            ttkstyle_tab, focuscolor="", foreground=foreground, padding=(6, 5)
        )
        self.style.map(
            ttkstyle_tab,
            background=[
                ("selected", self.colors.bg),
                ("!selected", background),
            ],
            lightcolor=[
                ("selected", self.colors.bg),
                ("!selected", background),
            ],
            bordercolor=[
                ("selected", bordercolor),
                ("!selected", bordercolor),
            ],
            padding=[("selected", (6, 5)), ("!selected", (6, 5))],
            foreground=[("selected", foreground), ("!selected", selectfg)],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_panedwindow_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Panedwindow widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        H_STYLE = "Horizontal.TPanedwindow"
        V_STYLE = "Vertical.TPanedwindow"

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            sashcolor = default_color
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            sashcolor = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{H_STYLE}"
            v_ttkstyle = f"{colorname}.{V_STYLE}"

        self.style._build_configure(
            "Sash", gripcount=0, sashthickness=self.scale_size(2)
        )
        self.style._build_configure(h_ttkstyle, background=sashcolor)
        self.style._build_configure(v_ttkstyle, background=sashcolor)

        # register ttkstyle
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_sizegrip_assets(self, color):
        """Create image assets used to build the sizegrip style.

        Parameters:

            color (str):
                The color _value_ used to draw the image.

        Returns:

            str:
                The PhotoImage name.
        """

        box = self.scale_size(1)
        pad = box * 2
        chunk = box + pad  # 4

        w = chunk * 3 + pad  # 14
        h = chunk * 3 + pad  # 14

        size = [w, h]

        im = Image.new("RGBA", size)
        draw = ImageDraw.Draw(im)

        draw.rectangle((chunk * 2 + pad, pad, chunk * 3, chunk), fill=color)
        draw.rectangle(
            (chunk * 2 + pad, chunk + pad, chunk * 3, chunk * 2), fill=color
        )
        draw.rectangle(
            (chunk * 2 + pad, chunk * 2 + pad, chunk * 3, chunk * 3),
            fill=color,
        )

        draw.rectangle(
            (chunk + pad, chunk + pad, chunk * 2, chunk * 2), fill=color
        )
        draw.rectangle(
            (chunk + pad, chunk * 2 + pad, chunk * 2, chunk * 3), fill=color
        )

        draw.rectangle((pad, chunk * 2 + pad, chunk, chunk * 3), fill=color)

        _img = ImageTk.PhotoImage(im)
        _name = util.get_image_name(_img)
        self.theme_images[_name] = _img
        return _name

    def create_sizegrip_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Sizegrip widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TSizegrip"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE

            if self.is_light_theme:
                grip_color = self.colors.border
            else:
                grip_color = self.colors.inputbg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            grip_color = self.colors.get(colorname)

        image = self.create_sizegrip_assets(grip_color)

        self.style.element_create(
            f"{ttkstyle}.Sizegrip.sizegrip", "image", image
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    f"{ttkstyle}.Sizegrip.sizegrip",
                    {"side": tk.BOTTOM, "sticky": tk.SE},
                )
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def update_combobox_popdown_style(self, widget):
        """Update the legacy ttk.Combobox elements. This method is
        called every time the theme is changed in order to ensure
        that the legacy tkinter components embedded in this ttk widget
        are styled appropriate to the current theme.

        The ttk.Combobox contains several elements that are not styled
        using the ttk theme engine. This includes the **popdownwindow**
        and the **scrollbar**. Both of these widgets are configured
        manually using calls to tcl/tk.

        Parameters:

            widget (ttk.Combobox):
                The combobox element to be updated.
        """
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        tk_settings = []
        tk_settings.extend(["-borderwidth", 2])
        tk_settings.extend(["-highlightthickness", 1])
        tk_settings.extend(["-highlightcolor", bordercolor])
        tk_settings.extend(["-background", self.colors.inputbg])
        tk_settings.extend(["-foreground", self.colors.inputfg])
        tk_settings.extend(["-selectbackground", self.colors.selectbg])
        tk_settings.extend(["-selectforeground", self.colors.selectfg])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)


class Keywords:
    # TODO possibly refactor the bootstyle keyword methods into this class?
    #   Leave for now.

    COLORS = [
        "primary",
        "secondary",
        "success",
        "info",
        "warning",
        "danger",
        "light",
        "dark",
    ]
    ORIENTS = ["horizontal", "vertical"]
    TYPES = [
        "outline",
        "link",
        "inverse",
        "round",
        "square",
        "striped",
        "focus",
        "input",
        "date",
        "metersubtxt",
        "meter",
        "table"
    ]
    CLASSES = [
        "button",
        "progressbar",
        "checkbutton",
        "combobox",
        "entry",
        "labelframe",
        "label",
        "frame",
        "floodgauge",
        "sizegrip",
        "optionmenu",
        "menubutton",
        "menu",
        "notebook",
        "panedwindow",
        "radiobutton",
        "separator",
        "scrollbar",
        "spinbox",
        "scale",
        "text",
        "toolbutton",
        "treeview",
        "toggle",
        "tk",
        "calendar",
        "listbox",
        "canvas",
        "toplevel",
    ]
    COLOR_PATTERN = re.compile("|".join(COLORS))
    ORIENT_PATTERN = re.compile("|".join(ORIENTS))
    CLASS_PATTERN = re.compile("|".join(CLASSES))
    TYPE_PATTERN = re.compile("|".join(TYPES))


class Bootstyle:
    @staticmethod
    def ttkstyle_widget_class(widget=None, string=""):
        """Find and return the widget class

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A widget class keyword.
        """
        # find widget class from string pattern
        match = re.search(Keywords.CLASS_PATTERN, string.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class

        # find widget class from tkinter/tcl method
        if widget is None:
            return ""
        _class = widget.winfo_class()
        match = re.search(Keywords.CLASS_PATTERN, _class.lower())
        if match is not None:
            widget_class = match.group(0)
            return widget_class
        else:
            return ""

    @staticmethod
    def ttkstyle_widget_type(string):
        """Find and return the widget type.

        Parameters:

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A widget type keyword.
        """
        match = re.search(Keywords.TYPE_PATTERN, string.lower())
        if match is None:
            return ""
        else:
            widget_type = match.group(0)
            return widget_type

    @staticmethod
    def ttkstyle_widget_orient(widget=None, string="", **kwargs):
        """Find and return widget orient, or default orient for widget if
        a widget with orientation.

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

            **kwargs:
                Optional keyword arguments passed in the widget constructor.

        Returns:

            str:
                A widget orientation keyword.
        """
        # string method (priority)
        match = re.search(Keywords.ORIENT_PATTERN, string)
        widget_orient = ""

        if match is not None:
            widget_orient = match.group(0)
            return widget_orient

        # orient from kwargs
        if "orient" in kwargs:
            _orient = kwargs.pop("orient")
            if _orient == "h":
                widget_orient = "horizontal"
            elif _orient == "v":
                widget_orient = "vertical"
            else:
                widget_orient = _orient
            return widget_orient

        # orient from settings
        if widget is None:
            return widget_orient
        try:
            widget_orient = str(widget.cget("orient"))
        except:
            pass

        return widget_orient

    @staticmethod
    def ttkstyle_widget_color(string):
        """Find and return widget color

        Parameters:

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A color keyword.
        """
        _color = re.search(Keywords.COLOR_PATTERN, string.lower())
        if _color is None:
            return ""
        else:
            widget_color = _color.group(0)
            return widget_color

    @staticmethod
    def ttkstyle_name(widget=None, string="", **kwargs):
        """Parse a string to build and return a ttkstyle name.

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

            **kwargs:
                Other keyword arguments to parse widget orientation.

        Returns:

            str:
                A ttk style name
        """
        style_string = "".join(string).lower()
        widget_color = Bootstyle.ttkstyle_widget_color(style_string)
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_orient = Bootstyle.ttkstyle_widget_orient(
            widget, style_string, **kwargs
        )
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        if widget_color:
            widget_color = f"{widget_color}."

        if widget_type:
            widget_type = f"{widget_type.title()}."

        if widget_orient:
            widget_orient = f"{widget_orient.title()}."

        if widget_class.startswith("t"):
            widget_class = widget_class.title()
        else:
            widget_class = f"T{widget_class.title()}"

        ttkstyle = f"{widget_color}{widget_type}{widget_orient}{widget_class}"
        return ttkstyle

    @staticmethod
    def ttkstyle_method_name(widget=None, string=""):
        """Parse a string to build and return the name of the
        `StyleBuilderTTK` method that creates the ttk style for the
        target widget.

        Parameters:

            widget (Widget):
                The widget object to lookup.

            string (str):
                The keyword string to parse.

        Returns:

            str:
                The name of the update method used to update the widget.
        """
        style_string = "".join(string).lower()
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        if widget_type:
            widget_type = f"_{widget_type}"

        if widget_class:
            widget_class = f"_{widget_class}"

        if not widget_type and not widget_class:
            return ""
        else:
            method_name = f"create{widget_type}{widget_class}_style"
            return method_name

    @staticmethod
    def tkupdate_method_name(widget):
        """Lookup the tkinter style update method from the widget class

        Parameters:

            widget (Widget):
                The widget object to lookup.

        Returns:

            str:
                The name of the method used to update the widget object.
        """
        widget_class = Bootstyle.ttkstyle_widget_class(widget)

        if widget_class:
            widget_class = f"_{widget_class}"

        method_name = f"update{widget_class}_style"
        return method_name

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override widget constructors with bootstyle api options.

        Parameters:

            func (Callable):
                The widget class `__init__` method
        """

        def __init__(self, *args, **kwargs):

            # capture bootstyle and style arguments
            if "bootstyle" in kwargs:
                bootstyle = kwargs.pop("bootstyle")
            else:
                bootstyle = ""

            if "style" in kwargs:
                style = kwargs.pop("style") or ""
            else:
                style = ""

            # instantiate the widget
            func(self, *args, **kwargs)

            # must be called AFTER instantiation in order to use winfo_class
            #    in the `get_ttkstyle_name` method

            if style:
                if Style.get_instance().style_exists_in_theme(style):
                    self.configure(style=style)
                else:
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, style, **kwargs
                    )
                    self.configure(style=ttkstyle)
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                self.configure(style=ttkstyle)
            else:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, "default", **kwargs
                )
                self.configure(style=ttkstyle)

        return __init__

    @staticmethod
    def override_ttk_widget_configure(func):
        """Overrides the configure method on a ttk widget.

        Parameters:

            func (Callable):
                The widget class `configure` method
        """

        def configure(self, cnf=None, **kwargs):
            # get configuration
            if cnf in ("bootstyle", "style"):
                return self.cget("style")

            if cnf is not None:
                return func(self, cnf)

            # set configuration
            if "bootstyle" in kwargs:
                bootstyle = kwargs.pop("bootstyle")
            else:
                bootstyle = ""

            if "style" in kwargs:
                style = kwargs.get("style")
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, style, **kwargs
                )
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                kwargs.update(style=ttkstyle)

            # update widget configuration
            func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def update_ttk_widget_style(
            widget: ttk.Widget = None, style_string: str = None, **kwargs
    ):
        """Update the ttk style or create if not existing.

        Parameters:

            widget (ttk.Widget):
                The widget instance being updated.

            style_string (str):
                The style string to evalulate. May be the `style`, `ttkstyle`
                or `bootstyle` argument depending on the context and scenario.

            **kwargs:
                Other optional keyword arguments.

        Returns:

            str:
                The ttkstyle or empty string if there is none.
        """
        style: Style = Style.get_instance() or Style()

        # get existing widget style if not provided
        if style_string is None:
            style_string = widget.cget("style")

        # do nothing if the style has not been set
        if not style_string:
            return ""

        if style_string == '.':
            return '.'

        # build style if not existing (example: theme changed)
        ttkstyle = Bootstyle.ttkstyle_name(widget, style_string, **kwargs)
        if not style.style_exists_in_theme(ttkstyle):
            widget_color = Bootstyle.ttkstyle_widget_color(ttkstyle)
            method_name = Bootstyle.ttkstyle_method_name(widget, ttkstyle)
            builder: StyleBuilderTTK = style._get_builder()
            builder_method = builder.name_to_method(method_name)
            builder_method(builder, widget_color)

        # subscribe popdown style to theme changes
        try:
            if widget.winfo_class() == "TCombobox":
                builder: StyleBuilderTTK = style._get_builder()
                winfo_id = hex(widget.winfo_id())
                winfo_pathname = widget.winfo_pathname(winfo_id)
                Publisher.subscribe(
                    name=winfo_pathname,
                    func=lambda w=widget: builder.update_combobox_popdown_style(
                        w
                    ),
                    channel=Channel.STD,
                )
                builder.update_combobox_popdown_style(widget)
        except:
            pass

        return ttkstyle

    @staticmethod
    def setup_ttkbootstrap_api():
        """Setup ttkbootstrap for use with tkinter and ttk. This method
        is called when ttkbootstrap is imported to perform all of the
        necessary method overrides that implement the bootstyle api."""
        from ttkbootstrap.widgets import TTK_WIDGETS
        from ttkbootstrap.widgets import TK_WIDGETS

        # TTK WIDGETS
        for widget in TTK_WIDGETS:
            try:
                # override widget constructor
                _init = Bootstyle.override_ttk_widget_constructor(
                    widget.__init__
                )
                widget.__init__ = _init

                # override configure method
                _configure = Bootstyle.override_ttk_widget_configure(
                    widget.configure
                )
                widget.configure = _configure
                widget.config = widget.configure

                # override get and set methods
                _orig_getitem = widget.__getitem
                _orig_setitem = widget.__setitem

                def __setitem(self, key, val):
                    if key in ("bootstyle", "style"):
                        return _configure(self, **{key: val})
                    return _orig_setitem(key, val)

                def __getitem(self, key):
                    if key in ("bootstyle", "style"):
                        return _configure(self, cnf=key)
                    return _orig_getitem(key)

                if (
                        widget.__name__ != "OptionMenu"
                ):  # this has it's own override
                    widget.__setitem__ = __setitem
                    widget.__getitem__ = __getitem
            except:
                # this may fail in python 3.6 for ttk widgets that do not exist
                #   in that version.
                continue

        # TK WIDGETS
        for widget in TK_WIDGETS:
            # override widget constructor
            _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
            widget.__init__ = _init

    @staticmethod
    def update_tk_widget_style(widget):
        """Lookup the widget name and call the appropriate update
        method

        Parameters:

            widget (object):
                The tcl/tk name given by `tkinter.Widget.winfo_name()`
        """
        try:
            style = Style.get_instance()
            method_name = Bootstyle.tkupdate_method_name(widget)
            builder = style._get_builder_tk()
            builder_method = getattr(StyleBuilderTK, method_name)
            builder_method(builder, widget)
        except:
            """Must pass here to prevent a failure when the user calls
            the `Style`method BEFORE an instance of `Tk` is instantiated.
            This will defer the update of the `Tk` background until the end
            of the `BootStyle` object instantiation (created by the `Style`
            method)"""
            pass

    @staticmethod
    def override_tk_widget_constructor(func):
        """Override widget constructors to apply default style for tk
        widgets.

        Parameters:

            func (Callable):
                The `__init__` method for this widget.
        """

        def __init__wrapper(self, *args, **kwargs):

            # check for autostyle flag
            if "autostyle" in kwargs:
                autostyle = kwargs.pop("autostyle")
            else:
                autostyle = True

            # instantiate the widget
            func(self, *args, **kwargs)

            if autostyle:
                Publisher.subscribe(
                    name=str(self),
                    func=lambda w=self: Bootstyle.update_tk_widget_style(w),
                    channel=Channel.STD,
                )
                Bootstyle.update_tk_widget_style(self)

        return __init__wrapper
