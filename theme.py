"""
    Izzy-Themes
        A package for creating modern ttk (tkinter) by customizing built-in ttk themes.

    Author
        Israel Dryer

    Modified
        2021-03-20


    The purpose of this package is to provide a simple and easy to use api for creating modern ttk themes using
    the themes that are already built into Tkinter and Python. It is possibly to customize these even further with
    image-based layouts. But, they are time-consuming to create and not flexible for creating varieties of colors.
    Fortunately, ttk is very flexible and allows the creating of brand new themes using the best parts of all the
    existing themes.

    I've created several new widget layouts using the parts of existing themes. For example, the Combobox widget uses
    the field element from the Spinbox so that I could create the border effect I wanted.  Another example is the
    Treeview, which uses the indicator from the `alt` theme, because I just think it looks nicer.

    I decided to use the clam theme as the base for much of this project because it provides a lot of flexibility when
    it comes to borders. Because the clam theme has an outer border and an inner border (light & dark), I am able to use
    the states to create a focus ring effect that is similar to what you would find with a CSS Boostrap theme. There
    are many cool tricks and hacks that you can tease out of the existing set of themes,  so I hope you enjoy this
    library as well as using the bones to create something of your own.
"""
import colorsys
from collections import namedtuple
from tkinter import ttk

VARIATIONS = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

Colors = namedtuple('Colors', ['primary', 'secondary', 'success', 'info', 'warning', 'danger',
                               'bg', 'fg', 'selectbg', 'selectfg', 'light', 'dark', 'active', 'border', 'inputfg'])

# TODO add color style for input font colors, which should be lighter

class Theme:
    """
    A ttk theme created with built-in elements and a supplied color scheme. A theme type can be light or dark. This
    changes the way that certain elements are created for the theme.
    """

    def __init__(self, style: ttk.Style, theme_name: str, colors: Colors, default_font: str, theme_type='light'):
        self.name = theme_name
        self.style = style
        self.colors = colors
        self.font = default_font
        self.theme_type = theme_type
        self.create_theme()

    def create_theme(self):
        """Create a new ttk theme"""
        self.style.theme_create(self.name, 'clam')
        self.style.theme_use(self.name)
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

    @staticmethod
    def hex_to_rgb(color):
        """Convert hexadecimal to rgb color representation"""
        r = round(int(color[1:3], 16) / 255, 2)
        g = round(int(color[3:5], 16) / 255, 2)
        b = round(int(color[5:], 16) / 255, 2)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r, g, b):
        """Convert rgb to hexadecimal color representation"""
        r_ = int(r * 255)
        g_ = int(g * 255)
        b_ = int(b * 255)
        return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)

    @classmethod
    def brightness(cls, hex_color, pct_change):
        """Adjust the value of a given hexadecimal color. The percent change is expected to be a float. Example: 0.15
        is a 15 percent increase in brightness, whereas -0.15 is a 15 percent decrease in brightness"""
        r, g, b = cls.hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v_ = (1 + pct_change) * v
        v_max = max(0, v_)
        v_min = min(1, v_max)
        r_, g_, b_ = colorsys.hsv_to_rgb(h, s, v_min)
        return cls.rgb_to_hex(r_, g_, b_)

    def lookup_color(self, color: str):
        """Lookup a color in the colors dictionary"""
        return self.colors._asdict().get(color)

    def apply_global_tk_styles(self):
        """Apply global settings to theme for non-ttk settings and widgets"""
        self.style.master.option_add('*background', self.colors.bg)
        self.style.master.option_add('*activeBackground', self.colors.selectbg)
        self.style.master.option_add('*activeForeground', self.colors.selectfg)
        self.style.master.option_add('*selectBackground', self.colors.selectbg)
        self.style.master.option_add('*selectForeground', self.colors.selectfg)
        self.style.master.option_add('*font', (self.font,))
        self.style.master.option_add('*Menu.tearOff', 0)
        self.style.master.option_add('*Listbox.background', 'white')
        self.style.master.option_add('*Listbox.foreground', self.colors.inputfg)
        # TODO set popdown list background to white

    def style_defaults(self):
        """Setup the default ttk style settings"""
        self.style.configure('.',
                             background=self.colors.bg,
                             darkcolor=self.colors.border,
                             lightcolor=self.colors.border,
                             foreground=self.colors.fg,
                             troughcolor=self.colors.bg,
                             selectbg=self.colors.selectbg,
                             selectfg=self.colors.selectfg,
                             selectforeground=self.colors.selectfg,
                             selectbackground=self.colors.selectbg,
                             fieldbg='white',
                             font=(self.font,),
                             borderwidth=1,
                             focuscolor='')

    def style_combobox(self):
        """
        Create a combobox widget style

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

        if self.theme_type == 'dark':
            self.style.element_create('Spinbox.field', 'from', 'default')

        self.style.element_create('Combobox.downarrow', 'from', 'default')
        self.style.element_create('Combobox.padding', 'from', 'clam')
        self.style.element_create('Combobox.textarea', 'from', 'clam')
        self.style.configure('TCombobox',
                             bordercolor=self.colors.border,
                             darkcolor=self.colors.bg,
                             lightcolor=self.colors.bg,
                             arrowcolor=self.colors.border,
                             foreground=self.colors.inputfg,
                             fieldbackground='white',
                             background='white',
                             relief='flat',
                             borderwidth=0,
                             padding=5,
                             arrowsize=16)
        self.style.map('TCombobox',
                       bordercolor=[
                           ('focus', self.colors.primary),
                           ('hover', self.colors.primary)],
                       lightcolor=[
                           ('focus', self.colors.primary),
                           ('pressed', self.colors.primary)],
                       darkcolor=[
                           ('focus', self.colors.primary),
                           ('pressed', self.colors.primary)],
                       arrowcolor=[
                           ('pressed', self.colors.dark),
                           ('focus', self.colors.primary),
                           ('hover', self.colors.primary)])

        for v in VARIATIONS:
            self.style.map(f'{v}.TCombobox',
                           bordercolor=[
                               ('focus', self.lookup_color(v)),
                               ('hover', self.lookup_color(v))],
                           lightcolor=[
                               ('focus', self.lookup_color(v)),
                               ('pressed', self.lookup_color(v))],
                           darkcolor=[
                               ('focus', self.lookup_color(v)),
                               ('pressed', self.lookup_color(v))],
                           arrowcolor=[
                               ('pressed', self.colors.dark),
                               ('focus', self.lookup_color(v)),
                               ('hover', self.lookup_color(v))])

    def style_progressbar(self):
        """
        Create a progress bar widget style

        Element Options:
            - Progressbar.trough: borderwidth, troughcolor, troughrelief
            - Progressbar.pbar: orient, thickness, barsize, pbarrelief, borderwidth, background
        """
        self.style.element_create('Progressbar.trough', 'from', 'default')
        self.style.element_create('Progressbar.pbar', 'from', 'default')

        self.style.configure('TProgressbar',
                             thickness=20,
                             borderwidth=0,
                             troughcolor=self.brightness(self.colors.light, -0.05),
                             background=self.colors.primary)

        for v in VARIATIONS:
            self.style.configure(f'{v}.Horizontal.TProgressbar', background=self.lookup_color(v))
            self.style.configure(f'{v}.Vertical.TProgressbar', background=self.lookup_color(v))

    def style_scale(self):
        """
        Create a scale widget style

        Element Options:
            - Scale.trough: borderwidth, troughcolor, troughrelief
            - Scale.slider: sliderlength, sliderthickness, sliderrelief, borderwidth, background, bordercolor, orient
        """
        self.style.element_create('Scale.trough', 'from', 'alt')
        self.style.element_create('Scale.slider', 'from', 'alt')

        self.style.configure('TScale',
                             sliderrelief='flat',
                             sliderthickness=18,
                             troughrelief='flat',
                             background=self.colors.primary,
                             troughcolor=self.brightness(self.colors.light, -0.05))

        self.style.map('TScale',
                       background=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.Horizontal.TScale', background=self.lookup_color(v))
            self.style.configure(f'{v}.Vertical.TScale', background=self.lookup_color(v))

            self.style.map(f'{v}.Horizontal.TScale',
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))])

            self.style.map(f'{v}.Vertical.TScale',
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))])

    def style_scrollbar(self):
        """
        Create a scrollbar widget style

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
                             troughcolor=self.colors.light,
                             background=self.colors.active,
                             arrowsize=16,
                             arrowcolor=self.colors.primary)

    def style_spinbox(self):
        """
        Create a spinbox widget style

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
        if self.theme_type == 'dark':
            self.style.element_create('custom.Spinbox.field', 'from', 'default')

        self.style.configure('TSpinbox',
                             bordercolor=self.colors.border,
                             lightcolor=self.colors.bg,
                             darkcolor=self.colors.bg,
                             foreground=self.colors.inputfg,
                             borderwidth=0,
                             background='white',
                             relief='flat',
                             arrowcolor=self.colors.border,
                             arrowsize=16,
                             padding=(10, 5))

        self.style.map('TSpinbox',
                       bordercolor=[
                           ('focus', self.colors.primary),
                           ('hover', self.colors.primary)],
                       arrowcolor=[
                           ('pressed', self.colors.dark),
                           ('hover', self.colors.primary)],
                       lightcolor=[('focus', self.colors.primary)],
                       darkcolor=[('focus', self.colors.primary)])

        # variation changes focus ring color
        for v in VARIATIONS:
            self.style.map(f'{v}.TSpinbox',
                           bordercolor=[
                               ('focus', self.lookup_color(v)),
                               ('hover', self.lookup_color(v))],
                           arrowcolor=[
                               ('pressed', self.colors.dark),
                               ('hover', self.lookup_color(v))],
                           lightcolor=[('focus', self.lookup_color(v))],
                           darkcolor=[('focus', self.lookup_color(v))])

    def style_treeview(self):
        """
        Create a treeview widget style

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
                             background='white',
                             foreground=self.colors.inputfg,
                             bordercolor=self.colors.border,
                             lightcolor=self.colors.bg,
                             darkcolor=self.colors.bg,
                             relief='raised' if self.theme_type == 'light' else 'flat',
                             padding=-1 if self.theme_type == 'light' else -2)

        self.style.map('Treeview',
                       background=[('selected', self.colors.light)],
                       bordercolor=[('focus', self.colors.border)])

        self.style.configure('Treeview.Heading',
                             background=self.colors.primary,
                             foreground=self.colors.selectfg,
                             relief='flat',
                             padding=5)

        # variations change header color and focus ring
        for v in VARIATIONS:
            self.style.configure(f'{v}.Treeview.Heading', background=self.lookup_color(v))
            self.style.map(f'{v}.Treeview', bordercolor=[('focus', self.lookup_color(v))])

    def style_frame(self):
        """
        Create a treeview widget style

        Element Options:
            - Frame.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
        """
        self.style.configure('TFrame',
                             background=self.colors.bg)

        for v in VARIATIONS:
            self.style.configure(f'{v}.TFrame', background=self.lookup_color(v))

    def style_solid_buttons(self):
        """
        Create a solid button widget style

        Element Options:
            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TButton',
                             foreground=self.colors.selectfg,
                             background=self.colors.primary,
                             bordercolor=self.colors.primary,
                             darkcolor=self.colors.primary,
                             lightcolor=self.colors.primary,
                             anchor='center',
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TButton',
                       background=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.TButton',
                                 foreground=self.colors.selectfg,
                                 background=self.lookup_color(v),
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.lookup_color(v),
                                 lightcolor=self.lookup_color(v),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.TButton',
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))])

    def style_outline_buttons(self):
        """
        Create an outline button widget style

        Element Options:
            - Button.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Button.focus: focuscolor, focusthickness
            - Button.padding: padding, relief, shiftrelief
            - Button.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('Outline.TButton',
                             foreground=self.colors.primary,
                             background=self.colors.bg,
                             bordercolor=self.colors.primary,
                             darkcolor=self.colors.bg,
                             lightcolor=self.colors.bg,
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TButton',
                       foreground=[
                           ('pressed', self.colors.selectfg),
                           ('hover', self.colors.selectfg)],
                       background=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.Outline.TButton',
                                 foreground=self.lookup_color(v),
                                 background=self.colors.bg,
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.colors.bg,
                                 lightcolor=self.colors.bg,
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.Outline.TButton',
                           foreground=[
                               ('pressed', self.colors.selectfg),
                               ('hover', self.colors.selectfg)],
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))])

    def style_entry(self):
        """
        Create an entry widget style

        Element Options:
            - Entry.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Entry.padding: padding, relief, shiftrelief
            - Entry.textarea: font, width        
        """
        self.style.configure('TEntry',
                             bordercolor=self.colors.border,
                             lightcolor=self.colors.bg,
                             darkcolor=self.colors.bg,
                             foreground=self.colors.inputfg,
                             padding=5)

        self.style.map('TEntry',
                       bordercolor=[
                           ('hover', self.colors.primary),
                           ('focus', self.colors.primary)],
                       lightcolor=[
                           ('focus', self.colors.primary)],
                       darkcolor=[
                           ('focus', self.colors.primary)])

        # variation changes the focus ring color
        for v in VARIATIONS:
            self.style.map(f'{v}.TEntry',
                           bordercolor=[('focus', self.lookup_color(v))],
                           lightcolor=[('focus', self.lookup_color(v))],
                           darkcolor=[('focus', self.lookup_color(v))])

    def style_radiobutton(self):
        """
        Create a radiobutton widget style

        Element Options:
            - Radiobutton.padding: padding, relief, shiftrelief
            - Radiobutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground, upperbordercolor, lowerbordercolor
            - Radiobutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TRadiobutton',
                             foreground=self.colors.dark,
                             indicatorsize=16,
                             indicatormargin=10,
                             indicatorforeground=self.colors.active,
                             indicatorbackground=self.colors.active,
                             upperbordercolor=self.colors.active,
                             lowerbordercolor=self.colors.active)

        self.style.map('TRadiobutton',
                       indicatorbackground=[
                           ('active selected', self.brightness(self.colors.primary, -0.2)),
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))],
                       indicatorforeground=[
                           ('active selected', self.brightness(self.colors.primary, -0.2)),
                           ('selected', self.colors.primary)],
                       foreground=[('active', self.colors.primary)],
                       upperbordercolor=[
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))],
                       lowerbordercolor=[
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))])

        # variations change the indicator color
        for v in VARIATIONS:
            self.style.map(f'{v}.TRadiobutton',
                           indicatorbackground=[
                               ('active selected', self.brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))],
                           indicatorforeground=[
                               ('active selected', self.brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.lookup_color(v))],
                           foreground=[
                               ('active', self.brightness(self.lookup_color(v), -0.2))],
                           upperbordercolor=[
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))],
                           lowerbordercolor=[
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))])

    def style_label(self):
        """
         Create a label widget style

        Element Options:
            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TLabel', foreground=self.colors.dark)
        for v in VARIATIONS:
            self.style.configure(f'{v}.TLabel', foreground=self.lookup_color(v))

    def style_labelframe(self):
        """
         Create a labelframe widget style

        Element Options:
            - Labelframe.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.fill: background
            - Label.text: text, font, foreground, underline, width, anchor, justify, wraplength, embossed
        """
        # TODO find a way to set the labelframe color to activate based on hovering inside it's boundaries
        self.style.configure('TLabelframe',
                             padding=(10, 5),
                             foreground=self.colors.dark,
                             relief='raised',
                             bordercolor=self.colors.border,
                             darkcolor=self.colors.bg,
                             lightcolor=self.colors.bg)

        self.style.configure('TLabelframe.Label', foreground=self.colors.dark)

        for v in VARIATIONS:
            self.style.configure(f'{v}.TLabelframe',
                                 foreground=self.lookup_color(v),
                                 bordercolor=self.lookup_color(v))

            self.style.configure(f'{v}.TLabelframe.Label', foreground=self.lookup_color(v))

    def style_checkbutton(self):
        """
         Create a checkbutton widget style

        Element Options:
            - Checkbutton.padding: padding, relief, shiftrelief
            - Checkbutton.indicator: indicatorsize, indicatormargin, indicatorbackground, indicatorforeground, upperbordercolor, lowerbordercolor
            - Checkbutton.focus: focuscolor, focusthickness
            - Checkbutton.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TCheckbutton',
                             foreground=self.colors.dark,
                             indicatorsize=16,
                             indicatormargin=10,
                             indicatorforeground=self.colors.active,
                             indicatorbackground=self.colors.active,
                             upperbordercolor=self.colors.active,
                             lowerbordercolor=self.colors.active)

        self.style.map('TCheckbutton',
                       indicatorbackground=[
                           ('active selected', self.brightness(self.colors.primary, -0.2)),
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))],
                       indicatorforeground=[
                           ('active selected', self.brightness(self.colors.primary, -0.2)),
                           ('selected', self.colors.primary)],
                       foreground=[('active', self.colors.primary)],
                       upperbordercolor=[
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))],
                       lowerbordercolor=[
                           ('selected', self.colors.primary),
                           ('active !selected', self.brightness(self.colors.dark, 0.3))])

        # variations change indicator color
        for v in VARIATIONS:
            self.style.map(f'{v}.TCheckbutton',
                           indicatorbackground=[
                               ('active selected', self.brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))],
                           indicatorforeground=[
                               ('active selected', self.brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.lookup_color(v))],
                           foreground=[
                               ('active', self.brightness(self.lookup_color(v), -0.2))],
                           upperbordercolor=[
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))],
                           lowerbordercolor=[
                               ('selected', self.lookup_color(v)),
                               ('active !selected', self.brightness(self.colors.dark, 0.3))])

    def style_solid_menubutton(self):
        """
        Create a solid menubutton widget style

        Element Options:
            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
            - Menubutton.label: 
        """
        self.style.configure('TMenubutton',
                             foreground=self.colors.selectfg,
                             background=self.colors.primary,
                             bordercolor=self.colors.primary,
                             darkcolor=self.colors.primary,
                             lightcolor=self.colors.primary,
                             arrowcolor=self.colors.bg,
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TMenubutton',
                       background=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.TMenubutton',
                                 foreground=self.colors.selectfg,
                                 background=self.lookup_color(v),
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.lookup_color(v),
                                 lightcolor=self.lookup_color(v),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.TMenubutton',
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))])

    def style_outline_menubutton(self):
        """
        Create an outline menubutton widget style

        Element Options:
            - Menubutton.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Menubutton.focus: focuscolor, focusthickness
            - Menubutton.indicator: arrowsize, arrowcolor, arrowpadding
            - Menubutton.padding: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
            - Menubutton.label:
        """
        self.style.configure('Outline.TMenubutton',
                             foreground=self.colors.primary,
                             background=self.colors.bg,
                             bordercolor=self.colors.primary,
                             darkcolor=self.colors.bg,
                             lightcolor=self.colors.bg,
                             arrowcolor=self.colors.primary,
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TMenubutton',
                       foreground=[
                           ('pressed', self.colors.fg),
                           ('hover', self.colors.fg)],
                       background=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       bordercolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       darkcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       lightcolor=[
                           ('pressed', self.brightness(self.colors.primary, -0.2)),
                           ('hover', self.brightness(self.colors.primary, -0.1))],
                       arrowcolor=[
                           ('pressed', self.colors.bg),
                           ('hover', self.colors.bg)])

        for v in VARIATIONS:
            self.style.configure(f'{v}.Outline.TMenubutton',
                                 foreground=self.lookup_color(v),
                                 background=self.colors.bg,
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.colors.bg,
                                 lightcolor=self.colors.bg,
                                 arrowcolor=self.lookup_color(v),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.Outline.TMenubutton',
                           foreground=[
                               ('pressed', self.colors.fg),
                               ('hover', self.colors.fg)],
                           background=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', self.brightness(self.lookup_color(v), -0.2)),
                               ('hover', self.brightness(self.lookup_color(v), -0.1))],
                           arrowcolor=[
                               ('pressed', self.colors.bg),
                               ('hover', self.colors.bg)])

    def style_notebook(self):
        """
        Create a notebook widget style

        Element Options:
            - Notebook.client: background, bordercolor, lightcolor, darkcolor
            - Notebook.tab: background, bordercolor, lightcolor, darkcolor
            - Notebook.padding: padding, relief, shiftrelief
            - Notebook.focus: focuscolor, focusthickness
            - Notebook.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
            
        """
        self.style.configure('TNotebook',
                             bordercolor=self.colors.border)

        self.style.configure('TNotebook.Tab',
                             bordercolor=self.colors.border,
                             foreground=self.colors.dark,
                             padding=(10, 5))

        self.style.map('TNotebook.Tab',
                       background=[('!selected', self.colors.light)],
                       lightcolor=[('!selected', self.colors.light)],
                       darkcolor=[('!selected', self.colors.light)],
                       bordercolor=[('!selected', self.colors.border)],
                       foreground=[('!selected', self.colors.inputfg)])
