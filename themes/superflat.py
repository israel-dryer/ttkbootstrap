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
    style.master.option_add('*font', (FONT_FAMILY,))

    # menu
    style.master.option_add('*Menu.tearOff', 0)


def create_layouts(style):
    """Create custom layouts for ttk widgets"""
    # Spinbox
    """use spinbox field to get border that encompasses entire widget"""
    style.layout('TCombobox', [('Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [
        ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}),
        ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
            ('Combobox.textarea', {'sticky': 'nswe'})]})]})])


def create_elements(style):
    """Create custom elements for ttk widgets"""
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
    style.element_create('Horizontal.Scrollbar.trough', 'from', 'alt')
    style.element_create('Horizontal.Scrollbar.thumb', 'from', 'alt')
    style.element_create('Horizontal.Scrollbar.uparrow', 'from', 'alt')
    style.element_create('Horizontal.Scrollbar.downarrow', 'from', 'alt')

    # Spinbox
    style.element_create('Spinbox.uparrow', 'from', 'default')
    style.element_create('Spinbox.downarrow', 'from', 'default')

    # Combobox
    style.element_create('Combobox.downarrow', 'from', 'default')
    style.element_create('Combobox.padding', 'from', 'clam')
    style.element_create('Combobox.textarea', 'from', 'clam')

    # Treeview
    style.element_create('Treeitem.indicator', 'from', 'alt')
    # style.element_create('Treeitem.padding', 'from', 'alt')
    # style.element_create('Treeitem.image', 'from', 'alt')
    # style.element_create('Treeitem.focus', 'from', 'alt')
    # style.element_create('Treeitem.text', 'from', 'alt')



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
                    anchor='center',
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

    # Label ------------------------------------------------------------------------------------------------------------
    style.configure('TLabel', foreground=COLORS['primary'])
    for v in variations:
        style.configure(f'{v}.TLabel', foreground=COLORS[v])

    # Labelframe -------------------------------------------------------------------------------------------------------
    style.configure('TLabelframe',
                    padding=(10, 5),
                    foreground=COLORS['dark'],
                    relief='raised',
                    bordercolor=COLORS['dark'])

    style.configure('TLabelframe.Label', foreground=COLORS['dark'])

    for v in variations:
        style.configure(f'{v}.TLabelframe',
                        foreground=COLORS[v],
                        bordercolor=COLORS[v])

        style.configure(f'{v}.TLabelframe.Label', foreground=COLORS[v])

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
                  ('hover', COLORS['bg'])])

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
    style.configure('TCombobox',
                    bordercolor=COLORS['dark'],
                    arrowcolor=COLORS['dark'],
                    foreground=COLORS['dark'],
                    relief='flat',
                    padding=5,
                    arrowsize=16)

    style.map('TCombobox',
              lightcolor=[
                  ('focus', COLORS['dark']),
                  ('pressed', COLORS['dark'])],
              darkcolor=[
                  ('focus', COLORS['dark']),
                  ('pressed', COLORS['dark'])],
              arrowcolor=[('pressed', COLORS['primary'])])

    for v in variations:
        style.map(f'{v}.TCombobox',
                  lightcolor=[
                      ('focus', COLORS[v]),
                      ('pressed', COLORS[v])],
                  darkcolor=[
                      ('focus', COLORS[v]),
                      ('pressed', COLORS[v])],
                  arrowcolor=[('pressed', COLORS[v])])


    # Notebook ---------------------------------------------------------------------------------------------------------
    """The notebook must be configure in two places... `client` and `tab"""
    style.configure('TNotebook',
                    bordercolor=COLORS['dark'])

    style.configure('TNotebook.Tab',
                    bordercolor=COLORS['dark'],
                    foreground=COLORS['dark'],
                    padding=(10, 5))

    style.map('TNotebook.Tab',
              background=[('!selected', COLORS['light'])],
              lightcolor=[('!selected', COLORS['light'])],
              darkcolor=[('!selected', COLORS['light'])],
              bordercolor=[('!selected', COLORS['dark'])],
              foreground=[('!selected', COLORS['success'])])

    # Scrollbar --------------------------------------------------------------------------------------------------------
    style.configure('TScrollbar',
                    troughrelief='flat',
                    relief='flat',
                    troughborderwidth=2,
                    troughcolor=COLORS['light'],
                    background=COLORS['active'],
                    arrowsize=16,
                    arrowcolor=COLORS['primary'])

    # Spinbox ----------------------------------------------------------------------------------------------------------
    style.configure('TSpinbox',
                    bordercolor=COLORS['dark'],
                    lightcolor=COLORS['bg'],
                    darkcolor=COLORS['bg'],
                    foreground=COLORS['dark'],
                    borderwidth=0,
                    relief='flat',
                    arrowcolor=COLORS['dark'],
                    arrowsize=16,
                    padding=(10, 5))

    style.map('TSpinbox',
              lightcolor=[('focus', COLORS['dark'])],
              darkcolor=[('focus', COLORS['dark'])],
              arrowcolor=[('pressed', COLORS['primary'])])

    # Treeview ---------------------------------------------------------------------------------------------------------
    style.configure('Treeview',
                    bordercolor=COLORS['dark'],
                    lightcolor=COLORS['bg'],
                    relief='sunken',
                    padding=-1)

    style.map('Treeview', background=[('selected', COLORS['light'])])

    style.configure('Treeview.Heading',
                    background=COLORS['primary'],
                    foreground=COLORS['selectfg'],
                    relief='flat',
                    padding=5)

    for v in variations:
        style.configure(f'{v}.Treeview.Heading', background=COLORS[v])


def create_theme(style):
    style.theme_create('superflat', 'clam')
    style.theme_use('superflat')
    style_tk_widgets(style)
    create_layouts(style)
    create_elements(style)
    create_widget_styles(style)
