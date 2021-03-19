"""
    A modern tkinter theme inspired by https://bootswatch.com/flatly/

    Author: Israel Dryer
    Modified: 2021-03-19

"""
from colorsys import rgb_to_hsv, hsv_to_rgb
from tkinter import ttk


COLORS = {
    'primary': '#2c3e50',
    'secondary': '#95a5a6',
    'success': '#18bc9c',
    'info': '#3498db',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'bg': '#fff',
    'fg': '#2c3e50',
    'selectbg': '#3498db',
    'selectfg': '#fff',
    'light': '#ecf0f1',
    'dark': '#7b8a8b',
    'active': '#dadada',
    'lighter': '#ced4da'
}

FONT_FAMILY = 'Roboto'


def hex_to_rgb(color):
    r = round(int(color[1:3], 16) / 255, 2)
    g = round(int(color[3:5], 16) / 255, 2)
    b = round(int(color[5:], 16) / 255, 2)
    return r, g, b


def rgb_to_hex(r, g, b):
    r_ = int(r * 255)
    g_ = int(g * 255)
    b_ = int(b * 255)
    return '#{:02x}{:02x}{:02x}'.format(r_, g_, b_)


def brightness(hex_color, pct_change):
    r, g, b = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(r, g, b)
    v_ = (1 + pct_change) * v
    v_max = max(0, v_)
    v_min = min(1, v_max)
    r_, g_, b_ = hsv_to_rgb(h, s, v_min)
    return rgb_to_hex(r_, g_, b_)


def style_tk_widgets(style):
    """Apply theme to non-ttk widgets"""
    # general
    style.master.option_add('*background', COLORS['bg'])
    style.master.option_add('*activeBackground', COLORS['selectbg'])
    style.master.option_add('*activeForeground', COLORS['selectfg'])
    style.master.option_add('*selectBackground', COLORS['selectbg'])
    style.master.option_add('*selectForeground', COLORS['selectfg'])

    # menu
    style.master.option_add('*Menu.borderWidth', '0')
    style.master.option_add('*Menu.tearOff', '0')

    # scrollbar


def create_layouts(style):

    # Vertical scroll bar -- removing arrows from theme
    style.layout('Vertical.TScrollbar', [
        ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
        ('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})]})])


def create_elements(style):
    # Progressbar
    style.element_create('Progressbar.trough', 'from', 'default')
    style.element_create('Progressbar.pbar', 'from', 'default')

    # Scale
    style.element_create('Scale.trough', 'from', 'alt')
    style.element_create('Scale.slider', 'from', 'alt')

    # Vertical scrollbar
    style.element_create('Vertical.Scrollbar.trough', 'from', 'alt')
    style.element_create('Vertical.Scrollbar.thumb', 'from', 'alt')
    style.element_create('Vertical.Scrollbar.uparrow', 'from', 'alt')
    style.element_create('Vertical.Scrollbar.downarrow', 'from', 'alt')

    # Horizontal scrollbar

def create_widget_styles(style):
    """Use the light and dark colors of the clam theme to create a highlight button effect for various states. For this
    theme, the light and dark colors should match the background color unless I'm specifically using them for effect"""

    variations = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

    # Application defaults ---------------------------------------------------------------------------------------------
    style.configure('.',
                    background=COLORS['bg'],
                    darkcolor=COLORS['bg'],
                    lightcolor=COLORS['bg'],
                    foreground=COLORS['fg'],
                    troughcolor=COLORS['bg'],
                    selectbg=COLORS['selectbg'],
                    selectfg=COLORS['selectfg'],
                    selectforeground=COLORS['selectfg'],
                    selectbackground=COLORS['selectbg'],
                    fieldbg=COLORS['bg'],
                    font=(FONT_FAMILY, ),
                    borderwidth=1,
                    focuscolor='')

    # Frame ------------------------------------------------------------------------------------------------------------
    style.configure('TFrame', background=COLORS['bg'])
    for v in variations:
        style.configure(f'{v}.TFrame', background=COLORS[v])

    # Solid buttons ----------------------------------------------------------------------------------------------------
    style.configure('TButton',
                    foreground=COLORS['selectfg'],
                    background=COLORS['primary'],
                    bordercolor=COLORS['primary'],
                    darkcolor=COLORS['primary'],
                    lightcolor=COLORS['primary'],
                    relief='raised',
                    focusthickness=0,
                    focuscolor='',
                    padding=(10, 5))

    style.map('TButton',
              background=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              bordercolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              darkcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              lightcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))])

    for v in variations:
        style.configure(f'{v}.TButton',
                        foreground=COLORS['selectfg'],
                        background=COLORS[v],
                        bordercolor=COLORS[v],
                        darkcolor=COLORS[v],
                        lightcolor=COLORS[v],
                        relief='raised',
                        focusthickness=0,
                        focuscolor='',
                        padding=(10, 5))

        style.map(f'{v}.TButton',
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  bordercolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  darkcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  lightcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))])

    # Outline buttons --------------------------------------------------------------------------------------------------
    style.configure('Outline.TButton',
                    foreground=COLORS['primary'],
                    background=COLORS['bg'],
                    bordercolor=COLORS['primary'],
                    darkcolor=COLORS['bg'],
                    lightcolor=COLORS['bg'],
                    relief='raised',
                    focusthickness=0,
                    focuscolor='',
                    padding=(10, 5))

    style.map('Outline.TButton',
              foreground=[
                  ('pressed', COLORS['selectfg']),
                  ('hover', COLORS['selectfg'])],
              background=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              bordercolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              darkcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              lightcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))])

    for v in variations:
        style.configure(f'{v}.Outline.TButton',
                        foreground=COLORS[v],
                        background=COLORS['bg'],
                        bordercolor=COLORS[v],
                        darkcolor=COLORS['bg'],
                        lightcolor=COLORS['bg'],
                        relief='raised',
                        focusthickness=0,
                        focuscolor='',
                        padding=(10, 5))

        style.map(f'{v}.Outline.TButton',
                  foreground=[
                      ('pressed', COLORS['selectfg']),
                      ('hover', COLORS['selectfg'])],
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  bordercolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  darkcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  lightcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))])

    # Progress bar -----------------------------------------------------------------------------------------------------
    style.configure('TProgressbar',
                    thickness=20,
                    borderwidth=0,
                    troughcolor=COLORS['light'],
                    background=COLORS['primary'])

    for v in variations:
        style.configure(f'{v}.Horizontal.TProgressbar', background=COLORS[v])
        style.configure(f'{v}.Vertical.TProgressbar', background=COLORS[v])

    # Entry ------------------------------------------------------------------------------------------------------------
    """Cannot change font with style, must be changed with widget options >> https://bugs.python.org/issue21341"""
    style.configure('TEntry',
                    bordercolor=COLORS['dark'],
                    lightcolor=COLORS['bg'],
                    darkcolor=COLORS['bg'],
                    foreground=COLORS['dark'],
                    padding=5)

    style.map('TEntry',
              lightcolor=[('focus', COLORS['dark'])],
              darkcolor=[('focus', COLORS['dark'])])

    # add variations to change the focus ring color
    for v in variations:
        style.map(f'{v}.TEntry',
                  bordercolor=[('focus', COLORS[v])],
                  lightcolor=[('focus', COLORS[v])],
                  darkcolor=[('focus', COLORS[v])])

    # Scale ------------------------------------------------------------------------------------------------------------
    """I'm not sold on this setup, but it gives me the ability to use a built-in theme without adding
    image elements. However, image elements would give this a nicer look"""
    style.configure('TScale',
                    sliderrelief='flat',
                    sliderthickness=18,
                    troughrelief='flat',
                    background=COLORS['primary'],
                    troughcolor=COLORS['light'])

    style.map('TScale',
              background=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))])

    # add variations
    for v in variations:
        style.configure(f'{v}.Horizontal.TScale', background=COLORS[v])
        style.configure(f'{v}.Vertical.TScale', background=COLORS[v])

        style.map(f'{v}.Horizontal.TScale',
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))])

        style.map(f'{v}.Vertical.TScale',
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))])

    # Radiobutton ------------------------------------------------------------------------------------------------------
    style.configure('TRadiobutton',
                    foreground=COLORS['dark'],
                    indicatorsize=16,
                    indicatormargin=10,
                    indicatorforeground=COLORS['active'],
                    indicatorbackground=COLORS['active'],
                    upperbordercolor=COLORS['active'],
                    lowerbordercolor=COLORS['active'])

    style.map('TRadiobutton',
              indicatorbackground=[
                  ('active selected', brightness(COLORS['primary'], -0.2)),
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))],
              indicatorforeground=[
                  ('active selected', brightness(COLORS['primary'], -0.2)),
                  ('selected', COLORS['primary'])],
              foreground=[('active', COLORS['primary'])],
              upperbordercolor=[
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))],
              lowerbordercolor=[
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))])

    # add variations to the button indicator
    for v in variations:
        style.map(f'{v}.TRadiobutton',
                        indicatorbackground=[
                            ('active selected', brightness(COLORS[v], -0.2)),
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))],
                        indicatorforeground=[
                            ('active selected', brightness(COLORS[v], -0.2)),
                            ('selected', COLORS[v])],
                        foreground=[
                            ('active', brightness(COLORS[v], -0.2))],
                        upperbordercolor=[
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))],
                        lowerbordercolor=[
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))])

    # Labelframe -------------------------------------------------------------------------------------------------------
    style.configure('TLabelframe',
                    padding=(10, 5),
                    foreground=COLORS['dark'],
                    relief='raised',
                    bordercolor=COLORS['dark'])

    # Checkbutton ------------------------------------------------------------------------------------------------------
    style.configure('TCheckbutton',
                    foreground=COLORS['dark'],
                    indicatorsize=16,
                    indicatormargin=10,
                    indicatorforeground=COLORS['active'],
                    indicatorbackground=COLORS['active'],
                    upperbordercolor=COLORS['active'],
                    lowerbordercolor=COLORS['active'])

    style.map('TCheckbutton',
              indicatorbackground=[
                  ('active selected', brightness(COLORS['primary'], -0.2)),
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))],
              indicatorforeground=[
                  ('active selected', brightness(COLORS['primary'], -0.2)),
                  ('selected', COLORS['primary'])],
              foreground=[('active', COLORS['primary'])],
              upperbordercolor=[
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))],
              lowerbordercolor=[
                  ('selected', COLORS['primary']),
                  ('active !selected', brightness(COLORS['dark'], 0.3))])

    # add variations to the button indicator
    for v in variations:
        style.map(f'{v}.TCheckbutton',
                        indicatorbackground=[
                            ('active selected', brightness(COLORS[v], -0.2)),
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))],
                        indicatorforeground=[
                            ('active selected', brightness(COLORS[v], -0.2)),
                            ('selected', COLORS[v])],
                        foreground=[
                            ('active', brightness(COLORS[v], -0.2))],
                        upperbordercolor=[
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))],
                        lowerbordercolor=[
                            ('selected', COLORS[v]),
                            ('active !selected', brightness(COLORS['dark'], 0.3))])

    # Solid menubutton -------------------------------------------------------------------------------------------------
    """Some of the menu list settings are set with the root widget options on initialization. This will be styled
    essentially like a regular button"""
    style.configure('TMenubutton',
                    foreground=COLORS['selectfg'],
                    background=COLORS['primary'],
                    bordercolor=COLORS['primary'],
                    darkcolor=COLORS['primary'],
                    lightcolor=COLORS['primary'],
                    arrowcolor=COLORS['bg'],
                    arrowpadding=(0, 0, 15, 0),
                    relief='raised',
                    focusthickness=0,
                    focuscolor='',
                    padding=(10, 5))

    style.map('TMenubutton',
              background=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              bordercolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              darkcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              lightcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))])

    # add variations
    for v in variations:
        style.configure(f'{v}.TMenubutton',
                        foreground=COLORS['selectfg'],
                        background=COLORS[v],
                        bordercolor=COLORS[v],
                        darkcolor=COLORS[v],
                        lightcolor=COLORS[v],
                        relief='raised',
                        focusthickness=0,
                        focuscolor='',
                        padding=(10, 5))

        style.map(f'{v}.TMenubutton',
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  bordercolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  darkcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  lightcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))])

    # Outline Menubuttons ----------------------------------------------------------------------------------------------
    style.configure('Outline.TMenubutton',
                    foreground=COLORS['primary'],
                    background=COLORS['bg'],
                    bordercolor=COLORS['primary'],
                    darkcolor=COLORS['bg'],
                    lightcolor=COLORS['bg'],
                    arrowcolor=COLORS['primary'],
                    arrowpadding=(0, 0, 15, 0),
                    relief='raised',
                    focusthickness=0,
                    focuscolor='',
                    padding=(10, 5))

    style.map('Outline.TMenubutton',
              foreground=[
                  ('pressed', COLORS['selectfg']),
                  ('hover', COLORS['selectfg'])],
              background=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              bordercolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              darkcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              lightcolor=[
                  ('pressed', brightness(COLORS['primary'], -0.2)),
                  ('hover', brightness(COLORS['primary'], -0.1))],
              arrowcolor=[
                  ('pressed', COLORS['bg']),
                  ('hover', COLORS['bg'])
              ])

    for v in variations:
        style.configure(f'{v}.Outline.TMenubutton',
                        foreground=COLORS[v],
                        background=COLORS['bg'],
                        bordercolor=COLORS[v],
                        darkcolor=COLORS['bg'],
                        lightcolor=COLORS['bg'],
                        arrowcolor=COLORS[v],
                        relief='raised',
                        focusthickness=0,
                        focuscolor='',
                        padding=(10, 5))

        style.map(f'{v}.Outline.TMenubutton',
                  foreground=[
                      ('pressed', COLORS['selectfg']),
                      ('hover', COLORS['selectfg'])],
                  background=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  bordercolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  darkcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  lightcolor=[
                      ('pressed', brightness(COLORS[v], -0.2)),
                      ('hover', brightness(COLORS[v], -0.1))],
                  arrowcolor=[
                      ('pressed', COLORS['bg']),
                      ('hover', COLORS['bg'])])

    # Combobox ---------------------------------------------------------------------------------------------------------
    """For whatever reason, the font cannot be changed through style... it must be changed in the widget settings"""
    style.configure('TCombobox',
                    bordercolor=COLORS['dark'],
                    arrowcolor=COLORS['dark'],
                    foreground=COLORS['dark'],
                    padding=5,
                    arrowsize=16)

    style.map('TCombobox',
              lightcolor=[('focus', COLORS['dark'])],
              darkcolor=[('focus', COLORS['dark'])])

    # Notebook ---------------------------------------------------------------------------------------------------------
    """The notebook must be configure in two places... `client` and `tab"""
    style.configure('TNotebook',
                    bordercolor=COLORS['dark'])
    style.configure('TNotebook.Tab',
                    bordercolor=COLORS['dark'],
                    foreground=COLORS['dark'],
                    relief='flat',
                    padding=(10, 5))

    """TODO find a way to remove the border when not selected... the current solutions shows a small intersection of
    white on the client border"""
    style.map('TNotebook.Tab',
              background=[('!selected', COLORS['bg'])],
              lightcolor=[('!selected', COLORS['bg'])],
              darkcolor=[('!selected', COLORS['bg'])],
              bordercolor=[('!selected', COLORS['bg'])],
              foreground=[('!selected', COLORS['success'])])

    # Scrollbar
    style.configure('TScrollbar',
                    troughrelief='flat',
                    relief='flat',
                    troughborderwidth=0,
                    troughcolor=COLORS['light'],
                    background=COLORS['active'])

    # Spinbox
    style


def create_theme(style):
    style.theme_create('superflat', 'clam')
    style.theme_use('superflat')
    style_tk_widgets(style)
    create_layouts(style)
    create_elements(style)
    create_widget_styles(style)


class Style(ttk.Style):
    def __init__(self):
        super().__init__()
        create_theme(self)
