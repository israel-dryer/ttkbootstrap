"""
    Why does this project exist?
    ============================
    Yes, Tkinter is old, and so often under-appreciated or overlooked for building modern GUI's. And yet, its theme
    engine is extremely powerful. This project was created to harness the power of ttk's (and thus Python's) existing
    built-in theme engine to create modern and professional-looking user interfaces which are inspired by, and in many
    cases, whole-sale rip-off's of the themes found on https://bootswatch.com/. Even better, you have the abilty to
    create and use your own custom themes using :ref:`TTK Creator <ttkcreator>`.

    A bootstrap approach to style
    =============================
    Many people are familiar with bootstrap for web developement. It comes pre-packaged with built-in css style classes
    that provide a professional and consistent api for quick development. I took a similar approach with this project
    by pre-defining styles for nearly all ttk widgets. This makes is very easy to apply the theme colors to various
    widgets by using style declarations. If you want a button in the `secondary` theme color, simply apply the
    ``secondary.TButton`` style to the button. Want a blue outlined button? Apply the ``info.Outline.TButton`` style to
    the button.

    What about the old tkinter widgets?
    ===================================
    Some of the ttk widgets utilize existing tkinter widgets. For example: there is a tkinter popdown list in the
    ``ttk.Combobox`` and a legacy tkinter widget inside the ``ttk.OptionMenu``. To make sure these widgets didn't stick
    out like a sore thumb, I created a ``StyleTK`` class to apply the same color and style to these legacy widgets.
    While these legacy widgets are not necessarily intended to be used (and will probably not look as nice as the ttk
    versions when they exist), they are available if needed, and shouldn't look completely out-of-place in your
    ttkbootstrap themed application.
"""
import colorsys
import importlib.resources
import json
from pathlib import Path
from tkinter import ttk

from PIL import ImageTk, Image, ImageDraw


class Style(ttk.Style):
    """
    A class for setting the application style.
    """

    def __init__(self, theme='flatly', themes_file=None, *args, **kwargs):
        """
        :param str theme: the name of the theme to use at runtime; *flatly* by default.
        :param str themes_file: Path to a user-defined themes file. Defaults to the themes file set in ttkcreator.
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
        """
        Load all ttkbootstrap defined themes
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
        """
        Register a theme definition; this makes the definition and name available at run-time so that
        the assets and styles can be created.

        :param str definition: an instance of the ``ThemeDefinition`` class
        """
        self._theme_names.add(definition.name)
        self._theme_definitions[definition.name] = definition

    def theme_use(self, themename=None):
        """
        If themename is None, returns the theme in use, otherwise, set the current theme to themename, refreshes all
        widgets and emits a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during* runtime. Otherwise, pass the theme name into the
        Style constructor to instantiate the style with a theme.

        :param str themename: the theme to apply when creating new widgets
        """
        # self.themes[settings.name] = StylerTTK(self, settings)
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
                self._theme_definitions[themename] = ThemeDefinition()
                return
            return

        # theme has not yet been created
        self._theme_objects[themename] = StylerTTK(self, self.theme)
        self._theme_objects[themename].styler_tk.style_tkinter_widgets()
        super().theme_use(themename)
        return


class ThemeDefinition:
    """
    A class to provide defined name, colors, and font settings for a ttkbootstrap theme.

    :param str name: The name of the theme
    :param str themetype: type: 'light' or 'dark'
    :param str font: Default font to apply to theme. Helvetica is used by default.
    :param Color colors: An instance of the `Colors` class.
    """

    def __init__(self, name='default', themetype='light', font='helvetica', colors=None):
        self.name = name
        self.type = themetype
        self.font = font
        self.colors = colors if colors else Colors()

    def __repr__(self):
        return f'name={self.name}, type={self.type}, font={self.font}, colors={self.colors}'


class Colors:
    """
    A collection of colors used in a ttkbootstrap theme definition.

    :param str primary: the primary theme color; is used as basis for all widgets
    :param str secondary: an accent color; typically the same as `selectbg` in built-in themes
    :param str success: an accent color; an orange hue in most themes
    :param str info: an accent color; a blue hue in most themes
    :param str warning: an accent color; an orange hue in most themes
    :param str danger: an accent color; a red hue in most themes
    :param str bg: background color; used for root window background
    :param str fg: primary font color; used for labels and non-input related widgets
    :param str selectfg: foreground color of selected text
    :param str selectbg: background color of selected text background
    :param str border: a color used on the border of several input widgets (combobox, entry, spinbox, etc...)
    :param str inputfg: a color used for input widgets; typically a reverse lightness of `fg`
    :param str inputbg: a color used for input widget background and trough color
    """

    def __init__(self, **kwargs):
        self.primary = kwargs.get('primary', '#ffffff')
        self.secondary = kwargs.get('secondary', '#ffffff')
        self.success = kwargs.get('success', '#ffffff')
        self.info = kwargs.get('info', '#ffffff')
        self.warning = kwargs.get('warning', '#ffffff')
        self.danger = kwargs.get('danger', '#ffffff')
        self.bg = kwargs.get('bg', '#ffffff')
        self.fg = kwargs.get('fg', '#000000')
        self.selectbg = kwargs.get('selectbg', '#000000')
        self.selectfg = kwargs.get('selectfg', '#ffffff')
        self.border = kwargs.get('border', '#000000')
        self.inputfg = kwargs.get('inputfg', '#000000')
        self.inputbg = kwargs.get('inputbg', '#000000')

    def get(self, color_label):
        """
        Lookup a color property

        :param str color_label: a color label corresponding to a class propery (primary, secondary, success, etc...)

        :returns: a hexadecimal color value
        :rtype: str
        """
        return self.__dict__.get(color_label)

    def set(self, color_label, color_value):
        """
        Set a color property

        :param str color_label: the name of the color to be set (key)
        :param str color_value: a hexadecimal color value

        Example::

            set('primary', '#fafafa')
        """
        self.__dict__[color_label] = color_value

    def __iter__(self):
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger'])

    def __repr__(self):
        return str((tuple(zip(self.__dict__.keys(), self.__dict__.values()))))

    @staticmethod
    def label_iter():
        """
         Iterates over all color label properties in the Color class

         :returns: an iterator representing the name of the color properties
         :rtype: iter[str]
        """
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'bg', 'fg', 'selectbg', 'selectfg',
                     'border', 'inputfg', 'inputbg'])

    @staticmethod
    def hex_to_rgb(color):
        """
        Convert hexadecimal color to rgb color value

        :param str color: hexadecimal color value

        :returns: rgb color value
        :rtype: tuple
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
        """
        Convert rgb to hexadecimal color value

        :param int r: red
        :param int g: green
        :param int b: blue

        :returns: a hexadecimal color value
        :rtype: str
        """
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """
        Modify the hue, saturation, and/or value of a given hex color value.

        :param str color: the hexadecimal color value that is the target of hsv changes
        :param float hd: % change in hue
        :param float sd: % change in saturation
        :param float vd: % change in value

        :returns: a new hexadecimal color value that results from the hsv arguments passed into the function
        :rtype: str
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
    """
    A class for styling tkinter widgets (not ttk).

    :param parent: an instance of `StylerTTK`
    """

    def __init__(self, parent):
        self.master = parent.style.master
        self.theme = parent.theme

    def style_tkinter_widgets(self):
        """
        A wrapper on all widget style methods. Applies current theme to all standard tkinter widgets
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
        pass

    def _set_option(self, *args):
        """
        A convenience method to shorten the call to ``option_add``. *Laziness is next to godliness*.
        """
        self.master.option_add(*args)

    def _style_window(self):
        """
        Apply global options to all matching ``tkinter`` widgets
        """
        self.master.configure(background=self.theme.colors.bg)
        self._set_option('*background', self.theme.colors.bg, 60)
        self._set_option('*font', self.theme.font, 60)
        self._set_option('*activeBackground', self.theme.colors.selectbg, 60)
        self._set_option('*activeForeground', self.theme.colors.selectfg, 60)
        self._set_option('*selectBackground', self.theme.colors.selectbg, 60)
        self._set_option('*selectForeground', self.theme.colors.selectfg, 60)

    def _style_canvas(self):
        """
        Apply style to ``tkinter.Canvas``
        """
        self._set_option('*Canvas.highlightThickness', 1)
        self._set_option('*Canvas.highlightBackground', self.theme.colors.border)
        self._set_option('*Canvas.background', self.theme.colors.bg)

    def _style_button(self):
        """
        Apply style to ``tkinter.Button``
        """
        active_bg = Colors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option('*Button.relief', 'flat')
        self._set_option('*Button.borderWidth', 0)
        self._set_option('*Button.activeBackground', active_bg)
        self._set_option('*Button.foreground', self.theme.colors.selectfg)
        self._set_option('*Button.background', self.theme.colors.primary)

    def _style_label(self):
        """
        Apply style to ``tkinter.Label``
        """
        self._set_option('*Label.foreground', self.theme.colors.fg)
        self._set_option('*Label.background', self.theme.colors.bg)

    def _style_checkbutton(self):
        """
        Apply style to ``tkinter.Checkbutton``
        """
        self._set_option('*Checkbutton.activeBackground', self.theme.colors.bg)
        self._set_option('*Checkbutton.activeForeground', self.theme.colors.primary)
        self._set_option('*Checkbutton.background', self.theme.colors.bg)
        self._set_option('*Checkbutton.foreground', self.theme.colors.fg)
        self._set_option('*Checkbutton.selectColor',
                         self.theme.colors.primary if self.theme.type == 'dark' else 'white')

    def _style_radiobutton(self):
        """
        Apply style to ``tkinter.Radiobutton``
        """
        self._set_option('*Radiobutton.activeBackground', self.theme.colors.bg)
        self._set_option('*Radiobutton.activeForeground', self.theme.colors.primary)
        self._set_option('*Radiobutton.background', self.theme.colors.bg)
        self._set_option('*Radiobutton.foreground', self.theme.colors.fg)
        self._set_option('*Radiobutton.selectColor',
                         self.theme.colors.primary if self.theme.type == 'dark' else 'white')

    def _style_entry(self):
        """
        Apply style to ``tkinter.Entry``
        """
        self._set_option('*Entry.relief', 'flat')
        self._set_option('*Entry.background',
                         (self.theme.colors.inputbg if self.theme.type == 'light' else
                          Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1)))
        self._set_option('*Entry.foreground', self.theme.colors.inputfg)
        self._set_option('*Entry.highlightThickness', 1)
        self._set_option('*Entry.highlightBackground', self.theme.colors.border)
        self._set_option('*Entry.highlightColor', self.theme.colors.primary)

    def _style_scale(self):
        """
        Apply style to ``tkinter.Scale``
        """
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
        """
        Apply style to `tkinter.Spinbox``
        """
        self._set_option('*Spinbox.foreground', self.theme.colors.inputfg)
        self._set_option('*Spinbox.relief', 'flat')
        self._set_option('*Spinbox.background',
                         (self.theme.colors.inputbg if self.theme.type == 'light' else
                          Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1)))
        self._set_option('*Spinbox.highlightThickness', 1)
        self._set_option('*Spinbox.highlightColor', self.theme.colors.primary)
        self._set_option('*Spinbox.highlightBackground', self.theme.colors.border)

    def _style_listbox(self):
        """
        Apply style to ``tkinter.Listbox``
        """
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
        """
        Apply style to ``tkinter.Menubutton``
        """
        hover_color = Colors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option('*Menubutton.activeBackground', hover_color)
        self._set_option('*Menubutton.background', self.theme.colors.primary)
        self._set_option('*Menubutton.foreground', self.theme.colors.selectfg)
        self._set_option('*Menubutton.borderWidth', 0)

    def _style_menu(self):
        """
        Apply style to ``tkinter.Menu``
        """
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
        """
        Apply style to ``tkinter.Labelframe``
        """
        self._set_option('*Labelframe.font', self.theme.font)
        self._set_option('*Labelframe.foreground', self.theme.colors.fg)
        self._set_option('*Labelframe.highlightColor', self.theme.colors.border)
        self._set_option('*Labelframe.borderWidth', 1)
        self._set_option('*Labelframe.highlightThickness', 0)

    def _style_textwidget(self):
        """
        Apply style to ``tkinter.Text``
        """
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
    """
    A class to create a new ttk theme.

    :param Style style: An instance of ``ttk.Style`` class
    :param ThemeDefinition definition: creates the settings for the theme to be created
    """

    def __init__(self, style, definition):
        self.style = style
        self.theme = definition
        self.theme_images = {}
        self.settings = {}
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """
        Create and style a new ttk theme. A wrapper around internal style methods.
        """
        self.update_ttk_theme_settings()
        self.style.theme_create(self.theme.name, 'clam', self.settings)

    def update_ttk_theme_settings(self):
        """
        Update the settings dictionary that is used to create a theme. This is a wrapper on all the `_style_widget`
        methods which define the layout, configuration, and styling mapping for each ttk widget.
        """
        self._style_labelframe()
        self._style_spinbox()
        self._style_scale()
        self._style_scrollbar()
        self._style_combobox()
        self._style_frame()
        self._style_checkbutton()
        self._style_entry()
        self._style_label()
        self._style_notebook()
        self._style_outline_buttons()
        self._style_outline_menubutton()
        self._style_outline_toolbutton()
        self._style_progressbar()
        self._style_radiobutton()
        self._style_solid_buttons()
        self._style_solid_menubutton()
        self._style_solid_toolbutton()
        self._style_treeview()
        self._style_separator()
        self._style_panedwindow()
        self._style_roundtoggle_toolbutton()
        self._style_squaretoggle_toolbutton()
        self._style_defaults()

    def _style_defaults(self):
        """
        Setup the default ``ttk.Style`` configuration. These defaults are applied to any widget that contains these
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
        """
        Create style configuration for ``ttk.Combobox``. This element style is created with a layout that combines
        *clam* and *default* theme elements.

        The options available in this widget based on this layout include:

            * Combobox.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            * Combobox.field: bordercolor, lightcolor, darkcolor, fieldbackground
            * Combobox.padding: padding, relief, shiftrelief
            * Combobox.textarea: font, width

        **NOTE:**

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
        """
        Create style configuration for ttk separator: *ttk.Separator*. The default style for light will be border, but
        dark will be primary, as this makes the most sense for general use. However, all other colors will be available
        as well through styling.

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

    def _style_progressbar(self):
        """
        Create style configuration for ttk progressbar: *ttk.Progressbar*

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
    def _create_slider_image(color, size=18):
        """
        Create a circle slider image based on given size and color; used in the slider widget.

        :param str color: a hexadecimal color value
        :param int size: the size diameter of the slider circle.

        :returns: An image draw in the shape of a circle of the theme color specified
        :rtype: ImageTk.PhotoImage
        """
        im = Image.new('RGBA', (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=color)
        return ImageTk.PhotoImage(im.resize((size, size), Image.LANCZOS))

    def _style_scale(self):
        """
        Create style configuration for ttk scale: *ttk.Scale*

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

    def _style_scrollbar(self):
        """
        Create style configuration for ttk scrollbar: *ttk.Scrollbar*. This theme uses elements from the *alt* theme to
        build the widget layout.

        The options available in this widget include:

            - Scrollbar.trough: orient, troughborderwidth, troughcolor, troughrelief, groovewidth
            - Scrollbar.uparrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.thumb: width, background, bordercolor, relief, orient
        """
        self.settings.update({
            'Vertical.Scrollbar.trough': {'element create': ('from', 'alt')},
            'Vertical.Scrollbar.thumb': {'element create': ('from', 'alt')},
            'Vertical.Scrollbar.uparrow': {'element create': ('from', 'alt')},
            'Vertical.Scrollbar.downarrow': {'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.trough': {'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.thumb': {'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.leftarrow': {'element create': ('from', 'alt')},
            'Horizontal.Scrollbar.rightarrow': {'element create': ('from', 'alt')},
            'TScrollbar': {'configure': {
                'troughrelief': 'flat',
                'relief': 'flat',
                'troughborderwidth': 2,
                'troughcolor': self.theme.colors.inputbg,
                'background': Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1),
                'arrowsize': 16,
                'arrowcolor': self.theme.colors.inputfg}}})

    def _style_spinbox(self):
        """
        Create style configuration for ttk spinbox: *ttk.Spinbox*

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
        """
        Create style configuration for ttk treeview: *ttk.Treeview*. This widget uses elements from the *alt* and *clam*
         theme to create the widget layout.

        The options available in this widget include:

            Treeview:

                - Treeview.field: bordercolor, lightcolor, darkcolor, fieldbackground
                - Treeview.padding: padding, relief, shiftrelief
                - Treeview.treearea:
                - Treeitem.padding: padding, relief, shiftrelief
                - Treeitem.indicator: foreground, diameter, indicatormargins
                - Treeitem.image: image, stipple, background
                - Treeitem.focus: focuscolor, focusthickness
                - Treeitem.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed

            Treeheading:

                - Treeheading.cell: background, rownumber
                - Treeheading.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
                - Treeheading.padding: padding, relief, shiftrelief
                - Treeheading.image: image, stipple, background
                - Treeheading.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed
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
        """
        Create style configuration for ttk frame: *ttk.Frame*

        The options available in this widget include:

            - Frame.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
        """
        self.settings.update({
            'TFrame': {'configure': {'background': self.theme.colors.bg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TFrame': {'configure': {'background': self.theme.colors.get(color)}}})

    def _style_solid_buttons(self):
        """
        Apply a solid color style to ttk button: *ttk.Button*

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
        """
        Apply an outline style to ttk button: *ttk.Button*. This button has a solid button look on focus and
        hover.

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

    def _create_squaretoggle_image(self, colorname):
        """
        Create a set of images for the square toggle button and return as ``PhotoImage``

        :param str colorname: the color label assigned to the colors property

        :returns: a tuple of images (toggle_on, toggle_off, toggle_disabled)
        :rtype: Tuple[PhotoImage]
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
        """
        Create a set of images for the rounded toggle button and return as ``PhotoImage``

        :param str colorname: the color label assigned to the colors property

        :returns: a tuple of images (toggle_on, toggle_off, toggle_disabled)
        :rtype: Tuple[PhotoImage]
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
        """
        Apply a rounded toggle switch style to ttk widgets that accept the toolbutton style (for example,
        a checkbutton: *ttk.Checkbutton*)

        The options available in this widget include:
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
        """
        Apply a square toggle switch style to ttk widgets that accept the toolbutton style (for example,
        a checkbutton: *ttk.Checkbutton*)

        The options available in this widget include:
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
        """
        Apply a solid color style to ttk widgets that use the Toolbutton style (for example,
        a checkbutton: *ttk.Checkbutton*)

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
            'Toolbutton': {
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
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg)],
                    'background': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'bordercolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'darkcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))],
                    'lightcolor': [
                        ('disabled', disabled_bg),
                        ('pressed !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('selected !disabled', Colors.update_hsv(self.theme.colors.primary, vd=pressed_vd)),
                        ('hover !disabled', Colors.update_hsv(self.theme.colors.primary, vd=hover_vd))]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.Toolbutton': {
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
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'bordercolor': [
                            ('disabled', disabled_bg),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'darkcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))],
                        'lightcolor': [
                            ('disabled', disabled_bg),
                            ('pressed !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=pressed_vd)),
                            ('hover !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=hover_vd))]}}})

    def _style_outline_toolbutton(self):
        """
        Apply an outline style to ttk widgets that use the Toolbutton style (for example,
        a checkbutton: *ttk.Checkbutton*). This button has a solid button look on focus and hover.

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
        """
        Create style configuration for ttk entry: *ttk.Entry*

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
                        ('hover !disabled', self.theme.colors.primary)],
                    'lightcolor': [
                        ('focus !disabled', self.theme.colors.primary)],
                    'darkcolor': [
                        ('focus !disabled', self.theme.colors.primary)]}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TEntry': {
                    'map': {
                        'foreground': [
                            ('disabled', disabled_fg)],
                        'bordercolor': [
                            ('focus !disabled', self.theme.colors.get(color))],
                        'lightcolor': [
                            ('focus !disabled', self.theme.colors.get(color))],
                        'darkcolor': [
                            ('focus !disabled', self.theme.colors.get(color))]}}})

    def _style_radiobutton(self):
        """
        Create style configuration for ttk radiobutton: *ttk.Radiobutton*

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
        """
        Create radiobutton assets

        :param str colorname: the name of the color to use for the button on state
        """
        prime_color = self.theme.colors.get(colorname)
        on_border = prime_color if self.theme.type == 'light' else self.theme.colors.selectbg
        on_indicator = self.theme.colors.selectfg if self.theme.type == 'light' else prime_color
        on_fill = prime_color if self.theme.type == 'light' else self.theme.colors.selectfg
        off_border = self.theme.colors.border if self.theme.type == 'light' else self.theme.colors.selectbg
        off_fill = self.theme.colors.inputbg if self.theme.type == 'light' else self.theme.colors.selectfg
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))
        disabled_bg = self.theme.colors.inputbg if self.theme.type == 'light' else disabled_fg

        # radio off
        radio_off = Image.new('RGBA', (134, 134))
        draw = ImageDraw.Draw(radio_off)
        draw.ellipse([2, 2, 132, 132], outline=off_border, width=8, fill=off_fill)

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
            f'{colorname}_radio_off': ImageTk.PhotoImage(radio_off.resize((16, 16), Image.LANCZOS)),
            f'{colorname}_radio_on': ImageTk.PhotoImage(radio_on.resize((16, 16), Image.LANCZOS)),
            f'{colorname}_radio_disabled': ImageTk.PhotoImage(radio_disabled.resize((16, 16), Image.LANCZOS))}

    def _style_label(self):
        """
        Create style configuration for ttk label: *ttk.Label*

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.settings.update({
            'TLabel': {'configure': {'foreground': self.theme.colors.fg}}})

        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TLabel': {
                    'configure': {
                        'foreground': self.theme.colors.get(color)}},
                f'{color}.Invert.TLabel': {
                    'configure': {
                        'foreground': self.theme.colors.selectfg,
                        'background': self.theme.colors.get(color)}}})

    def _style_labelframe(self):
        """
        Create style configuration for ttk labelframe: *ttk.LabelFrame*

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
        """
        Create style configuration for ttk checkbutton: *ttk.Checkbutton*

        The options available in this widget include:

            - Checkbutton.padding: padding, relief, shiftrelief
            - Checkbutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground,
                upperbordercolor, lowerbordercolor
            - Checkbutton.focus: focuscolor, focusthickness
            - Checkbutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background

        **NOTE:**
            On Windows, the button defaults to the 'xpnative' theme look. This means that you cannot change the look
            and feel with styles. On Linux and MacOS, defaults to stylized 'clam' theme, so the style can be changed.
        """
        disabled_fg = (Colors.update_hsv(self.theme.colors.inputbg, vd=-0.2) if self.theme.type == 'light' else
                       Colors.update_hsv(self.theme.colors.inputbg, vd=-0.3))

        if 'xpnative' in self.style.theme_names():
            self.settings.update({
                'Checkbutton.indicator': {
                    'element create': ('from', 'xpnative')}})

        self.settings.update({
            'TCheckbutton': {
                'configure': {
                    'foreground': self.theme.colors.fg,
                    'indicatorsize': 10,
                    'indicatormargin': 10,
                    'indicatorforeground': self.theme.colors.selectbg},
                'map': {
                    'foreground': [
                        ('disabled', disabled_fg),
                        ('active !disabled', self.theme.colors.primary)],
                    'indicatorforeground': [
                        ('disabled', disabled_fg),
                        ('active selected !disabled', self.theme.colors.primary)]}}})

        # variations change indicator color
        for color in self.theme.colors:
            self.settings.update({
                f'{color}.TCheckbutton': {
                    'configure': {'indicatorforeground': self.theme.colors.get(color)},
                    'map': {
                        'indicatorforeground': [
                            ('disabled', disabled_fg),
                            ('active selected !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=-0.2))],
                        'foreground': [
                            ('disabled', disabled_fg),
                            ('active !disabled', Colors.update_hsv(self.theme.colors.get(color), vd=-0.2))]}}})

    def _style_solid_menubutton(self):
        """
        Apply a solid color style to ttk menubutton: *ttk.Menubutton*

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
        """
        Apply and outline style to ttk menubutton: *ttk.Menubutton*

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
        """
        Create style configuration for ttk notebook: *ttk.Notebook*

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
        """
        Create style configuration for ttk paned window: *ttk.PanedWindow*

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
                    'background': Colors.update_hsv(self.theme.colors.inputbg, vd=-0.1)}},
            'Sash': {
                'configure': {
                    'bordercolor': self.theme.colors.inputfg,
                    'lightcolor': self.theme.colors.inputbg,
                    'sashthickness': 9,
                    'sashpad': 0,
                    'gripcount': 25}}})

    def _style_sizegroup(self):
        """
        Create style configuration for ttk sizegrip: *ttk.Sizegrip*

        The options available in this widget include:

            - Sizegrip.sizegrip: background

        **NOT IMPLEMENTED as existing styles are already covering this.**
        """
        pass
