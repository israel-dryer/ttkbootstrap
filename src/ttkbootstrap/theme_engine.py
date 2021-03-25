import json
import colorsys
from pathlib import Path
import importlib.resources
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw


def hex_to_rgb(color):
    """Convert hexadecimal to rgb color representation"""
    r = round(int(color[1:3], 16) / 255, 2)
    g = round(int(color[3:5], 16) / 255, 2)
    b = round(int(color[5:], 16) / 255, 2)
    return r, g, b


def rgb_to_hex(r, g, b):
    """Convert rgb to hexadecimal color representation"""
    r_ = int(r * 255)
    g_ = int(g * 255)
    b_ = int(b * 255)
    return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)


def brightness(hex_color, pct_change):
    """Adjust the value of a given hexadecimal color. The percent change is expected to be a float. Example: 0.15
    is a 15 percent increase in brightness, whereas -0.15 is a 15 percent decrease in brightness"""
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    v_ = (1 + pct_change) * v
    v_max = max(0, v_)
    v_min = min(1, v_max)
    r_, g_, b_ = colorsys.hsv_to_rgb(h, s, v_min)
    return rgb_to_hex(r_, g_, b_)


class BootStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.themes = {}
        self.load_izzy_themes()
        self.settings = None

    def load_izzy_themes(self):
        """Load all izzy defined themes"""
        json_data = importlib.resources.read_text('ttkbootstrap', 'themes.json')
        settings = json.loads(json_data)
        for theme in settings['themes']:
            settings = ThemeSettings(
                name=theme['name'],
                type=theme['type'],
                font=theme['font'],
                colors=Colors(**theme['colors']))
            self.themes[settings.name] = StylerTTK(self, settings)

    def theme_use(self, themename=None):
        """If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a <<ThemeChanged>> event."""
        if themename is None:
            # Starting on Tk 8.6, checking this global is no longer needed
            # since it allows doing self.tk.call(self._name, "theme", "use")
            return self.tk.eval("return $ttk::currentTheme")

        try:
            current_theme = self.themes.get(themename)
            current_theme.styler_tk.apply_style()
            self.settings = current_theme.settings
        except AttributeError:
            pass

        # using "ttk::setTheme" instead of "ttk::style theme use" causes
        # the variable currentTheme to be updated, also, ttk::setTheme calls
        # "ttk::style theme use" in order to change theme.
        self.tk.call("ttk::setTheme", themename)

    def theme_names(self):
        """Return a sorted list of available themes"""
        return sorted(super().theme_names())


class ThemeSettings:
    """Settings for a ttkbootstrap theme.

    Attributes:
        name: The name of the theme
        type: 'light' or 'dark'
        font: Default font to apply to theme. Helvetica is used by default.
        colors: An instance of the `Colors` class.
    """

    def __init__(self, name='default', type='light', font='helvetica', colors=None):
        self.name = name
        self.type = 'light'
        self.font = font
        self.colors = colors if colors else Colors()

    def __repr__(self):
        return f'name={self.name}, type={self.type}, font={self.font}, colors={self.colors}'


class Colors:
    """A collection of colors used in a ttkbootstrap theme.

    Attributes:
        primary, secondary, success, info, warning, danger, bg, fg, selectfg, selectbg, light, border, inputfg
    """

    def __init__(self, **kwargs):
        self.primary = kwargs.get('primary', 'gray10')
        self.secondary = kwargs.get('secondary', 'gray60')
        self.success = kwargs.get('success', 'DarkSlateGray3')
        self.info = kwargs.get('info', 'SkyBlue1')
        self.warning = kwargs.get('warning', 'Gold2')
        self.danger = kwargs.get('danger', 'brown1')
        self.bg = kwargs.get('bg', 'white')
        self.fg = kwargs.get('fg', 'black')
        self.selectbg = kwargs.get('selectbg', 'gray60')
        self.selectfg = kwargs.get('selectfg', 'white')
        self.light = kwargs.get('light', 'snow2')
        self.border = kwargs.get('border', 'gray64')
        self.inputfg = kwargs.get('inputfg', 'black')

    def get(self, color):
        """Accepts a color name and returns the color value"""
        return self.__dict__.get(color)

    def __iter__(self):
        return iter(['primary', 'secondary', 'success', 'info', 'warning', 'danger'])

    def __repr__(self):
        return str((tuple(zip(self.__dict__.keys(), self.__dict__.values()))))


class StylerTK:
    """A flat theme applied to standard tkinter widgets (THESE ARE NOT TTK WIDGETS).

    This can be used independent of the Themed TTK widgets, but it is primary designed to supplement the few widgets
    that are used in conjunction with the TTK widgets. So, please be aware that standard tkinter widgets may not have
    the desired look.

    Attributes:
        parent: an instance of `StylerTTK`
    """

    def __init__(self, parent):
        self.master = parent.style.master
        self.settings = parent.settings

    def set_option(self, *args):
        """A convenience method to shorten the call to `option_add`"""
        self.master.option_add(*args)

    def apply_style(self):
        """A wrapper on all widget style methods. Applies current theme to all standard tkinter widgets (NOT TTK)"""
        self.style_window()
        self.style_button()
        self.style_label()
        self.style_checkbutton()
        self.style_radiobutton()
        self.style_entry()
        self.style_scale()
        self.style_listbox()
        self.style_spinbox()
        self.style_menu()
        self.style_menubutton()
        self.style_labelframe()
        self.style_scrollbar()
        self.style_optionmenu()

    def style_window(self):
        """Apply global options to all matching tkinter widgets"""
        self.set_option('*background', self.settings.colors.bg)
        self.set_option('*font', 'Helvetica')
        self.set_option('*borderWidth', 0)
        self.set_option('*relief', 'flat')
        self.set_option('*activeBackground', self.settings.colors.selectbg)
        self.set_option('*activeForeground', self.settings.colors.selectfg)
        self.set_option('*selectBackground', self.settings.colors.selectbg)
        self.set_option('*selectForeground', self.settings.colors.selectfg)

    def style_button(self):
        """Apply style to tkinter button: `tkinter.Button`"""
        self.set_option('*Button.foreground', self.settings.colors.selectfg)
        self.set_option('*Button.background', self.settings.colors.primary)

    def style_label(self):
        """Apply style to tkinter label: `tkinter.Label`"""
        self.set_option('*Label.foreground', self.settings.colors.fg)
        self.set_option('*Label.background', self.settings.colors.bg)

    def style_checkbutton(self):
        """Apply style to tkinter checkbutton: `tkinter.Checkbutton`"""
        self.set_option('*Checkbutton.background', self.settings.colors.bg)
        self.set_option('*Checkbutton.foreground', self.settings.colors.fg)
        self.set_option('*Checkbutton.selectColor',
                        self.settings.colors.primary if self.settings.type == 'dark' else 'white')

    def style_radiobutton(self):
        """Apply style to tkinter radiobutton: `tkinter.Radiobutton`"""
        self.set_option('*Radiobutton.background', self.settings.colors.bg)
        self.set_option('*Radiobutton.foreground', self.settings.colors.fg)
        self.set_option('*Radiobutton.selectColor',
                        self.settings.colors.primary if self.settings.type == 'dark' else 'white')

    def style_entry(self):
        """Apply style to tkinter entry: `tkinter.Entry`"""
        self.set_option('*Entry.relief', 'flat')
        self.set_option('*Entry.background',
                        (self.settings.colors.light if self.settings.type == 'light' else
                         brightness(self.settings.colors.light, -0.1)))
        self.set_option('*Entry.foreground', self.settings.colors.fg)
        self.set_option('*Entry.highlightThickness', 1)
        self.set_option('*Entry.highlightBackground', self.settings.colors.border)
        self.set_option('*Entry.highlightColor', self.settings.colors.primary)

    def style_scale(self):
        """Apply style to tkinter scale: `tkinter.Scale`"""
        self.set_option('*Scale.background', self.settings.colors.primary)
        self.set_option('*Scale.showValue', False)
        self.set_option('*Scale.sliderRelief', 'flat')
        self.set_option('*Scale.highlightThickness', 1)
        self.set_option('*Scale.highlightColor', self.settings.colors.primary)
        self.set_option('*Scale.highlightBackground', self.settings.colors.border)
        self.set_option('*Scale.troughColor',
                        (self.settings.colors.light if self.settings.type == 'light' else
                         brightness(self.settings.colors.light, -0.1)))

    def style_spinbox(self):
        """Apply style to tkinter spinbox: `tkinter.Spinbox`"""
        self.set_option('*Spinbox.foreground', self.settings.colors.fg)
        self.set_option('*Spinbox.background',
                        (self.settings.colors.light if self.settings.type == 'light' else
                         brightness(self.settings.colors.light, -0.1)))
        self.set_option('*Spinbox.highlightThickness', 1)
        self.set_option('*Spinbox.highlightColor', self.settings.colors.primary)
        self.set_option('*Spinbox.highlightBackground', self.settings.colors.border)

    def style_listbox(self):
        """Apply style to tkinter listbox: `tkinter.Listbox`"""
        self.set_option('*Listbox.foreground', self.settings.colors.fg)
        self.set_option('*Listbox.background',
                        (self.settings.colors.light if self.settings.type == 'light' else
                         brightness(self.settings.colors.light, -0.1)))
        self.set_option('*Listbox.relief', 'flat')
        self.set_option('*Listbox.activeStyle', 'none')
        self.set_option('*Listbox.highlightThickness', 1)
        self.set_option('*Listbox.highlightColor', self.settings.colors.primary)
        self.set_option('*Listbox.highlightBackground', self.settings.colors.border)

    def style_menubutton(self):
        """Apply style to tkinter menubutton: `tkinter.Menubutton`"""
        self.set_option('*Menubutton.background', self.settings.colors.primary)
        self.set_option('*Menubutton.foreground', self.settings.colors.selectfg)

    def style_menu(self):
        """Apply style to tkinter menu: `tkinter.Menu`"""
        self.set_option('*Menu.tearOff', 0)
        self.set_option('*Menu.foreground', self.settings.colors.fg)
        self.set_option('*Menu.selectColor', self.settings.colors.primary)

    def style_labelframe(self):
        """Apply style to tkinter labelframe: `tkinter.Labelframe`"""
        self.set_option('*Labelframe.foreground', self.settings.colors.fg)
        self.set_option('*Labelframe.highlightColor', self.settings.colors.border)
        self.set_option('*Labelframe.highlightBackground', self.settings.colors.border)
        self.set_option('*Labelframe.highlightThickness', 1)

    def style_scrollbar(self):
        """Apply style to tkinter scrollbar: `tkinter.Scrollbar`"""
        # It does not appear to be possible to style the scrollbar on windows
        pass

    def style_optionmenu(self):
        """Apply style to tkinter option menu: `tkinter.OptionMenu`"""
        # The widget constructor rejects all keyword arguments, so it cannot be set with options, only with
        # configuration after the widget has been created.
        pass


class StylerTTK:
    """A flat TTK theme created with built-in elements and a supplied color scheme.

    Attributes:
        style: An instance of the `ttk.Style` class
        settings: An instance of the `ThemeSettings` class
    """

    def __init__(self, style, settings):
        self.style = style
        self.settings = settings
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """Create a new ttk theme"""
        self.style.theme_create(self.settings.name, 'clam')
        self.style.theme_use(self.settings.name)
        self.style_defaults()
        self.style_spinbox()
        self.style_scale()
        self.style_scrollbar()
        self.style_combobox()
        self.style_frame()
        self.style_checkbutton()
        self.style_entry()
        self.style_label()
        self.style_labelframe()
        self.style_notebook()
        self.style_outline_buttons()
        self.style_outline_menubutton()
        self.style_progressbar()
        self.style_radiobutton()
        self.style_solid_buttons()
        self.style_solid_menubutton()
        self.style_treeview()

    def style_defaults(self):
        """Setup the default ttk style settings"""
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

    def style_combobox(self):
        """Apply style to ttk combobox: `ttk.Combobox`

        Element Options:
            - Combobox.downarrow: arrowsize, background, bordercolor, relief, arrowcolor
            - Combobox.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Combobox.padding: padding, relief, shiftrelief
            - Combobox.textarea: font, width
        """
        self.style.layout('TCombobox', [('Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
            ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}),
            ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                ('Combobox.textarea', {'sticky': 'nswe'})]})]})])

        if self.settings.type == 'dark':
            self.style.element_create('Spinbox.field', 'from', 'default')

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
                           ('hover', self.settings.colors.primary)],
                       lightcolor=[
                           ('focus', self.settings.colors.primary),
                           ('pressed', self.settings.colors.primary)],
                       darkcolor=[
                           ('focus', self.settings.colors.primary),
                           ('pressed', self.settings.colors.primary)],
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

    def style_progressbar(self):
        """Apply style to ttk progressbar: `ttk.Progressbar`

        Element Options:
            - Progressbar.trough: borderwidth, troughcolor, troughrelief
            - Progressbar.pbar: orient, thickness, barsize, pbarrelief, borderwidth, background
        """
        self.style.element_create('Progressbar.trough', 'from', 'default')
        self.style.element_create('Progressbar.pbar', 'from', 'default')

        self.style.configure('TProgressbar',
                             thickness=20,
                             borderwidth=0,
                             troughcolor=brightness(self.settings.colors.light, -0.05),
                             background=self.settings.colors.primary)

        for color in self.settings.colors:
            self.style.configure(f'{color}.Horizontal.TProgressbar', background=self.settings.colors.get(color))
            self.style.configure(f'{color}.Vertical.TProgressbar', background=self.settings.colors.get(color))

    @staticmethod
    def create_slider_image(color, size=18):
        """Create a slider based on given size and color"""
        im = Image.new('RGBA', (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=color)
        return ImageTk.PhotoImage(im.resize((size, size), Image.LANCZOS))

    def style_scale(self):
        """Apply style to ttk scale: `ttk.Scale`

        Element Options:
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
        self.scale_images['primary_regular'] = self.create_slider_image(self.settings.colors.primary)
        self.scale_images['primary_pressed'] = self.create_slider_image(brightness(self.settings.colors.primary, -0.2))
        self.scale_images['primary_hover'] = self.create_slider_image(brightness(self.settings.colors.primary, -0.1))
        self.scale_images['trough'] = ImageTk.PhotoImage(
            Image.new('RGB', (8, 8), brightness(self.settings.colors.light, -0.05)))

        # create new elements based on images
        self.style.element_create('Scale.track', 'image', self.scale_images['trough'])
        self.style.element_create('Scale.slider', 'image', self.scale_images['primary_regular'],
                                  ('pressed', self.scale_images['primary_pressed']),
                                  ('hover', self.scale_images['primary_hover']))

    def style_scrollbar(self):
        """Apply style to ttk scrollbar: ttk.Scrollbar

        Element Options:
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
                             background=brightness(self.settings.colors.light, -0.1),
                             arrowsize=16,
                             arrowcolor=self.settings.colors.inputfg)

    def style_spinbox(self):
        """Apply style to ttk spinbox: `ttk.Spinbox`

        Element Options:
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
                             bordercolor=self.settings.colors.border,
                             lightcolor=self.settings.colors.bg,
                             darkcolor=self.settings.colors.bg,
                             foreground=self.settings.colors.inputfg,
                             borderwidth=0,
                             background=self.settings.colors.light,
                             fieldbackground=self.settings.colors.light,
                             relief='flat',
                             arrowcolor=self.settings.colors.inputfg,
                             arrowsize=16,
                             padding=(10, 5))

        self.style.map('TSpinbox',
                       bordercolor=[
                           ('focus', self.settings.colors.primary),
                           ('hover', self.settings.colors.primary)],
                       arrowcolor=[
                           ('pressed', self.settings.colors.primary),
                           ('focus', self.settings.colors.inputfg),
                           ('hover', self.settings.colors.inputfg)],
                       lightcolor=[('focus', self.settings.colors.primary)],
                       darkcolor=[('focus', self.settings.colors.primary)])

        # variation changes focus ring color
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

    def style_treeview(self):
        """Apply style to ttk treeview: `ttk.Treeview`

        Element Options:
            - Treeview.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Treeview.padding: padding, relief, shiftrelief
            - Treeview.treearea: 
            - Treeitem.padding: padding, relief, shiftrelief
            - Treeitem.indicator: foreground, diameter, indicatormargins
            - Treeitem.image: image, stipple, background
            - Treeitem.focus: focuscolor, focusthickness
            - Treeitem.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed
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

        # variations change header color and focus ring
        for color in self.settings.colors:
            self.style.configure(f'{color}.Treeview.Heading', background=self.settings.colors.get(color))
            self.style.map(f'{color}.Treeview', bordercolor=[('focus', self.settings.colors.get(color))])

    def style_frame(self):
        """Apply style to ttk frame: `ttk.Frame`

        Element Options:
            - Frame.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
        """
        self.style.configure('TFrame',
                             background=self.settings.colors.bg)

        for color in self.settings.colors:
            self.style.configure(f'{color}.TFrame', background=self.settings.colors.get(color))

    def style_solid_buttons(self):
        """Apply a solid color style to ttk button: `ttk.Button`

        Element Options:
            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
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
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))])

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
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))])

    def style_outline_buttons(self):
        """Apply an outline style to ttk button: `ttk.Button`

        Element Options:
            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
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
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))])

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
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))])

    def style_entry(self):
        """Apply style to ttk entry: `ttk.Entry`

        Element Options:
            - Entry.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Entry.padding: padding, relief, shiftrelief
            - Entry.textarea: font, width        
        """
        self.style.configure('TEntry',
                             fieldbackground=self.settings.colors.light,
                             bordercolor=self.settings.colors.border,
                             lightcolor=self.settings.colors.bg,
                             darkcolor=self.settings.colors.bg,
                             foreground=self.settings.colors.inputfg,
                             padding=5)

        self.style.map('TEntry',
                       bordercolor=[
                           ('hover', self.settings.colors.primary),
                           ('focus', self.settings.colors.primary)],
                       lightcolor=[
                           ('focus', self.settings.colors.primary)],
                       darkcolor=[
                           ('focus', self.settings.colors.primary)])

        # variation changes the focus ring color
        for color in self.settings.colors:
            self.style.map(f'{color}.TEntry',
                           bordercolor=[('focus', self.settings.colors.get(color))],
                           lightcolor=[('focus', self.settings.colors.get(color))],
                           darkcolor=[('focus', self.settings.colors.get(color))])

    def style_radiobutton(self):
        """Apply style to ttk radiobutton: `ttk.Radiobutton`

        Operating System:
            WINDOWS: defaults to the 'xpnative' theme look. Styles will not change the look and feel.
            LINUX / MAC OS: defaults to stylized 'clam' theme. You can use styles with this setup.

        Element Options:
            - Radiobutton.padding: padding, relief, shiftrelief
            - Radiobutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground, upperbordercolor, lowerbordercolor
            - Radiobutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Radiobutton.indicator', 'from', 'xpnative')

        self.style.configure('TRadiobutton',
                             indicatormargin=8,
                             indicatorsize=12,
                             upperbordercolor=self.settings.colors.fg if self.settings.type == 'light' else self.settings.colors.light,
                             lowerbordercolor=self.settings.colors.fg if self.settings.type == 'light' else self.settings.colors.light,
                             indicatorforeground=self.settings.colors.fg if self.settings.type == 'light' else self.settings.colors.bg)

        self.style.map('TRadiobutton',
                       foreground=[
                           ('active', self.settings.colors.primary if (self.settings.type == 'light') else 'white')],
                       indicatorforeground=[
                           ('active', self.settings.colors.primary if (self.settings.type == 'light') else 'black')])

        # variations change the indicator color
        for color in self.settings.colors:
            self.style.map(f'{color}.TRadiobutton',
                           foreground=[('active', brightness(self.settings.colors.get(color), -0.2))],
                           indicatorforeground=[('active', brightness(self.settings.colors.get(color), -0.2))])

    def style_label(self):
        """Apply style to ttk label: `ttk.Label`

        Element Options:
            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TLabel', foreground=self.settings.colors.fg)
        for color in self.settings.colors:
            self.style.configure(f'{color}.TLabel', foreground=self.settings.colors.get(color))

    def style_labelframe(self):
        """Apply style to ttk labelframe: `ttk.LabelFrame`

        Element Options:
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

    def style_checkbutton(self):
        """Apply style to ttk checkbutton: `ttk.Checkbutton`

        Element Options:
            - Checkbutton.padding: padding, relief, shiftrelief
            - Checkbutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground, upperbordercolor, lowerbordercolor
            - Checkbutton.focus: focuscolor, focusthickness
            - Checkbutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        # Use xpnative if available; the buttons look so much better
        # TODO check for native options on Linux and MacOS
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Checkbutton.indicator', 'from', 'xpnative')

        self.style.configure('TCheckbutton',
                             foreground=self.settings.colors.fg,
                             indicatorsize=10,
                             indicatormargin=10,
                             indicatorforeground=self.settings.colors.selectfg)

        self.style.map('TCheckbutton',
                       indicatorbackground=[
                           ('active selected', brightness(self.settings.colors.primary, -0.2)),
                           ('selected', self.settings.colors.fg),
                           ('active !selected', self.settings.colors.light)],
                       foreground=[('active', self.settings.colors.primary)])

        # variations change indicator color
        for color in self.settings.colors:
            self.style.map(f'{color}.TCheckbutton',
                           indicatorbackground=[
                               ('active selected', brightness(self.settings.colors.get(color), -0.2)),
                               ('selected', self.settings.colors.fg),
                               ('active !selected', self.settings.colors.light)],
                           indicatorforeground=[
                               ('active selected', brightness(self.settings.colors.get(color), -0.2)),
                               ('selected', self.settings.colors.get(color))],
                           foreground=[
                               ('active', brightness(self.settings.colors.get(color), -0.2))])

    def style_solid_menubutton(self):
        """Apply a solid color style to ttk menubutton: `ttk.Menubutton`

        Element Options:
            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
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
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))])

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
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))])

    def style_outline_menubutton(self):
        """Apply and outline style to ttk menubutton: `ttk.Menubutton`

        Element Options:
            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
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
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.colors.primary, -0.2)),
                           ('hover', brightness(self.settings.colors.primary, -0.1))],
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
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.settings.colors.get(color), -0.2)),
                               ('hover', brightness(self.settings.colors.get(color), -0.1))],
                           arrowcolor=[
                               ('pressed', self.settings.colors.bg),
                               ('hover', self.settings.colors.bg)])

    def style_notebook(self):
        """Apply style to ttk notebook: `ttk.Notebook`

        Element Options:
            - Notebook.client: background, bordercolor, lightcolor, darkcolor
            - Notebook.tab: background, bordercolor, lightcolor, darkcolor
            - Notebook.padding: padding, relief, shiftrelief
            - Notebook.focus: focuscolor, focusthickness
            - Notebook.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
            
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
