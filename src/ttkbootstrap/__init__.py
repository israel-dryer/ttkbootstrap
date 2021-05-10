"""
    Why does this project exist?
    ============================
    The purpose of this project is create a set of beautifully designed and easy to apply styles for your tkinter
    applications. Ttk can be very time-consuming to style if you are just a casual user. This project takes the pain
    out of getting a modern look and feel so that you can focus on designing your application. This project was created
    to harness the power of ttk's (and thus Python's) existing built-in theme engine to create modern and
    professional-looking user interfaces which are inspired by, and in many cases, whole-sale rip-off's of the themes
    found on Bootswatch_. Even better, you have the abilty to :ref:`create and use your own custom
    themes <tutorial:create a new theme>` using TTK Creator.

    A bootstrap approach to style
    =============================
    Many people are familiar with bootstrap for web developement. It comes pre-packaged with built-in css style classes
    that provide a professional and consistent api for quick development. I took a similar approach with this project
    by pre-defining styles for nearly all ttk widgets. This makes is very easy to apply the theme colors to various
    widgets by using style declarations. If you want a button in the `secondary` theme color, simply apply the
    **secondary.TButton** style to the button. Want a blue outlined button? Apply the **info.Outline.TButton** style to
    the button.

    What about the old tkinter widgets?
    ===================================
    Some of the ttk widgets utilize existing tkinter widgets. For example: there is a tkinter popdown list in the
    ``ttk.Combobox`` and a legacy tkinter widget inside the ``ttk.OptionMenu``. To make sure these widgets didn't stick
    out like a sore thumb, I created a ``StyleTK`` class to apply the same color and style to these legacy widgets.
    While these legacy widgets are not necessarily intended to be used (and will probably not look as nice as the ttk
    versions when they exist), they are available if needed, and shouldn't look completely out-of-place in your
    ttkbootstrap themed application.  :ref:`Check out this example <themes:legacy widget styles>` to see for yourself.

    .. _Bootswatch: https://bootswatch.com/

"""
import colorsys
import importlib.resources
import json
from pathlib import Path
from tkinter import ttk

from PIL import ImageTk, Image, ImageDraw, ImageFont


class Style(ttk.Style):
    """A class for setting the application style.

    Sets the theme of the ``tkinter.Tk`` instance and supports all ttkbootstrap and ttk themes provided. This class is
    meant to be a drop-in replacement for ``ttk.Style`` and inherits all of it's methods and properties. Creating a
    ``Style`` object will instantiate the ``tkinter.Tk`` instance in the ``Style.master`` property, and so it is not
    necessary to explicitly create an instance of ``tkinter.Tk``. For more details on the ``ttk.Style`` class, see the
    python documentation_.

    .. code-block:: python

        # instantiate the style with default theme *flatly*
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='superhero')

        # instantiate the style with a theme from a specific themes file
        style = Style(theme='custom_name', themes_file='C:/example/my_themes.json')

        # available themes
        for theme in style.theme_names():
            print(theme)

    .. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style
    """

    def __init__(self, theme='flatly', themes_file=None, *args, **kwargs):
        """
        Args:
            theme (str): the name of the theme to use at runtime; *flatly* by default.
            themes_file (str): Path to a user-defined themes file. Defaults to the themes file set in ttkcreator.
        """
        super().__init__(*args, **kwargs)
        self._styler = None
        self._theme_names = set(self.theme_names())
        self._theme_objects = {}  # used to prevent garbage collection of theme assets when changing themes at runtime
        self._theme_definitions = {}
        self._load_themes(themes_file)

        # load selected or default theme
        self.theme_use(themename=theme)

    @property
    def colors(self):
        theme = self.theme_use()
        if theme in list(self._theme_names):
            return self._theme_definitions.get(theme).colors
        else:
            return Colors()

    def _load_themes(self, themes_file=None):
        """Load all ttkbootstrap defined themes

        Args:
            themes_file (str): the path of the `themes.json` file.
        """
        # pre-defined themes
        json_data = importlib.resources.read_text('ttkbootstrap', 'themes.json')
        builtin_themes = json.loads(json_data)

        # application-defined or user-defined themes
        if themes_file is None:
            themes_file = builtin_themes['userpath']
        user_path = Path(themes_file)
        if user_path.exists():
            with user_path.open(encoding='utf-8') as f:
                user_themes = json.load(f)
        else:
            user_themes = {'themes': []}

        # create a theme definition object for each theme, this will be used to generate
        #  the theme in tkinter along with any assets at run-time
        theme_settings = {'themes': builtin_themes['themes'] + user_themes['themes']}
        for theme in theme_settings['themes']:
            self.register_theme(
                ThemeDefinition(
                    name=theme['name'],
                    themetype=theme['type'],
                    font=theme['font'],
                    colors=Colors(**theme['colors'])))

    def register_theme(self, definition):
        """Registers a theme definition for use by the ``Style`` class.

        This makes the definition and name available at run-time so that the assets and styles can be created.

        Args:
            definition (ThemeDefinition): an instance of the ``ThemeDefinition`` class
        """
        self._theme_names.add(definition.name)
        self._theme_definitions[definition.name] = definition

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set the current theme to themename, refreshes all
        widgets and emits a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during* runtime. Otherwise, pass the theme name into the
        Style constructor to instantiate the style with a theme.

        Keyword Args:
            themename (str): the theme to apply when creating new widgets
        """
        self.theme = self._theme_definitions.get(themename)

        if not themename:
            return super().theme_use()

        if all([themename, themename not in self._theme_names]):
            print(f"{themename} is not a valid theme name. Please try one of the following:")
            print(list(self._theme_names))
            return

        if themename in self.theme_names():
            # the theme has already been created in tkinter
            super().theme_use(themename)
            if not self.theme:
                # this is not a bootstrap theme
                # self._theme_definitions[themename] = ThemeDefinition()
                return
            return

        # theme has not yet been created
        self._theme_objects[themename] = StylerTTK(self, self.theme)
        self._theme_objects[themename].styler_tk.style_tkinter_widgets()
        super().theme_use(themename)
        return


class ThemeDefinition:
    """A class to provide defined name, colors, and font settings for a ttkbootstrap theme."""

    def __init__(self, name='default', themetype='light', font='helvetica', colors=None):
        """
        Args:
            name (str): the name of the theme; default is 'default'.
            themetype (str): the type of theme: *light* or *dark*; default is 'light'.
            font (str): the default font to use for the application; default is 'helvetica'.
            colors (Colors): an instance of the `Colors` class. One is provided by default.
        """
        self.name = name
        self.type = themetype
        self.font = font
        self.colors = colors if colors else Colors()

    def __repr__(self):
        return f'name={self.name}, type={self.type}, font={self.font}, colors={self.colors}'


class Colors:
    """A class that contains the theme colors as well as several helper methods for manipulating colors.

    This class is attached to the ``Style`` object at run-time for the selected theme, and so is available to use with
    ``Style.colors``. The colors can be accessed via dot notation or get method:

    .. code-block:: python

        # dot-notation
        Colors.primary

        # get method
        Colors.get('primary')

    This class is an iterator, so you can iterate over the main style color labels (primary, secondary, success, info,
    warning, danger):

    .. code-block:: python

        for color_label in Colors:
            color = Colors.get(color_label)
            print(color_label, color)

    If, for some reason, you need to iterate over all theme color labels, then you can use the ``Colors.label_iter``
    method. This will include all theme colors, including border, fg, bg, etc...

    .. code-block:: python

        for color_label in Colors.label_iter():
            color = Colors.get(color_label)
            print(color_label, color)
    """

    def __init__(self, primary, secondary, success, info, warning, danger, bg, fg, selectbg, selectfg,
                 border, inputfg, inputbg):
        """
            Args:
                primary (str): the primary theme color; used by default for all widgets.
                secondary (str): an accent color; commonly of a `grey` hue.
                success (str): an accent color; commonly of a `green` hue.
                info (str): an accent color; commonly of a `blue` hue.
                warning (str): an accent color; commonly of an `orange` hue.
                danger (str): an accent color; commonly of a `red` hue.
                bg (str): background color.
                fg (str): default text color.
                selectfg (str): the color of selected text.
                selectbg (str): the background color of selected text.
                border (str): the color used for widget borders.
                inputfg (str): the text color for input widgets: ie. ``Entry``, ``Combobox``, etc...
                inputbg (str): the text background color for input widgets.
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

        Args:
            color_label (str): a color label corresponding to a class propery (primary, secondary, success, etc...)

        Returns:
            str: a hexadecimal color value.
        """
        return self.__dict__.get(color_label)

    def set(self, color_label, color_value):
        """Set a color property

        Args:
            color_label (str): the name of the color to be set (key)
            color_value (str): a hexadecimal color value

        Example:

            .. code-block:
                set('primary', '#fafafa')
        """
        self.__dict__[color_label] = color_value

    def __iter__(self):
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger'])

    def __repr__(self):
        return str((tuple(zip(self.__dict__.keys(), self.__dict__.values()))))

    @staticmethod
    def label_iter():
        """Iterate over all color label properties in the Color class

            Returns:
                iter: an iterator representing the name of the color properties
        """
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'bg', 'fg', 'selectbg', 'selectfg',
                     'border', 'inputfg', 'inputbg'])

    @staticmethod
    def hex_to_rgb(color):
        """Convert hexadecimal color to rgb color value

        Args:
            color (str): param str color: hexadecimal color value

        Returns:
            tuple[int, int, int]: rgb color value.
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

        Args:
            r (int): red
            g (int): green
            b (int): blue

        Returns:
            str: a hexadecimal colorl value
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex color value.

        Args:
            color (str): the hexadecimal color value that is the target of hsv changes.
            hd (float): % change in hue
            sd (float): % change in saturation
            vd (float): % change in value

        Returns:
            str: a new hexadecimal color value that results from the hsv arguments passed into the function
        """
        r, g, b = Colors.hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # hue
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= (1 + hd)

        # saturation
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= (1 + sd)

        # value
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= (1 + vd)

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Colors.rgb_to_hex(r, g, b)


class StylerTK:
    """A class for styling tkinter widgets (not ttk).

    Several ttk widgets utilize tkinter widgets in some capacity, such as the `popdownlist` on the ``ttk.Combobox``. To
    create a consistent user experience, standard tkinter widgets are themed as much as possible with the look and feel
    of the **ttkbootstrap** theme applied. Tkinter widgets are not the primary target of this project; however, they can
    be used without looking entirely out-of-place in most cases.

    Attributes:
        master (Tk): the root window.
        theme (ThemeDefinition): the color settings defined in the `themes.json` file.
    """

    def __init__(self, styler_ttk):
        """
        Args:
            styler_ttk (StylerTTK): an instance of the ``StylerTTK`` class.
        """
        self.master = styler_ttk.style.master
        self.theme = styler_ttk.theme

    def style_tkinter_widgets(self):
        """A wrapper on all widget style methods. Applies current theme to all standard tkinter widgets"""
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
        """A convenience wrapper method to shorten the call to ``option_add``. *Laziness is next to godliness*.

        Args:
            *args (Tuple[str]): (pattern, value, priority=80)
        """
        self.master.option_add(*args)

    def _style_window(self):
        """Apply global options to all matching ``tkinter`` widgets"""
        self.master.configure(background=self.theme.colors.bg)
        self._set_option('*background', self.theme.colors.bg, 60)
        self._set_option('*font', self.theme.font, 60)
        self._set_option('*activeBackground', self.theme.colors.selectbg, 60)
        self._set_option('*activeForeground', self.theme.colors.selectfg, 60)
        self._set_option('*selectBackground', self.theme.colors.selectbg, 60)
        self._set_option('*selectForeground', self.theme.colors.selectfg, 60)

    def _style_canvas(self):
        """Apply style to ``tkinter.Canvas``"""
        self._set_option('*Canvas.highlightThickness', 1)
        self._set_option('*Canvas.highlightBackground', self.theme.colors.border)
        self._set_option('*Canvas.background', self.theme.colors.bg)

    def _style_button(self):
        """Apply style to ``tkinter.Button``"""
        active_bg = Colors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option('*Button.relief', 'flat')
        self._set_option('*Button.borderWidth', 0)
        self._set_option('*Button.activeBackground', active_bg)
        self._set_option('*Button.foreground', self.theme.colors.selectfg)
        self._set_option('*Button.background', self.theme.colors.primary)

    def _style_label(self):
        """Apply style to ``tkinter.Label``"""
        self._set_option('*Label.foreground', self.theme.colors.fg)
        self._set_option('*Label.background', self.theme.colors.bg)

    def _style_checkbutton(self):
        """Apply style to ``tkinter.Checkbutton``"""
        self._set_option('*Checkbutton.activeBackground', self.theme.colors.bg)
        self._set_option('*Checkbutton.activeForeground', self.theme.colors.primary)
        self._set_option('*Checkbutton.background', self.theme.colors.bg)
        self._set_option('*Checkbutton.foreground', self.theme.colors.fg)
        self._set_option('*Checkbutton.selectColor',
                         self.theme.colors.primary if self.theme.type == 'dark' else 'white')

    def _style_radiobutton(self):
        """Apply style to ``tkinter.Radiobutton``"""
        self._set_option('*Radiobutton.activeBackground', self.theme.colors.bg)
        self._set_option('*Radiobutton.activeForeground', self.theme.colors.primary)
        self._set_option('*Radiobutton.background', self.theme.colors.bg)
        self._set_option('*Radiobutton.foreground', self.theme.colors.fg)
        self._set_option('*Radiobutton.selectColor',
                         self.theme.colors.primary if self.theme.type == 'dark' else 'white')

    def _style_entry(self):
        """Apply style to ``tkinter.Entry``"""
        self._set_option('*Entry.relief', 'flat')
        self._set_option('*Entry.background',
                         (self.theme.colors.inputbg if self.theme.type == 'light' else
                          Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1)))
        self._set_option('*Entry.foreground', self.theme.colors.inputfg)
        self._set_option('*Entry.highlightThickness', 1)
        self._set_option('*Entry.highlightBackground', self.theme.colors.border)
        self._set_option('*Entry.highlightColor', self.theme.colors.primary)

    def _style_scale(self):
        """Apply style to ``tkinter.Scale``"""
        active_color = Colors.update_hsv(self.theme.colors.primary, vd=-0.2)

        self._set_option('*Scale.background', self.theme.colors.primary)
        self._set_option('*Scale.showValue', False)
        self._set_option('*Scale.sliderRelief', 'flat')
        self._set_option('*Scale.borderWidth', 0)
        self._set_option('*Scale.activeBackground', active_color)
        self._set_option('*Scale.highlightThickness', 1)
        self._set_option('*Scale.highlightColor', self.theme.colors.border)
        self._set_option('*Scale.highlightBackground', self.theme.colors.border)
        self._set_option('*Scale.troughColor', self.theme.colors.inputbg)

    def _style_spinbox(self):
        """Apply style to `tkinter.Spinbox``"""
        self._set_option('*Spinbox.foreground', self.theme.colors.inputfg)
        self._set_option('*Spinbox.relief', 'flat')
        self._set_option('*Spinbox.background',
                         (self.theme.colors.inputbg if self.theme.type == 'light' else
                          Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1)))
        self._set_option('*Spinbox.highlightThickness', 1)
        self._set_option('*Spinbox.highlightColor', self.theme.colors.primary)
        self._set_option('*Spinbox.highlightBackground', self.theme.colors.border)

    def _style_listbox(self):
        """Apply style to ``tkinter.Listbox``"""
        self._set_option('*Listbox.foreground', self.theme.colors.inputfg)
        self._set_option('*Listbox.background', self.theme.colors.inputbg)
        self._set_option('*Listbox.selectBackground', self.theme.colors.selectbg)
        self._set_option('*Listbox.selectForeground', self.theme.colors.selectfg)
        self._set_option('*Listbox.relief', 'flat')
        self._set_option('*Listbox.activeStyle', 'none')
        self._set_option('*Listbox.highlightThickness', 1)
        self._set_option('*Listbox.highlightColor', self.theme.colors.primary)
        self._set_option('*Listbox.highlightBackground', self.theme.colors.border)

    def _style_menubutton(self):
        """Apply style to ``tkinter.Menubutton``"""
        hover_color = Colors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option('*Menubutton.activeBackground', hover_color)
        self._set_option('*Menubutton.background', self.theme.colors.primary)
        self._set_option('*Menubutton.foreground', self.theme.colors.selectfg)
        self._set_option('*Menubutton.borderWidth', 0)

    def _style_menu(self):
        """Apply style to ``tkinter.Menu``"""
        self._set_option('*Menu.tearOff', 0)
        self._set_option('*Menu.foreground', self.theme.colors.fg)
        self._set_option('*Menu.selectColor', self.theme.colors.primary)
        self._set_option('*Menu.font', self.theme.font)
        self._set_option('*Menu.background', (
            self.theme.colors.inputbg if self.theme.type == 'light' else
            self.theme.colors.bg))
        self._set_option('*Menu.activeBackground', self.theme.colors.selectbg)
        self._set_option('*Menu.activeForeground', self.theme.colors.selectfg)

    def _style_labelframe(self):
        """Apply style to ``tkinter.Labelframe``"""
        self._set_option('*Labelframe.font', self.theme.font)
        self._set_option('*Labelframe.foreground', self.theme.colors.fg)
        self._set_option('*Labelframe.highlightColor', self.theme.colors.border)
        self._set_option('*Labelframe.borderWidth', 1)
        self._set_option('*Labelframe.highlightThickness', 0)

    def _style_textwidget(self):
        """Apply style to ``tkinter.Text``"""
        self._set_option('*Text.background', self.theme.colors.inputbg)
        self._set_option('*Text.foreground', self.theme.colors.inputfg)
        self._set_option('*Text.highlightColor', self.theme.colors.primary)
        self._set_option('*Text.highlightBackground', self.theme.colors.border)
        self._set_option('*Text.borderColor', self.theme.colors.border)
        self._set_option('*Text.highlightThickness', 1)
        self._set_option('*Text.relief', 'flat')
        self._set_option('*Text.font', self.theme.font)
        self._set_option('*Text.padX', 5)
        self._set_option('*Text.padY', 5)


class StylerTTK:
    """A class to create a new ttk theme.

    Create a new ttk theme by using a combination of built-in themes and some image-based elements using ``pillow``. A
    theme is generated at runtime and is available to use with the ``Style`` class methods. The base theme of all
    **ttkbootstrap** themes is *clam*. In many cases, widget layouts are re-created using an assortment of elements from
    various styles such as *clam*, *alt*, *default*, etc...

    Attributes:
        theme_images (dict): theme assets used for various widgets.
        settings (dict): settings used to build the actual theme using the ``theme_create`` method.
        styler_tk (StylerTk): an object used to style tkinter widgets (not ttk).
        theme (ThemeDefinition): the theme settings defined in the `themes.json` file.
    """

    def __init__(self, style, definition):
        """
        Args:
            style (Style): an instance of ``ttk.Style``.
            definition (ThemeDefinition): an instance of ``ThemeDefinition``; used to create the theme settings.
        """
        self.style = style
        self.theme = definition
        self.theme_images = {}
        self.settings = {}
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal style methods."""
        self.update_ttk_theme_settings()
        self.style.theme_create(self.theme.name, 'clam', self.settings)

    def update_ttk_theme_settings(self):
        """Update the settings dictionary that is used to create a theme. This is a wrapper on all the `_style_widget`
        methods which define the layout, configuration, and styling mapping for each ttk widget.
        """
        self._style_labelframe()
        self._style_spinbox()
        self._style_scale()
        self._style_scrollbar()
        self._style_combobox()
        self._style_exit_button()
        self._style_frame()
        self._style_calendar()
        self._style_checkbutton()
        self._style_entry()
        self._style_label()
        self._style_meter()
        self._style_notebook()
        self._style_outline_buttons()
        self._style_outline_menubutton()
        self._style_outline_toolbutton()
        self._style_progressbar()
        self._style_striped_progressbar()
        self._style_floodgauge()
        self._style_radiobutton()
        self._style_solid_buttons()
        self._style_link_buttons()
        self._style_solid_menubutton()
        self._style_solid_toolbutton()
        self._style_treeview()
        self._style_separator()
        self._style_panedwindow()
        self._style_roundtoggle_toolbutton()
        self._style_squaretoggle_toolbutton()
        self._style_sizegrip()
        self._style_defaults()

    def _style_defaults(self):
        """Setup the default ``ttk.Style`` configuration. These defaults are applied to any widget that contains these
        element options. This method should be called *first* before any other style is applied during theme creation.
        """
        self.settings.update({
            '.': {
                'configure': {
                    'background': self.theme.colors.bg,
                    'darkcolor': self.theme.colors.border,
                    'foreground': self.theme.colors.fg,
                    'troughcolor': self.theme.colors.bg,
                    'selectbg': self.theme.colors.selectbg,
                    'selectfg': self.theme.colors.selectfg,
                    'selectforeground': self.theme.colors.selectfg,
                    'selectbackground': self.theme.colors.selectbg,
                    'fieldbg': 'white',
                    'font': self.theme.font,
                    'borderwidth': 1,
                    'focuscolor': ''}}})

    def _style_combobox(self):
        """Create style configuration for ``ttk.Combobox``. This element style is created with a layout that combines
        *clam* and *default* theme elements.

        The options available in this widget based on this layout include:

            - Combobox.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Combobox.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Combobox.padding: padding, relief, shiftrelief
            - Combobox.textarea: font, width

        .. info::

            When the dark theme is used, I used the *spinbox.field* from the *default* theme because the background
            shines through the corners using the `clam` theme. This is an unfortuate hack to make it look ok. Hopefully
            there will be a more permanent/better solution in the future.
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        if self.theme.type == 'dark':
            self.settings.update({
                'combo.Spinbox.field': {'element create': ('from', 'default')}})

        self.settings.update({
            'Combobox.downarrow': {'element create': ('from', 'default')},
            'Combobox.padding': {'element create': ('from', 'clam')},
            'Combobox.textarea': {'element create': ('from', 'clam')},
            'TCombobox': {
                'layout': [('combo.Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
                    ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}),
                    ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                        ('Combobox.textarea', {'sticky': 'nswe'})]})]})],
                'configure': {
                    'bordercolor': self.theme.colors.border,
                    'darkcolor': self.theme.colors.inputbg,
                    'lightcolor': self.theme.colors.inputbg,
                    'arrowcolor': self.theme.colors.inputfg,
                    'foreground': self.theme.colors.inputfg,
                    'fieldbackground ': self.theme.colors.inputbg,
                    'background ': self.theme.colors.inputbg,
                    'relief': 'flat',
                    'borderwidth ': 0,  # only applies to dark theme border
                    'padding': 5,
                    'arrowsize ': 14},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'bordercolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.bg)],
                    'lightcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'arrowcolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.inputbg),
                        ('focus !disabled', self.theme.colors.inputfg),
                        ('hover !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TCombobox': {
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'bordercolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('pressed !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('pressed !disabled', self.theme.colors.get(color))],
                        'arrowcolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.inputbg),
                            ('focus !disabled', self.theme.colors.inputfg),
                            ('hover !disabled', self.theme.colors.primary)]}}})

    def _style_separator(self):
        """Create style configuration for ttk separator: *ttk.Separator*. The default style for light will be border,
        but dark will be primary, as this makes the most sense for general use. However, all other colors will be
        available as well through styling.

        The options available in this widget include:

            - Separator.separator: orient, background
        """
        # horizontal separator default
        default_color = self.theme.colors.border if self.theme.type == 'light' else self.theme.colors.selectbg
        h_im = Image.new('RGB', (40, 1))
        draw = ImageDraw.Draw(h_im)
        draw.rectangle([0, 0, 40, 1], fill=default_color)
        self.theme_images['hseparator'] = ImageTk.PhotoImage(h_im)

        self.settings.update({
            'Horizontal.Separator.separator': {
                'element create': ('image', self.theme_images['hseparator'])},
            'Horizontal.TSeparator': {
                'layout': [
                    ('Horizontal.Separator.separator', {'sticky': 'ew'})]}})

        # horizontal separator variations
        for color in self.theme.colors:
            h_im = Image.new('RGB', (40, 1))
            draw = ImageDraw.Draw(h_im)
            draw.rectangle([0, 0, 40, 1], fill=self.theme.colors.get(color))
            self.theme_images[f'{color}_hseparator'] = ImageTk.PhotoImage(h_im)

            self.settings.update({
                f'{color}.Horizontal.Separator.separator': {
                    'element create': ('image', self.theme_images[f'{color}_hseparator'])},
                f'{color}.Horizontal.TSeparator': {
                    'layout': [
                        (f'{color}.Horizontal.Separator.separator', {'sticky': 'ew'})]}})

        # vertical separator default
        default_color = self.theme.colors.border if self.theme.type == 'light' else self.theme.colors.selectbg
        v_im = Image.new('RGB', (1, 40))
        draw = ImageDraw.Draw(v_im)
        draw.rectangle([0, 0, 1, 40], fill=default_color)
        self.theme_images['vseparator'] = ImageTk.PhotoImage(v_im)

        self.settings.update({
            'Vertical.Separator.separator': {
                'element create': ('image', self.theme_images['vseparator'])},
            'Vertical.TSeparator': {
                'layout': [
                    ('Vertical.Separator.separator', {'sticky': 'ns'})]}})

        # vertical separator variations
        for color in self.theme.colors:
            v_im = Image.new('RGB', (1, 40))
            draw = ImageDraw.Draw(v_im)
            draw.rectangle([0, 0, 1, 40], fill=self.theme.colors.get(color))
            self.theme_images[f'{color}_vseparator'] = ImageTk.PhotoImage(v_im)

            self.settings.update({
                f'{color}.Vertical.Separator.separator': {
                    'element create': ('image', self.theme_images[f'{color}_vseparator'])},
                f'{color}.Vertical.TSeparator': {
                    'layout': [
                        (f'{color}.Vertical.Separator.separator', {'sticky': 'ns'})]}})

    def _style_striped_progressbar(self):
        """Apply a striped theme to the progressbar"""
        self.theme_images.update(self._create_striped_progressbar_image('primary'))
        self.settings.update({
            'Striped.Horizontal.Progressbar.pbar': {
                'element create': ('image', self.theme_images['primary_striped_hpbar'], {'width': 20, 'sticky': 'ew'})},
            'Striped.Horizontal.TProgressbar': {
                'layout': [
                    ('Horizontal.Progressbar.trough', {'sticky': 'nswe', 'children': [
                        ('Striped.Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})]})],
                'configure': {
                    'troughcolor': self.theme.colors.inputbg,
                    'thickness': 20,
                    'borderwidth': 1,
                    'lightcolor':
                        self.theme.colors.border if self.theme.type == 'light' else
                        self.theme.colors.inputbg}}})

        for color in self.theme.colors:
            self.theme_images.update(self._create_striped_progressbar_image(color))
            self.settings.update({
                f'{color}.Striped.Horizontal.Progressbar.pbar': {
                    'element create': (
                        'image', self.theme_images[f'{color}_striped_hpbar'], {'width': 20, 'sticky': 'ew'})},
                f'{color}.Striped.Horizontal.TProgressbar': {
                    'layout': [
                        ('Horizontal.Progressbar.trough', {'sticky': 'nswe', 'children': [
                            (f'{color}.Striped.Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})]})],
                    'configure': {
                        'troughcolor': self.theme.colors.inputbg,
                        'thickness': 20,
                        'borderwidth': 1,
                        'lightcolor':
                            self.theme.colors.border if self.theme.type == 'light' else
                            self.theme.colors.inputbg}}})

    def _create_striped_progressbar_image(self, colorname):
        """Create the striped progressbar image and return as a ``PhotoImage``

        Args:
            colorname (str): the color label assigned to the colors property; eg. `primary`, `secondary`, `success`.

        Returns:
            dict: a dictionary containing the widget images.
        """
        bar_primary = self.theme.colors.get(colorname)

        # calculate value of light color
        brightness = colorsys.rgb_to_hsv(*Colors.hex_to_rgb(bar_primary))[2]
        if brightness < 0.4:
            value_delta = 0.3
        elif brightness > 0.8:
            value_delta = 0
        else:
            value_delta = 0.1
        bar_secondary = Colors.update_hsv(bar_primary, sd=-0.2, vd=value_delta)

        # need to check the darkness of the color before setting the secondary

        # horizontal progressbar
        h_im = Image.new('RGBA', (100, 100), bar_secondary)
        draw = ImageDraw.Draw(h_im)
        draw.polygon([(0, 0), (48, 0), (100, 52), (100, 100), (100, 100)], fill=bar_primary)
        draw.polygon([(0, 52), (48, 100), (0, 100)], fill=bar_primary)
        horizontal_img = ImageTk.PhotoImage(h_im.resize((22, 22), Image.LANCZOS))

        # TODO vertical progressbar

        return {f'{colorname}_striped_hpbar': horizontal_img}

    def _style_progressbar(self):
        """Create style configuration for ttk progressbar: *ttk.Progressbar*

        The options available in this widget include:

            - Progressbar.trough: borderwidth, troughcolor, troughrelief
            - Progressbar.pbar: orient, thickness, barsize, pbarrelief, borderwidth, background
        """
        self.settings.update({
            'Progressbar.trough': {'element create': ('from', 'clam')},
            'Progressbar.pbar': {'element create': ('from', 'default')},
            'TProgressbar': {'configure': {
                'thickness': 20,
                'borderwidth': 1,
                'bordercolor': self.theme.colors.border if self.theme.type == 'light' else self.theme.colors.inputbg,
                'lightcolor': self.theme.colors.border,
                'pbarrelief': 'flat',
                'troughcolor': self.theme.colors.inputbg,
                'background': self.theme.colors.primary}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Horizontal.TProgressbar': {
                    'configure': {
                        'background': self.theme.colors.get(color)}},
                f'{color}.Vertical.TProgressbar': {
                    'configure': {
                        'background': self.theme.colors.get(color)}}})

    @staticmethod
    def _create_slider_image(color, size=16):
        """Create a circle slider image based on given size and color; used in the slider widget.

        Args:
            color (str): a hexadecimal color value.
            size (int): the size diameter of the slider circle; default=16.

        Returns:
            ImageTk.PhotoImage: an image drawn in the shape of the circle of the theme color specified.
        """
        im = Image.new('RGBA', (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=color)
        return ImageTk.PhotoImage(im.resize((size, size), Image.LANCZOS))

    def _style_scale(self):
        """Create style configuration for ttk scale: *ttk.Scale*

        The options available in this widget include:

            - Scale.trough: borderwidth, troughcolor, troughrelief
            - Scale.slider: sliderlength, sliderthickness, sliderrelief, borderwidth, background, bordercolor, orient
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        trough_color = (self.theme.colors.inputbg if self.theme.type == 'dark' else
                        Colors.update_hsv(self.theme.colors.inputbg, vd=-0.03))

        pressed_vd = -0.2
        hover_vd = -0.1

        # create widget images
        self.theme_images.update({
            'primary_disabled': self._create_slider_image(disabled_fg),
            'primary_regular': self._create_slider_image(self.theme.colors.primary),
            'primary_pressed': self._create_slider_image(
                Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
            'primary_hover': self._create_slider_image(
                Colors.update_hsv(self.theme.colors.primary, vd=hover_vd)),
            'htrough': ImageTk.PhotoImage(Image.new('RGB', (40, 8), trough_color)),
            'vtrough': ImageTk.PhotoImage(Image.new('RGB', (8, 40), trough_color))})

        # The layout is derived from the 'xpnative' theme
        self.settings.update({
            'Horizontal.TScale': {
                'layout': [
                    ('Scale.focus', {'expand': '1', 'sticky': 'nswe', 'children': [
                        ('Horizontal.Scale.track', {'sticky': 'we'}),
                        ('Horizontal.Scale.slider', {'side': 'left', 'sticky': ''})]})]},
            'Vertical.TScale': {
                'layout': [
                    ('Scale.focus', {'expand': '1', 'sticky': 'nswe', 'children': [
                        ('Vertical.Scale.track', {'sticky': 'ns'}),
                        ('Vertical.Scale.slider', {'side': 'top', 'sticky': ''})]})]},
            'Horizontal.Scale.track': {'element create': ('image', self.theme_images['htrough'])},
            'Vertical.Scale.track': {'element create': ('image', self.theme_images['vtrough'])},
            'Scale.slider': {
                'element create':
                    ('image', self.theme_images['primary_regular'],
                     ('disabled', self.theme_images['primary_disabled']),
                     ('pressed !disabled', self.theme_images['primary_pressed']),
                     ('hover !disabled', self.theme_images['primary_hover']))}})

        for color in self.theme.colors:
            self.theme_images.update({
                f'{color}_regular': self._create_slider_image(self.theme.colors.get(color)),
                f'{color}_pressed': self._create_slider_image(
                    Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                f'{color}_hover': self._create_slider_image(
                    Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))})

            # The layout is derived from the 'xpnative' theme
            self.settings.update({
                f'{color}.Horizontal.TScale': {
                    'layout': [
                        ('Scale.focus', {
                            'expand': '1', 'sticky': 'nswe', 'children': [
                                ('Horizontal.Scale.track', {'sticky': 'we'}),
                                (f'{color}.Scale.slider', {'side': 'left', 'sticky': ''})]})]},
                f'{color}.Vertical.TScale': {
                    'layout': [
                        (f'{color}.Scale.focus', {
                            'expand': '1', 'sticky': 'nswe', 'children': [
                                ('Vertical.Scale.track', {'sticky': 'ns'}),
                                (f'{color}.Scale.slider', {'side': 'top', 'sticky': ''})]})]},
                f'{color}.Scale.slider': {
                    'element create':
                        ('image', self.theme_images[f'{color}_regular'],
                         ('disabled', self.theme_images['primary_disabled']),
                         ('pressed', self.theme_images[f'{color}_pressed']),
                         ('hover', self.theme_images[f'{color}_hover']))}})

    def _create_scrollbar_images(self):
        """Create assets needed for scrollbar arrows. The assets are saved to the ``theme_images`` property."""
        font_size = 13
        with importlib.resources.open_binary('ttkbootstrap', 'Symbola.ttf') as font_path:
            fnt = ImageFont.truetype(font_path, font_size)

        # up arrow
        vs_upim = Image.new('RGBA', (font_size, font_size))
        up_draw = ImageDraw.Draw(vs_upim)
        up_draw.text((1, 5), "🞁", font=fnt,
                     fill=self.theme.colors.inputfg if self.theme.type == 'light' else
                     Colors.update_hsv(self.theme.colors.selectbg, vd=0.35, sd=-0.1))
        self.theme_images['vsup'] = ImageTk.PhotoImage(vs_upim)

        # down arrow
        hsdown_im = Image.new('RGBA', (font_size, font_size))
        down_draw = ImageDraw.Draw(hsdown_im)
        down_draw.text((1, -4), "🞃", font=fnt,
                       fill=self.theme.colors.inputfg if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.selectbg, vd=0.35, sd=-0.1))
        self.theme_images['vsdown'] = ImageTk.PhotoImage(hsdown_im)

        # left arrow
        vs_upim = Image.new('RGBA', (font_size, font_size))
        up_draw = ImageDraw.Draw(vs_upim)
        up_draw.text((1, 1), "🞀", font=fnt,
                     fill=self.theme.colors.inputfg if self.theme.type == 'light' else
                     Colors.update_hsv(self.theme.colors.selectbg, vd=0.35, sd=-0.1))
        self.theme_images['hsleft'] = ImageTk.PhotoImage(vs_upim)

        # right arrow
        vs_upim = Image.new('RGBA', (font_size, font_size))
        up_draw = ImageDraw.Draw(vs_upim)
        up_draw.text((1, 1), "🞂", font=fnt,
                     fill=self.theme.colors.inputfg if self.theme.type == 'light' else
                     Colors.update_hsv(self.theme.colors.selectbg, vd=0.35, sd=-0.1))
        self.theme_images['hsright'] = ImageTk.PhotoImage(vs_upim)

    def _style_floodgauge(self):
        """Create a style configuration for the *ttk.Progressbar* that makes it into a floodgauge. Which is essentially
        a very large progress bar with text in the middle.

        The options available in this widget include:

            - Floodgauge.trough: borderwidth, troughcolor, troughrelief
            - Floodgauge.pbar: orient, thickness, barsize, pbarrelief, borderwidth, background
            - Floodgauge.text: 'text', 'font', 'foreground', 'underline', 'width', 'anchor', 'justify', 'wraplength',
                'embossed'
        """
        self.settings.update({
            'Floodgauge.trough': {'element create': ('from', 'clam')},
            'Floodgauge.pbar': {'element create': ('from', 'default')},
            'Horizontal.TFloodgauge': {
                'layout': [('Floodgauge.trough', {'children': [
                    ('Floodgauge.pbar', {'sticky': 'ns'}),
                    ("Floodgauge.label", {"sticky": ""})],
                    'sticky': 'nswe'})],
                'configure': {
                    'thickness': 50,
                    'borderwidth': 1,
                    'bordercolor': self.theme.colors.primary,
                    'lightcolor': self.theme.colors.primary,
                    'pbarrelief': 'flat',
                    'troughcolor': Colors.update_hsv(self.theme.colors.primary, sd=-0.3, vd=0.8),
                    'background': self.theme.colors.primary,
                    'foreground': self.theme.colors.selectfg,
                    'justify': 'center',
                    'anchor': 'center',
                    'font': 'helvetica 14'}},
            'Vertical.TFloodgauge': {
                'layout': [('Floodgauge.trough', {'children': [
                    ('Floodgauge.pbar', {'sticky': 'we'}),
                    ("Floodgauge.label", {"sticky": ""})],
                    'sticky': 'nswe'})],
                'configure': {
                    'thickness': 50,
                    'borderwidth': 1,
                    'bordercolor': self.theme.colors.primary,
                    'lightcolor': self.theme.colors.primary,
                    'pbarrelief': 'flat',
                    'troughcolor': Colors.update_hsv(self.theme.colors.primary, sd=-0.3, vd=0.8),
                    'background': self.theme.colors.primary,
                    'foreground': self.theme.colors.selectfg,
                    'justify': 'center',
                    'anchor': 'center',
                    'font': 'helvetica 14'}
            }})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Horizontal.TFloodgauge': {
                    'configure': {
                        'thickness': 50,
                        'borderwidth': 1,
                        'bordercolor': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'pbarrelief': 'flat',
                        'troughcolor': Colors.update_hsv(self.theme.colors.get(color), sd=-0.3, vd=0.8),
                        'background': self.theme.colors.get(color),
                        'foreground': self.theme.colors.selectfg,
                        'justify': 'center',
                        'anchor': 'center',
                        'font': 'helvetica 14'}},
                f'{color}.Vertical.TFloodgauge': {
                    'configure': {
                        'thickness': 50,
                        'borderwidth': 1,
                        'bordercolor': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'pbarrelief': 'flat',
                        'troughcolor': Colors.update_hsv(self.theme.colors.get(color), sd=-0.3, vd=0.8),
                        'background': self.theme.colors.get(color),
                        'foreground': self.theme.colors.selectfg,
                        'justify': 'center',
                        'anchor': 'center',
                        'font': 'helvetica 14'}
                }})

    def _style_scrollbar(self):
        """Create style configuration for ttk scrollbar: *ttk.Scrollbar*. This theme uses elements from the *alt* theme
        tobuild the widget layout.

        The options available in this widget include:

            - Scrollbar.trough: orient, troughborderwidth, troughcolor, troughrelief, groovewidth
            - Scrollbar.uparrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.thumb: width, background, bordercolor, relief, orient
        """
        self._create_scrollbar_images()

        self.settings.update({
            'Vertical.Scrollbar.trough': {
                'element create': ('from', 'alt')},
            'Vertical.Scrollbar.thumb': {
                'element create': ('from', 'alt')},
            'Vertical.Scrollbar.uparrow': {
                'element create': ('image', self.theme_images['vsup'])},
            'Vertical.Scrollbar.downarrow': {
                'element create': ('image', self.theme_images['vsdown'])},
            'Horizontal.Scrollbar.trough': {
                'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.thumb': {
                'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.leftarrow': {
                'element create': ('image', self.theme_images['hsleft'])},
            'Horizontal.Scrollbar.rightarrow': {
                'element create': ('image', self.theme_images['hsright'])},
            'TScrollbar': {
                'configure': {
                    'troughrelief': 'flat',
                    'relief': 'flat',
                    'troughborderwidth': 2,
                    'troughcolor': Colors.update_hsv(self.theme.colors.bg, vd=-0.05),
                    'background':
                        Colors.update_hsv(self.theme.colors.bg, vd=-0.15) if self.theme.type == 'light' else
                        Colors.update_hsv(self.theme.colors.selectbg, vd=0.25, sd=-0.1),
                    'width': 16},
                'map': {
                    'background': [
                        ('pressed',
                         Colors.update_hsv(self.theme.colors.bg, vd=-0.35) if self.theme.type == 'light' else
                         Colors.update_hsv(self.theme.colors.selectbg, vd=0.05)),
                        ('active',
                         Colors.update_hsv(self.theme.colors.bg, vd=-0.25) if self.theme.type == 'light' else
                         Colors.update_hsv(self.theme.colors.selectbg, vd=0.15))]}}})

    def _style_spinbox(self):
        """Create style configuration for ttk spinbox: *ttk.Spinbox*

        This widget uses elements from the *default* and *clam* theme to create the widget layout.
        For dark themes,the spinbox.field is created from the *default* theme element because the background
        color shines through the corners of the widget when the primary theme background color is dark.

        The options available in this widget include:

            - Spinbox.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - spinbox.uparrow: background, relief, borderwidth, arrowcolor, arrowsize
            - spinbox.downarrow: background, relief, borderwidth, arrowcolor, arrowsize
            - spinbox.padding: padding, relief, shiftrelief
            - spinbox.textarea: font, width
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        if self.theme.type == 'dark':
            self.settings.update({'custom.Spinbox.field': {'element create': ('from', 'default')}})

        self.settings.update({
            'Spinbox.uparrow': {'element create': ('from', 'default')},
            'Spinbox.downarrow': {'element create': ('from', 'default')},
            'TSpinbox': {
                'layout': [
                    ('custom.Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
                        ('null', {'side': 'right', 'sticky': '', 'children': [
                            ('Spinbox.uparrow', {'side': 'top', 'sticky': 'e'}),
                            ('Spinbox.downarrow', {'side': 'bottom', 'sticky': 'e'})]}),
                        ('Spinbox.padding', {'sticky': 'nswe', 'children': [
                            ('Spinbox.textarea', {'sticky': 'nswe'})]})]})],
                'configure': {
                    'bordercolor': self.theme.colors.border,
                    'darkcolor': self.theme.colors.inputbg,
                    'lightcolor': self.theme.colors.inputbg,
                    'fieldbackground': self.theme.colors.inputbg,
                    'foreground': self.theme.colors.inputfg,
                    'borderwidth': 0,
                    'background': self.theme.colors.inputbg,
                    'relief': 'flat',
                    'arrowcolor': self.theme.colors.inputfg,
                    'arrowsize': 14,
                    'padding': (10, 5)
                },
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'bordercolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.bg)],
                    'lightcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'arrowcolor': [
                        ('disabled !disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.primary),
                        ('focus !disabled', self.theme.colors.inputfg),
                        ('hover !disabled', self.theme.colors.inputfg)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TSpinbox': {
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'bordercolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'arrowcolor': [
                            ('disabled !disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.inputfg)],
                        'lightcolor': [
                            ('focus !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('focus !disabled', self.theme.colors.get(color))]}}})

    def _style_treeview(self):
        """Create style configuration for ttk treeview: *ttk.Treeview*. This widget uses elements from the *alt* and
        *clam* theme to create the widget layout.

        The options available in this widget include:

            Treeview:

                - Treeview.field: bordercolor, lightcolor, darkcolor, fieldbackground
                - Treeview.padding: padding, relief, shiftrelief
                - Treeview.treearea

            Item:

                - Treeitem.padding: padding, relief, shiftrelief
                - Treeitem.indicator: foreground, diameter, indicatormargins
                - Treeitem.image: image, stipple, background
                - Treeitem.focus: focuscolor, focusthickness
                - Treeitem.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed

            Heading:

                - Treeheading.cell: background, rownumber
                - Treeheading.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
                - Treeheading.padding: padding, relief, shiftrelief
                - Treeheading.image: image, stipple, background
                - Treeheading.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed

            Cell:
                - Treedata.padding: padding, relief, shiftrelief
                - Treeitem.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed

        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        self.settings.update({
            'Treeview': {
                'layout': [
                    ('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [
                        ('Treeview.padding', {'sticky': 'nswe', 'children': [
                            ('Treeview.treearea', {'sticky': 'nswe'})]})]})],
                'configure': {
                    'background': self.theme.colors.inputbg,
                    'foreground': self.theme.colors.inputfg,
                    'bordercolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.border,
                    'darkcolor': self.theme.colors.border,
                    'relief': 'raised' if self.theme.type == 'light' else 'flat',
                    'padding': 0 if self.theme.type == 'light' else -2
                },
                'map': {
                    'background': [
                        ('selected', self.theme.colors.selectbg)],
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('selected', self.theme.colors.selectfg)]}},
            'Treeview.Heading': {
                'configure': {
                    'background': self.theme.colors.primary,
                    'foreground': self.theme.colors.selectfg,
                    'relief': 'flat',
                    'padding': 5}},
            'Treeitem.indicator': {'element create': ('from', 'alt')}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Treeview.Heading': {
                    'configure': {
                        'background': self.theme.colors.get(color)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'bordercolor': [
                            ('focus !disabled', self.theme.colors.get(color))]}}})

    def _style_frame(self):
        """Create style configuration for ttk frame: *ttk.Frame*

        The options available in this widget include:

            - Frame.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
        """
        self.settings.update({
            'TFrame': {'configure': {'background': self.theme.colors.bg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TFrame': {'configure': {'background': self.theme.colors.get(color)}}})

    def _style_solid_buttons(self):
        """Apply a solid color style to ttk button: *ttk.Button*

        The options available in this widget include:

            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = self.theme.colors.inputfg
        disabled_bg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.2
        hover_vd = -0.1

        self.settings.update({
            'TButton': {
                'configure': {
                    'foreground': self.theme.colors.selectfg,
                    'background': self.theme.colors.primary,
                    'bordercolor': self.theme.colors.primary,
                    'darkcolor': self.theme.colors.primary,
                    'lightcolor': self.theme.colors.primary,
                    'font': self.theme.font,
                    'anchor': 'center',
                    'relief': 'raised',
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                # TODO should I remove default padding? I can also use: width: -12 to set a minimum width
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'background': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'bordercolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'darkcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'lightcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TButton': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color),
                        'bordercolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'background': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'bordercolor': [
                            ('disabled', disabled_bg),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'darkcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'lightcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))]}}})

    def _style_outline_buttons(self):
        """Apply an outline style to ttk button: *ttk.Button*. This button has a solid button look on focus and hover.

        The options available in this widget include:

            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.10

        self.settings.update({
            'Outline.TButton': {
                'configure': {
                    'foreground': self.theme.colors.primary,
                    'background': self.theme.colors.bg,
                    'bordercolor': self.theme.colors.primary,
                    'darkcolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'relief': 'raised',
                    'font': self.theme.font,
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.selectfg),
                        ('hover !disabled', self.theme.colors.selectfg)],
                    'background': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'bordercolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'lightcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Outline.TButton': {
                    'configure': {
                        'foreground': self.theme.colors.get(color),
                        'background': self.theme.colors.bg,
                        'bordercolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.bg,
                        'lightcolor': self.theme.colors.bg,
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.selectfg),
                            ('hover !disabled', self.theme.colors.selectfg)],
                        'background': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'bordercolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))]}}})

    def _style_link_buttons(self):
        """Apply a solid color style to ttk button: *ttk.Button*

        The options available in this widget include:

            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = 0
        hover_vd = 0

        self.settings.update({
            'Link.TButton': {
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'background': self.theme.colors.bg,
                    'bordercolor': self.theme.colors.bg,
                    'darkcolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'relief': 'raised',
                    'font': self.theme.font,
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.info, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.info, vd=hover_vd))],
                    'shiftrelief': [
                        ('pressed !disabled', -1)],
                    'background': [
                        ('pressed !disabled', self.theme.colors.bg),
                        ('hover !disabled', self.theme.colors.bg)],
                    'bordercolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.bg),
                        ('hover !disabled', self.theme.colors.bg)],
                    'darkcolor': [
                        ('pressed !disabled', self.theme.colors.bg),
                        ('hover !disabled', self.theme.colors.bg)],
                    'lightcolor': [
                        ('pressed !disabled', self.theme.colors.bg),
                        ('hover !disabled', self.theme.colors.bg)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Link.TButton': {
                    'configure': {
                        'foreground': self.theme.colors.get(color),
                        'background': self.theme.colors.bg,
                        'bordercolor': self.theme.colors.bg,
                        'darkcolor': self.theme.colors.bg,
                        'lightcolor': self.theme.colors.bg,
                        'relief': 'raised',
                        'font': self.theme.font,
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.info, vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.info, vd=hover_vd))],
                        'shiftrelief': [
                            ('pressed !disabled', -1)],
                        'background': [
                            ('pressed !disabled', self.theme.colors.bg),
                            ('hover !disabled', self.theme.colors.bg)],
                        'bordercolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.bg),
                            ('hover !disabled', self.theme.colors.bg)],
                        'darkcolor': [
                            ('pressed !disabled', self.theme.colors.bg),
                            ('hover !disabled', self.theme.colors.bg)],
                        'lightcolor': [
                            ('pressed !disabled', self.theme.colors.bg),
                            ('hover !disabled', self.theme.colors.bg)]}}})

    def _create_squaretoggle_image(self, colorname):
        """Create a set of images for the square toggle button and return as ``PhotoImage``

        Args:
            colorname (str): the color label assigned to the colors property

        Returns:
            Tuple[PhotoImage]: a tuple of images (toggle_on, toggle_off, toggle_disabled)
        """
        prime_color = self.theme.colors.get(colorname)
        on_border = prime_color
        on_indicator = prime_color
        on_fill = self.theme.colors.bg
        off_border = self.theme.colors.selectbg if self.theme.type == 'light' else self.theme.colors.inputbg
        off_indicator = self.theme.colors.selectbg if self.theme.type == 'light' else self.theme.colors.inputbg
        off_fill = self.theme.colors.bg
        disabled_fill = self.theme.colors.bg
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        toggle_off = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rectangle([1, 1, 225, 129], outline=off_border, width=6, fill=off_fill)
        draw.rectangle([18, 18, 110, 110], fill=off_indicator)

        toggle_on = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rectangle([1, 1, 225, 129], outline=on_border, width=6, fill=on_fill)
        draw.rectangle([18, 18, 110, 110], fill=on_indicator)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        toggle_disabled = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)

        images = {}
        images[f'{colorname}_squaretoggle_on'] = ImageTk.PhotoImage(toggle_on.resize((24, 15), Image.LANCZOS))
        images[f'{colorname}_squaretoggle_off'] = ImageTk.PhotoImage(toggle_off.resize((24, 15), Image.LANCZOS))
        images[f'{colorname}_squaretoggle_disabled'] = ImageTk.PhotoImage(
            toggle_disabled.resize((24, 15), Image.LANCZOS))
        return images

    def _create_roundtoggle_image(self, colorname):
        """Create a set of images for the rounded toggle button and return as ``PhotoImage``

        Args:
            colorname (str): the color label assigned to the colors property

        Returns:
            Tuple[PhotoImage]
        """
        prime_color = self.theme.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.theme.colors.selectfg
        on_fill = prime_color
        off_border = self.theme.colors.selectbg if self.theme.type == 'light' else self.theme.colors.inputbg
        off_indicator = self.theme.colors.selectbg if self.theme.type == 'light' else self.theme.colors.inputbg
        off_fill = self.theme.colors.bg
        disabled_fill = self.theme.colors.bg
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        toggle_off = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rounded_rectangle([1, 1, 225, 129], radius=(128 / 2), outline=off_border, width=6, fill=off_fill)
        draw.ellipse([20, 18, 112, 110], fill=off_indicator)

        toggle_on = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rounded_rectangle([1, 1, 225, 129], radius=(128 / 2), outline=on_border, width=6, fill=on_fill)
        draw.ellipse([20, 18, 112, 110], fill=on_indicator)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        toggle_disabled = Image.new('RGBA', (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rounded_rectangle([1, 1, 225, 129], radius=(128 / 2), outline=disabled_fg, width=6)
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)

        images = {}
        images[f'{colorname}_roundtoggle_on'] = ImageTk.PhotoImage(toggle_on.resize((24, 15), Image.LANCZOS))
        images[f'{colorname}_roundtoggle_off'] = ImageTk.PhotoImage(toggle_off.resize((24, 15), Image.LANCZOS))
        images[f'{colorname}_roundtoggle_disabled'] = ImageTk.PhotoImage(
            toggle_disabled.resize((24, 15), Image.LANCZOS))
        return images

    def _style_roundtoggle_toolbutton(self):
        """Apply a rounded toggle switch style to ttk widgets that accept the toolbutton style (for example, a
        checkbutton: *ttk.Checkbutton*)
        """
        self.theme_images.update(self._create_roundtoggle_image('primary'))
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # create indicator element
        self.settings.update({
            'Roundtoggle.Toolbutton.indicator': {
                'element create': ('image', self.theme_images['primary_roundtoggle_on'],
                                   ('disabled', self.theme_images['primary_roundtoggle_disabled']),
                                   ('!selected', self.theme_images['primary_roundtoggle_off']),
                                   {'width': 28, 'border': 4, 'sticky': 'w'})},
            'Roundtoggle.Toolbutton': {
                'layout': [('Toolbutton.border', {'sticky': 'nswe', 'children': [
                    ('Toolbutton.padding', {'sticky': 'nswe', 'children': [
                        ('Roundtoggle.Toolbutton.indicator', {'side': 'left'}),
                        ('Toolbutton.label', {'side': 'left'})]})]})],
                'configure': {
                    'relief': 'flat',
                    'borderwidth': 0,
                    'foreground': self.theme.colors.fg},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('hover', self.theme.colors.primary)],
                    'background': [
                        ('selected', self.theme.colors.bg),
                        ('!selected', self.theme.colors.bg)]}}})

        # color variations
        for color in self.theme.colors:
            self.theme_images.update(self._create_roundtoggle_image(color))

            # create indicator element
            self.settings.update({
                f'{color}.Roundtoggle.Toolbutton.indicator': {
                    'element create': ('image', self.theme_images[f'{color}_roundtoggle_on'],
                                       ('disabled', self.theme_images[f'{color}_roundtoggle_disabled']),
                                       ('!selected', self.theme_images[f'{color}_roundtoggle_off']),
                                       {'width': 28, 'border': 4, 'sticky': 'w'})},
                f'{color}.Roundtoggle.Toolbutton': {
                    'layout': [('Toolbutton.border', {'sticky': 'nswe', 'children': [
                        ('Toolbutton.padding', {'sticky': 'nswe', 'children': [
                            (f'{color}.Roundtoggle.Toolbutton.indicator', {'side': 'left'}),
                            ('Toolbutton.label', {'side': 'left'})]})]})],
                    'configure': {
                        'relief': 'flat',
                        'borderwidth': 0,
                        'foreground': self.theme.colors.fg},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('hover', self.theme.colors.get(color))],
                        'background': [
                            ('selected', self.theme.colors.bg),
                            ('!selected', self.theme.colors.bg)]}}})

    def _style_squaretoggle_toolbutton(self):
        """Apply a square toggle switch style to ttk widgets that accept the toolbutton style (for example, a
        checkbutton: *ttk.Checkbutton*)
        """
        self.theme_images.update(self._create_squaretoggle_image('primary'))
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # create indicator element
        self.settings.update({
            'Squaretoggle.Toolbutton.indicator': {
                'element create': ('image', self.theme_images['primary_squaretoggle_on'],
                                   ('disabled', self.theme_images['primary_squaretoggle_disabled']),
                                   ('!selected', self.theme_images['primary_squaretoggle_off']),
                                   {'width': 28, 'border': 4, 'sticky': 'w'})},
            'Squaretoggle.Toolbutton': {
                'layout': [('Toolbutton.border', {'sticky': 'nswe', 'children': [
                    ('Toolbutton.padding', {'sticky': 'nswe', 'children': [
                        ('Squaretoggle.Toolbutton.indicator', {'side': 'left'}),
                        ('Toolbutton.label', {'side': 'left'})]})]})],
                'configure': {
                    'relief': 'flat',
                    'borderwidth': 0,
                    'foreground': self.theme.colors.fg},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('hover', self.theme.colors.primary)],
                    'background': [
                        ('selected', self.theme.colors.bg),
                        ('!selected', self.theme.colors.bg)]}}})

        # color variations
        for color in self.theme.colors:
            self.theme_images.update(self._create_squaretoggle_image(color))

            # create indicator element
            self.settings.update({
                f'{color}.Squaretoggle.Toolbutton.indicator': {
                    'element create': ('image', self.theme_images[f'{color}_squaretoggle_on'],
                                       ('disabled', self.theme_images[f'{color}_squaretoggle_disabled']),
                                       ('!selected', self.theme_images[f'{color}_squaretoggle_off']),
                                       {'width': 28, 'border': 4, 'sticky': 'w'})},
                f'{color}.Squaretoggle.Toolbutton': {
                    'layout': [('Toolbutton.border', {'sticky': 'nswe', 'children': [
                        ('Toolbutton.padding', {'sticky': 'nswe', 'children': [
                            (f'{color}.Squaretoggle.Toolbutton.indicator', {'side': 'left'}),
                            ('Toolbutton.label', {'side': 'left'})]})]})],
                    'configure': {
                        'relief': 'flat',
                        'borderwidth': 0,
                        'foreground': self.theme.colors.fg},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('hover', self.theme.colors.get(color))],
                        'background': [
                            ('selected', self.theme.colors.bg),
                            ('!selected', self.theme.colors.bg)]}}})

    def _style_solid_toolbutton(self):
        """Apply a solid color style to ttk widgets that use the Toolbutton style (for example, a checkbutton:
        *ttk.Checkbutton*)

        The options available in this widget include:

            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = self.theme.colors.inputfg
        disabled_bg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.2
        hover_vd = -0.1
        normal_sd = -0.5
        normal_vd = 0.1

        self.settings.update({
            'Toolbutton': {
                'configure': {
                    'foreground': self.theme.colors.selectfg,
                    'background': Colors.update_hsv(self.theme.colors.primary, sd=normal_sd, vd=normal_vd),
                    'bordercolor': Colors.update_hsv(self.theme.colors.primary, sd=normal_sd, vd=normal_vd),
                    'darkcolor': Colors.update_hsv(self.theme.colors.primary, sd=normal_sd, vd=normal_vd),
                    'lightcolor': Colors.update_hsv(self.theme.colors.primary, sd=normal_sd, vd=normal_vd),
                    'font': self.theme.font,
                    'anchor': 'center',
                    'relief': 'raised',
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'background': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', self.theme.colors.primary),
                        ('selected !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'bordercolor': [
                        ('disabled', disabled_bg),
                        ('selected !disabled', self.theme.colors.primary),
                        ('pressed !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', self.theme.colors.primary),
                        ('selected !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'lightcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', self.theme.colors.primary),
                        ('selected !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Toolbutton': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': Colors.update_hsv(self.theme.colors.get(color), sd=normal_sd, vd=normal_vd),
                        'bordercolor': Colors.update_hsv(self.theme.colors.get(color), sd=normal_sd, vd=normal_vd),
                        'darkcolor': Colors.update_hsv(self.theme.colors.get(color), sd=normal_sd, vd=normal_vd),
                        'lightcolor': Colors.update_hsv(self.theme.colors.get(color), sd=normal_sd, vd=normal_vd),
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'background': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', self.theme.colors.get(color)),
                            ('selected !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'bordercolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', self.theme.colors.get(color)),
                            ('selected !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', self.theme.colors.get(color)),
                            ('selected !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', self.theme.colors.get(color)),
                            ('selected !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))]}}})

    def _style_outline_toolbutton(self):
        """Apply an outline style to ttk widgets that use the Toolbutton style (for example, a checkbutton:
        *ttk.Checkbutton*). This button has a solid button look on focus and hover.

        The options available in this widget include:

            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.10

        self.settings.update({
            'Outline.Toolbutton': {
                'configure': {
                    'foreground': self.theme.colors.primary,
                    'background': self.theme.colors.bg,
                    'bordercolor': self.theme.colors.border,
                    'darkcolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'relief': 'raised',
                    'font': self.theme.font,
                    'focusthickness': 0,
                    'focuscolor': '',
                    'borderwidth': 1,
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.selectfg),
                        ('selected !disabled', self.theme.colors.selectfg),
                        ('hover !disabled', self.theme.colors.selectfg)],
                    'background': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'bordercolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'lightcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Outline.Toolbutton': {
                    'configure': {
                        'foreground': self.theme.colors.get(color),
                        'background': self.theme.colors.bg,
                        'bordercolor': self.theme.colors.border,
                        'darkcolor': self.theme.colors.bg,
                        'lightcolor': self.theme.colors.bg,
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'borderwidth': 1,
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.selectfg),
                            ('selected !disabled', self.theme.colors.selectfg),
                            ('hover !disabled', self.theme.colors.selectfg)],
                        'background': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'bordercolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))]}}})

    def _style_entry(self):
        """Create style configuration for ttk entry: *ttk.Entry*

        The options available in this widget include:

            - Entry.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Entry.padding: padding, relief, shiftrelief
            - Entry.textarea: font, width
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        if self.theme.type == 'dark':
            self.settings.update({'Entry.field': {'element create': ('from', 'default')}})

        self.settings.update({
            'TEntry': {
                'configure': {
                    'bordercolor': self.theme.colors.border,
                    'darkcolor': self.theme.colors.inputbg,
                    'lightcolor': self.theme.colors.inputbg,
                    'fieldbackground': self.theme.colors.inputbg,
                    'foreground': self.theme.colors.inputfg,
                    'borderwidth': 0,  # only applies to border on darktheme
                    'padding': 5},
                'map': {
                    'foreground': [('disabled', disabled_fg)],
                    'bordercolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.bg)],
                    'lightcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('focus !disabled', self.theme.colors.primary),
                        ('hover !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TEntry': {
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'bordercolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.bg)],
                        'lightcolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('focus !disabled', self.theme.colors.get(color)),
                            ('hover !disabled', self.theme.colors.get(color))]}}})

    def _style_radiobutton(self):
        """Create style configuration for ttk radiobutton: *ttk.Radiobutton*

        The options available in this widget include:

            - Radiobutton.padding: padding, relief, shiftrelief
            - Radiobutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground,
                upperbordercolor, lowerbordercolor
            - Radiobutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))
        disabled_bg = self.theme.colors.inputbg if self.theme.type == 'light' else disabled_fg

        self.theme_images.update(self._create_radiobutton_images('primary'))
        self.settings.update({
            'Radiobutton.indicator': {
                'element create': ('image', self.theme_images['primary_radio_on'],
                                   ('disabled', self.theme_images['primary_radio_disabled']),
                                   ('!selected', self.theme_images['primary_radio_off']),
                                   {'width': 20, 'border': 4, 'sticky': 'w'})},
            'TRadiobutton': {
                'layout': [
                    ('Radiobutton.padding', {'children': [
                        ('Radiobutton.indicator', {'side': 'left', 'sticky': ''}),
                        ('Radiobutton.focus', {'children': [
                            ('Radiobutton.label', {'sticky': 'nswe'})], 'side': 'left', 'sticky': ''})],
                        'sticky': 'nswe'})],
                'configure': {
                    'font': self.theme.font},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('active', self.theme.colors.primary)],
                    'indicatorforeground': [
                        ('disabled', disabled_fg),
                        ('active selected !disabled', self.theme.colors.primary)]}}})

        # variations change the indicator color
        for color in self.theme.colors:
            self.theme_images.update(self._create_radiobutton_images(color))
            self.settings.update({
                f'{color}.Radiobutton.indicator': {
                    'element create': ('image', self.theme_images[f'{color}_radio_on'],
                                       ('disabled', self.theme_images[f'{color}_radio_disabled']),
                                       ('!selected', self.theme_images[f'{color}_radio_off']),
                                       {'width': 20, 'border': 4, 'sticky': 'w'})},
                f'{color}.TRadiobutton': {
                    'layout': [
                        ('Radiobutton.padding', {'children': [
                            (f'{color}.Radiobutton.indicator', {'side': 'left', 'sticky': ''}),
                            ('Radiobutton.focus', {'children': [
                                ('Radiobutton.label', {'sticky': 'nswe'})], 'side': 'left', 'sticky': ''})],
                            'sticky': 'nswe'})],
                    'configure': {
                        'font': self.theme.font},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('active', Colors.update_hsv(self.theme.colors.get(color), vd=-0.2))],
                        'indicatorforeground': [
                            ('disabled', disabled_fg),
                            ('active selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=-0.2))]}}})

    def _create_radiobutton_images(self, colorname):
        """Create radiobutton assets

        Args:
            colorname (str): the name of the color to use for the button on state

        Returns:
            Tuple[PhotoImage]: a tuple of widget images.
        """
        prime_color = self.theme.colors.get(colorname)
        on_border = prime_color if self.theme.type == 'light' else self.theme.colors.selectbg
        on_indicator = self.theme.colors.selectfg if self.theme.type == 'light' else prime_color
        on_fill = prime_color if self.theme.type == 'light' else self.theme.colors.selectfg
        off_border = self.theme.colors.selectbg
        off_fill = self.theme.colors.inputbg if self.theme.type == 'light' else self.theme.colors.selectfg
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))
        disabled_bg = self.theme.colors.inputbg if self.theme.type == 'light' else disabled_fg

        # radio off
        radio_off = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(radio_off)
        draw.ellipse([2, 2, 132, 132], outline=off_border, width=3, fill=off_fill)

        # radio on
        radio_on = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(radio_on)
        draw.ellipse([2, 2, 132, 132], outline=on_border, width=12 if self.theme.type == 'light' else 6, fill=on_fill)
        if self.theme.type == 'light':
            draw.ellipse([40, 40, 94, 94], fill=on_indicator)  # small indicator for light theme
        else:
            draw.ellipse([30, 30, 104, 104], fill=on_indicator)  # large indicator for dark theme

        # radio disabled
        radio_disabled = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(radio_disabled)
        draw.ellipse([2, 2, 132, 132], outline=disabled_fg, width=3, fill=off_fill)

        return {
            f'{colorname}_radio_off': ImageTk.PhotoImage(radio_off.resize((14, 14), Image.LANCZOS)),
            f'{colorname}_radio_on': ImageTk.PhotoImage(radio_on.resize((14, 14), Image.LANCZOS)),
            f'{colorname}_radio_disabled': ImageTk.PhotoImage(radio_disabled.resize((14, 14), Image.LANCZOS))}

    def _style_calendar(self):
        """Create style configuration for the ttkbootstrap.widgets.datechooser

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.10

        self.settings.update({
            'TCalendar': {
                'layout': [
                    ('Toolbutton.border', {'sticky': 'nswe', 'children': [
                        ('Toolbutton.padding', {'sticky': 'nswe', 'children': [
                            ('Toolbutton.label', {'sticky': 'nswe'})]})]})],
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'background': self.theme.colors.bg,
                    'bordercolor': self.theme.colors.bg,
                    'darkcolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'relief': 'raised',
                    'font': self.theme.font,
                    'focusthickness': 0,
                    'focuscolor': '',
                    'borderwidth': 1,
                    'anchor': 'center',
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.selectfg),
                        ('selected !disabled', self.theme.colors.selectfg),
                        ('hover !disabled', self.theme.colors.selectfg)],
                    'background': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'bordercolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)],
                    'lightcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.primary)]}},
        'chevron.TButton': {
            'configure': {'font': 'helvetica 14'}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TCalendar': {
                    'configure': {
                        'foreground': self.theme.colors.fg,
                        'background': self.theme.colors.bg,
                        'bordercolor': self.theme.colors.bg,
                        'darkcolor': self.theme.colors.bg,
                        'lightcolor': self.theme.colors.bg,
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'borderwidth': 1,
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.selectfg),
                            ('selected !disabled', self.theme.colors.selectfg),
                            ('hover !disabled', self.theme.colors.selectfg)],
                        'background': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'bordercolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.get(color))]}},
            f'chevron.{color}.TButton': {
                'configure': {'font': 'helvetica 14'}}})

    def _style_exit_button(self):
        """Create style configuration for the toolbutton exit button"""
        disabled_bg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))
        pressed_vd = -0.2

        self.settings.update({
            'exit.TButton': {
                'configure': {
                    'relief': 'flat',
                    'font': 'helvetica 12'},
                'map': {
                    'background': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', self.theme.colors.danger)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'exit.{color}.TButton': {
                    'configure': {
                        'relief': 'flat',
                        'font': 'helvetica 12'},
                    'map': {
                        'background': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', self.theme.colors.danger)]}}})

    def _style_meter(self):
        """Create style configuration for the ttkbootstrap.widgets.meter

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.settings.update({
            'TMeter': {
                'layout': [
                    ('Label.border', {'sticky': 'nswe', 'border': '1', 'children': [
                        ('Label.padding', {'sticky': 'nswe', 'border': '1', 'children': [
                            ('Label.label', {'sticky': 'nswe'})]})]})],
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'background': self.theme.colors.bg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TMeter': {
                    'configure': {
                        'foreground': self.theme.colors.get(color)}}})

    def _style_label(self):
        """Create style configuration for ttk label: *ttk.Label*

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.settings.update({
            'TLabel': {
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'background': self.theme.colors.bg}},
            'Inverse.TLabel': {
                'configure': {
                    'foreground': self.theme.colors.bg,
                    'background': self.theme.colors.fg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TLabel': {
                    'configure': {
                        'foreground': self.theme.colors.get(color)}},
                f'{color}.Inverse.TLabel': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color)}},
                # TODO deprecate this version down the road
                f'{color}.Invert.TLabel': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color)}}})

    def _style_labelframe(self):
        """Create style configuration for ttk labelframe: *ttk.LabelFrame*

        The options available in this widget include:

            - Labelframe.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.fill: background
            - Label.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed
        """
        self.settings.update({
            'Labelframe.Label': {'element create': ('from', 'clam')},
            'Label.fill': {'element create': ('from', 'clam')},
            'Label.text': {'element create': ('from', 'clam')},
            'TLabelframe.Label': {
                'layout': [('Label.fill', {'sticky': 'nswe', 'children': [('Label.text', {'sticky': 'nswe'})]})],
                'configure': {
                    'foreground': self.theme.colors.fg
                }},
            'TLabelframe': {
                'layout': [('Labelframe.border', {'sticky': 'nswe'})],
                'configure': {
                    'relief': 'raised',
                    'borderwidth': '1',
                    'bordercolor': (self.theme.colors.border if self.theme.type == 'light'
                                    else self.theme.colors.selectbg),
                    'lightcolor': self.theme.colors.bg,
                    'darkcolor': self.theme.colors.bg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TLabelframe': {
                    'configure': {
                        'background': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.get(color)}},
                f'{color}.TLabelframe.Label': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.get(color)}}})

    def _style_checkbutton(self):
        """Create style configuration for ttk checkbutton: *ttk.Checkbutton*

        The options available in this widget include:

            - Checkbutton.padding: padding, relief, shiftrelief
            - Checkbutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground,
                upperbordercolor, lowerbordercolor
            - Checkbutton.focus: focuscolor, focusthickness
            - Checkbutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        self.theme_images.update(self._create_checkbutton_images('primary'))

        self.settings.update({
            'Checkbutton.indicator': {
                'element create': ('image', self.theme_images['primary_checkbutton_on'],
                                   ('disabled', self.theme_images['primary_checkbutton_disabled']),
                                   ('!selected', self.theme_images['primary_checkbutton_off']),
                                   {'width': 20, 'border': 4, 'sticky': 'w'})},
            'TCheckbutton': {
                'layout': [
                    ('Checkbutton.padding', {'children': [
                        ('primary.Checkbutton.indicator', {'side': 'left', 'sticky': ''}),
                        ('Checkbutton.focus', {'children': [
                            ('Checkbutton.label', {'sticky': 'nswe'})], 'side': 'left', 'sticky': ''})],
                        'sticky': 'nswe'})],
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'background': self.theme.colors.bg,
                    'focuscolor': ''},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('active !disabled', self.theme.colors.primary)]}}})

        # variations change indicator color
        for color in self.theme.colors:
            self.theme_images.update(self._create_checkbutton_images(color))
            self.settings.update({
                f'{color}.Checkbutton.indicator': {
                    'element create': ('image', self.theme_images[f'{color}_checkbutton_on'],
                                       ('disabled', self.theme_images[f'{color}_checkbutton_disabled']),
                                       ('!selected', self.theme_images[f'{color}_checkbutton_off']),
                                       {'width': 20, 'border': 4, 'sticky': 'w'})},
                f'{color}.TCheckbutton': {
                    'layout': [
                        ('Checkbutton.padding', {'children': [
                            (f'{color}.Checkbutton.indicator', {'side': 'left', 'sticky': ''}),
                            ('Checkbutton.focus', {'children': [
                                ('Checkbutton.label', {'sticky': 'nswe'})], 'side': 'left', 'sticky': ''})],
                            'sticky': 'nswe'})],
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('active !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=-0.2))]}}})

    def _create_checkbutton_images(self, colorname):
        """Create radiobutton assets

        Args:
            colorname (str): the name of the color to use for the button on state

        Returns:
            Tuple[PhotoImage]: a tuple of widget images.
        """
        prime_color = self.theme.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.theme.colors.selectbg
        on_fill = prime_color
        off_border = self.theme.colors.selectbg
        off_fill = self.theme.colors.inputbg if self.theme.type == 'light' else self.theme.colors.selectfg
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))
        disabled_bg = self.theme.colors.inputbg if self.theme.type == 'light' else disabled_fg

        # checkbutton off
        checkbutton_off = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(checkbutton_off)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, outline=off_border, width=3, fill=off_fill)

        # checkbutton on
        with importlib.resources.open_binary('ttkbootstrap', 'Symbola.ttf') as font_path:
            fnt = ImageFont.truetype(font_path, 130)
        checkbutton_on = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(checkbutton_on)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, fill=on_fill, outline=on_border, width=3)
        draw.text((20, 8), "✓", font=fnt, fill=self.theme.colors.selectfg)

        # checkbutton disabled
        checkbutton_disabled = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(checkbutton_disabled)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, outline=disabled_fg, width=3, fill=disabled_bg)

        return {
            f'{colorname}_checkbutton_off':
                ImageTk.PhotoImage(checkbutton_off.resize((14, 14), Image.LANCZOS)),
            f'{colorname}_checkbutton_on':
                ImageTk.PhotoImage(checkbutton_on.resize((14, 14), Image.LANCZOS)),
            f'{colorname}_checkbutton_disabled':
                ImageTk.PhotoImage(checkbutton_disabled.resize((14, 14), Image.LANCZOS))}

    def _style_solid_menubutton(self):
        """Apply a solid color style to ttk menubutton: *ttk.Menubutton*

        The options available in this widget include:

            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify,
                wraplength, embossed, image, stipple, background
            - Menubutton.label:
        """
        # disabled settings
        disabled_fg = self.theme.colors.inputfg
        disabled_bg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.2
        hover_vd = -0.1

        self.settings.update({
            'TMenubutton': {
                'configure': {
                    'foreground': self.theme.colors.selectfg,
                    'background': self.theme.colors.primary,
                    'bordercolor': self.theme.colors.primary,
                    'darkcolor': self.theme.colors.primary,
                    'lightcolor': self.theme.colors.primary,
                    'arrowsize': 4,
                    'arrowcolor': self.theme.colors.bg if self.theme.type == 'light' else 'white',
                    'arrowpadding': (0, 0, 15, 0),
                    'relief': 'raised',
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                'map': {
                    'arrowcolor': [
                        ('disabled', disabled_fg)],
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'background': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'bordercolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'darkcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'lightcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TMenubutton': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color),
                        'bordercolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.get(color),
                        'lightcolor': self.theme.colors.get(color),
                        'arrowsize': 4,
                        'arrowcolor': self.theme.colors.bg if self.theme.type == 'light' else 'white',
                        'arrowpadding': (0, 0, 15, 0),
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'arrowcolor': [
                            ('disabled', disabled_fg)],
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'background': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'bordercolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'darkcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'lightcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))]}}})

    def _style_outline_menubutton(self):
        """Apply and outline style to ttk menubutton: *ttk.Menubutton*

        The options available in this widget include:

            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify,
                wraplength, embossed, image, stipple, background
            - Menubutton.label:
        """
        # disabled settings
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        # pressed and hover settings
        pressed_vd = -0.2
        hover_vd = -0.1

        self.settings.update({
            'Outline.TMenubutton': {
                'configure': {
                    'font': self.theme.font,
                    'foreground': self.theme.colors.primary,
                    'background': self.theme.colors.bg,
                    'bordercolor': self.theme.colors.primary,
                    'darkcolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'arrowcolor': self.theme.colors.primary,
                    'arrowpadding': (0, 0, 15, 0),
                    'relief': 'raised',
                    'focusthickness': 0,
                    'focuscolor': '',
                    'padding': (10, 5)},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.selectfg),
                        ('hover !disabled', self.theme.colors.selectfg)],
                    'background': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'bordercolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'darkcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'lightcolor': [
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'arrowcolor': [
                        ('disabled', disabled_fg),
                        ('pressed !disabled', self.theme.colors.selectfg),
                        ('hover !disabled', self.theme.colors.selectfg)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Outline.TMenubutton': {
                    'configure': {
                        'foreground': self.theme.colors.get(color),
                        'background': self.theme.colors.bg,
                        'bordercolor': self.theme.colors.get(color),
                        'darkcolor': self.theme.colors.bg,
                        'lightcolor': self.theme.colors.bg,
                        'arrowcolor': self.theme.colors.get(color),
                        'arrowpadding': (0, 0, 15, 0),
                        'relief': 'raised',
                        'focusthickness': 0,
                        'focuscolor': '',
                        'padding': (10, 5)},
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.selectfg),
                            ('hover !disabled', self.theme.colors.selectfg)],
                        'background': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'bordercolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'darkcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'lightcolor': [
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'arrowcolor': [
                            ('disabled', disabled_fg),
                            ('pressed !disabled', self.theme.colors.selectfg),
                            ('hover !disabled', self.theme.colors.selectfg)]}}})

    def _style_notebook(self):
        """Create style configuration for ttk notebook: *ttk.Notebook*

        The options available in this widget include:

            - Notebook.client: background, bordercolor, lightcolor, darkcolor
            - Notebook.tab: background, bordercolor, lightcolor, darkcolor
            - Notebook.padding: padding, relief, shiftrelief
            - Notebook.focus: focuscolor, focusthickness
            - Notebook.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        border_color = self.theme.colors.border if self.theme.type == 'light' else self.theme.colors.selectbg
        fg_color = self.theme.colors.inputfg if self.theme.type == 'light' else self.theme.colors.inputbg
        bg_color = self.theme.colors.inputbg if self.theme.type == 'light' else border_color

        self.settings.update({
            'TNotebook': {
                'configure': {
                    'bordercolor': border_color,
                    'lightcolor': self.theme.colors.bg,
                    'darkcolor': self.theme.colors.bg,
                    'borderwidth': 1}},
            'TNotebook.Tab': {
                'configure': {
                    'bordercolor': border_color,
                    'lightcolor': self.theme.colors.bg,
                    'foreground': self.theme.colors.fg,
                    'padding': (10, 5)},
                'map': {
                    'background': [
                        ('!selected', bg_color)],
                    'lightcolor': [
                        ('!selected', bg_color)],
                    'darkcolor': [
                        ('!selected', bg_color)],
                    'bordercolor': [
                        ('!selected', border_color)],
                    'foreground': [
                        ('!selected', fg_color)]}}})

    def _style_panedwindow(self):
        """Create style configuration for ttk paned window: *ttk.PanedWindow*

        The options available in this widget include:

            Paned Window:

                - Panedwindow.background: background

            Sash:

                - Sash.hsash: sashthickness
                - Sash.hgrip: lightcolor, bordercolor, gripcount
                - Sash.vsash: sashthickness
                - Sash.vgrip: lightcolor, bordercolor, gripcount
        """
        self.settings.update({
            'TPanedwindow': {
                'configure': {
                    'background': self.theme.colors.bg}},
            'Sash': {
                'configure': {
                    'bordercolor': self.theme.colors.bg,
                    'lightcolor': self.theme.colors.bg,
                    'sashthickness': 8,
                    'sashpad': 0,
                    'gripcount': 0}}})

    def _style_sizegrip(self):
        """Create style configuration for ttk sizegrip: *ttk.Sizegrip*

        The options available in this widget include:

            - Sizegrip.sizegrip: background
        """
        default_color = 'border' if self.theme.type == 'light' else 'inputbg'
        self._create_sizegrip_images(default_color)
        self.settings.update({
            'Sizegrip.sizegrip': {
                'element create': ('image', self.theme_images[f'{default_color}_sizegrip'])},
            'TSizegrip': {
                'layout': [('Sizegrip.sizegrip', {'side': 'bottom', 'sticky': 'se'})]}})

        for color in self.theme.colors:
            self._create_sizegrip_images(color)
            self.settings.update({
                f'{color}.Sizegrip.sizegrip': {
                    'element create': ('image', self.theme_images[f'{color}_sizegrip'])},
                f'{color}.TSizegrip': {
                    'layout': [(f'{color}.Sizegrip.sizegrip', {'side': 'bottom', 'sticky': 'se'})]}})

    def _create_sizegrip_images(self, colorname):
        """Create assets for size grip

        Args:
            colorname (str): the name of the color to use for the sizegrip images
        """
        im = Image.new('RGBA', (14, 14))
        draw = ImageDraw.Draw(im)
        color = self.theme.colors.get(colorname)
        draw.rectangle((9, 3, 10, 4), fill=color)  # top
        draw.rectangle((6, 6, 7, 7), fill=color)  # middle
        draw.rectangle((9, 6, 10, 7), fill=color)
        draw.rectangle((3, 9, 4, 10), fill=color)  # bottom
        draw.rectangle((6, 9, 7, 10), fill=color)
        draw.rectangle((9, 9, 10, 10), fill=color)
        self.theme_images[f'{colorname}_sizegrip'] = ImageTk.PhotoImage(im)
