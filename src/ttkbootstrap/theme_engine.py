"""
    Izzy-Themes
        A package for creating modern ttk (tkinter) by customizing built-in ttk themes.

    Author
        Israel Dryer

    Modified
        2021-03-24


    PURPOSE:
        The purpose of this package is to provide a simple and easy to use api for creating modern ttk themes using
        the themes that are already built into Tkinter and Python.

    APPROACH:
        I've created several new widget layouts using the parts of existing themes. For example, the Combobox widget
        uses the field element from the Spinbox so that I could create the border effect I wanted.  Another example is
        the Treeview, which uses the indicator from the `alt` theme, because I just think it looks nicer.

        For Windows, I'm using the checkbutton and radiobutton from the `xpnative` theme. For Linux and MacOS, it defaults
        the the clam theme elements.

        I decided to use PILLOW to draw the scale widget on the fly for each theme because the look was so much better than
        the native looks. Hopefully this will not be a noticeable performance issue, and it does require you to pip install
        pillow (PIL).

        I decided to use the clam theme as the base for much of this project because it provides a lot of flexibility when
        it comes to borders. Because the clam theme has an outer border and an inner border (light & dark), I am able to use
        the states to create a focus ring effect that is similar to what you would find with a CSS Boostrap theme. There
        are many cool tricks and hacks that you can tease out of the existing set of themes,  so I hope you enjoy this
        library as well as using the bones to create something of your own.

    USING STANDARD TK WIDGETS (WARNING):
        There are some widgets in TTK that borrow from standard TK widgets, such as the popdown list in the TTK
        combobox, or the dropdown menu. To make sure the style for these legacy widgets is consistent, I've created
        a StyleTK class that takes care of styling these widgets. However, because with TK the styling is
        tightly-coupled with the widget creation, you cannot easily change the style of a widget that is built with
        standard TK options --- unlike with TTK, which separates the style and structure of the elements. So, if you
        plan to do anything fancy, like support light and dark changeable themes, you'll need to make sure you
        create a mechanism for manually configuring the style of the standard TK widget. You can also destroy and then
        re-create the window as I have done in the example (actually I'm building the entire inside frame and then
        rebuilding when the style changes).
"""
from PIL import ImageTk, Image, ImageDraw
from collections import namedtuple
from ._utils import brightness

VARIATIONS = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

ThemeSettings = namedtuple('ThemeSettings', ['name', 'type', 'font', 'primary', 'secondary', 'success', 'info',
                                             'warning', 'danger', 'bg', 'fg', 'selectbg', 'selectfg', 'light',
                                             'border', 'inputfg'])


class StylerTK:
    """
    A flat theme applied to standard tkinter widgets (THESE ARE NOT TTK WIDGETS). This can be used independent of the
    Themed TTK widgets, but it is primary designed to supplement the few widgets that are used in conjunction with the
    TTK widgets. So, please be aware that standard tkinter widgets may not have the desired look.
    """

    def __init__(self, parent):
        self.master=parent.style.master
        self.settings=parent.settings

    def set_option(self, *args):
        self.master.option_add(*args)

    def apply_style(self):
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
        self.set_option('*background', self.settings.bg)
        self.set_option('*font', 'Helvetica')
        self.set_option('*borderWidth', 0)
        self.set_option('*relief', 'flat')
        self.set_option('*activeBackground', self.settings.selectbg)
        self.set_option('*activeForeground', self.settings.selectfg)
        self.set_option('*selectBackground', self.settings.selectbg)
        self.set_option('*selectForeground', self.settings.selectfg)

    def style_button(self):
        self.set_option('*Button.foreground', self.settings.selectfg)
        self.set_option('*Button.background', self.settings.primary)

    def style_label(self):
        self.set_option('*Label.foreground', self.settings.fg)
        self.set_option('*Label.background', self.settings.bg)

    def style_checkbutton(self):
        self.set_option('*Checkbutton.background', self.settings.bg)
        self.set_option('*Checkbutton.foreground', self.settings.fg)
        self.set_option('*Checkbutton.selectColor',
                        self.settings.primary if self.settings.type == 'dark' else 'white')

    def style_radiobutton(self):
        self.set_option('*Radiobutton.background', self.settings.bg)
        self.set_option('*Radiobutton.foreground', self.settings.fg)
        self.set_option('*Radiobutton.selectColor',
                        self.settings.primary if self.settings.type == 'dark' else 'white')

    def style_entry(self):
        self.set_option('*Entry.relief', 'flat')
        self.set_option('*Entry.background',
                        (self.settings.light if self.settings.type == 'light' else
                         brightness(self.settings.light, -0.1)))
        self.set_option('*Entry.foreground', self.settings.fg)
        self.set_option('*Entry.highlightThickness', 1)
        self.set_option('*Entry.highlightBackground', self.settings.border)
        self.set_option('*Entry.highlightColor', self.settings.primary)

    def style_scale(self):
        self.set_option('*Scale.background', self.settings.primary)
        self.set_option('*Scale.showValue', False)
        self.set_option('*Scale.sliderRelief', 'flat')
        self.set_option('*Scale.highlightThickness', 1)
        self.set_option('*Scale.highlightColor', self.settings.primary)
        self.set_option('*Scale.highlightBackground', self.settings.border)
        self.set_option('*Scale.troughColor',
                        (self.settings.light if self.settings.type == 'light' else
                         brightness(self.settings.light, -0.1)))

    def style_spinbox(self):
        self.set_option('*Spinbox.foreground', self.settings.fg)
        self.set_option('*Spinbox.background',
                        (self.settings.light if self.settings.type == 'light' else
                         brightness(self.settings.light, -0.1)))
        self.set_option('*Spinbox.highlightThickness', 1)
        self.set_option('*Spinbox.highlightColor', self.settings.primary)
        self.set_option('*Spinbox.highlightBackground', self.settings.border)

    def style_listbox(self):
        self.set_option('*Listbox.foreground', self.settings.fg)
        self.set_option('*Listbox.background',
                        (self.settings.light if self.settings.type == 'light' else
                         brightness(self.settings.light, -0.1)))
        self.set_option('*Listbox.relief', 'flat')
        self.set_option('*Listbox.activeStyle', 'none')
        self.set_option('*Listbox.highlightThickness', 1)
        self.set_option('*Listbox.highlightColor', self.settings.primary)
        self.set_option('*Listbox.highlightBackground', self.settings.border)

    def style_menubutton(self):
        self.set_option('*Menubutton.background', self.settings.primary)
        self.set_option('*Menubutton.foreground', self.settings.selectfg)

    def style_menu(self):
        self.set_option('*Menu.tearOff', 0)
        self.set_option('*Menu.foreground', self.settings.fg)
        self.set_option('*Menu.selectColor', self.settings.primary)

    def style_labelframe(self):
        self.set_option('*Labelframe.foreground', self.settings.fg)
        self.set_option('*Labelframe.highlightColor', self.settings.border)
        self.set_option('*Labelframe.highlightBackground', self.settings.border)
        self.set_option('*Labelframe.highlightThickness', 1)

    def style_scrollbar(self):
        # It does not appear to be possible to style the scrollbar on windows
        pass

    def style_optionmenu(self):
        """The widget constructor rejects all keyword arguments, so it cannot be set with options, only with
        configuration after the widget has been created."""
        pass


class StylerTTK:
    """
    A flat TTK theme created with built-in elements and a supplied color scheme. A theme type can be light or dark. This
    changes the way that certain elements are created for the theme.
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

    def lookup_color(self, color: str):
        """Lookup a color in the colors dictionary"""
        return self.settings._asdict().get(color)

    def style_defaults(self):
        """Setup the default ttk style settings"""
        self.style.configure('.',
                             background=self.settings.bg,
                             darkcolor=self.settings.border,
                             lightcolor=self.settings.border,
                             foreground=self.settings.fg,
                             troughcolor=self.settings.bg,
                             selectbg=self.settings.selectbg,
                             selectfg=self.settings.selectfg,
                             selectforeground=self.settings.selectfg,
                             selectbackground=self.settings.selectbg,
                             fieldbg='white',
                             font=(self.settings.font,),
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

        if self.settings.type == 'dark':
            self.style.element_create('Spinbox.field', 'from', 'default')

        self.style.element_create('Combobox.downarrow', 'from', 'default')
        self.style.element_create('Combobox.padding', 'from', 'clam')
        self.style.element_create('Combobox.textarea', 'from', 'clam')
        self.style.configure('TCombobox',
                             bordercolor=self.settings.border,
                             darkcolor=self.settings.bg,
                             lightcolor=self.settings.bg,
                             arrowcolor=self.settings.inputfg,
                             foreground=self.settings.inputfg,
                             fieldbackground=self.settings.light,
                             background=self.settings.light,
                             relief='flat',
                             borderwidth=0,
                             padding=5,
                             arrowsize=16)
        self.style.map('TCombobox',
                       bordercolor=[
                           ('focus', self.settings.primary),
                           ('hover', self.settings.primary)],
                       lightcolor=[
                           ('focus', self.settings.primary),
                           ('pressed', self.settings.primary)],
                       darkcolor=[
                           ('focus', self.settings.primary),
                           ('pressed', self.settings.primary)],
                       arrowcolor=[
                           ('pressed', self.settings.light),
                           ('focus', self.settings.inputfg),
                           ('hover', self.settings.primary)])

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
                               ('pressed', self.settings.light),
                               ('focus', self.settings.inputfg),
                               ('hover', self.settings.primary)])

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
                             troughcolor=brightness(self.settings.light, -0.05),
                             background=self.settings.primary)

        for v in VARIATIONS:
            self.style.configure(f'{v}.Horizontal.TProgressbar', background=self.lookup_color(v))
            self.style.configure(f'{v}.Vertical.TProgressbar', background=self.lookup_color(v))

    @staticmethod
    def create_slider_image(color, size=18):
        """Create a slider based on given size and color"""
        im = Image.new('RGBA', (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=color)
        return ImageTk.PhotoImage(im.resize((size, size), Image.LANCZOS))

    def style_scale(self):
        """
        Create a scale widget style

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
        self.scale_images['primary_regular'] = self.create_slider_image(self.settings.primary)
        self.scale_images['primary_pressed'] = self.create_slider_image(brightness(self.settings.primary, -0.2))
        self.scale_images['primary_hover'] = self.create_slider_image(brightness(self.settings.primary, -0.1))
        self.scale_images['trough'] = ImageTk.PhotoImage(
            Image.new('RGB', (8, 8), brightness(self.settings.light, -0.05)))

        # create new elements based on images
        self.style.element_create('Scale.track', 'image', self.scale_images['trough'])
        self.style.element_create('Scale.slider', 'image', self.scale_images['primary_regular'],
                                  ('pressed', self.scale_images['primary_pressed']),
                                  ('hover', self.scale_images['primary_hover']))

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
                             troughcolor=self.settings.light,
                             background=brightness(self.settings.light, -0.1),
                             arrowsize=16,
                             arrowcolor=self.settings.inputfg)

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
        if self.settings.type == 'dark':
            self.style.element_create('custom.Spinbox.field', 'from', 'default')

        self.style.configure('TSpinbox',
                             bordercolor=self.settings.border,
                             lightcolor=self.settings.bg,
                             darkcolor=self.settings.bg,
                             foreground=self.settings.inputfg,
                             borderwidth=0,
                             background=self.settings.light,
                             fieldbackground=self.settings.light,
                             relief='flat',
                             arrowcolor=self.settings.inputfg,
                             arrowsize=16,
                             padding=(10, 5))

        self.style.map('TSpinbox',
                       bordercolor=[
                           ('focus', self.settings.primary),
                           ('hover', self.settings.primary)],
                       arrowcolor=[
                           ('pressed', self.settings.primary),
                           ('focus', self.settings.inputfg),
                           ('hover', self.settings.inputfg)],
                       lightcolor=[('focus', self.settings.primary)],
                       darkcolor=[('focus', self.settings.primary)])

        # variation changes focus ring color
        for v in VARIATIONS:
            self.style.map(f'{v}.TSpinbox',
                           bordercolor=[
                               ('focus', self.lookup_color(v)),
                               ('hover', self.lookup_color(v))],
                           arrowcolor=[
                               ('pressed', self.lookup_color(v)),
                               ('pressed', self.settings.inputfg),
                               ('hover', self.settings.inputfg)],
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
                             background=self.settings.light,
                             foreground=self.settings.inputfg,
                             bordercolor=self.settings.border,
                             lightcolor=self.settings.bg,
                             darkcolor=self.settings.bg,
                             relief='raised' if self.settings.type == 'light' else 'flat',
                             padding=-1 if self.settings.type == 'light' else -2)

        self.style.map('Treeview',
                       background=[('selected', self.settings.selectbg)],
                       foreground=[('selected', self.settings.selectfg)],
                       bordercolor=[('focus', self.settings.border)])

        self.style.configure('Treeview.Heading',
                             background=self.settings.primary,
                             foreground=self.settings.selectfg,
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
                             background=self.settings.bg)

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
                             foreground=self.settings.selectfg,
                             background=self.settings.primary,
                             bordercolor=self.settings.primary,
                             darkcolor=self.settings.primary,
                             lightcolor=self.settings.primary,
                             anchor='center',
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TButton',
                       background=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.TButton',
                                 foreground=self.settings.selectfg,
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
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))])

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
                             foreground=self.settings.primary,
                             background=self.settings.bg,
                             bordercolor=self.settings.primary,
                             darkcolor=self.settings.bg,
                             lightcolor=self.settings.bg,
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TButton',
                       foreground=[
                           ('pressed', self.settings.selectfg),
                           ('hover', self.settings.selectfg)],
                       background=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.Outline.TButton',
                                 foreground=self.lookup_color(v),
                                 background=self.settings.bg,
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.settings.bg,
                                 lightcolor=self.settings.bg,
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.Outline.TButton',
                           foreground=[
                               ('pressed', self.settings.selectfg),
                               ('hover', self.settings.selectfg)],
                           background=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))])

    def style_entry(self):
        """
        Create an entry widget style

        Element Options:
            - Entry.field: bordercolor, lightcolor, darkcolor, fieldbackground
            - Entry.padding: padding, relief, shiftrelief
            - Entry.textarea: font, width        
        """
        self.style.configure('TEntry',
                             fieldbackground=self.settings.light,
                             bordercolor=self.settings.border,
                             lightcolor=self.settings.bg,
                             darkcolor=self.settings.bg,
                             foreground=self.settings.inputfg,
                             padding=5)

        self.style.map('TEntry',
                       bordercolor=[
                           ('hover', self.settings.primary),
                           ('focus', self.settings.primary)],
                       lightcolor=[
                           ('focus', self.settings.primary)],
                       darkcolor=[
                           ('focus', self.settings.primary)])

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
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Radiobutton.indicator', 'from', 'xpnative')

        self.style.configure('TRadiobutton',
                             indicatormargin=8,
                             indicatorsize=12,
                             upperbordercolor=self.settings.fg if self.settings.type == 'light' else self.settings.light,
                             lowerbordercolor=self.settings.fg if self.settings.type == 'light' else self.settings.light,
                             indicatorforeground=self.settings.fg if self.settings.type == 'light' else self.settings.bg)

        self.style.map('TRadiobutton',
                       foreground=[('active', self.settings.primary if (self.settings.type == 'light') else 'white')],
                       indicatorforeground=[
                           ('active', self.settings.primary if (self.settings.type == 'light') else 'black')])

        # variations change the indicator color
        for v in VARIATIONS:
            self.style.map(f'{v}.TRadiobutton',
                           foreground=[('active', brightness(self.lookup_color(v), -0.2))],
                           indicatorforeground=[('active', brightness(self.lookup_color(v), -0.2))])

    def style_label(self):
        """
         Create a label widget style

        Element Options:
            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength, embossed, image, stipple, background
        """
        self.style.configure('TLabel', foreground=self.settings.fg)
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
                             foreground=self.settings.fg,
                             relief='raised',
                             bordercolor=self.settings.border,
                             darkcolor=self.settings.bg,
                             lightcolor=self.settings.bg)

        self.style.configure('TLabelframe.Label', foreground=self.settings.fg)

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
        # Use xpnative if available; the buttons look so much better
        # TODO check for native options on Linux and MacOS
        if 'xpnative' in self.style.theme_names():
            self.style.element_create('Checkbutton.indicator', 'from', 'xpnative')

        self.style.configure('TCheckbutton',
                             foreground=self.settings.fg,
                             indicatorsize=10,
                             indicatormargin=10,
                             indicatorforeground=self.settings.selectfg)

        self.style.map('TCheckbutton',
                       indicatorbackground=[
                           ('active selected', brightness(self.settings.primary, -0.2)),
                           ('selected', self.settings.fg),
                           ('active !selected', self.settings.light)],
                       foreground=[('active', self.settings.primary)])

        # variations change indicator color
        for v in VARIATIONS:
            self.style.map(f'{v}.TCheckbutton',
                           indicatorbackground=[
                               ('active selected', brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.settings.fg),
                               ('active !selected', self.settings.light)],
                           indicatorforeground=[
                               ('active selected', brightness(self.lookup_color(v), -0.2)),
                               ('selected', self.lookup_color(v))],
                           foreground=[
                               ('active', brightness(self.lookup_color(v), -0.2))])

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
                             foreground=self.settings.selectfg,
                             background=self.settings.primary,
                             bordercolor=self.settings.primary,
                             darkcolor=self.settings.primary,
                             lightcolor=self.settings.primary,
                             arrowcolor=self.settings.bg if self.settings.type == 'light' else 'white',
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('TMenubutton',
                       background=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))])

        for v in VARIATIONS:
            self.style.configure(f'{v}.TMenubutton',
                                 foreground=self.settings.selectfg,
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
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))])

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
                             foreground=self.settings.primary,
                             background=self.settings.bg,
                             bordercolor=self.settings.primary,
                             darkcolor=self.settings.bg,
                             lightcolor=self.settings.bg,
                             arrowcolor=self.settings.primary,
                             arrowpadding=(0, 0, 15, 0),
                             relief='raised',
                             focusthickness=0,
                             focuscolor='',
                             padding=(10, 5))

        self.style.map('Outline.TMenubutton',
                       foreground=[
                           ('pressed', self.settings.selectfg),
                           ('hover', self.settings.selectfg)],
                       background=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       bordercolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       darkcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       lightcolor=[
                           ('pressed', brightness(self.settings.primary, -0.2)),
                           ('hover', brightness(self.settings.primary, -0.1))],
                       arrowcolor=[
                           ('pressed', self.settings.selectfg),
                           ('hover', self.settings.selectfg)])

        for v in VARIATIONS:
            self.style.configure(f'{v}.Outline.TMenubutton',
                                 foreground=self.lookup_color(v),
                                 background=self.settings.bg,
                                 bordercolor=self.lookup_color(v),
                                 darkcolor=self.settings.bg,
                                 lightcolor=self.settings.bg,
                                 arrowcolor=self.lookup_color(v),
                                 relief='raised',
                                 focusthickness=0,
                                 focuscolor='',
                                 padding=(10, 5))

            self.style.map(f'{v}.Outline.TMenubutton',
                           foreground=[
                               ('pressed', self.settings.fg),
                               ('hover', self.settings.fg)],
                           background=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           bordercolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           darkcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           lightcolor=[
                               ('pressed', brightness(self.lookup_color(v), -0.2)),
                               ('hover', brightness(self.lookup_color(v), -0.1))],
                           arrowcolor=[
                               ('pressed', self.settings.bg),
                               ('hover', self.settings.bg)])

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
                             bordercolor=self.settings.border,
                             borderwidth=1)

        self.style.configure('TNotebook.Tab',
                             bordercolor=self.settings.border,
                             foreground=self.settings.fg,
                             padding=(10, 5))

        self.style.map('TNotebook.Tab',
                       background=[('!selected', self.settings.light)],
                       lightcolor=[('!selected', self.settings.light)],
                       darkcolor=[('!selected', self.settings.light)],
                       bordercolor=[('!selected', self.settings.border)],
                       foreground=[('!selected', self.settings.inputfg)])
