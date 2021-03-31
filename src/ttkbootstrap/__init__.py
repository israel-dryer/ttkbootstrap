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
import json
import colorsys
from pathlib import Path
import importlib.resources
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw


class Style(ttk.Style):
    """
    A class for setting the application style.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.themes = {}
        self._load_themes()
        self.settings = None
        self.colors = None

    def _load_themes(self):
        """
        Load all ttkbootstrap defined themes
        """
        json_data = importlib.resources.read_text('ttkbootstrap', 'themes.json')
        json_data_user = importlib.resources.read_text('ttkbootstrap', 'user_themes.json')

        builtin_themes = json.loads(json_data)
        user_themes = json.loads(json_data_user)
        settings = {'themes': builtin_themes['themes'] + user_themes['themes']}

        for theme in settings['themes']:
            if theme['name'] not in self.theme_names():
                settings = ThemeSettings(
                    name=theme['name'],
                    type=theme['type'],
                    font=theme['font'],
                    colors=Colors(**theme['colors']))
                self.themes[settings.name] = StylerTTK(self, settings)

    def theme_use(self, themename=None):
        """
        If themename is None, returns the theme in use, otherwise, set the current theme to themename, refreshes all
        widgets and emits a <<ThemeChanged>> event.

        :param str themename: the theme to apply when creating new widgets
        """
        if themename is None:
            # Starting on Tk 8.6, checking this global is no longer needed
            # since it allows doing self.tk.call(self._name, "theme", "use")
            return self.tk.eval("return $ttk::currentTheme")

        try:
            current_theme = self.themes.get(themename)
            current_theme.styler_tk.apply_style()
            self.settings = current_theme.settings
            self.colors = current_theme.settings.colors
        except AttributeError as e:
            pass

        # using "ttk::setTheme" instead of "ttk::style theme use" causes
        # the variable currentTheme to be updated, also, ttk::setTheme calls
        # "ttk::style theme use" in order to change theme.
        self.tk.call("ttk::setTheme", themename)


class ThemeSettings:
    """
    A class to provide settings for a ttkbootstrap theme.

    :param str name: The name of the theme
    :param str type: type: 'light' or 'dark'
    :param str font: Default font to apply to theme. Helvetica is used by default.
    :param Color colors: An instance of the `Colors` class.
    """

    def __init__(self, name='default', type='light', font='helvetica', colors=None):
        self.name = name
        self.type = type
        self.font = font
        self.colors = colors if colors else Colors()

    def __repr__(self):
        return f'name={self.name}, type={self.type}, font={self.font}, colors={self.colors}'


class Colors:
    """
    A collection of colors used in a ttkbootstrap theme.

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
    :param str light: a color used for input widget background and trough color
    :param str border: a color used on the border of several input widgets (combobox, entry, spinbox, etc...)
    :param str inputfg: a color used for input widgets; typically a reverse lightness of `fg`
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
        self.light = kwargs.get('light', '#ffffff')
        self.border = kwargs.get('border', '#000000')
        self.inputfg = kwargs.get('inputfg', '#000000')

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

    def label_iter(self):
        """
         Iterates over all color label properties in the Color class

         :returns: an iterator representing the name of the color properties
         :rtype: iter[str]
        """
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'bg', 'fg', 'selectbg', 'selectfg',
                     'light', 'border', 'inputfg'])

    @staticmethod
    def hex_to_rgb(color):
        """
        Convert hexadecimal color to rgb color value

        :param str color: hexadecimal color value

        :returns: rgb color value
        :rtype: tuple
        """
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
    def brightness(hex_color, pct_change):
        """
        Adjust the value of a given hexadecimal color. The percent change is expected to be a float.

        To return a *lighter* color, use a positive floating value::

            Colors.brightness('#fafafa', 0.15)

        To return a *darker* color, use a negative floating value::

            Colors.brightness('#fafafa', -0.15)

        :param str hex_color: hexadecimal color
        :param float pct_change: a floating value

        :returns: a lightened or darkened hexadecimal color value
        :rtype: str
        """
        r, g, b = Colors.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v_ = (1 + pct_change) * v
        v_max = max(0, v_)
        v_min = min(1, v_max)
        r_, g_, b_ = colorsys.hsv_to_rgb(h, s, v_min)
        return Colors.rgb_to_hex(r_, g_, b_)


class StylerTK:
    """
    A class for styling tkinter widgets (not ttk). Several ttk widgets utilize tkinter widgets in some capacity, such
    as the *popdownlist* on the ``ttk.Combobox``. To create a consistent user experience, standard tkinter widgets are
    themed as much as possible with the look and feel of the ttkbootstrap theme applied. Tkinter widgets are not the
    primary target of this project; however, they can be used without looking entirely out-of-place in most cases.

    :param parent: an instance of `StylerTTK`
    """

    def __init__(self, parent):
        self.master = parent.style.master
        self.settings = parent.settings

    def apply_style(self):
        """
        A wrapper on all widget style methods. Applies current theme to all standard tkinter widgets
        """
        self._style_window()
        self._style_button()
        self._style_label()
        self._style_checkbutton()
        self._style_radiobutton()
        self._style_entry()
        self._style_scale()
        self._style_listbox()
        self._style_spinbox()
        self._style_menu()
        self._style_menubutton()
        self._style_labelframe()
        self._style_scrollbar()
        self._style_optionmenu()

    def _set_option(self, *args):
        """
        A convenience method to shorten the call to ``option_add``. *Laziness is next to godliness*.
        """
        self.master.option_add(*args)

    def _style_window(self):
        """
        Apply global options to all matching ``tkinter`` widgets
        """
        self.master.configure(background=self.settings.colors.bg)
        self._set_option('*background', self.settings.colors.bg, 20)
        self._set_option('*font', 'Helvetica', 20)
        self._set_option('*borderWidth', 0, 20)
        self._set_option('*relief', 'flat', 20)
        self._set_option('*activeBackground', self.settings.colors.selectbg, 20)
        self._set_option('*activeForeground', self.settings.colors.selectfg, 20)
        self._set_option('*selectBackground', self.settings.colors.selectbg, 20)
        self._set_option('*selectForeground', self.settings.colors.selectfg, 20)

    def _style_button(self):
        """
        Apply style to ``tkinter.Button``
        """
        self._set_option('*Button.foreground', self.settings.colors.selectfg)
        self._set_option('*Button.background', self.settings.colors.primary)

    def _style_label(self):
        """
        Apply style to ``tkinter.Label``
        """
        self._set_option('*Label.foreground', self.settings.colors.fg)
        self._set_option('*Label.background', self.settings.colors.bg)

    def _style_checkbutton(self):
        """
        Apply style to ``tkinter.Checkbutton``
        """
        self._set_option('*Checkbutton.background', self.settings.colors.bg)
        self._set_option('*Checkbutton.foreground', self.settings.colors.fg)
        self._set_option('*Checkbutton.selectColor',
                         self.settings.colors.primary if self.settings.type == 'dark' else 'white')

    def _style_radiobutton(self):
        """
        Apply style to ``tkinter.Radiobutton``
        """
        self._set_option('*Radiobutton.background', self.settings.colors.bg)
        self._set_option('*Radiobutton.foreground', self.settings.colors.fg)
        self._set_option('*Radiobutton.selectColor',
                         self.settings.colors.primary if self.settings.type == 'dark' else 'white')

    def _style_entry(self):
        """
        Apply style to ``tkinter.Entry``
        """
        self._set_option('*Entry.relief', 'flat')
        self._set_option('*Entry.background',
                         (self.settings.colors.light if self.settings.type == 'light' else
                          Colors.brightness(self.settings.colors.light, -0.1)))
        self._set_option('*Entry.foreground', self.settings.colors.fg)
        self._set_option('*Entry.highlightThickness', 1)
        self._set_option('*Entry.highlightBackground', self.settings.colors.border)
        self._set_option('*Entry.highlightColor', self.settings.colors.primary)

    def _style_scale(self):
        """
        Apply style to ``tkinter.Scale``
        """
        self._set_option('*Scale.background', self.settings.colors.primary)
        self._set_option('*Scale.showValue', False)
        self._set_option('*Scale.sliderRelief', 'flat')
        self._set_option('*Scale.highlightThickness', 1)
        self._set_option('*Scale.highlightColor', self.settings.colors.primary)
        self._set_option('*Scale.highlightBackground', self.settings.colors.border)
        self._set_option('*Scale.troughColor',
                         (self.settings.colors.light if self.settings.type == 'light' else
                          Colors.brightness(self.settings.colors.light, -0.1)))

    def _style_spinbox(self):
        """
        Apply style to `tkinter.Spinbox``
        """
        self._set_option('*Spinbox.foreground', self.settings.colors.fg)
        self._set_option('*Spinbox.background',
                         (self.settings.colors.light if self.settings.type == 'light' else
                          Colors.brightness(self.settings.colors.light, -0.1)))
        self._set_option('*Spinbox.highlightThickness', 1)
        self._set_option('*Spinbox.highlightColor', self.settings.colors.primary)
        self._set_option('*Spinbox.highlightBackground', self.settings.colors.border)

    def _style_listbox(self):
        """
        Apply style to ``tkinter.Listbox``
        """
        self._set_option('*Listbox.foreground', self.settings.colors.fg)
        self._set_option('*Listbox.background',
                         (self.settings.colors.light if self.settings.type == 'light' else
                          Colors.brightness(self.settings.colors.light, -0.1)))
        self._set_option('*Listbox.relief', 'flat')
        self._set_option('*Listbox.activeStyle', 'none')
        self._set_option('*Listbox.highlightThickness', 1)
        self._set_option('*Listbox.highlightColor', self.settings.colors.primary)
        self._set_option('*Listbox.highlightBackground', self.settings.colors.border)

    def _style_menubutton(self):
        """
        Apply style to ``tkinter.Menubutton``
        """
        self._set_option('*Menubutton.background', self.settings.colors.primary)
        self._set_option('*Menubutton.foreground', self.settings.colors.selectfg)

    def _style_menu(self):
        """
        Apply style to ``tkinter.Menu``
        """
        self._set_option('*Menu.tearOff', 0)
        self._set_option('*Menu.foreground', self.settings.colors.fg)
        self._set_option('*Menu.selectColor', self.settings.colors.primary)

    def _style_labelframe(self):
        """
        Apply style to ``tkinter.Labelframe``
        """
        self._set_option('*Labelframe.foreground', self.settings.colors.fg)
        self._set_option('*Labelframe.highlightColor', self.settings.colors.border)
        self._set_option('*Labelframe.highlightBackground', self.settings.colors.border)
        self._set_option('*Labelframe.highlightThickness', 1)

    def _style_scrollbar(self):
        """
        Apply style to ``tkinter.Scrollbar``

        .. warning::
            It appears this widget can only be styled in the constructor**
        """

        pass

    def _style_optionmenu(self):
        """
        Apply style to ``tkinter.OptionMenu``

        .. warning::
            It appears this widget can only be styled in the constructor
        """
        pass

    def _style_separator(self):
        """
        Apply style to ``tkinter.Separator``

        .. warning::
            Not implemented
        """
        pass


class StylerTTK:
    """
    A class to create a new ttk theme by using a combination of built-in themes and some image-based elements using
    ``pillow``. A theme is generated at runtime and is available to use with the ``Style`` class methods.
    The base theme of all ttkbootstrap themes is *clam*. In many cases, widget layouts are re-created using an
    assortment of elements from various styles such as *clam*, *alt*, *default*, etc...

    :param Style style: An instance of ``ttk.Style`` class
    :param ThemeSettings settings: creates the settings for the theme to be created
    """

    def __init__(self, style, settings):
        self.style = style
        self.settings = settings
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """
        Create and style a new ttk theme. A wrapper around internal style methods.
        """
        self.style.theme_create(self.settings.name, 'clam')
        self.style.theme_use(self.settings.name)
        self._style_defaults()
        self._style_spinbox()
        self._style_scale()
        self._style_scrollbar()
        self._style_combobox()
        self._style_frame()
        self._style_checkbutton()
        self._style_entry()
        self._style_label()
        self._style_labelframe()
        self._style_notebook()
        self._style_outline_buttons()
        self._style_outline_menubutton()
        self._style_progressbar()
        self._style_radiobutton()
        self._style_solid_buttons()
        self._style_solid_menubutton()
        self._style_treeview()
        self._style_separator()
        self._style_panedwindow()

    def _style_defaults(self):
        """
        Setup the default ``ttk.Style`` configuration. These defaults are applied to any widget that contains these
        element options. This method should be called *first* before any other style is applied during theme creation.
        """
        self.style.configure('.',
                             background=self.settings.colors.bg,
                             darkcolor=self.settings.colors.border,
                             lightcolor=self.settings.colors.border,
                             foreground=self.settings.colors.fg,
                             troughcolor=self.settings.colors.bg,
                             selectbg=self.settings.colors.selectbg,
                             selectfg=self.settings.colors.selectfg,
                             selectforeground=self.settings.colors.selectfg,
                             selectbackground=self.settings.colors.selectbg,
                             fieldbg='white',
                             font=(self.settings.font,),
                             borderwidth=1,
                             focuscolor='')

    def _style_combobox(self):
        """
        Apply style to ``ttk.Combobox``. This element style is created with a layout that combines *clam* and *default*
        theme elements.

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
        self.style.layout('TCombobox', [('combo.Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
            ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}),
            ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                ('Combobox.textarea', {'sticky': 'nswe'})]})]})])

        if self.settings.type == 'dark':
            self.style.element_create('combo.Spinbox.field', 'from', 'default')

        self.style.element_create('Combobox.downarrow', 'from', 'default')
        self.style.element_create('Combobox.padding', 'from', 'clam')
        self.style.element_create('Combobox.textarea', 'from', 'clam')
        self.style.configure('TCombobox',
                             bordercolor=self.settings.colors.border,
                             darkcolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.bg,
                             arrowcolor=self.settings.colors.inputfg,
                             foreground=self.settings.colors.inputfg,
                             fieldbackground=self.settings.colors.light,
                             background=self.settings.colors.light,
                             relief='flat',
                             borderwidth=0,
                             padding=5,
                             arrowsize=16)
        self.style.map('TCombobox',
                       bordercolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.bg)],
                       lightcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       darkcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       arrowcolor=[
                           ('pressed', self.settings.colors.light),
                           ('focus', self.settings.colors.inputfg),
                           ('hover', self.settings.colors.primary)])

        for color in self.settings.colors:
            self.style.map(f'{color}.TCombobox',
                           bordercolor=[
                               ('focus', self.settings.colors.get(color)),
                               ('hover', self.settings.colors.get(color))],
                           lightcolor=[
                               ('focus', self.settings.colors.get(color)),
                               ('pressed', self.settings.colors.get(color))],
                           darkcolor=[
                               ('focus', self.settings.colors.get(color)),
                               ('pressed', self.settings.colors.get(color))],
                           arrowcolor=[
                               ('pressed', self.settings.colors.light),
                               ('focus', self.settings.colors.inputfg),
                               ('hover', self.settings.colors.primary)])

    def _style_separator(self):
        """
        Apply style to ttk separator: *ttk.Separator*. The default style for light will be border, but dark will be
        primary, as this makes the most sense for general use. However, all other colors will be available as well
        through styling.

        The options avaiable in this widget include:

            - Separator.separator: orient, background
        """
        self.style.configure('Horizontal.TSeparator',
                             background=(self.settings.colors.border
                                         if self.settings.type == 'light'
                                         else self.settings.colors.primary))

        self.style.configure('Vertical.TSeparator',
                             background=(self.settings.colors.border
                                         if self.settings.type == 'light'
                                         else self.settings.colors.primary))

        for color in self.settings.colors:
            self.style.configure(f'{color}.Horizontal.TSeparator', background=self.settings.colors.get(color))
            self.style.configure(f'{color}.Vertical.TSeparator', background=self.settings.colors.get(color))

    def _style_progressbar(self):
        """
        Apply style to ttk progressbar: *ttk.Progressbar*

        The options available in this widget include:

            - Progressbar.trough: borderwidth, troughcolor, troughrelief
            - Progressbar.pbar: orient, thickness, barsize, pbarrelief, borderwidth, background

        """
        self.style.element_create('Progressbar.trough', 'from', 'default')
        self.style.element_create('Progressbar.pbar', 'from', 'default')

        self.style.configure('TProgressbar',
                             thickness=20,
                             borderwidth=0,
                             troughcolor=Colors.brightness(self.settings.colors.light, -0.05),
                             background=self.settings.colors.primary)

        for color in self.settings.colors:
            self.style.configure(f'{color}.Horizontal.TProgressbar', background=self.settings.colors.get(color))
            self.style.configure(f'{color}.Vertical.TProgressbar', background=self.settings.colors.get(color))

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
        Apply style to ttk scale: *ttk.Scale*

        The options available in this widget include:

            - Scale.trough: borderwidth, troughcolor, troughrelief
            - Scale.slider: sliderlength, sliderthickness, sliderrelief, borderwidth, background, bordercolor, orient
        """
        self.style.layout('Horizontal.TScale', [
            ('Scale.focus', {'expand': '1', 'sticky': 'nswe', 'children': [
                ('Horizontal.Scale.track', {'sticky': 'we'}),
                ('Horizontal.Scale.slider', {'side': 'left', 'sticky': ''})]})])

        self.style.layout('Vertical.TScale', [
            ('Scale.focus', {'expand': '1', 'sticky': 'nswe', 'children': [
                ('Vertical.Scale.track', {'sticky': 'we'}),
                ('Vertical.Scale.slider', {'side': 'left', 'sticky': ''})]})])

        # create widget images
        self.scale_images = {}
        self.scale_images['primary_regular'] = self._create_slider_image(self.settings.colors.primary)
        self.scale_images['primary_pressed'] = self._create_slider_image(
            Colors.brightness(self.settings.colors.primary, -0.2))
        self.scale_images['primary_hover'] = self._create_slider_image(
            Colors.brightness(self.settings.colors.primary, -0.1))
        self.scale_images['trough'] = ImageTk.PhotoImage(
            Image.new('RGB', (8, 8), Colors.brightness(self.settings.colors.light, -0.05)))

        # create new elements based on images
        self.style.element_create('Scale.track', 'image', self.scale_images['trough'])
        self.style.element_create('Scale.slider', 'image', self.scale_images['primary_regular'],
                                  ('pressed', self.scale_images['primary_pressed']),
                                  ('hover', self.scale_images['primary_hover']))

    def _style_scrollbar(self):
        """
        Apply style to ttk scrollbar: *ttk.Scrollbar*. This theme uses elements from the *alt* theme to build the
        widget layout.

        The options available in this widget include:

            - Scrollbar.trough: orient, troughborderwidth, troughcolor, troughrelief, groovewidth
            - Scrollbar.uparrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Scrollbar.thumb: width, background, bordercolor, relief, orient
        """
        self.style.element_create('Vertical.Scrollbar.trough', 'from', 'alt')
        self.style.element_create('Vertical.Scrollbar.thumb', 'from', 'alt')
        self.style.element_create('Vertical.Scrollbar.uparrow', 'from', 'alt')
        self.style.element_create('Vertical.Scrollbar.downarrow', 'from', 'alt')
        self.style.element_create('Horizontal.Scrollbar.trough', 'from', 'alt')
        self.style.element_create('Horizontal.Scrollbar.thumb', 'from', 'alt')
        self.style.element_create('Horizontal.Scrollbar.uparrow', 'from', 'alt')
        self.style.element_create('Horizontal.Scrollbar.downarrow', 'from', 'alt')

        self.style.configure('TScrollbar',
                             troughrelief='flat',
                             relief='flat',
                             troughborderwidth=2,
                             troughcolor=self.settings.colors.light,
                             background=Colors.brightness(self.settings.colors.light, -0.1),
                             arrowsize=16,
                             arrowcolor=self.settings.colors.inputfg)

    def _style_spinbox(self):
        """
        Apply style to ttk spinbox: *ttk.Spinbox*

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
        self.style.layout('TSpinbox', [
            ('custom.Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
                ('null', {'side': 'right', 'sticky': '', 'children': [
                    ('Spinbox.uparrow', {'side': 'top', 'sticky': 'e'}),
                    ('Spinbox.downarrow', {'side': 'bottom', 'sticky': 'e'})]}),
                ('Spinbox.padding', {'sticky': 'nswe', 'children': [
                    ('Spinbox.textarea', {'sticky': 'nswe'})]})]})])

        self.style.element_create('Spinbox.uparrow', 'from', 'default')
        self.style.element_create('Spinbox.downarrow', 'from', 'default')
        if self.settings.type == 'dark':
            self.style.element_create('custom.Spinbox.field', 'from', 'default')

        self.style.configure('TSpinbox',
                             fieldbackground=self.settings.colors.light,
                             bordercolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.border,
                             darkcolor=self.settings.colors.border,
                             foreground=self.settings.colors.inputfg,
                             borderwidth=0,
                             background=self.settings.colors.light,
                             relief='flat',
                             arrowcolor=self.settings.colors.inputfg,
                             arrowsize=16,
                             padding=(10, 5))

        self.style.map('TSpinbox',
                       bordercolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.bg)],
                       lightcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       darkcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       arrowcolor=[
                           ('pressed', self.settings.colors.primary),
                           ('focus', self.settings.colors.inputfg),
                           ('hover', self.settings.colors.inputfg)])

        for color in self.settings.colors:
            self.style.map(f'{color}.TSpinbox',
                           bordercolor=[
                               ('focus', self.settings.colors.get(color)),
                               ('hover', self.settings.colors.get(color))],
                           arrowcolor=[
                               ('pressed', self.settings.colors.get(color)),
                               ('pressed', self.settings.colors.inputfg),
                               ('hover', self.settings.colors.inputfg)],
                           lightcolor=[('focus', self.settings.colors.get(color))],
                           darkcolor=[('focus', self.settings.colors.get(color))])

    def _style_treeview(self):
        """
        Apply style to ttk treeview: *ttk.Treeview*. This widget uses elements from the *alt* and *clam* theme to
        create the widget layout.

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
        self.style.element_create('Treeitem.indicator', 'from', 'alt')

        self.style.layout('Treeview', [
            ('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [
                ('Treeview.padding', {'sticky': 'nswe', 'children': [
                    ('Treeview.treearea', {'sticky': 'nswe'})]})]})])

        self.style.configure('Treeview',
                             background=self.settings.colors.light,
                             foreground=self.settings.colors.inputfg,
                             bordercolor=self.settings.colors.border,
                             lightcolor=self.settings.colors.bg,
                             darkcolor=self.settings.colors.bg,
                             relief='raised' if self.settings.type == 'light' else 'flat',

                             # border showing through on dark theme... so pulling in the border with -2 padding
                             padding=-1 if self.settings.type == 'light' else -2)

        self.style.map('Treeview',
                       background=[('selected', self.settings.colors.selectbg)],
                       foreground=[('selected', self.settings.colors.selectfg)],
                       bordercolor=[('focus', self.settings.colors.border)])

        self.style.configure('Treeview.Heading',
                             background=self.settings.colors.primary,
                             foreground=self.settings.colors.selectfg,
                             relief='flat',
                             padding=5)

        for color in self.settings.colors:
            self.style.configure(f'{color}.Treeview.Heading', background=self.settings.colors.get(color))
            self.style.map(f'{color}.Treeview', bordercolor=[('focus', self.settings.colors.get(color))])

    def _style_frame(self):
        """
        Apply style to ttk frame: *ttk.Frame*

        The options available in this widget include:

            - Frame.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
        """
        self.style.configure('TFrame',
                             background=self.settings.colors.bg)

        for color in self.settings.colors:
            self.style.configure(f'{color}.TFrame', background=self.settings.colors.get(color))

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
        self.style.configure('TButton',
                             foreground=self.settings.colors.selectfg,
                             background=self.settings.colors.primary,
                             bordercolor=self.settings.colors.primary,
                             darkcolor=self.settings.colors.primary,
                             lightcolor=self.settings.colors.primary,
                             anchor='center',
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TButton',
                       background=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))])

        for color in self.settings.colors:
            self.style.configure(f'{color}.TButton',
                                 foreground=self.settings.colors.selectfg,
                                 background=self.settings.colors.get(color),
                                 bordercolor=self.settings.colors.get(color),
                                 darkcolor=self.settings.colors.get(color),
                                 lightcolor=self.settings.colors.get(color),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{color}.TButton',
                           background=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))])

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
        self.style.configure('Outline.TButton',
                             foreground=self.settings.colors.primary,
                             background=self.settings.colors.bg,
                             bordercolor=self.settings.colors.primary,
                             darkcolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.bg,
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TButton',
                       foreground=[
                           ('pressed', self.settings.colors.selectfg),
                           ('hover', self.settings.colors.selectfg)],
                       background=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))])

        for color in self.settings.colors:
            self.style.configure(f'{color}.Outline.TButton',
                                 foreground=self.settings.colors.get(color),
                                 background=self.settings.colors.bg,
                                 bordercolor=self.settings.colors.get(color),
                                 darkcolor=self.settings.colors.bg,
                                 lightcolor=self.settings.colors.bg,
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{color}.Outline.TButton',
                           foreground=[
                               ('pressed', self.settings.colors.selectfg),
                               ('hover', self.settings.colors.selectfg)],
                           background=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))])

    def _style_entry(self):
        """
        Apply style to ttk entry: *ttk.Entry*

        The options available in this widget include:

            - Entry.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Entry.padding: padding, relief, shiftrelief
            - Entry.textarea: font, width
        """
        self.style.configure('TEntry',
                             fieldbackground=self.settings.colors.light,
                             bordercolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.border,
                             darkcolor=self.settings.colors.border,
                             foreground=self.settings.colors.inputfg,
                             padding=5)

        self.style.map('TEntry',
                       bordercolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.bg)],
                       lightcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       darkcolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)])

        for color in self.settings.colors:
            self.style.map(f'{color}.TEntry',
                           bordercolor=[('focus', self.settings.colors.get(color))],
                           lightcolor=[('focus', self.settings.colors.get(color))],
                           darkcolor=[('focus', self.settings.colors.get(color))])

    def _style_radiobutton(self):
        """
        Apply style to ttk radiobutton: *ttk.Radiobutton*

        The options available in this widget include:

            - Radiobutton.padding: padding, relief, shiftrelief
            - Radiobutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground,
                upperbordercolor, lowerbordercolor
            - Radiobutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background

        **NOTE:**

            On Windows, the button defaults to the 'xpnative' theme look. This means that you cannot change the look
            and feel with styles. On Linux and MacOS, defaults to stylized 'clam' theme, so the style can be changed.
        """
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Radiobutton.indicator', 'from', 'xpnative')

        self.style.configure('TRadiobutton',
                             indicatormargin=8,
                             indicatorsize=12,
                             upperbordercolor=(self.settings.colors.fg
                                               if self.settings.type == 'light'
                                               else self.settings.colors.light),
                             lowerbordercolor=(self.settings.colors.fg
                                               if self.settings.type == 'light'
                                               else self.settings.colors.light),
                             indicatorforeground=(self.settings.colors.fg
                                                  if self.settings.type == 'light'
                                                  else self.settings.colors.bg))

        self.style.map('TRadiobutton',
                       foreground=[('active', self.settings.colors.primary)],
                       indicatorforeground=[
                           ('active', self.settings.colors.primary if (self.settings.type == 'light') else 'black')])

        # variations change the indicator color
        for color in self.settings.colors:
            self.style.map(f'{color}.TRadiobutton',
                           foreground=[('active', Colors.brightness(self.settings.colors.get(color), -0.2))],
                           indicatorforeground=[('active', Colors.brightness(self.settings.colors.get(color), -0.2))])

    def _style_label(self):
        """
        Apply style to ttk label: *ttk.Label*

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.style.configure('TLabel', foreground=self.settings.colors.fg)
        for color in self.settings.colors:
            self.style.configure(f'{color}.TLabel', foreground=self.settings.colors.get(color))

    def _style_labelframe(self):
        """
        Apply style to ttk labelframe: *ttk.LabelFrame*

        The options available in this widget include:

            - Labelframe.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.fill: background
            - Label.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed
        """
        self.style.configure('TLabelframe',
                             padding=(10, 5),
                             foreground=self.settings.colors.fg,
                             relief='raised',
                             bordercolor=self.settings.colors.border,
                             darkcolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.bg)

        self.style.configure('TLabelframe.Label', foreground=self.settings.colors.fg)

        for color in self.settings.colors:
            self.style.configure(f'{color}.TLabelframe',
                                 foreground=self.settings.colors.get(color),
                                 bordercolor=self.settings.colors.get(color))

            self.style.configure(f'{color}.TLabelframe.Label', foreground=self.settings.colors.get(color))

    def _style_checkbutton(self):
        """
        Apply style to ttk checkbutton: *ttk.Checkbutton*

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
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Checkbutton.indicator', 'from', 'xpnative')

        self.style.configure('TCheckbutton',
                             foreground=self.settings.colors.fg,
                             indicatorsize=10,
                             indicatormargin=10,
                             indicatorforeground=self.settings.colors.selectfg)

        self.style.map('TCheckbutton',
                       indicatorbackground=[
                           ('active selected', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('selected', self.settings.colors.fg),
                           ('active !selected', self.settings.colors.light)],
                       foreground=[('active', self.settings.colors.primary)])

        # variations change indicator color
        for color in self.settings.colors:
            self.style.map(f'{color}.TCheckbutton',
                           indicatorbackground=[
                               ('active selected', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('selected', self.settings.colors.fg),
                               ('active !selected', self.settings.colors.light)],
                           indicatorforeground=[
                               ('active selected', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('selected', self.settings.colors.get(color))],
                           foreground=[
                               ('active', Colors.brightness(self.settings.colors.get(color), -0.2))])

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
        self.style.configure('TMenubutton',
                             foreground=self.settings.colors.selectfg,
                             background=self.settings.colors.primary,
                             bordercolor=self.settings.colors.primary,
                             darkcolor=self.settings.colors.primary,
                             lightcolor=self.settings.colors.primary,
                             arrowcolor=self.settings.colors.bg if self.settings.type == 'light' else 'white',
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TMenubutton',
                       background=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))])

        for color in self.settings.colors:
            self.style.configure(f'{color}.TMenubutton',
                                 foreground=self.settings.colors.selectfg,
                                 background=self.settings.colors.get(color),
                                 bordercolor=self.settings.colors.get(color),
                                 darkcolor=self.settings.colors.get(color),
                                 lightcolor=self.settings.colors.get(color),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{color}.TMenubutton',
                           background=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))])

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
        self.style.configure('Outline.TMenubutton',
                             foreground=self.settings.colors.primary,
                             background=self.settings.colors.bg,
                             bordercolor=self.settings.colors.primary,
                             darkcolor=self.settings.colors.bg,
                             lightcolor=self.settings.colors.bg,
                             arrowcolor=self.settings.colors.primary,
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TMenubutton',
                       foreground=[
                           ('pressed', self.settings.colors.selectfg),
                           ('hover', self.settings.colors.selectfg)],
                       background=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', Colors.brightness(self.settings.colors.primary, -0.2)),
                           ('hover', Colors.brightness(self.settings.colors.primary, -0.1))],
                       arrowcolor=[
                           ('pressed', self.settings.colors.selectfg),
                           ('hover', self.settings.colors.selectfg)])

        for color in self.settings.colors:
            self.style.configure(f'{color}.Outline.TMenubutton',
                                 foreground=self.settings.colors.get(color),
                                 background=self.settings.colors.bg,
                                 bordercolor=self.settings.colors.get(color),
                                 darkcolor=self.settings.colors.bg,
                                 lightcolor=self.settings.colors.bg,
                                 arrowcolor=self.settings.colors.get(color),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{color}.Outline.TMenubutton',
                           foreground=[
                               ('pressed', self.settings.colors.fg),
                               ('hover', self.settings.colors.fg)],
                           background=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', Colors.brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', Colors.brightness(self.settings.colors.get(color), -0.1))],
                           arrowcolor=[
                               ('pressed', self.settings.colors.bg),
                               ('hover', self.settings.colors.bg)])

    def _style_notebook(self):
        """
        Apply style to ttk notebook: *ttk.Notebook*

        The options available in this widget include:

            - Notebook.client: background, bordercolor, lightcolor, darkcolor
            - Notebook.tab: background, bordercolor, lightcolor, darkcolor
            - Notebook.padding: padding, relief, shiftrelief
            - Notebook.focus: focuscolor, focusthickness
            - Notebook.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.style.configure('TNotebook',
                             bordercolor=self.settings.colors.border,
                             borderwidth=1)

        self.style.configure('TNotebook.Tab',
                             bordercolor=self.settings.colors.border,
                             foreground=self.settings.colors.fg,
                             padding=(10, 5))

        self.style.map('TNotebook.Tab',
                       background=[('!selected', self.settings.colors.light)],
                       lightcolor=[('!selected', self.settings.colors.light)],
                       darkcolor=[('!selected', self.settings.colors.light)],
                       bordercolor=[('!selected', self.settings.colors.border)],
                       foreground=[('!selected', self.settings.colors.inputfg)])

    def _style_panedwindow(self):
        """
        Apply style to ttk paned window: *ttk.PanedWindow*

        The options available in this widget include:

            Paned Window:

                - Panedwindow.background: background

            Sash:

                - Sash.hsash: sashthickness
                - Sash.hgrip: lightcolor, bordercolor, gripcount
                - Sash.vsash: sashthickness
                - Sash.vgrip: lightcolor, bordercolor, gripcount
        """
        self.style.configure('TPanedwindow', background=Colors.brightness(self.settings.colors.light, -0.1))
        self.style.configure('Sash', bordercolor=self.settings.colors.inputfg, lightcolor=self.settings.colors.light,
                             sashthickness=9, sashpad=0, gripcount=25)

    def _style_sizegroup(self):
        """
        Apply style to ttk sizegrip: *ttk.Sizegrip*

        The options available in this widget include:

            - Sizegrip.sizegrip: background

        **NOT IMPLEMENTED as existing styles are already covering this.**
        """
        pass
