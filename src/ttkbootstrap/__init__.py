"""
    Why does this project exist?
    ============================
    The purpose of this project is create a set of beautifully designed 
    and easy to apply styles for your tkinter applications. Ttk can be 
    very time-consuming to style if you are just a casual user. This 
    project takes the pain out of getting a modern look and feel so 
    that you can focus on designing your application. This project was 
    created to harness the power of ttk's (and thus Python's) existing 
    built-in theme engine to create modern and professional-looking 
    user interfaces which are inspired by, and in many cases, 
    whole-sale rip-off's of the themes found on Bootswatch_. Even 
    better, you have the abilty to 
    :ref:`create and use your own custom themes <tutorial:create a new theme>` 
    using TTK Creator.

    A bootstrap approach to style
    =============================
    Many people are familiar with bootstrap for web developement. It 
    comes pre-packaged with built-in css style classes that provide a 
    professional and consistent api for quick development. I took a 
    similar approach with this project by pre-defining styles for 
    nearly all ttk widgets. This makes is very easy to apply the 
    theme colors to various widgets by using style declarations. If 
    you want a button in the `secondary` theme color, simply apply the
    **secondary.TButton** style to the button. Want a blue outlined 
    button? Apply the **info.Outline.TButton** style to the button.

    What about the old tkinter widgets?
    ===================================
    Some of the ttk widgets utilize existing tkinter widgets. For 
    example: there is a tkinter popdown list in the ``ttk.Combobox`` 
    and a legacy tkinter widget inside the ``ttk.OptionMenu``. To 
    make sure these widgets didn't stick out like a sore thumb, I 
    created a ``StyleTK`` class to apply the same color and style to 
    these legacy widgets. While these legacy widgets are not 
    necessarily intended to be used (and will probably not look as 
    nice as the ttk versions when they exist), they are available if 
    needed, and shouldn't look completely out-of-place in your 
    ttkbootstrap themed application.  
    :ref:`Check out this example <themes:legacy widget styles>` to 
    see for yourself.

    .. _Bootswatch: https://bootswatch.com/

"""
import colorsys
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import bootstyle
from ttkbootstrap.themes import DEFINED_THEMES
from ttkbootstrap.user_defined import USER_DEFINED
from PIL import ImageTk, Image, ImageDraw, ImageFont

DEFAULT = 'default'
LIGHT = 'light'
DARK = 'dark'
DEFAULT_FONT = 'Helvetica 10'
DEFAULT_THEME = 'flatly'
TTK_CLAM = 'clam'
TTK_ALT = 'alt'
TTK_DEFAULT = 'default'

bootstyle.inject_bootstyle_keyword_api()


class Style(ttk.Style):
    """A class for setting the application style.

    Sets the theme of the ``tkinter.Tk`` instance and supports all
    ttkbootstrap and ttk themes provided. This class is meant to be a
    drop-in replacement for ``ttk.Style`` and inherits all of it's
    methods and properties. Creating a ``Style`` object will
    instantiate the ``tkinter.Tk`` instance in the ``Style.master``
    property, and so it is not necessary to explicitly create an
    instance of ``tkinter.Tk``. For more details on the ``ttk.Style``
    class, see the python documentation_.

    .. code-block:: python

        # instantiate the style with default theme *flatly*
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='superhero')

        # available themes
        for theme in style.theme_names():
            print(theme)

    .. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style
    """

    def __init__(self, theme=DEFAULT_THEME, *args, **kwargs):
        """
        Parameters
        ----------
        theme : str
            the name of the theme to use at runtime; default='flatly'.

        *args : Any
            Other optional arguments

        **kwargs : Any
            Other optional keyword arguments
        """
        # this parameter has been replaced internally with py file
        if "themes_file" in kwargs:
            del kwargs["themes_file"]

        super().__init__(*args, **kwargs)
        self._styler = None
        self._theme_names = set(super().theme_names())
        self._theme_objects = {}  # prevents image garbage collection
        self._theme_definitions = {}
        self._load_themes()

        # load selected or default theme
        self.theme_use(themename=theme)

    @property
    def colors(self):
        """The theme colors"""
        theme = self.theme_use()
        if theme in list(self._theme_names):
            definition = self._theme_definitions.get(theme)
            if not definition:
                return Colors()
            else:
                return definition.colors
        else:
            return Colors()

    def _load_themes(self):
        """Load all ttkbootstrap defined themes"""
        # create a theme definition object for each theme, this will be
        # used to generate the theme in tkinter along with any assets
        # at run-time
        if USER_DEFINED:
            DEFINED_THEMES.update(USER_DEFINED)
        theme_settings = {"themes": DEFINED_THEMES}
        for name, definition in theme_settings["themes"].items():
            self.register_theme(
                ThemeDefinition(
                    name=name,
                    themetype=definition["type"],
                    font=definition.get("font") or DEFAULT_FONT,
                    colors=Colors(**definition["colors"]),
                )
            )

    def theme_names(self):
        """Return a list of all ttkbootstrap themes"""
        return list(self._theme_definitions.keys())

    def register_theme(self, definition):
        """Registers a theme definition for use by the ``Style`` class.

        This makes the definition and name available at run-time so
        that the assets and styles can be created.

        Parameters
        ----------
        definition : ThemeDefinition
            An instance of the ``ThemeDefinition`` class
        """
        self._theme_names.add(definition.name)
        self._theme_definitions[definition.name] = definition

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during*
        runtime. Otherwise, pass the theme name into the Style
        constructor to instantiate the style with a theme.

        Parameters
        ----------
        themename : str
            The name of the theme to apply when creating new widgets
        """
        self.theme = self._theme_definitions.get(themename)

        if not themename:
            return super().theme_use()

        if all([themename, themename not in self._theme_names]):
            print(f"{themename} is invalid.Try one of the following:")
            print(list(self._theme_names))
            return

        if themename in super().theme_names():
            # the theme has already been created in tkinter
            super().theme_use(themename)
            if not self.theme:
                return
            return

        # theme has not yet been created
        self._theme_objects[themename] = StylerTTK(self, self.theme)
        self._theme_objects[themename].styler_tk.style_tkinter_widgets()
        super().theme_use(themename)
        return


class ThemeDefinition:
    """A class to provide defined name, colors, and font settings for a
    ttkbootstrap theme."""

    def __init__(
        self, name="default", themetype=LIGHT, font=DEFAULT_FONT, colors=None
    ):
        """
        Parameters
        ----------
        name : str
            The name of the theme; default='default'.

        themetype : str
            The type of theme: *light* or *dark*; default='light'.

        font : str
            The default font to use for the application;
            default='helvetica'.

        colors : Colors
            An instance of the `Colors` class (provided by default)
        """
        self.name = name
        self.type = themetype
        self.font = font
        self.colors = colors if colors else Colors()

    def __repr__(self):

        return " ".join(
            [
                f"name={self.name},",
                f"type={self.type},",
                f"font={self.font},",
                f"colors={self.colors}",
            ]
        )


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
        self.bg = bg
        self.fg = fg
        self.selectbg = selectbg
        self.selectfg = selectfg
        self.border = border
        self.inputfg = inputfg
        self.inputbg = inputbg

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
            ["primary", "secondary", "success", "info", "warning", "danger"]
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


class StylerTK:
    """A class for styling tkinter widgets (not ttk)"""

    def __init__(self, styler_ttk):
        """Several ttk widgets utilize tkinter widgets in some
        capacity, such as the `popdownlist` on the ``ttk.Combobox``. To
        create a consistent user experience, standard tkinter widgets
        are themed as much as possible with the look and feel of the
        **ttkbootstrap** theme applied. Tkinter widgets are not the
        primary target of this project; however, they can be used
        without looking entirely out-of-place in most cases.

        Parameters
        ----------
        styler_ttk : StylerTTK
            An instance of the ``StylerTTK`` class.
        """
        self.master = styler_ttk.style.master
        self.theme: ThemeDefinition = styler_ttk.theme

        self.colors = self.theme.colors
        self.is_light_theme = self.theme.type == LIGHT

    def style_tkinter_widgets(self):
        """A wrapper on all widget style methods. Applies current theme
        to all standard tkinter widgets
        """
        self._style_spinbox()
        self._style_textwidget()
        self._style_button()
        self._style_label()
        self._style_checkbutton()
        self._style_radiobutton()
        self._style_entry()
        self._style_scale()
        self._style_listbox()
        self._style_menu()
        self._style_menubutton()
        self._style_labelframe()
        self._style_canvas()
        self._style_window()

    def _set_option(self, *args):
        """A convenience wrapper method to shorten the call to
        ``option_add``. *Laziness is next to godliness*.

        Parameters
        ----------
        *args : Tuple[str]
            (pattern, value, priority=80)
        """
        self.master.option_add(*args)

    def _style_window(self):
        """Apply global options to all matching ``tkinter`` widgets"""
        self.master.configure(background=self.colors.bg)
        self._set_option("*background", self.colors.bg, 60)
        self._set_option("*font", self.theme.font, 60)
        self._set_option("*activeBackground", self.colors.selectbg, 60)
        self._set_option("*activeForeground", self.colors.selectfg, 60)
        self._set_option("*selectBackground", self.colors.selectbg, 60)
        self._set_option("*selectForeground", self.colors.selectfg, 60)

    def _style_canvas(self):
        """Apply style to ``tkinter.Canvas``"""
        self._set_option("*Canvas.highlightThickness", 1)
        self._set_option("*Canvas.background", self.colors.bg)
        self._set_option("*Canvas.highlightBackground", self.colors.border)

    def _style_button(self):
        """Apply style to ``tkinter.Button``"""
        active_bg = Colors.update_hsv(self.colors.primary, vd=-0.2)
        self._set_option("*Button.relief", tk.FLAT)
        self._set_option("*Button.borderWidth", 0)
        self._set_option("*Button.activeBackground", active_bg)
        self._set_option("*Button.foreground", self.colors.selectfg)
        self._set_option("*Button.background", self.colors.primary)

    def _style_label(self):
        """Apply style to ``tkinter.Label``"""
        self._set_option("*Label.foreground", self.colors.fg)
        self._set_option("*Label.background", self.colors.bg)

    def _style_checkbutton(self):
        """Apply style to ``tkinter.Checkbutton``"""
        self._set_option("*Checkbutton.activeBackground", self.colors.bg)
        self._set_option("*Checkbutton.activeForeground", self.colors.primary)
        self._set_option("*Checkbutton.background", self.colors.bg)
        self._set_option("*Checkbutton.foreground", self.colors.fg)
        if not self.is_light_theme:
            self._set_option("*Checkbutton.selectColor", self.colors.primary)
        else:
            self._set_option("*Checkbutton.selectColor", "white")

    def _style_radiobutton(self):
        """Apply style to ``tkinter.Radiobutton``"""
        self._set_option("*Radiobutton.activeBackground", self.colors.bg)
        self._set_option("*Radiobutton.activeForeground", self.colors.primary)
        self._set_option("*Radiobutton.background", self.colors.bg)
        self._set_option("*Radiobutton.foreground", self.colors.fg)
        if not self.is_light_theme:
            self._set_option("*Radiobutton.selectColor", self.colors.primary)
        else:
            self._set_option("*Checkbutton.selectColor", "white")

    def _style_entry(self):
        """Apply style to ``tkinter.Entry``"""
        self._set_option("*Entry.relief", tk.FLAT)
        self._set_option("*Entry.highlightThickness", 1)
        self._set_option("*Entry.foreground", self.colors.inputfg)
        self._set_option("*Entry.highlightBackground", self.colors.border)
        self._set_option("*Entry.highlightColor", self.colors.primary)

        if self.is_light_theme:
            self._set_option("*Entry.background", self.colors.inputbg)
        else:
            self._set_option(
                "*Entry.background",
                Colors.update_hsv(self.colors.inputbg, vd=-0.1),
            )

    def _style_scale(self):
        """Apply style to ``tkinter.Scale``"""
        active_color = Colors.update_hsv(self.colors.primary, vd=-0.2)
        self._set_option("*Scale.background", self.colors.primary)
        self._set_option("*Scale.showValue", False)
        self._set_option("*Scale.sliderRelief", tk.FLAT)
        self._set_option("*Scale.borderWidth", 0)
        self._set_option("*Scale.activeBackground", active_color)
        self._set_option("*Scale.highlightThickness", 1)
        self._set_option("*Scale.highlightColor", self.colors.border)
        self._set_option("*Scale.highlightBackground", self.colors.border)
        self._set_option("*Scale.troughColor", self.colors.inputbg)

    def _style_spinbox(self):
        """Apply style to `tkinter.Spinbox``"""
        self._set_option("*Spinbox.foreground", self.colors.inputfg)
        self._set_option("*Spinbox.relief", tk.FLAT)
        self._set_option("*Spinbox.highlightThickness", 1)
        self._set_option("*Spinbox.highlightColor", self.colors.primary)
        self._set_option("*Spinbox.highlightBackground", self.colors.border)
        if self.is_light_theme:
            self._set_option("*Spinbox.background", self.colors.inputbg)
        else:
            self._set_option(
                "*Spinbox.background",
                Colors.update_hsv(self.colors.inputbg, vd=-0.1),
            )

    def _style_listbox(self):
        """Apply style to ``tkinter.Listbox``"""
        self._set_option("*Listbox.foreground", self.colors.inputfg)
        self._set_option("*Listbox.background", self.colors.inputbg)
        self._set_option("*Listbox.selectBackground", self.colors.selectbg)
        self._set_option("*Listbox.selectForeground", self.colors.selectfg)
        self._set_option("*Listbox.highlightColor", self.colors.primary)
        self._set_option("*Listbox.highlightBackground", self.colors.border)
        self._set_option("*Listbox.highlightThickness", 1)
        self._set_option("*Listbox.activeStyle", "none")
        self._set_option("*Listbox.relief", tk.FLAT)

    def _style_menubutton(self):
        """Apply style to ``tkinter.Menubutton``"""
        hover_color = Colors.update_hsv(self.colors.primary, vd=-0.2)
        self._set_option("*Menubutton.background", self.colors.primary)
        self._set_option("*Menubutton.foreground", self.colors.selectfg)
        self._set_option("*Menubutton.activeBackground", hover_color)
        self._set_option("*Menubutton.borderWidth", 0)

    def _style_menu(self):
        """Apply style to ``tkinter.Menu``"""
        self._set_option("*Menu.tearOff", 0)
        self._set_option("*Menu.activeBackground", self.colors.selectbg)
        self._set_option("*Menu.activeForeground", self.colors.selectfg)
        self._set_option("*Menu.foreground", self.colors.fg)
        self._set_option("*Menu.selectColor", self.colors.primary)
        self._set_option("*Menu.font", self.theme.font)
        if self.is_light_theme:
            self._set_option("*Menu.background", self.colors.inputbg)
        else:
            self._set_option("*Menu.background", self.colors.bg)

    def _style_labelframe(self):
        """Apply style to ``tkinter.Labelframe``"""
        self._set_option("*Labelframe.highlightColor", self.colors.border)
        self._set_option("*Labelframe.foreground", self.colors.fg)
        self._set_option("*Labelframe.font", self.theme.font)
        self._set_option("*Labelframe.borderWidth", 1)
        self._set_option("*Labelframe.highlightThickness", 0)

    def _style_textwidget(self):
        """Apply style to ``tkinter.Text``"""
        self._set_option("*Text.background", self.colors.inputbg)
        self._set_option("*Text.foreground", self.colors.inputfg)
        self._set_option("*Text.highlightColor", self.colors.primary)
        self._set_option("*Text.highlightBackground", self.colors.border)
        self._set_option("*Text.borderColor", self.colors.border)
        self._set_option("*Text.insertBackground", self.colors.inputfg)
        self._set_option("*Text.insertWidth", 1)
        self._set_option("*Text.highlightThickness", 1)
        self._set_option("*Text.relief", tk.FLAT)
        self._set_option("*Text.font", self.theme.font)
        self._set_option("*Text.padX", 5)
        self._set_option("*Text.padY", 5)


class StylerTTK:
    """A class to create a new ttk theme"""

    def __init__(self, style, definition):
        """Create a new ttk theme by using a combination of built-in
        themes and some image-based elements using ``pillow``. A theme
        is generated at runtime and is available to use with the
        ``Style`` class methods. The base theme of all **ttkbootstrap**
        themes is *clam*. In many cases, widget layouts are re-created
        using an assortment of elements from various styles such as
        *clam*, *alt*, *default*, etc...

        Parameters
        ----------
        style : Style
            An instance of ``ttk.Style``.

        definition : ThemeDefinition
            An instance of ``ThemeDefinition``; used to create the
            theme settings.
        """
        self.style = style
        self.theme: ThemeDefinition = definition
        self.theme_images = {}
        self.colors = self.theme.colors
        self.is_light_theme = self.theme.type == LIGHT
        self.settings = {}
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal
        style methods.
        """
        self.update_ttk_theme_settings()
        self.style.theme_create(self.theme.name, TTK_CLAM, self.settings)

    def update_ttk_theme_settings(self):
        """Update the settings dictionary that is used to create a
        theme. This is a wrapper on all the `_style_widget` methods
        which define the layout, configuration, and styling mapping
        for each ttk widget.
        """
        self.create_default_style()
        self.create_labelframe_style()
        self.create_spinbox_style()
        self.create_scale_style()
        self.create_scrollbar_style()
        self.create_combobox_style()
        self.create_exit_button_style()
        self.create_frame_style()
        self.create_calendar_style()
        self.create_checkbutton_style()
        self.create_entry_style()
        self.create_label_style()
        self.create_meter_style()
        self.create_notebook_style()
        self.create_outline_button_style()
        self.create_outline_menubutton_style()
        self.create_outline_toolbutton_style()
        self.create_progressbar_style()
        self.create_striped_progressbar_style()
        self.create_floodgauge_style()
        self.create_radiobutton_style()
        self.create_solid_button_style()
        self.create_link_button_style()
        self.create_solid_menubutton()
        self.create_solid_toolbutton_style()
        self.create_treeview_style()
        self.create_separator_style()
        self.create_panedwindow_style()
        self.create_round_toggle_style()
        self.create_square_toggle_style()
        self.create_sizegrip_style()

    def create_default_style(self):
        """Setup the default ``ttk.Style`` configuration. These
        defaults are applied to any widget that contains these
        element options. This method should be called *first* before
        any other style is applied during theme creation.
        """
        self.settings.update(
            {
                ".": {
                    "configure": {
                        "background": self.colors.bg,
                        "darkcolor": self.colors.border,
                        "foreground": self.colors.fg,
                        "troughcolor": self.colors.bg,
                        "selectbg": self.colors.selectbg,
                        "selectfg": self.colors.selectfg,
                        "selectforeground": self.colors.selectfg,
                        "selectbackground": self.colors.selectbg,
                        "fieldbg": "white",
                        "font": self.theme.font,
                        "borderwidth": 1,
                        "focuscolor": "",
                    }
                }
            }
        )

    def create_combobox_style(self):
        """Create style configuration for ``ttk.Combobox``. This
        element style is created with a layout that combines *clam* and
        *default* theme elements.
        """
        STYLE = 'TCombobox'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg

        self.settings.update(
            {
                "Combobox.downarrow": {
                    "element create": ("from", TTK_DEFAULT)},
                "Combobox.padding": {
                    "element create": ("from", TTK_CLAM)},
                "Combobox.textarea": {
                    "element create": ("from", TTK_CLAM)}})

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                ttkstyle = STYLE
                focuscolor = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                focuscolor = self.colors.get(color)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "bordercolor": bordercolor,
                            "darkcolor": self.colors.inputbg,
                            "lightcolor": self.colors.inputbg,
                            "arrowcolor": self.colors.inputfg,
                            "foreground": self.colors.inputfg,
                            "fieldbackground ": self.colors.inputbg,
                            "background ": self.colors.inputbg,
                            "insertcolor": self.colors.inputfg,
                            "relief": tk.FLAT,
                            "padding": 5,
                            "arrowsize ": 14
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "bordercolor": [
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", focuscolor),
                            ],
                            "lightcolor": [
                                ("focus !disabled", focuscolor),
                                ("pressed !disabled", focuscolor),
                            ],
                            "darkcolor": [
                                ("focus !disabled", focuscolor),
                                ("pressed !disabled", focuscolor),
                            ],
                            "arrowcolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", focuscolor),
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", focuscolor)]
                        },
                        "layout": [
                            ("combo.Spinbox.field", {
                                "side": tk.TOP,
                                "sticky": tk.EW,
                                "children": [
                                    ("Combobox.downarrow", {
                                        "side": tk.RIGHT,
                                        "sticky": tk.NS
                                    }),
                                    ("Combobox.padding", {
                                        "expand": "1",
                                        "sticky": tk.NSEW,
                                        "children": [
                                            ("Combobox.textarea", {
                                                "sticky": tk.NSEW})]})]})]
                    }
                }
            )

    def create_separator_style(self):
        """Create style configuration for ttk separator:
        *ttk.Separator*. The default style for light will be border,
        but dark will be primary, as this makes the most sense for
        general use. However, all other colors will be available as
        well through styling.
        """
        HSTYLE = 'Horizontal.TSeparator'
        VSTYLE = 'Vertical.TSeparator'

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        # horizontal separator
        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                background = default_color
                ttkstyle = HSTYLE
            else:
                background = self.colors.get(color)
                ttkstyle = f'{color}.{HSTYLE}'

            # create separator image
            _img = ImageTk.PhotoImage(Image.new("RGB", (40, 1), background))
            _name = _img._PhotoImage__photo.name
            self.theme_images[_name] = _img
            self.settings.update(
                {
                    f"{ttkstyle}.Separator.separator": {
                        "element create": ("image", _name)},
                    ttkstyle: {
                        "layout": [
                            (f"{ttkstyle}.Separator.separator",
                             {"sticky": tk.EW})]
                    }
                }
            )

        # vertical separator
        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                background = default_color
                ttkstyle = VSTYLE
            else:
                background = self.colors.get(color)
                ttkstyle = f'{color}.{VSTYLE}'

            _img = ImageTk.PhotoImage(Image.new("RGB", (1, 40), background))
            _name = _img._PhotoImage__photo.name
            self.theme_images[_name] = _img
            self.settings.update(
                {
                    f"{ttkstyle}.Separator.separator": {
                        "element create": ("image", _name)},
                    ttkstyle: {
                        "layout": [
                            (f"{ttkstyle}.Separator.separator",
                             {"sticky": tk.NS})]
                    }
                }
            )

    def create_striped_progressbar_assets(self, colorname):
        """Create the striped progressbar image and return as a
        ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property; eg.
            `primary`, `secondary`, `success`.

        Returns
        -------
        List[str]
            A list of photoimage names.
        """
        if colorname == DEFAULT:
            barcolor = self.colors.primary
        else:
            barcolor = self.colors.get(colorname)

        # calculate value of the light color
        brightness = colorsys.rgb_to_hsv(*Colors.hex_to_rgb(barcolor))[2]
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
        draw.polygon(
            xy=[(0, 52), (48, 100), (0, 100)],
            fill=barcolor)

        _resized = img.resize((16, 16), Image.LANCZOS)
        h_img = ImageTk.PhotoImage(_resized)
        h_name = h_img._PhotoImage__photo.name
        v_img = ImageTk.PhotoImage(_resized.rotate(90))
        v_name = v_img._PhotoImage__photo.name

        self.theme_images[h_name] = h_img
        self.theme_images[v_name] = v_img
        return [h_name, v_name]

    def create_striped_progressbar_style(self):
        """Apply a striped theme to the progressbar"""
        HSTYLE = 'Striped.Horizontal.TProgressbar'
        VSTYLE = 'Striped.Vertical.TProgressbar'

        for color in [DEFAULT, *self.colors]:

            h_img, v_img = self.create_striped_progressbar_assets(color)

            if color == DEFAULT:
                h_ttkstyle = HSTYLE
                v_ttkstyle = VSTYLE
            else:
                h_ttkstyle = f'{color}.{HSTYLE}'
                v_ttkstyle = f'{color}.{VSTYLE}'

            self.settings.update(
                {
                    f"{h_ttkstyle}.Progressbar.pbar": {
                        "element create": (
                            "image", h_img,
                            {"width": 16, "sticky": tk.EW})},
                    h_ttkstyle: {
                        "layout": [
                            ("Horizontal.Progressbar.trough", {
                                "sticky": tk.NSEW,
                                "children": [
                                    (f"{h_ttkstyle}.Progressbar.pbar", {
                                        "side": tk.LEFT,
                                        "sticky": tk.NS})]})],
                        "configure": {
                            "troughcolor": self.colors.inputbg,
                            "thickness": 16,
                            "borderwidth": 1
                        }
                    },
                    f"{v_ttkstyle}.Progressbar.pbar": {
                        "element create": (
                            "image", v_img,
                            {"width": 16, "sticky": tk.NS})},
                    v_ttkstyle: {
                        "layout": [
                            ("Vertical.Progressbar.trough", {
                                "sticky": tk.NSEW,
                                "children": [
                                    (f"{v_ttkstyle}.Progressbar.pbar", {
                                        "side": tk.BOTTOM,
                                        "sticky": tk.EW})]})],
                        "configure": {
                            "troughcolor": self.colors.inputbg,
                            "thickness": 16,
                            "borderwidth": 1
                        }
                    }
                }
            )

    def create_progressbar_style(self):
        """Create style configuration for ttk progressbar"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.inputbg

        self.settings.update(
            {
                "Progressbar.trough": {"element create": ("from", TTK_CLAM)},
                "Progressbar.pbar": {"element create": ("from", TTK_DEFAULT)},
                "TProgressbar": {
                    "configure": {
                        "thickness": 14,
                        "borderwidth": 1,
                        "bordercolor": bordercolor,
                        "lightcolor": self.colors.border,
                        "pbarrelief": tk.FLAT,
                        "troughcolor": self.colors.inputbg,
                        "background": self.colors.primary,
                    }
                },
            }
        )
        for color in self.colors:
            self.settings.update(
                {
                    f"{color}.Horizontal.TProgressbar": {
                        "configure": {"background": self.colors.get(color)}
                    },
                    f"{color}.Vertical.TProgressbar": {
                        "configure": {"background": self.colors.get(color)}
                    }
                }
            )

    @staticmethod
    def create_scale_assets(color, size=16):
        """Create a circle slider image based on given size and color;
        used in the slider widget.

        Parameters
        ----------
        color : str
            A hexadecimal color value.

        size : int
            The size diameter of the slider circle; default=16.

        Returns
        -------
        ImageTk.PhotoImage
            An image drawn in the shape of the circle of the theme
            color specified.
        """
        im = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=color)
        return ImageTk.PhotoImage(im.resize((size, size), Image.LANCZOS))

    def create_scale_style(self):
        """Create style configuration for ttk scale: *ttk.Scale*"""
        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            trough_color = Colors.update_hsv(self.colors.inputbg, vd=-0.03)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            trough_color = self.colors.inputbg

        pressed_vd = -0.2
        hover_vd = -0.1

        # create widget images
        self.theme_images.update(
            {
                "primary_disabled": self.create_scale_assets(disabled_fg),
                "primary_regular": self.create_scale_assets(
                    self.colors.primary
                ),
                "primary_pressed": self.create_scale_assets(
                    Colors.update_hsv(self.colors.primary, vd=pressed_vd)
                ),
                "primary_hover": self.create_scale_assets(
                    Colors.update_hsv(self.colors.primary, vd=hover_vd)
                ),
                "htrough": ImageTk.PhotoImage(
                    Image.new("RGB", (40, 5), trough_color)
                ),
                "vtrough": ImageTk.PhotoImage(
                    Image.new("RGB", (5, 40), trough_color)
                ),
            }
        )

        # The layout is derived from the 'xpnative' theme
        self.settings.update(
            {
                "Horizontal.TScale": {
                    "layout": [
                        (
                            "Scale.focus",
                            {
                                "expand": "1",
                                "sticky": tk.NSEW,
                                "children": [
                                    (
                                        "Horizontal.Scale.track",
                                        {"sticky": tk.EW},
                                    ),
                                    (
                                        "Horizontal.Scale.slider",
                                        {"side": tk.LEFT, "sticky": ""},
                                    ),
                                ],
                            },
                        )
                    ]
                },
                "Vertical.TScale": {
                    "layout": [
                        (
                            "Scale.focus",
                            {
                                "expand": "1",
                                "sticky": tk.NSEW,
                                "children": [
                                    ("Vertical.Scale.track",
                                     {"sticky": tk.NS}),
                                    (
                                        "Vertical.Scale.slider",
                                        {"side": tk.TOP, "sticky": ""},
                                    ),
                                ],
                            },
                        )
                    ]
                },
                "Horizontal.Scale.track": {
                    "element create": ("image", self.theme_images["htrough"])
                },
                "Vertical.Scale.track": {
                    "element create": ("image", self.theme_images["vtrough"])
                },
                "Scale.slider": {
                    "element create": (
                        "image",
                        self.theme_images["primary_regular"],
                        ("disabled", self.theme_images["primary_disabled"]),
                        (
                            "pressed !disabled",
                            self.theme_images["primary_pressed"],
                        ),
                        (
                            "hover !disabled",
                            self.theme_images["primary_hover"],
                        ),
                    )
                },
            }
        )
        for color in self.colors:
            self.theme_images.update(
                {
                    f"{color}_regular": self.create_scale_assets(
                        self.colors.get(color)
                    ),
                    f"{color}_pressed": self.create_scale_assets(
                        Colors.update_hsv(
                            self.colors.get(color), vd=pressed_vd
                        )
                    ),
                    f"{color}_hover": self.create_scale_assets(
                        Colors.update_hsv(self.colors.get(color), vd=hover_vd)
                    ),
                }
            )

            # The layout is derived from the 'xpnative' theme
            self.settings.update(
                {
                    f"{color}.Horizontal.TScale": {
                        "layout": [
                            (
                                "Scale.focus",
                                {
                                    "expand": "1",
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Horizontal.Scale.track",
                                            {"sticky": tk.EW},
                                        ),
                                        (
                                            f"{color}.Scale.slider",
                                            {"side": tk.LEFT, "sticky": ""},
                                        ),
                                    ],
                                },
                            )
                        ]
                    },
                    f"{color}.Vertical.TScale": {
                        "layout": [
                            (
                                f"{color}.Scale.focus",
                                {
                                    "expand": "1",
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Vertical.Scale.track",
                                            {"sticky": tk.NS},
                                        ),
                                        (
                                            f"{color}.Scale.slider",
                                            {"side": tk.TOP, "sticky": ""},
                                        ),
                                    ],
                                },
                            )
                        ]
                    },
                    f"{color}.Scale.slider": {
                        "element create": (
                            "image",
                            self.theme_images[f"{color}_regular"],
                            (
                                "disabled",
                                self.theme_images["primary_disabled"],
                            ),
                            ("pressed", self.theme_images[f"{color}_pressed"]),
                            ("hover", self.theme_images[f"{color}_hover"]),
                        )
                    },
                }
            )

    def create_floodgauge_style(self):
        """Create a style configuration for the *ttk.Progressbar* that makes 
        it into a floodgauge. Which is essentially a very large progress bar 
        with text in the middle.
        """
        HSTYLE = 'Horizontal.TFloodgauge'
        VSTYLE = 'Vertical.TFloodgauge'
        FLOOD_FONT = 'helvetica 14'

        self.settings.update(
            {
                "Floodgauge.trough": {"element create": ("from", TTK_CLAM)},
                "Floodgauge.pbar": {"element create": ("from", TTK_DEFAULT)},
            }
        )
        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                h_ttkstyle = HSTYLE
                v_ttkstyle = VSTYLE
                background = self.colors.primary
            else:
                h_ttkstyle = f'{color}.{HSTYLE}'
                v_ttkstyle = f'{color}.{VSTYLE}'
                background = self.colors.get(color)

            troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)

            self.settings.update({
                "Horizontal.TFloodgauge": {
                    "layout": [
                        ("Floodgauge.trough", {"children": [
                            ("Floodgauge.pbar", {"sticky": tk.NS}),
                            ("Floodgauge.label", {"sticky": ""})],
                            "sticky": tk.NSEW}
                         )
                    ]
                },
                "Vertical.TFloodgauge": {
                    "layout": [
                        ("Floodgauge.trough", {"children": [
                            ("Floodgauge.pbar", {"sticky": tk.EW}),
                            ("Floodgauge.label", {"sticky": ""})],
                            "sticky": tk.NSEW
                        }
                        )
                    ]
                },
                h_ttkstyle: {
                    "configure": {
                        "thickness": 50,
                        "borderwidth": 1,
                        "bordercolor": background,
                        "lightcolor": background,
                        "pbarrelief": tk.FLAT,
                        "troughcolor": troughcolor,
                        "background": background,
                        "foreground": self.colors.selectfg,
                        "justify": tk.CENTER,
                        "anchor": tk.CENTER,
                        "font": FLOOD_FONT,
                    }
                },
                v_ttkstyle: {
                    "configure": {
                        "thickness": 50,
                        "borderwidth": 1,
                        "bordercolor": background,
                        "lightcolor": background,
                        "pbarrelief": tk.FLAT,
                        "troughcolor": troughcolor,
                        "background": background,
                        "foreground": self.colors.selectfg,
                        "justify": tk.CENTER,
                        "anchor": tk.CENTER,
                        "font": FLOOD_FONT
                    }
                },
            }
            )

    def create_arrow_assets(self, arrowcolor, pressed, active):
        """Create horizontal and vertical arrow assets to be used for
        buttons"""
        assets = dict()

        def draw_arrow(color: str, name: str):

            img = Image.new("RGBA", (11, 11))
            draw = ImageDraw.Draw(img)

            draw.line([2, 6, 2, 9], fill=color)
            draw.line([3, 5, 3, 8], fill=color)
            draw.line([4, 4, 4, 7], fill=color)
            draw.line([5, 3, 5, 6], fill=color)
            draw.line([6, 4, 6, 7], fill=color)
            draw.line([7, 5, 7, 8], fill=color)
            draw.line([8, 6, 8, 9], fill=color)

            _name = f'{self.theme.name}.{name}'
            assets.update({f"{_name}.uparrow": ImageTk.PhotoImage(img)})
            assets.update(
                {f"{_name}.downarrow": ImageTk.PhotoImage(img.rotate(180))})
            assets.update(
                {f"{_name}.leftarrow": ImageTk.PhotoImage(img.rotate(90))})
            assets.update(
                {f"{_name}.rightarrow": ImageTk.PhotoImage(img.rotate(-90))})

        draw_arrow(arrowcolor, "normal")
        draw_arrow(pressed, "pressed")
        draw_arrow(active, "active")
        self.theme_images = {**self.theme_images, **assets}

    def create_scrollbar_style(self):
        """Create style configuration for ttk scrollbar: *ttk.Scrollbar*. This 
        theme uses elements from the *alt* theme tobuild the widget layout.
        """
        troughcolor = Colors.update_hsv(self.colors.bg, vd=-0.05)

        if self.is_light_theme:
            background = Colors.update_hsv(self.colors.bg, vd=-0.25)
            pressed = Colors.update_hsv(background, vd=-0.35)
            active = Colors.update_hsv(background, vd=-0.25)
        else:
            background = Colors.update_hsv(
                color=self.colors.selectbg,
                vd=0.35,
                sd=-0.1
            )
            pressed = Colors.update_hsv(background, vd=0.05)
            active = Colors.update_hsv(background, vd=0.15)

        img_test = self.theme_images.get(f'{self.theme.name}.normal.uparrow')
        if img_test is None:
            self.create_arrow_assets(background, pressed, active)

        img = self.theme_images
        _name = self.theme.name

        up_normal = img.get(f'{_name}.normal.uparrow')
        up_pressed = img.get(f'{_name}.pressed.uparrow')
        up_active = img.get(f'{_name}.active.uparrow')

        dw_normal = img.get(f'{_name}.normal.downarrow')
        dw_pressed = img.get(f'{_name}.pressed.downarrow')
        dw_active = img.get(f'{_name}.active.downarrow')

        lf_normal = img.get(f'{_name}.normal.leftarrow')
        lf_pressed = img.get(f'{_name}.pressed.leftarrow')
        lf_active = img.get(f'{_name}.active.leftarrow')

        rt_normal = img.get(f'{_name}.normal.rightarrow')
        rt_pressed = img.get(f'{_name}.pressed.rightarrow')
        rt_active = img.get(f'{_name}.active.rightarrow')

        self.settings.update(
            {
                "Vertical.Scrollbar.trough": {
                    "element create": ("from", TTK_ALT)
                },
                "Vertical.Scrollbar.thumb": {
                    "element create": ("from", TTK_ALT)
                },
                "Vertical.Scrollbar.uparrow": {
                    "element create": ("image", up_normal, ('pressed', up_pressed), ('active', up_active))
                },
                "Vertical.Scrollbar.downarrow": {
                    "element create": ("image", dw_normal, ('pressed', dw_pressed), ('active', dw_active))
                },
                "Horizontal.Scrollbar.trough": {
                    "element create": ("from", TTK_ALT)
                },
                "Horizontal.Scrollbar.thumb": {
                    "element create": ("from", TTK_ALT)
                },
                "Horizontal.Scrollbar.leftarrow": {
                    "element create": ("image", lf_normal, ('pressed', lf_pressed), ('active', lf_active))
                },
                "Horizontal.Scrollbar.rightarrow": {
                    "element create": ("image", rt_normal, ('pressed', rt_pressed), ('active', rt_active))
                },
                "TScrollbar": {
                    "configure": {
                        "troughrelief": tk.FLAT,
                        "relief": tk.FLAT,
                        "troughborderwidth": 1,
                        "arrowcolor": self.colors.inputfg,
                        "troughcolor": troughcolor,
                        "background": background,
                        "arrowsize": 11,
                        "width": 11
                    },
                    "map": {
                        "background": [
                            ("pressed", pressed),
                            ("active", active),
                        ]
                    },
                },
            }
        )

    def create_spinbox_style(self):
        """Create style configuration for ttk spinbox: *ttk.Spinbox*

        This widget uses elements from the *default* and *clam* theme 
        to create the widget layout. For dark themes,the spinbox.field 
        is created from the *default* theme element because the 
        background color shines through the corners of the widget when 
        the primary theme background color is dark.
        """
        STYLE = 'TSpinbox'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg

        self.settings.update(
            {
                "Spinbox.uparrow": {
                    "element create": ("from", TTK_DEFAULT)},
                "Spinbox.downarrow": {
                    "element create": ("from", TTK_DEFAULT)},
                STYLE: {"layout": [
                    ("custom.Spinbox.field", {
                        "side": tk.TOP,
                        "sticky": tk.EW,
                        "children": [
                            ("null", {
                                "side": tk.RIGHT,
                                "sticky": "",
                                "children": [
                                    (
                                        "Spinbox.uparrow", {
                                            "side": tk.TOP,
                                            "sticky": tk.E}
                                    ),
                                    ("Spinbox.downarrow", {
                                        "side": tk.BOTTOM,
                                        "sticky": tk.E,
                                    }
                                    )]
                            }
                            ),
                            (
                                "Spinbox.padding", {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        (
                                            "Spinbox.textarea",
                                            {"sticky": tk.NSEW})]
                                }
                            )
                        ]
                    }
                    )
                ]
                }
            }
        )

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                ttkstyle = STYLE
                focuscolor = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                focuscolor = self.colors.get(color)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "bordercolor": bordercolor,
                            "darkcolor": self.colors.inputbg,
                            "lightcolor": self.colors.inputbg,
                            "fieldbackground": self.colors.inputbg,
                            "foreground": self.colors.inputfg,
                            "borderwidth": 0,
                            "background": self.colors.inputbg,
                            "relief": tk.FLAT,
                            "arrowcolor": self.colors.inputfg,
                            "insertcolor": self.colors.inputfg,
                            "arrowsize": 14,
                            "padding": (10, 5),
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "bordercolor": [
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", focuscolor),
                            ],
                            "arrowcolor": [
                                ("disabled !disabled", disabled_fg),
                                ("pressed !disabled", focuscolor),
                                ("hover !disabled", self.colors.inputfg),
                            ],
                            "lightcolor": [
                                ("focus !disabled", focuscolor)
                            ],
                            "darkcolor": [
                                ("focus !disabled", focuscolor)
                            ],
                        }
                    }
                }
            )

    def create_treeview_style(self):
        """Create style configuration for ttk treeview"""
        STYLE = 'Treeview'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)

        self.settings.update(
            {
                STYLE: {
                    "layout": [
                        ("Button.border", {
                            "sticky": tk.NSEW,
                            "border": "1",
                            "children": [
                                ("Treeview.padding", {
                                    "sticky": tk.NSEW,
                                    "children": [
                                        ("Treeview.treearea", {
                                            "sticky": tk.NSEW})]})]})]
                },
                "Treeitem.indicator": {"element create": ("from", TTK_ALT)},
            }
        )

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                background = self.colors.inputbg
                foreground = self.colors.inputfg
                body_style = 'Treeview'
                header_style = 'Treeview.Heading'
            else:
                background = self.colors.get(color)
                foreground = self.colors.selectfg
                body_style = f'{color}.Treeview'
                header_style = f'{color}.Treeview.Heading'

            self.settings.update(
                {
                    body_style: {
                        "configure": {
                            "background": self.colors.inputbg,
                            "fieldbackground": self.colors.inputbg,
                            "foreground": self.colors.inputfg,
                            "bordercolor": self.colors.bg,
                            "lightcolor": self.colors.border,
                            "darkcolor": self.colors.border,
                        },
                        "map": {
                            "background": [
                                ("selected", self.colors.selectbg)],
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("selected", self.colors.selectfg)],
                        },
                    },
                    header_style: {
                        "configure": {
                            "background": background,
                            "foreground": foreground,
                            "relief": tk.FLAT,
                            "padding": 5
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "bordercolor": [
                                ("focus !disabled", background)
                            ],
                        },
                    }
                }
            )

    def create_frame_style(self):
        """Create style configuration for ttk frame"""
        STYLE = 'TFrame'

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                ttkstyle = STYLE
                background = self.colors.bg
            else:
                ttkstyle = f'{color}.{STYLE}'
                background = self.colors.get(color)

            self.settings.update(
                {
                    ttkstyle:
                    {
                        "configure":
                        {
                            "background": background
                        }
                    }
                }
            )

    def create_solid_button_style(self):
        """Apply a solid color style to ttk button"""

        STYLE = 'TButton'

        disabled_fg = self.colors.selectbg
        disabled_bg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                background = self.colors.primary
                ttkstyle = STYLE
            else:
                background = self.colors.get(color)
                ttkstyle = f'{color}.{STYLE}'
            if self.is_light_theme:
                pressed = Colors.update_hsv(background, vd=-0.2)
                hover = Colors.update_hsv(background, vd=-0.1)
            else:
                pressed = Colors.update_hsv(background, vd=0.2)
                hover = Colors.update_hsv(background, vd=0.1)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": self.colors.selectfg,
                            "background": background,
                            "bordercolor": background,
                            "darkcolor": background,
                            "lightcolor": background,
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": self.colors.selectfg,
                            "padding": (10, 5),
                            "anchor": tk.CENTER
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "background": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "darkcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover)
                            ],
                            "lightcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover)
                            ]}
                    }
                }
            )

    def create_outline_button_style(self):
        """Apply an outline style to ttk button. This button has a 
        solid button look on focus and hover.
        """
        STYLE = 'Outline.TButton'

        disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                foreground = self.colors.primary
                ttkstyle = STYLE
            else:
                foreground = self.colors.get(color)
                ttkstyle = f'{color}.{STYLE}'

            if self.is_light_theme:
                pressed = Colors.update_hsv(foreground, vd=-0.1)
                hover = Colors.update_hsv(foreground, vd=-0.2)
            else:
                pressed = Colors.update_hsv(foreground, vd=0.1)
                hover = Colors.update_hsv(foreground, vd=0.2)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": foreground,
                            "background": self.colors.bg,
                            "bordercolor": foreground,
                            "darkcolor": self.colors.bg,
                            "lightcolor": self.colors.bg,
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": foreground,
                            "padding": (10, 5),
                            "anchor": tk.CENTER
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                            "background": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "focuscolor": [
                                ("pressed !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                            "darkcolor": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "lightcolor": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                        },
                    }
                }
            )

    def create_link_button_style(self):
        """Apply a solid color style to ttk button"""

        STYLE = 'Link.TButton'

        pressed = self.colors.info
        hover = self.colors.info

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                foreground = self.colors.fg
                ttkstyle = STYLE
                focuscolor = self.colors.fg
            else:
                foreground = self.colors.get(color)
                ttkstyle = f'{color}.{STYLE}'
                focuscolor = foreground

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": foreground,
                            "background": self.colors.bg,
                            "bordercolor": self.colors.bg,
                            "darkcolor": self.colors.bg,
                            "lightcolor": self.colors.bg,
                            "relief": tk.RAISED,
                            "font": self.theme.font,
                            "focusthickness": 0,
                            "focuscolor": foreground,
                            "padding": (10, 5),
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover)
                            ],
                            "shiftrelief": [("pressed !disabled", -1)],
                            "focuscolor": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", pressed)
                            ],
                            "background": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", self.colors.bg),
                                ("hover !disabled", self.colors.bg),
                            ],
                            "bordercolor": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", self.colors.bg),
                                ("hover !disabled", self.colors.bg),
                            ],
                            "darkcolor": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", self.colors.bg),
                                ("hover !disabled", self.colors.bg),
                            ],
                            "lightcolor": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", self.colors.bg),
                                ("hover !disabled", self.colors.bg),
                            ],
                        },
                    }
                }
            )

    def create_square_toggle_assets(self, colorname):
        """Create a set of images for the square toggle button and 
        return as ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property

        Returns
        -------
        List[str]
            A list of tkinter image names
        """
        if colorname == DEFAULT:
            prime_color = self.colors.primary
        else:
            prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = prime_color
        on_fill = self.colors.bg

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)

        else:
            off_border = self.colors.inputbg
            off_indicator = self.colors.inputbg
            disabled_fg = self.colors.inputbg

        off_fill = self.colors.bg
        toggle_off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rectangle(
            xy=[1, 1, 225, 129],
            outline=off_border,
            width=6,
            fill=off_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=off_indicator)

        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rectangle(
            xy=[1, 1, 225, 129],
            outline=on_border,
            width=6,
            fill=on_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=on_indicator)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        toggle_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)

        image_names = []
        for im in [toggle_on, toggle_off, toggle_disabled]:
            _im = ImageTk.PhotoImage(im.resize((24, 15), Image.LANCZOS))
            _name = _im._PhotoImage__photo.name
            image_names.append(_name)
            self.theme_images[_name] = _im

        return image_names

    def create_round_toggle_assets(self, colorname):
        """Create a set of images for the rounded toggle button and 
        return as ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property

        Returns
        -------
        List[str]
            A list of tkinter image names
        """
        if colorname == DEFAULT:
            prime_color = self.colors.primary
        else:
            prime_color = self.colors.get(colorname)

        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            off_border = self.colors.inputbg
            off_indicator = self.colors.inputbg
            disabled_fg = self.colors.inputbg

        off_fill = self.colors.bg
        toggle_off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=off_border,
            width=6,
            fill=off_fill,
        )
        draw.ellipse([20, 18, 112, 110], fill=off_indicator)

        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=on_border,
            width=6,
            fill=on_fill,
        )
        draw.ellipse([20, 18, 112, 110], fill=on_indicator)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        toggle_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=disabled_fg,
            width=6
        )
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)

        image_names = []
        for im in [toggle_on, toggle_off, toggle_disabled]:
            _im = ImageTk.PhotoImage(im.resize((24, 15), Image.LANCZOS))
            _name = _im._PhotoImage__photo.name
            image_names.append(_name)
            self.theme_images[_name] = _im

        return image_names

    def create_round_toggle_style(self):
        """Apply a rounded toggle switch style to ttk widgets that accept 
        the toolbutton style (for example, a checkbutton: *ttk.Checkbutton*)
        """
        STYLE = 'Roundtoggle.Toolbutton'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:

            _on, _off, _disabled = self.create_round_toggle_assets(color)

            if color == DEFAULT:
                ttkstyle = STYLE
                indicatorcolor = self.colors.primary
            else:
                ttkstyle = f"{color}.{STYLE}"
                indicatorcolor = self.colors.get(color)

            self.settings.update(
                {
                    f"{ttkstyle}.indicator": {
                        "element create": ("image", _on,
                                           ("disabled", _disabled),
                                           ("!selected", _off),
                                           {"width": 28, "border": 4, "sticky": tk.W})},
                    ttkstyle: {
                        "layout": [
                            ("Toolbutton.border", {
                                "sticky": tk.NSEW,
                                "children": [
                                    ("Toolbutton.padding", {
                                        "sticky": tk.NSEW,
                                        "children": [
                                            (f"{ttkstyle}.indicator",
                                             {"side": tk.LEFT}),
                                            ("Toolbutton.label",
                                             {"side": tk.LEFT})]})]})],
                        "configure": {
                            "relief": tk.FLAT,
                            "borderwidth": 0,
                            "foreground": self.colors.fg,
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("hover", indicatorcolor),
                            ],
                            "background": [
                                ("selected", self.colors.bg),
                                ("!selected", self.colors.bg)]}}})

    def create_square_toggle_style(self):
        """Apply a square toggle switch style to ttk widgets that 
        accept the toolbutton style
        """
        STYLE = 'Squaretoggle.Toolbutton'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        # color variations
        for color in [DEFAULT, *self.colors]:

            _on, _off, _disabled = self.create_square_toggle_assets(color)

            if color == DEFAULT:
                ttkstyle = STYLE
                indicatorcolor = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                indicatorcolor = self.colors.get(color)

            # create indicator element
            self.settings.update(
                {
                    f"{ttkstyle}.indicator": {
                        "element create": ("image", _on,
                                           ("disabled", _disabled),
                                           ("!selected", _off),
                                           {"width": 28, "border": 4, "sticky": tk.W})},
                    ttkstyle: {
                        "layout": [
                            ("Toolbutton.border", {
                                "sticky": tk.NSEW,
                                "children": [
                                    ("Toolbutton.padding", {
                                        "sticky": tk.NSEW,
                                        "children": [
                                            (f"{ttkstyle}.indicator",
                                             {"side": tk.LEFT}),
                                            ("Toolbutton.label",
                                             {"side": tk.LEFT})]})]})],
                        "configure": {
                            "relief": tk.FLAT,
                            "borderwidth": 0,
                            "foreground": self.colors.fg},
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("hover", indicatorcolor),
                            ],
                            "background": [
                                ("selected", self.colors.bg),
                                ("!selected", self.colors.bg)]}}})

    def create_solid_toolbutton_style(self):
        """Apply a solid color style to ttk widgets that use the 
        Toolbutton style.
        """
        STYLE = 'Toolbutton'

        if self.is_light_theme:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(self.colors.inputbg, sd=0.3)
        else:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(self.colors.inputbg, sd=-0.3)

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                ttkstyle = STYLE
                toggle_on = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                toggle_on = self.colors.get(color)

            if self.is_light_theme:
                toggle_off = self.colors.selectbg
            else:
                toggle_off = self.colors.inputbg

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": self.colors.selectfg,
                            "background": toggle_off,
                            "bordercolor": toggle_off,
                            "darkcolor": toggle_off,
                            "lightcolor": toggle_off,
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": "",
                            "padding": (10, 5),
                            "anchor": tk.CENTER
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "background": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", toggle_on),
                                ("selected !disabled", toggle_on),
                                ("hover !disabled", toggle_on),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", toggle_on),
                                ("selected !disabled", toggle_on),
                                ("hover !disabled", toggle_on),
                            ],
                            "darkcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", toggle_on),
                                ("selected !disabled", toggle_on),
                                ("hover !disabled", toggle_on),
                            ],
                            "lightcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", toggle_on),
                                ("selected !disabled", toggle_on),
                                ("hover !disabled", toggle_on),
                            ],
                        },
                    }
                }
            )

    def create_outline_toolbutton_style(self):
        """Apply an outline style to ttk widgets that use the 
        Toolbutton style. This button has a solid button look on focus 
        and hover.
        """
        STYLE = 'Outline.Toolbutton'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                ttkstyle = STYLE
                foreground = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                foreground = self.colors.get(color)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": foreground,
                            "background": self.colors.bg,
                            "bordercolor": foreground,
                            "darkcolor": self.colors.bg,
                            "lightcolor": self.colors.bg,
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": "",
                            "borderwidth": 1,
                            "padding": (10, 5),
                            "anchor": tk.CENTER
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.colors.selectfg),
                                ("selected !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                            "background": [
                                ("pressed !disabled", foreground),
                                ("selected !disabled", foreground),
                                ("hover !disabled", foreground),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", foreground),
                                ("selected !disabled", foreground),
                                ("hover !disabled", foreground),
                            ],
                            "darkcolor": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", foreground),
                                ("selected !disabled", foreground),
                                ("hover !disabled", foreground),
                            ],
                            "lightcolor": [
                                ("disabled", self.colors.bg),
                                ("pressed !disabled", foreground),
                                ("selected !disabled", foreground),
                                ("hover !disabled", foreground),
                            ],
                        },
                    }
                }
            )

    def create_entry_style(self):
        """Create style configuration for ttk entry"""
        STYLE = 'TEntry'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                ttkstyle = STYLE
                focuscolor = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                focuscolor = self.colors.get(color)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "bordercolor": bordercolor,
                            "darkcolor": self.colors.inputbg,
                            "lightcolor": self.colors.inputbg,
                            "fieldbackground": self.colors.inputbg,
                            "foreground": self.colors.inputfg,
                            "insertcolor": self.colors.inputfg,
                            "padding": 5,
                        },
                        "map": {
                            "foreground": [("disabled", disabled_fg)],
                            "bordercolor": [
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", self.colors.bg),
                            ],
                            "lightcolor": [
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", focuscolor),
                            ],
                            "darkcolor": [
                                ("focus !disabled", focuscolor),
                                ("hover !disabled", focuscolor),
                            ],
                        }
                    }
                }
            )

    def create_radiobutton_assets(self, colorname):
        """Create radiobutton assets

        Parameters
        ----------
        colorname : str
            The name of the color to use for the button on state

        Returns
        -------
        List[str]
            A list of photoimage names
        """
        if colorname == DEFAULT:
            prime_color = self.colors.primary
        else:
            prime_color = self.colors.get(colorname)

        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_border = self.colors.selectbg

        if self.is_light_theme:
            on_border = prime_color
            off_fill = self.colors.inputbg
            disabled = self.colors.border
        else:
            on_border = self.colors.selectbg
            disabled = self.colors.selectbg
            off_fill = self.colors.selectbg

        # radio off
        radio_off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_off)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=off_border,
            width=3,
            fill=off_fill
        )

        # radio on
        radio_on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_on)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=on_border,
            width=12,
            fill=on_fill
        )
        draw.ellipse([40, 40, 94, 94], fill=on_indicator)

        # radio disabled
        radio_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_disabled)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=disabled,
            width=3,
            fill=off_fill
        )

        image_names = []

        for image in [radio_on, radio_off, radio_disabled]:
            _img = ImageTk.PhotoImage(image.resize((14, 14), Image.LANCZOS))
            _name = _img._PhotoImage__photo.name
            image_names.append(_name)
            self.theme_images[_name] = _img

        return image_names

    def create_radiobutton_style(self):
        """Create style configuration for ttk radiobutton"""

        STYLE = 'TRadiobutton'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:
            _on, _off, _disabled = self.create_radiobutton_assets(color)

            if color == DEFAULT:
                ttkstyle = STYLE
                focuscolor = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                focuscolor = self.colors.get(color)

            self.settings.update(
                {
                    f"{ttkstyle}.indicator": {
                        "element create": (
                            "image", _on,
                            ("disabled", _disabled),
                            ("!selected", _off),
                            {"width": 20, "border": 4, "sticky": tk.W})},
                    ttkstyle: {
                        "layout": [
                            ("Radiobutton.padding", {"children": [
                                (f"{ttkstyle}.indicator",
                                 {"side": tk.LEFT, "sticky": ""}),
                                ("Radiobutton.focus", {"children": [
                                    ("Radiobutton.label",
                                     {"sticky": tk.NSEW})],
                                    "side": tk.LEFT, "sticky": ""})],
                                "sticky": tk.NSEW})],
                        "configure": {"font": self.theme.font},
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("active", focuscolor)]}}})

    def create_calendar_style(self):
        """Create style configuration for the date chooser"""

        STYLE = 'TCalendar'

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                prime_color = self.colors.primary
                ttkstyle = STYLE
                chevron_style = "chevron.TButton"
            else:
                prime_color = self.colors.get(color)
                ttkstyle = f'{color}.{STYLE}'
                chevron_style = f"chevron.{color}.TButton"

            if self.is_light_theme:
                disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
                pressed = Colors.update_hsv(prime_color, vd=-0.1)
            else:
                disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
                pressed = Colors.update_hsv(prime_color, vd=0.1)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": self.colors.fg,
                            "background": self.colors.bg,
                            "bordercolor": self.colors.bg,
                            "darkcolor": self.colors.bg,
                            "lightcolor": self.colors.bg,
                            "relief": "raised",
                            "focusthickness": 0,
                            "focuscolor": "",
                            "borderwidth": 1,
                            "padding": (10, 5),
                            "anchor": tk.CENTER
                        },
                        "layout": [
                            ("Toolbutton.border", {
                                "sticky": tk.NSEW, "children": [
                                    ("Toolbutton.padding",
                                     {"sticky": tk.NSEW, "children": [
                                         ("Toolbutton.label",
                                          {"sticky": tk.NSEW})]})]})
                        ],
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.colors.selectfg),
                                ("selected !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                            "background": [
                                ("pressed !disabled", pressed),
                                ("selected !disabled", pressed),
                                ("hover !disabled", pressed)
                            ],
                            "bordercolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", pressed),
                                ("selected !disabled", pressed),
                                ("hover !disabled", pressed)
                            ],
                            "darkcolor": [
                                ("pressed !disabled", pressed),
                                ("selected !disabled", pressed),
                                ("hover !disabled", pressed)
                            ],
                            "lightcolor": [
                                ("pressed !disabled", pressed),
                                ("selected !disabled", pressed),
                                ("hover !disabled", pressed)
                            ],
                        },
                    },
                    chevron_style: {
                        "configure": {"font": "helvetica 14"}
                    },
                }
            )

    def create_exit_button_style(self):
        """Create style configuration for the toolbutton exit button"""
        if self.is_light_theme:
            disabled_bg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_bg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)

        pressed_vd = -0.2
        self.settings.update(
            {
                "exit.TButton": {
                    "configure": {"relief": tk.FLAT, "font": "helvetica 12"},
                    "map": {
                        "background": [
                            ("disabled", disabled_bg),
                            (
                                "pressed !disabled",
                                Colors.update_hsv(
                                    self.colors.primary, vd=pressed_vd
                                ),
                            ),
                            ("hover !disabled", self.colors.danger),
                        ]
                    },
                }
            }
        )

        for color in self.colors:
            self.settings.update(
                {
                    f"exit.{color}.TButton": {
                        "configure": {
                            "relief": tk.FLAT,
                            "font": "helvetica 12",
                        },
                        "map": {
                            "background": [
                                ("disabled", disabled_bg),
                                (
                                    "pressed !disabled",
                                    Colors.update_hsv(
                                        self.colors.get(color), vd=pressed_vd
                                    ),
                                ),
                                ("hover !disabled", self.colors.danger),
                            ]
                        },
                    }
                }
            )

    def create_meter_style(self):
        """Create style configuration for the meter"""
        self.settings.update(
            {
                "TMeter": {
                    "layout": [
                        (
                            "Label.border",
                            {
                                "sticky": tk.NSEW,
                                "border": "1",
                                "children": [
                                    (
                                        "Label.padding",
                                        {
                                            "sticky": tk.NSEW,
                                            "border": "1",
                                            "children": [
                                                (
                                                    "Label.label",
                                                    {"sticky": tk.NSEW},
                                                )
                                            ],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "configure": {
                        "foreground": self.colors.fg,
                        "background": self.colors.bg,
                    },
                }
            }
        )

        for color in self.colors:
            self.settings.update(
                {
                    f"{color}.TMeter": {
                        "configure": {"foreground": self.colors.get(color)}
                    }
                }
            )

    def create_label_style(self):
        """Create style configuration for ttk label"""

        STYLE = 'TLabel'

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                ttkstyle = STYLE
                inverse_ttkstyle = f'Inverse.{STYLE}'
                stylecolor = self.colors.fg
                inv_foreground = self.colors.bg
            else:
                ttkstyle = f'{color}.{STYLE}'
                inverse_ttkstyle = f'{color}.Inverse.{STYLE}'
                stylecolor = self.colors.get(color)
                inv_foreground = self.colors.selectfg

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": stylecolor,
                            "background": self.colors.bg
                        }
                    },
                    inverse_ttkstyle: {
                        "configure": {
                            "foreground": inv_foreground,
                            "background": stylecolor
                        }
                    },
                }
            )

    def create_labelframe_style(self):
        """Create style configuration for ttk labelframe"""
        self.settings.update(
            {
                "Labelframe.Label": {"element create": ("from", TTK_CLAM)},
                "Label.fill": {"element create": ("from", TTK_CLAM)},
                "Label.text": {"element create": ("from", TTK_CLAM)},
                "TLabelframe.Label": {
                    "layout": [
                        (
                            "Label.fill",
                            {
                                "sticky": tk.NSEW,
                                "children": [
                                    ("Label.text", {"sticky": tk.NSEW})
                                ],
                            },
                        )
                    ],
                    "configure": {"foreground": self.colors.fg},
                },
                "TLabelframe": {
                    "layout": [("Labelframe.border", {"sticky": tk.NSEW})],
                    "configure": {
                        "relief": "raised",
                        "borderwidth": "1",
                        "bordercolor": (
                            self.colors.border
                            if self.theme.type == "light"
                            else self.colors.selectbg
                        ),
                        "lightcolor": self.colors.bg,
                        "darkcolor": self.colors.bg,
                    },
                },
            }
        )

        for color in self.colors:
            self.settings.update(
                {
                    f"{color}.TLabelframe": {
                        "configure": {
                            "background": self.colors.get(color),
                            "lightcolor": self.colors.get(color),
                            "darkcolor": self.colors.get(color),
                        }
                    },
                    f"{color}.TLabelframe.Label": {
                        "configure": {
                            "foreground": self.colors.selectfg,
                            "background": self.colors.get(color),
                            "lightcolor": self.colors.get(color),
                            "darkcolor": self.colors.get(color),
                        }
                    },
                }
            )

    def create_checkbutton_style(self):
        """Create style configuration for ttk checkbutton"""
        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        self.theme_images.update(self.create_checkbutton_assets("primary"))

        self.settings.update(
            {
                "Checkbutton.indicator": {
                    "element create": (
                        "image",
                        self.theme_images["primary_checkbutton_on"],
                        (
                            "disabled",
                            self.theme_images["primary_checkbutton_disabled"],
                        ),
                        (
                            "!selected",
                            self.theme_images["primary_checkbutton_off"],
                        ),
                        {"width": 20, "border": 4, "sticky": tk.W},
                    )
                },
                "TCheckbutton": {
                    "layout": [
                        (
                            "Checkbutton.padding",
                            {
                                "children": [
                                    (
                                        "primary.Checkbutton.indicator",
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
                    "configure": {
                        "foreground": self.colors.fg,
                        "background": self.colors.bg,
                        "focuscolor": "",
                    },
                    "map": {
                        "foreground": [
                            ("disabled", disabled_fg),
                            ("active !disabled", self.colors.primary),
                        ]
                    },
                },
            }
        )

        # variations change indicator color
        for color in self.colors:
            self.theme_images.update(self.create_checkbutton_assets(color))
            self.settings.update(
                {
                    f"{color}.Checkbutton.indicator": {
                        "element create": (
                            "image",
                            self.theme_images[f"{color}_checkbutton_on"],
                            (
                                "disabled",
                                self.theme_images[
                                    f"{color}_checkbutton_disabled"
                                ],
                            ),
                            (
                                "!selected",
                                self.theme_images[f"{color}_checkbutton_off"],
                            ),
                            {"width": 20, "border": 4, "sticky": tk.W},
                        )
                    },
                    f"{color}.TCheckbutton": {
                        "layout": [
                            (
                                "Checkbutton.padding",
                                {
                                    "children": [
                                        (
                                            f"{color}.Checkbutton.indicator",
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
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                (
                                    "active !disabled",
                                    Colors.update_hsv(
                                        self.colors.get(color), vd=-0.2
                                    ),
                                ),
                            ]
                        },
                    },
                }
            )

    def create_checkbutton_assets(self, colorname):
        """Create radiobutton assets

        Parameters
        ----------
        colorname : str
            The name of the color to use for the button on state

        Returns
        -------
        Tuple[PhotoImage]
            A tuple of widget images.
        """
        # set platform specific checkfont
        winsys = self.style.tk.call("tk", "windowingsystem")
        if winsys == "win32":
            fnt = ImageFont.truetype("seguisym.ttf", 120)
            font_offset = -20
        elif winsys == "x11":
            fnt = ImageFont.truetype("FreeSerif.ttf", 130)
            font_offset = 10
        else:
            fnt = ImageFont.truetype("LucidaGrande.ttc", 120)
            font_offset = -10

        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_fill = prime_color
        off_border = self.colors.selectbg

        if self.is_light_theme:
            off_fill = self.colors.inputbg
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            disabled_bg = self.colors.inputbg
        else:
            off_fill = self.colors.selectbg
            disabled_fg = self.colors.inputbg
            disabled_bg = disabled_fg

        # checkbutton off
        checkbutton_off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_off)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            outline=off_border,
            width=3,
            fill=off_fill,
        )

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
        draw.text((20, font_offset), "✓", font=fnt, fill=self.colors.selectfg)

        # checkbutton disabled
        checkbutton_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            outline=disabled_fg,
            width=3,
            fill=disabled_bg,
        )

        return {
            f"{colorname}_checkbutton_off": ImageTk.PhotoImage(
                checkbutton_off.resize((14, 14), Image.LANCZOS)
            ),
            f"{colorname}_checkbutton_on": ImageTk.PhotoImage(
                checkbutton_on.resize((14, 14), Image.LANCZOS)
            ),
            f"{colorname}_checkbutton_disabled": ImageTk.PhotoImage(
                checkbutton_disabled.resize((14, 14), Image.LANCZOS)
            ),
        }

    def create_solid_menubutton(self):
        """Apply a solid color style to ttk menubutton"""
        STYLE = 'TMenubutton'

        disabled_fg = self.colors.selectbg
        disabled_bg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                ttkstyle = STYLE
                background = self.colors.primary
            else:
                ttkstyle = f'{color}.{STYLE}'
                background = self.colors.get(color)

            if self.is_light_theme:
                pressed = Colors.update_hsv(background, vd=-0.2)
                hover = Colors.update_hsv(background, vd=-0.1)
                arrowcolor = self.colors.bg

            else:
                pressed = Colors.update_hsv(background, vd=0.2)
                hover = Colors.update_hsv(background, vd=0.1)
                arrowcolor = self.colors.selectfg

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": self.colors.selectfg,
                            "background": background,
                            "bordercolor": background,
                            "darkcolor": background,
                            "lightcolor": background,
                            "arrowsize": 4,
                            "arrowcolor": arrowcolor,
                            "arrowpadding": (0, 0, 15, 0),
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": self.colors.selectfg,
                            "padding": (10, 5),
                        },
                        "map": {
                            "arrowcolor": [("disabled", disabled_fg)],
                            "foreground": [("disabled", disabled_fg)],
                            "background": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "darkcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "lightcolor": [
                                ("disabled", disabled_bg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                        },
                    }
                }
            )

    def create_outline_menubutton_style(self):
        """Apply and outline style to ttk menubutton"""

        STYLE = 'Outline.TMenubutton'

        disabled_fg = self.colors.inputbg

        for color in [DEFAULT, *self.colors]:
            if color == DEFAULT:
                foreground = self.colors.primary
                ttkstyle = STYLE
            else:
                foreground = self.colors.get(color)
                ttkstyle = f'{color}.{STYLE}'

            if self.is_light_theme:
                pressed = Colors.update_hsv(foreground, vd=-0.1)
                hover = Colors.update_hsv(foreground, vd=-0.2)
            else:
                pressed = Colors.update_hsv(foreground, vd=0.1)
                hover = Colors.update_hsv(foreground, vd=0.2)

            self.settings.update(
                {
                    ttkstyle: {
                        "configure": {
                            "foreground": foreground,
                            "background": self.colors.bg,
                            "bordercolor": foreground,
                            "darkcolor": self.colors.bg,
                            "lightcolor": self.colors.bg,
                            "arrowcolor": foreground,
                            "arrowpadding": (0, 0, 15, 0),
                            "relief": tk.RAISED,
                            "focusthickness": 0,
                            "focuscolor": foreground,
                            "padding": (10, 5),
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                            "background": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "darkcolor": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "lightcolor": [
                                ("pressed !disabled", pressed),
                                ("hover !disabled", hover),
                            ],
                            "arrowcolor": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.colors.selectfg),
                                ("hover !disabled", self.colors.selectfg),
                            ],
                        },
                    }
                }
            )

    def create_notebook_style(self):
        """Create style configuration for ttk notebook"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        self.settings.update(
            {
                "TNotebook": {
                    "configure": {
                        "bordercolor": bordercolor,
                        "lightcolor": self.colors.bg,
                        "darkcolor": self.colors.bg,
                        "borderwidth": 1,
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "bordercolor": bordercolor,
                        "lightcolor": self.colors.bg,
                        "foreground": self.colors.fg,
                        "padding": (10, 5),
                    },
                    "map": {
                        "background": [("!selected", self.colors.inputbg)],
                        "lightcolor": [("!selected", self.colors.inputbg)],
                        "darkcolor": [("!selected", self.colors.inputbg)],
                        "bordercolor": [("!selected", bordercolor)],
                        "foreground": [("!selected", self.colors.fg)],
                    },
                },
            }
        )

    def create_panedwindow_style(self):
        """Create style configuration for ttk paned window"""

        PANE_STYLE = 'TPanedwindow'

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        self.settings.update(
            {
                'Sash': {
                    "configure": {
                        "sashthickness": 3,
                        "gripcount": 0,
                    },
                }
            }
        )

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                sashcolor = default_color
                sash_ttkstyle = PANE_STYLE
            else:
                sashcolor = self.colors.get(color)
                sash_ttkstyle = f'{color}.{PANE_STYLE}'

            self.settings.update(
                {
                    sash_ttkstyle: {
                        "configure": {
                            "background": sashcolor
                        }
                    },
                }
            )

    def create_sizegrip_assets(self, colorname):
        """Create assets for size grip

        Parameters
        ----------
        colorname : str
            The name of the color to use for the sizegrip images

        Returns
        -------
        str
            The PhotoImage name.
        """
        im = Image.new("RGBA", (14, 14))
        draw = ImageDraw.Draw(im)
        color = self.colors.get(colorname)
        draw.rectangle((9, 3, 10, 4), fill=color)  # top
        draw.rectangle((6, 6, 7, 7), fill=color)  # middle
        draw.rectangle((9, 6, 10, 7), fill=color)
        draw.rectangle((3, 9, 4, 10), fill=color)  # bottom
        draw.rectangle((6, 9, 7, 10), fill=color)
        draw.rectangle((9, 9, 10, 10), fill=color)

        _img = ImageTk.PhotoImage(im)
        _name = _img._PhotoImage__photo.name
        self.theme_images[_name] = _img
        return _name

    def create_sizegrip_style(self):
        """Create style configuration for ttk sizegrip"""
        STYLE = 'TSizegrip'

        if self.is_light_theme:
            default_color = "border"
        else:
            default_color = "inputbg"

        for color in [DEFAULT, *self.colors]:

            if color == DEFAULT:
                grip_image = self.create_sizegrip_assets(default_color)
                ttkstyle = STYLE
            else:
                grip_image = self.create_sizegrip_assets(color)
                ttkstyle = f'{color}.{STYLE}'

            self.settings.update(
                {
                    f"{ttkstyle}.Sizegrip.sizegrip": {
                        "element create": ("image", grip_image)},
                    ttkstyle: {
                        "layout": [
                            (
                                f"{ttkstyle}.Sizegrip.sizegrip", {
                                    "side": tk.BOTTOM, "sticky": tk.SE},
                            )
                        ]
                    },
                }
            )
