import tkinter as tk
from tkinter.ttk import Style
from ttkbootstrap.constants import *
from ttkbootstrap.style.colors import Colors
from PIL import Image, ImageDraw, ImageTk, ImageFont

def get_image_name(image):
    return image._PhotoImage__photo.name


class ThemeDefinition:
    """A class to provide defined name, colors, and font settings for a
    ttkbootstrap theme."""

    def __init__(
        self, name, colors, themetype=LIGHT, font=DEFAULT_FONT,
    ):
        """
        Parameters
        ----------
        name : str
            The name of the theme.

        colors : Dict[str, str]
            A dictionary containing the theme colors.

        themetype : str
            The type of theme: *light* or *dark*; default='light'.

        font : str
            The default font to use for the application;
            default='helvetica'.
        """
        self.name = name
        self.colors = Colors(**colors)
        self.type = themetype
        self.font = font

    def __repr__(self):

        return " ".join(
            [
                f"name={self.name},",
                f"type={self.type},",
                f"font={self.font},",
                f"colors={self.colors}",
            ]
        )

class StyleBuilderTK:
    """A class for styling tkinter widgets (not ttk)"""

    def __init__(self, builder):
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
        self.master = builder.style.master
        self.theme: ThemeDefinition = builder.theme

        self.colors = self.theme.colors
        self.is_light_theme = self.theme.type == LIGHT

    def _set_option(self, *args):
        """A convenience wrapper method to shorten the call to
        ``option_add``. *Laziness is next to godliness*.

        Parameters
        ----------
        *args : Tuple[str]
            (pattern, value, priority=80)
        """
        self.master.option_add(*args)

    @staticmethod
    def name_to_method(method_name):
        func = getattr(StyleBuilderTK, method_name)
        return func                

    def style_tkinter_widgets(self):
        """A wrapper on all widget style methods. Applies current theme
        to all standard tkinter widgets
        """
        self.update_spinbox_style()
        self.update_label_style()
        self.update_checkbutton_style()
        self.update_radiobutton_style()
        self.update_entry_style()
        self.update_scale_style()
        self.update_listbox_style()
        self.update_menu_style()
        self.update_menubutton_style()
        self.update_labelframe_style()
        self.update_canvas_style()
        self.update_window_style()        

    def update_window_style(self):
        """Apply global options to all matching ``tkinter`` widgets"""
        self.master.configure(background=self.colors.bg)
        self._set_option("*background", self.colors.bg, 60)
        self._set_option("*font", self.theme.font, 60)
        self._set_option("*activeBackground", self.colors.selectbg, 60)
        self._set_option("*activeForeground", self.colors.selectfg, 60)
        self._set_option("*selectBackground", self.colors.selectbg, 60)
        self._set_option("*selectForeground", self.colors.selectfg, 60)

    def update_canvas_style(self):
        """Apply style to ``tkinter.Canvas``"""
        self._set_option("*Canvas.highlightThickness", 1)
        self._set_option("*Canvas.background", self.colors.bg)
        self._set_option("*Canvas.highlightBackground", self.colors.border)

    def update_button_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Button``"""
        background = self.colors.primary
        foreground = self.colors.selectfg
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)

        if self.is_light_theme:
            disabledforeround = self.colors.border
        else:
            disabledforeround = self.colors.selectbg

        widget.configure(
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=activebackground,
            highlightbackground=self.colors.selectfg,
        )


    def update_label_style(self):
        """Apply style to ``tkinter.Label``"""
        self._set_option("*Label.foreground", self.colors.fg)
        self._set_option("*Label.background", self.colors.bg)

    def update_checkbutton_style(self):
        """Apply style to ``tkinter.Checkbutton``"""
        self._set_option("*Checkbutton.activeBackground", self.colors.bg)
        self._set_option("*Checkbutton.activeForeground", self.colors.primary)
        self._set_option("*Checkbutton.background", self.colors.bg)
        self._set_option("*Checkbutton.foreground", self.colors.fg)
        if not self.is_light_theme:
            self._set_option("*Checkbutton.selectColor", self.colors.primary)
        else:
            self._set_option("*Checkbutton.selectColor", "white")

    def update_radiobutton_style(self):
        """Apply style to ``tkinter.Radiobutton``"""
        self._set_option("*Radiobutton.activeBackground", self.colors.bg)
        self._set_option("*Radiobutton.activeForeground", self.colors.primary)
        self._set_option("*Radiobutton.background", self.colors.bg)
        self._set_option("*Radiobutton.foreground", self.colors.fg)
        if not self.is_light_theme:
            self._set_option("*Radiobutton.selectColor", self.colors.primary)
        else:
            self._set_option("*Checkbutton.selectColor", "white")

    def update_entry_style(self):
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

    def update_scale_style(self):
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

    def update_spinbox_style(self):
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

    def update_listbox_style(self):
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

    def update_menubutton_style(self):
        """Apply style to ``tkinter.Menubutton``"""
        hover_color = Colors.update_hsv(self.colors.primary, vd=-0.2)
        self._set_option("*Menubutton.background", self.colors.primary)
        self._set_option("*Menubutton.foreground", self.colors.selectfg)
        self._set_option("*Menubutton.activeBackground", hover_color)
        self._set_option("*Menubutton.borderWidth", 0)

    def update_menu_style(self):
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

    def update_labelframe_style(self):
        """Apply style to ``tkinter.Labelframe``"""
        self._set_option("*Labelframe.highlightColor", self.colors.border)
        self._set_option("*Labelframe.foreground", self.colors.fg)
        self._set_option("*Labelframe.font", self.theme.font)
        self._set_option("*Labelframe.borderWidth", 1)
        self._set_option("*Labelframe.highlightThickness", 0)

    def update_text_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Text``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg
        widget.configure(
            background=self.colors.inputbg,
            foreground=self.colors.inputfg,
            highlightcolor=self.colors.primary,
            highlightbackground=bordercolor,
            insertbackground=self.colors.inputfg,
            insertwidth=1,
            highlightthickness=1,
            relief=tk.FLAT,
            font=self.theme.font,
            padx=5,
            pady=5
        )


class StyleBuilderTTK:
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
        self.style: Style = style
        self.theme: ThemeDefinition = definition
        self.theme_images = {}
        self.colors = self.theme.colors
        self.is_light_theme = self.theme.type == LIGHT
        self.settings = {}
        self.builder_tk = StyleBuilderTK(self)
        self.create_theme()

    @staticmethod
    def name_to_method(method_name):
        func = getattr(StyleBuilderTTK, method_name)
        return func        

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal
        style methods.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self):
        """Update the settings dictionary that is used to create a
        theme. This is a wrapper on all the `_style_widget` methods
        which define the layout, configuration, and styling mapping
        for each ttk widget.
        """
        self.create_default_style()

        # widgets with orientation
        self.create_separator_style()
        self.create_progressbar_style()
        self.create_striped_progressbar_style()
        self.create_scale_style()
        self.create_scrollbar_style()
        self.create_floodgauge_style()
        self.create_panedwindow_style()

        # entry widgets            
        self.create_entry_style()
        self.create_combobox_style()
        self.create_spinbox_style()

        # button widgets
        self.create_button_style()
        self.create_outline_button_style()
        self.create_link_button_style()

        self.create_toolbutton_style()
        self.create_outline_toolbutton_style()

        self.create_menubutton_style()
        self.create_outline_menubutton_style()

        self.create_checkbutton_style()
        self.create_radiobutton_style()
        self.create_toggle_style()
        self.create_round_toggle_style()
        self.create_square_toggle_style()

        # other widgets
        self.create_label_style()
        self.create_inverse_label_style()
        self.create_frame_style()
        self.create_treeview_style()
        self.create_notebook_style()
        self.create_sizegrip_style()
        self.create_labelframe_style()

        # custom widgets
        self.create_calendar_style()
        self.create_meter_style()


    def create_default_style(self):
        """Setup the default ``ttk.Style`` configuration. These
        defaults are applied to any widget that contains these
        element options. This method should be called *first* before
        any other style is applied during theme creation.
        """
        self.style.configure(
            style=".",
            background= self.colors.bg,
            darkcolor= self.colors.border,
            foreground= self.colors.fg,
            troughcolor= self.colors.bg,
            selectbg= self.colors.selectbg,
            selectfg= self.colors.selectfg,
            selectforeground= self.colors.selectfg,
            selectbackground= self.colors.selectbg,
            fieldbg= "white",
            font= self.theme.font,
            borderwidth= 1,
            focuscolor= ''
        )

    def create_combobox_style(self, colorname=DEFAULT):
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

        if colorname == DEFAULT:
            ttkstyle = STYLE
            element = f"{ttkstyle.replace('TC','C')}"
            focuscolor = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            element = f"{ttkstyle.replace('TC','C')}"
            focuscolor = self.colors.get(colorname)
            
        self.style.element_create(f'{element}.downarrow', 'from', TTK_DEFAULT)
        self.style.element_create(f'{element}.padding', 'from', TTK_CLAM)
        self.style.element_create(f'{element}.textarea', 'from', TTK_CLAM)

        self.style.configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            arrowcolor=self.colors.inputfg,
            foreground=self.colors.inputfg,
            fieldbackground =self.colors.inputbg,
            background =self.colors.inputbg,
            insertcolor=self.colors.inputfg,
            relief=tk.FLAT,
            padding=5,
            arrowsize=13
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            bordercolor=[
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
            ],
            darkcolor=[
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
            ],
            arrowcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", focuscolor),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)]
        )
        self.style.layout(
            ttkstyle,
            [
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
        )
        self.style.register_ttkstyle(ttkstyle)

    def create_separator_style(self, colorname=DEFAULT):
        """Create style configuration for ttk separator:
        *ttk.Separator*. The default style for light will be border,
        but dark will be primary, as this makes the most sense for
        general use. However, all other colors will be available as
        well through styling.
        """
        HSTYLE = 'Horizontal.TSeparator'
        VSTYLE = 'Vertical.TSeparator'

        # style colors
        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if colorname == DEFAULT:
            background = default_color
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'

        # horizontal separator
        h_element = h_ttkstyle.replace('.TS', '.S')            
        h_img = ImageTk.PhotoImage(Image.new("RGB", (40, 1), background))
        h_name = get_image_name(h_img)
        self.theme_images[h_name] = h_img

        self.style.element_create(f'{h_element}.separator', 'image', h_name)
        self.style.layout(
            h_ttkstyle, 
            [(f'{h_element}.separator', {'sticky': tk.EW})]
        )

        # vertical separator
        v_element = v_ttkstyle.replace('.TS', '.S')
        v_img = ImageTk.PhotoImage(Image.new("RGB", (1, 40), background))
        v_name = get_image_name(v_img)
        self.theme_images[v_name] = v_img
        self.style.element_create(f'{v_element}.separator', 'image', v_name)
        self.style.layout(
            v_ttkstyle, 
            [(f'{v_element}.separator', {'sticky': tk.NS})]
        )
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_striped_progressbar_assets(self, colorname=DEFAULT):
        """Create the striped progressbar image and return as a
        ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property; eg.
            `primary`, `secondary`, `success`.

        Returns
        -------
        Tuple[str]
            A list of photoimage names.
        """
        if colorname == DEFAULT:
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
        return h_name, v_name

    def create_striped_progressbar_style(self, colorname=DEFAULT):
        """Apply a striped theme to the progressbar"""
        HSTYLE = 'Striped.Horizontal.TProgressbar'
        VSTYLE = 'Striped.Vertical.TProgressbar'

        if colorname == DEFAULT:
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'

        # ( horizontal, vertical )
        images = self.create_striped_progressbar_assets(colorname)

        # horizontal progressbar
        h_element = h_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{h_element}.pbar', 'image', images[0],
            width=16, sticky=tk.EW
        )
        self.style.layout(
            h_ttkstyle, 
            [
                (f"{h_element}.trough", {
                    "sticky": tk.NSEW,
                    "children": [
                        (f"{h_element}.pbar", {
                            "side": tk.LEFT,
                            "sticky": tk.NS})
                        ]
                    }
                )
            ]
        )
        self.style.configure(
            h_ttkstyle,
            troughcolor=self.colors.inputbg,
            thickness=16,
            borderwidth=1
        ) 

        # vertical progressbar
        v_element = v_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{v_element}.pbar', 'image', images[1],
            width=16, sticky=tk.NS
        )
        self.style.layout(
            v_ttkstyle,
            [
                (f"{v_element}.trough", {
                    "sticky": tk.NSEW,
                    "children": [
                        (f"{v_element}.pbar", {
                            "side": tk.BOTTOM,
                            "sticky": tk.EW})]
                    }
                )
            ]
        )
        self.style.configure(
            v_ttkstyle,
            troughcolor=self.colors.inputbg,
            thickness=16
        )
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_progressbar_style(self, colorname=DEFAULT):
        """Create style configuration for ttk progressbar"""
        H_STYLE = 'Horizontal.TProgressbar'
        V_STYLE = 'Vertical.TProgressbar'

        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.inputbg

        if colorname == DEFAULT:
            background = self.colors.primary
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{H_STYLE}'
            v_ttkstyle = f'{colorname}.{V_STYLE}'

        self.style.configure(
            'TProgressbar',
            thickness=14,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=self.colors.inputbg,
        )

         # horizontal progressbar
        h_element = h_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{h_element}.trough', 'from', TTK_CLAM)
        self.style.element_create(f'{h_element}.pbar', 'from', TTK_DEFAULT)
        self.style.configure(h_ttkstyle, background=background)

        # vertical progressbar
        v_element = v_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{v_element}.trough', 'from', TTK_CLAM)
        self.style.element_create(f'{v_element}.pbar', 'from', TTK_DEFAULT)
        self.style.configure(v_ttkstyle, background=background)

        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)


    def create_scale_assets(self, color_name=DEFAULT, size=16):
        """Create a circle slider image based on given size and color;
        used in the slider widget.

        Parameters
        ----------
        color_name : str
            The color name to use as the primary color

        size : int
            The size diameter of the slider circle; default=16.

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names.
        """
        if self.is_light_theme:
            disabled_color = self.colors.inputbg
            track_color = Colors.update_hsv(self.colors.inputbg, vd=-0.03)
        else:
            disabled_color = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            track_color = self.colors.inputbg

        if color_name == DEFAULT:
            normal_color = self.colors.primary
        else:
            normal_color = self.colors.get(color_name)

        pressed_color = Colors.update_hsv(normal_color, vd=-0.1)
        hover_color = Colors.update_hsv(normal_color, vd=0.1)

        # normal state
        _normal = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_normal)
        draw.ellipse((0, 0, 95, 95), fill=normal_color)
        normal_img = ImageTk.PhotoImage(
            _normal.resize((size, size), Image.LANCZOS)
        )
        normal_name = get_image_name(normal_img)
        self.theme_images[normal_name] = normal_img

        # pressed state
        _pressed = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_pressed)
        draw.ellipse((0, 0, 95, 95), fill=pressed_color)
        pressed_img = ImageTk.PhotoImage(
            _pressed.resize((size, size), Image.LANCZOS)
        )
        pressed_name = get_image_name(pressed_img)
        self.theme_images[pressed_name] = pressed_img

        # hover state
        _hover = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_hover)
        draw.ellipse((0, 0, 95, 95), fill=hover_color)
        hover_img = ImageTk.PhotoImage(
            _hover.resize((size, size), Image.LANCZOS)
        )
        hover_name = get_image_name(hover_img)
        self.theme_images[hover_name] = hover_img

        # disabled state
        _disabled = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse((0, 0, 95, 95), fill=disabled_color)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((size, size), Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img        

        # vertical track
        h_track_img = ImageTk.PhotoImage(
            Image.new("RGB", (40, 5), track_color)
        )
        h_track_name = get_image_name(h_track_img)
        self.theme_images[h_track_name] = h_track_img

        # horizontal track
        v_track_img = ImageTk.PhotoImage(
            Image.new("RGB", (5, 40), track_color)
        )
        v_track_name = get_image_name(v_track_img)
        self.theme_images[v_track_name] = v_track_img

        return (
            normal_name, pressed_name, hover_name, 
            disabled_name, h_track_name, v_track_name
        )

    def create_scale_style(self, colorname=DEFAULT):
        """Create style configuration for ttk scale: *ttk.Scale*"""
        STYLE = 'TScale'

        if colorname == DEFAULT:
            h_ttkstyle = f'Horizontal.{STYLE}'
            v_ttkstyle = f'Vertical.{STYLE}'
        else:
            h_ttkstyle = f'{colorname}.Horizontal.{STYLE}'
            v_ttkstyle = f'{colorname}.Vertical.{STYLE}'

        # ( normal, pressed, hover, disabled, htrack, vtrack )
        images = self.create_scale_assets(colorname)
        
        # horizontal scale
        h_element = h_ttkstyle.replace('.TS', '.S')
        self.style.element_create(f'{h_element}.slider', 'image', images[0],
            ('disabled', images[3]),
            ('pressed', images[1]),
            ('hover', images[2])
        )
        self.style.element_create(f'{h_element}.track', 'image', images[4])
        self.style.layout(
            h_ttkstyle,
            [
                (f'{h_element}.focus', {
                    "expand": "1",
                    "sticky": tk.NSEW,
                    "children": [
                        (f'{h_element}.track', {"sticky": tk.EW}),
                        (f'{h_element}.slider', {"side": tk.LEFT, "sticky": ""})
                    ]}
                )
            ]
        )
        # vertical scale
        v_element = v_ttkstyle.replace('.TS', '.S')
        self.style.element_create(f'{v_element}.slider', 'image', images[0],
            ('disabled', images[3]),
            ('pressed', images[1]),
            ('hover', images[2])
        )
        self.style.element_create(f'{v_element}.track', 'image', images[5])
        self.style.layout(
            v_ttkstyle,
            [
                (f'{v_element}.focus', {
                    "expand": "1",
                    "sticky": tk.NSEW,
                    "children": [
                        (f'{v_element}.track', {"sticky": tk.NS}),
                        (f'{v_element}.slider', {"side": tk.TOP, "sticky": ""})
                    ]}
                )
            ]   
        )
        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)


    def create_floodgauge_style(self, colorname=DEFAULT):
        """Create a style configuration for the *ttk.Progressbar* that makes 
        it into a floodgauge. Which is essentially a very large progress bar 
        with text in the middle.
        """
        HSTYLE = 'Horizontal.TFloodgauge'
        VSTYLE = 'Vertical.TFloodgauge'
        FLOOD_FONT = 'helvetica 14'

        if colorname == DEFAULT:
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
            background = self.colors.primary
        else:
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'
            background = self.colors.get(colorname)
        troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)

        # horizontal floodgauge
        h_element = h_ttkstyle.replace('.TF', '.F')
        self.style.element_create(f'{h_element}.trough', 'from', TTK_CLAM)
        self.style.element_create(f'{h_element}.pbar', 'from', TTK_DEFAULT)
        self.style.layout(
            h_ttkstyle, 
            [
                (f"{h_element}.trough", {"children": [
                    (f"{h_element}.pbar", {"sticky": tk.NS}),
                    ("Floodgauge.label", {"sticky": ""})], "sticky": tk.NSEW})
            ]
        )
        self.style.configure(
            h_ttkstyle,
            thickness=50,
            borderwidth=1,
            bordercolor=background,
            lightcolor=background,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
            background=background,
            foreground=self.colors.selectfg,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            font=FLOOD_FONT,            
        )
        # vertical floodgauge
        v_element = v_ttkstyle.replace('.TF', '.F')
        self.style.element_create(f'{v_element}.trough', 'from', TTK_CLAM)
        self.style.element_create(f'{v_element}.pbar', 'from', TTK_DEFAULT)
        self.style.layout(
            v_ttkstyle,
            [
                (f"{v_element}.trough", {"children": [
                    (f"{v_element}.pbar", {"sticky": tk.EW}),
                    ("Floodgauge.label", {"sticky": ""})], "sticky": tk.NSEW})
            ]
        )
        self.style.configure(
            v_ttkstyle,
            thickness=50,
            borderwidth=1,
            bordercolor=background,
            lightcolor=background,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
            background=background,
            foreground=self.colors.selectfg,
            justify=tk.CENTER,
            anchor=tk.CENTER,
            font=FLOOD_FONT,            
        )
        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_arrow_assets(self, arrowcolor, pressed, active):
        """Create horizontal and vertical arrow assets to be used for
        buttons"""

        def draw_arrow(color: str):

            img = Image.new("RGBA", (11, 11))
            draw = ImageDraw.Draw(img)

            draw.line([2, 6, 2, 9], fill=color)
            draw.line([3, 5, 3, 8], fill=color)
            draw.line([4, 4, 4, 7], fill=color)
            draw.line([5, 3, 5, 6], fill=color)
            draw.line([6, 4, 6, 7], fill=color)
            draw.line([7, 5, 7, 8], fill=color)
            draw.line([8, 6, 8, 9], fill=color)

            up_img = ImageTk.PhotoImage(img)
            up_name = get_image_name(up_img)
            self.theme_images[up_name] = up_img
            
            down_img = ImageTk.PhotoImage(img.rotate(180))
            down_name = get_image_name(down_img)
            self.theme_images[down_name] = down_img
            
            left_img = ImageTk.PhotoImage(img.rotate(90))
            left_name = get_image_name(left_img)
            self.theme_images[left_name] = left_img
            
            right_img = ImageTk.PhotoImage(img.rotate(-90))
            right_name = get_image_name(right_img)
            self.theme_images[right_name] = right_img

            return up_name, down_name, left_name, right_name

        normal_names = draw_arrow(arrowcolor)
        pressed_names = draw_arrow(pressed)
        active_names = draw_arrow(active)

        return normal_names, pressed_names, active_names

    def create_scrollbar_style(self, colorname=DEFAULT):
        """Create style configuration for ttk scrollbar: *ttk.Scrollbar* 
        This theme uses elements from the *alt* theme tobuild the widget 
        layout.
        """
        STYLE = 'TScrollbar'

        troughcolor = Colors.update_hsv(self.colors.bg, vd=-0.05)

        if colorname == DEFAULT:
            h_ttkstyle = f'Horizontal.{STYLE}'
            v_ttkstyle = f'Vertical.{STYLE}'

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f'{colorname}.Horizontal.{STYLE}'
            v_ttkstyle = f'{colorname}.Vertical.{STYLE}'
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        # ( normal, pressed, active ) ( up, down, left, right )
        images = self.create_arrow_assets(background, pressed, active)

        # vertical scrollbar
        v_element = v_ttkstyle.replace('.TS', '.S')
        self.style.element_create(f'{v_element}.trough', 'from', TTK_ALT)
        self.style.element_create(f'{v_element}.thumb', 'from', TTK_ALT)
        self.style.element_create(f'{v_element}.uparrow', 'image', 
            images[0][0], 
            ('pressed', images[1][0]),
            ('active', images[2][0])
        )
        self.style.element_create(f'{v_element}.downarrow', 'image', 
            images[0][1], 
            ('pressed', images[1][1]),
            ('active', images[2][1])
        )
        self.style.configure(
            v_ttkstyle,
            troughrelief=tk.FLAT,
            relief=tk.FLAT,
            troughborderwidth=1,
            troughcolor=troughcolor,
            background=background
        )
        self.style.map(
            v_ttkstyle, 
            background=[('pressed', pressed), ('active', active)]
        )
        self.style.layout(
            v_ttkstyle,
            [
                (f'{v_element}.trough', {
                    'sticky': tk.NS, 'children': [
                        (f'{v_element}.uparrow', 
                            {'side': tk.TOP, 'sticky': ''}), 
                        (f'{v_element}.downarrow', 
                            {'side': 'bottom', 'sticky': ''}), 
                        (f'{v_element}.thumb', 
                            {'expand': True, 'sticky': tk.NSEW})
                    ]}
                )
            ]
        )

        # horizontal scrollbar
        h_element = h_ttkstyle.replace('.T', '.')
        self.style.element_create(f'{h_element}.trough', 'from', TTK_ALT)
        self.style.element_create(f'{h_element}.thumb', 'from', TTK_ALT)
        self.style.element_create(f'{h_element}.leftarrow', 'image', 
            images[1][2], 
            ('pressed', images[1][2]),
            ('active', images[2][2])
        )
        self.style.element_create(f'{h_element}.rightarrow', 'image', 
            images[0][3],
            ('pressed', images[1][3]),
            ('active', images[2][3])
        )
        self.style.configure(
            h_ttkstyle,
            troughrelief=tk.FLAT,
            relief=tk.FLAT,
            troughborderwidth=1,
            troughcolor=troughcolor,
            background=background
        )
        self.style.map(
            h_ttkstyle, 
            background=[('pressed', pressed), ('active', active)]
        )        
        self.style.layout(
            h_ttkstyle,
            [
                (f'{h_element}.trough', {
                    'sticky': tk.EW, 'children': [
                (f'{h_element}.leftarrow', 
                    {'side': tk.LEFT, 'sticky': ''}), 
                (f'{h_element}.rightarrow', 
                    {'side': tk.RIGHT, 'sticky': ''}), 
                (f'{h_element}.thumb', 
                    {'expand': True, 'sticky': tk.NSEW})]
                })
            ]
        )
        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)


    def create_spinbox_style(self, colorname=DEFAULT):
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

        if colorname == DEFAULT:
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            focuscolor = self.colors.get(colorname)

        element = ttkstyle.replace('.TS', '.S')
        self.style.element_create(f'{element}.uparrow', 'from', TTK_DEFAULT)
        self.style.element_create(f'{element}.downarrow', 'from', TTK_DEFAULT)
        self.style.layout(
            ttkstyle, 
            [
                (f"{element}.field", 
                    {"side": tk.TOP, "sticky": tk.EW, "children": [
                        ("null", 
                            {"side": tk.RIGHT, "sticky": "", "children": [
                                (f"{element}.uparrow", 
                                    {"side": tk.TOP, "sticky": tk.E}),
                                (f"{element}.downarrow", 
                                    {"side": tk.BOTTOM, "sticky": tk.E})
                                ]
                            }
                        ),
                        (
                            f"{element}.padding", 
                                {"sticky": tk.NSEW, "children": [
                                    (f"{element}.textarea", 
                                        {"sticky": tk.NSEW})
                                    ]
                                }
                            )
                        ]
                    }
                )
            ]            
        )
        self.style.configure(
            ttkstyle, 
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            borderwidth=0,
            background=self.colors.inputbg,
            relief=tk.FLAT,
            arrowcolor=self.colors.inputfg,
            insertcolor=self.colors.inputfg,
            arrowsize=13,
            padding=(10, 5),            
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            lightcolor=[("focus !disabled", focuscolor)],
            darkcolor=[("focus !disabled", focuscolor)],
            bordercolor=[
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)],
            arrowcolor=[
                ("disabled !disabled", disabled_fg),
                ("pressed !disabled", focuscolor),
                ("hover !disabled", self.colors.inputfg)],
        )
        # register ttkstyles
        self.style.register_ttkstyle(ttkstyle)

    def create_treeview_style(self, colorname=DEFAULT):
        """Create style configuration for ttk treeview"""
        STYLE = 'Treeview'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg

        if colorname == DEFAULT:
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f'{STYLE}.Heading'
            item_style = 'Item'
            focuscolor = bordercolor
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f'{colorname}.{STYLE}'
            header_style = f'{colorname}.{STYLE}.Heading'
            item_style = f'{colorname}.Item'
            focuscolor = background

        # treeview header
        self.style.configure(
            header_style,
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            padding=5            
        )
        self.style.map(
            header_style,
            foreground=[("disabled", disabled_fg)],
            bordercolor=[("focus !disabled", background)],
        )
        # treeview body
        self.style.configure(
            body_style,
            background=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            bordercolor=bordercolor,
            lightcolor=self.colors.inputbg,
            darkcolor=self.colors.inputbg,            
        )
        self.style.map(
            body_style,
            background=[("selected", self.colors.selectbg)],
            foreground=[
                ("disabled", disabled_fg), 
                ("selected", self.colors.selectfg)],
            bordercolor=[
                ("disabled", bordercolor),
                ("focus", focuscolor),
                ("pressed", focuscolor),
                ("hover", focuscolor)],
            lightcolor=[("focus", focuscolor)],
            darkcolor=[("focus", focuscolor)]
        )
        self.style.layout(
            body_style,
            [
                ("Button.border",
                    {"sticky": tk.NSEW, "border": "1", "children": [
                        ("Treeview.padding", 
                            {"sticky": tk.NSEW, "children": [
                                ("Treeview.treearea", {"sticky": tk.NSEW})]
                            }
                        )
                    ]
                })
            ]
        )
        self.style.element_create(f'{item_style}.Treeitem.indicator', 
            'from', TTK_ALT
        )
        self.style.layout(
            item_style,
            [
                ('Treeitem.padding', {'sticky': 'nswe', 'children': [
                    (f'{item_style}.Treeitem.indicator', 
                        {'side': 'left', 'sticky': ''}), 
                    ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                    ('Treeitem.focus', 
                        {'side': 'left', 'sticky': '', 'children': [
                            ('Treeitem.text', {'side': 'left', 'sticky': ''})
                        ]}
                    )]}
                )
            ]
        )
        # register ttkstyles
        self.style.register_ttkstyle(body_style)
        self.style.register_ttkstyle(header_style)
        self.style.register_ttkstyle(item_style)

    def create_frame_style(self, colorname=DEFAULT):
        """Create style configuration for ttk frame"""
        STYLE = 'TFrame'

        if colorname == DEFAULT:
            ttkstyle = STYLE
            background = self.colors.bg
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            background = self.colors.get(colorname)

        self.style.configure(ttkstyle, background=background)
        
        # register style
        self.style.register_ttkstyle(ttkstyle)

    def create_button_style(self, colorname=DEFAULT):
        """Apply a solid color style to ttk button"""

        STYLE = 'TButton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
            disabled_bg = self.colors.inputbg
        else:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(disabled_fg, vd=-0.2)

        if colorname == DEFAULT:
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
            bordercolor = background
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)
            bordercolor = background
            
        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.10)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            bordercolor=[
                ("disabled", disabled_bg)],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_outline_button_style(self, colorname=DEFAULT):
        """Apply an outline style to ttk button. This button has a 
        solid button look on focus and hover.
        """
        STYLE = 'Outline.TButton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if colorname == LIGHT and self.is_light_theme:
            foreground = self.colors.fg
            foreground_pressed = foreground
            background = self.colors.bg
            bordercolor = self.colors.border
            pressed = self.colors.border
            hover = self.colors.border
            ttkstyle = f'{colorname}.{STYLE}'                
        else:
            if colorname == DEFAULT:
                ttkstyle = STYLE
                colorname = PRIMARY
            else:
                ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get(colorname)
            background = self.colors.get_foreground(colorname)
            foreground_pressed = background
            bordercolor = foreground
            pressed = foreground
            hover = foreground

        self.style.configure(
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
            anchor=tk.CENTER
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed)],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            focuscolor=[
                ("pressed !disabled", background),
                ("hover !disabled", background)],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_link_button_style(self, colorname=DEFAULT):
        """Apply a solid color style to ttk button"""
        STYLE = 'Link.TButton'

        pressed = self.colors.info
        hover = self.colors.info

        if colorname == DEFAULT:
            foreground = self.colors.primary
            ttkstyle = STYLE
        elif colorname == LIGHT:
            foreground = self.colors.fg
            ttkstyle = f'{colorname}.{STYLE}'
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            font=self.theme.font,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            shiftrelief=[("pressed !disabled", -1)],
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            focuscolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", pressed)],
            background=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg)],
            bordercolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg)],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg)],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg)]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_square_toggle_assets(self, colorname=DEFAULT):
        """Create a set of images for the square toggle button and 
        return as ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names.
        """
        if colorname == DEFAULT:
            colorname = PRIMARY
        
        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)

        else:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = self.colors.inputbg

        off_fill = self.colors.bg

        # toggle off
        _off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_off)
        draw.rectangle(
            xy=[1, 1, 225, 129],
            outline=off_border,
            width=6,
            fill=off_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=off_indicator)
        off_img = ImageTk.PhotoImage(_off.resize((24, 15), Image.LANCZOS))
        off_name = get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # toggle on
        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rectangle(
            xy=[1, 1, 225, 129],
            outline=on_border,
            width=6,
            fill=on_fill
        )
        draw.rectangle([18, 18, 110, 110], fill=on_indicator)
        _on = toggle_on.transpose(Image.ROTATE_180)
        on_img = ImageTk.PhotoImage(_on.resize((24, 15), Image.LANCZOS))
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # toggle disabled
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((24, 15), Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img
        
        return off_name, on_name, disabled_name

    def create_toggle_style(self, colorname=DEFAULT):
        """Create a toggle style. This method is the same as the
        `create_round_toggle_style` method, as round toggle is the
        default toggle style.
        """
        self.create_round_toggle_style(colorname)
        # STYLE = 'Toggle'

        # if self.is_light_theme:
        #     disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        # else:
        #     disabled_fg = self.colors.inputbg

        # if colorname == DEFAULT:
        #     ttkstyle = STYLE
        #     colorname = PRIMARY
        # else:
        #     ttkstyle = f"{colorname}.{STYLE}"

        # # ( off, on, disabled )
        # images = self.create_round_toggle_assets(colorname)

        # self.style.element_create(
        #     f'{ttkstyle}.indicator', 'image', images[1],
        #     ('disabled', images[2]),
        #     ('!selected', images[0]),
        #     width=28, border=4, sticky=tk.W
        # )
        # self.style.configure(
        #     ttkstyle,
        #     relief=tk.FLAT,
        #     borderwidth=0,
        #     padding=0,
        #     foreground=self.colors.fg,
        #     background=self.colors.bg
        # )
        # self.style.map(ttkstyle, 
        #     foreground=[('disabled', disabled_fg)],
        #     background=[('selected', self.colors.bg)]
        # )
        # self.style.layout(
        #     ttkstyle,
        #     [
        #         ("Toolbutton.border", {
        #             "sticky": tk.NSEW, "children": [
        #                 ("Toolbutton.padding", {
        #                     "sticky": tk.NSEW, "children": [
        #                         (f"{ttkstyle}.indicator", {"side": tk.LEFT}),
        #                         ("Toolbutton.label", {"side": tk.LEFT})]})]})
        #     ]
        # )
        # # register ttkstyle
        # self.style.register_ttkstyle(ttkstyle)     

    def create_round_toggle_assets(self, colorname=DEFAULT):
        """Create a set of images for the rounded toggle button and 
        return as ``PhotoImage``

        Parameters
        ----------
        colorname : str
            The color label assigned to the colors property

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names
        """
        if colorname == DEFAULT:
            colorname = PRIMARY

        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = self.colors.inputbg

        off_fill = self.colors.bg

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
        off_img = ImageTk.PhotoImage(_off.resize((24, 15), Image.LANCZOS))
        off_name = get_image_name(off_img)
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
        _on = _on.transpose(Image.ROTATE_180)
        on_img = ImageTk.PhotoImage(_on.resize((24, 15), Image.LANCZOS))
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # toggle disabled
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        draw.rounded_rectangle(
            xy=[1, 1, 225, 129],
            radius=(128 / 2),
            outline=disabled_fg,
            width=6
        )
        draw.ellipse([20, 18, 112, 110], fill=disabled_fg)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((24, 15), Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name

    def create_round_toggle_style(self, colorname=DEFAULT):
        """Apply a rounded toggle switch style to ttk widgets that accept 
        the toolbutton style (for example, a checkbutton: *ttk.Checkbutton*)
        """
        STYLE = 'Round.Toggle'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        if colorname == DEFAULT:
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.create_round_toggle_assets(colorname)

        try:
            self.style.element_create(
                f'{ttkstyle}.indicator', 'image', images[1],
                ('disabled', images[2]),
                ('!selected', images[0]),
                width=28, border=4, sticky=tk.W
            )
        except:
            """This method is used as the default Toggle style, so it
            is neccessary to catch Tcl Errors when it tries to create
            and element that was already created by the Toggle or 
            Round Toggle style"""
            pass
        
        self.style.configure(
            ttkstyle,
            relief=tk.FLAT,
            borderwidth=0,
            padding=0,
            foreground=self.colors.fg,
            background=self.colors.bg
        )
        self.style.map(ttkstyle, 
            foreground=[('disabled', disabled_fg)],
            background=[('selected', self.colors.bg)]
        )
        self.style.layout(
            ttkstyle,
            [
                ("Toolbutton.border", {
                    "sticky": tk.NSEW, "children": [
                        ("Toolbutton.padding", {
                            "sticky": tk.NSEW, "children": [
                                (f"{ttkstyle}.indicator", {"side": tk.LEFT}),
                                ("Toolbutton.label", {"side": tk.LEFT})]})]})
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_square_toggle_style(self, colorname=DEFAULT):
        """Apply a square toggle switch style to ttk widgets that 
        accept the toolbutton style
        """
        
        STYLE = 'Square.Toggle'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        if colorname == DEFAULT:
            ttkstyle = STYLE
        else:
            ttkstyle = f'{colorname}.{STYLE}'

        # ( off, on, disabled )
        images = self.create_square_toggle_assets(colorname)

        self.style.element_create(
            f'{ttkstyle}.indicator', 'image', images[1],
            ('disabled', images[2]),
            ('!selected', images[0]),
            width=28, border=4, sticky=tk.W
        )
        self.style.layout(
            ttkstyle,
            [
                ("Toolbutton.border", {
                    "sticky": tk.NSEW, "children": [
                        ("Toolbutton.padding", {
                            "sticky": tk.NSEW, "children": [
                                (f"{ttkstyle}.indicator", {"side": tk.LEFT}),
                                ("Toolbutton.label", {"side": tk.LEFT})]
                            }
                        )
                    ]
                })
            ]
        )
        self.style.configure(
            ttkstyle,
            relief=tk.FLAT,
            borderwidth=0,
            foreground=self.colors.fg
        )
        self.style.map(
            ttkstyle, 
            foreground=[('disabled', disabled_fg)],
            background=[
                ('selected', self.colors.bg), 
                ('!selected', self.colors.bg)
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_toolbutton_style(self, colorname=DEFAULT):
        """Apply a solid color style to ttk widgets that use the 
        Toolbutton style.
        """
        STYLE = 'Toolbutton'
        
        if colorname == DEFAULT:
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            toggle_on = self.colors.get(colorname)

        if self.is_light_theme:
            toggle_off = self.colors.selectbg
        else:
            toggle_off = self.colors.inputbg

        if self.is_light_theme:
            disabled_fg = self.colors.border
            disabled_bg = self.colors.inputbg
        else:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(disabled_fg, vd=-0.2)

        self.style.configure(
            ttkstyle,
            foreground=self.colors.selectfg,
            background=toggle_off,
            bordercolor=toggle_off,
            darkcolor=toggle_off,
            lightcolor=toggle_off,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor="",
            padding=(10, 5),
            anchor=tk.CENTER
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on)],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on)],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on)],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_outline_toolbutton_style(self, colorname=DEFAULT):
        """Apply an outline style to ttk widgets that use the 
        Toolbutton style. This button has a solid button look on focus 
        and hover.
        """
        STYLE = 'Outline.Toolbutton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if colorname == DEFAULT:
            ttkstyle = STYLE
            foreground = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get(colorname)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=foreground,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor="",
            borderwidth=1,
            padding=(10, 5),
            anchor=tk.CENTER
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg)],
            background=[
                ("pressed !disabled", foreground),
                ("selected !disabled", foreground),
                ("hover !disabled", foreground)],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground),
                ("selected !disabled", foreground),
                ("hover !disabled", foreground)],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", foreground),
                ("selected !disabled", foreground),
                ("hover !disabled", foreground)],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", foreground),
                ("selected !disabled", foreground),
                ("hover !disabled", foreground)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_entry_style(self, colorname=DEFAULT):
        """Create style configuration for ttk entry"""
        
        STYLE = 'TEntry'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg

        if colorname == DEFAULT:
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            focuscolor = self.colors.get(colorname)

        self.style.configure(
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
            bordercolor=[
                ("focus !disabled", focuscolor),
                ("hover !disabled", self.colors.bg)],
            lightcolor=[
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)],
            darkcolor=[
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_radiobutton_assets(self, colorname=DEFAULT):
        """Create radiobutton assets

        Parameters
        ----------
        colorname : str
            The name of the color to use for the button on state

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names
        """
        if colorname == DEFAULT:
            colorname = PRIMARY

        prime_color = self.colors.get(colorname)
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_border = self.colors.selectbg
        off_fill = self.colors.bg

        if self.is_light_theme:
            disabled = self.colors.border
        else:
            disabled = self.colors.inputbg

        # radio off
        _off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_off)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=off_border,
            width=6,
            fill=off_fill
        )
        off_img = ImageTk.PhotoImage(_off.resize((14, 14), Image.LANCZOS))
        off_name = get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # radio on
        _on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=on_fill,
            width=3,
            fill=on_fill
        )
        draw.ellipse([40, 40, 94, 94], fill=on_indicator)
        on_img = ImageTk.PhotoImage(_on.resize((14, 14), Image.LANCZOS))
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # radio disabled
        _disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse(
            xy=[2, 2, 132, 132],
            outline=disabled,
            width=3,
            fill=off_fill
        )
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize((14, 14), Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name

    def create_radiobutton_style(self, colorname=DEFAULT):
        """Create style configuration for ttk radiobutton"""

        STYLE = 'TRadiobutton'

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
        else:
            disabled_fg = self.colors.inputbg

        if colorname == DEFAULT:
            ttkstyle = STYLE
        else:
            ttkstyle = f'{colorname}.{STYLE}'

        # ( off, on, disabled )
        images = self.create_radiobutton_assets(colorname)

        self.style.element_create(
            f'{ttkstyle}.indicator', 'image', images[1],
            ('disabled', images[2]),
            ('!selected', images[0]),
            width=20, border=4, sticky=tk.W
        )
        self.style.map(ttkstyle, [('disabled', disabled_fg)])
        self.style.configure(ttkstyle, font=self.theme.font)
        self.style.layout(
            ttkstyle,
            [
                ("Radiobutton.padding", {"children": [
                    (f"{ttkstyle}.indicator", 
                        {"side": tk.LEFT, "sticky": ""}),
                    ("Radiobutton.focus", 
                        {"children": [
                            ("Radiobutton.label", 
                                {"sticky": tk.NSEW})
                            ],
                            "side": tk.LEFT, "sticky": ""})],
                            "sticky": tk.NSEW
                    }
                )
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_calendar_style(self, colorname=DEFAULT):
        """Create style configuration for the date chooser"""

        STYLE = 'TCalendar'

        if colorname == DEFAULT:
            prime_color = self.colors.primary
            ttkstyle = STYLE
            chevron_style = "chevron.TButton"
        else:
            prime_color = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'
            chevron_style = f"chevron.{colorname}.TButton"

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            pressed = Colors.update_hsv(prime_color, vd=-0.1)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            pressed = Colors.update_hsv(prime_color, vd=0.1)

        self.style.configure(
            ttkstyle,
            foreground=self.colors.fg,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor='',
            borderwidth=1,
            padding=(10, 5),
            anchor=tk.CENTER            
        )
        self.style.layout(
            ttkstyle,
            [
                ("Toolbutton.border", {"sticky": tk.NSEW, "children": [
                    ("Toolbutton.padding", {"sticky": tk.NSEW, "children": [
                        ("Toolbutton.label", {"sticky": tk.NSEW})]})]}
                )
            ]
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg)],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed)],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed)],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed)],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed)],
        )
        self.style.configure(chevron_style, font='helvetica 14')

        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)
        self.style.register_ttkstyle(chevron_style)        

    def create_meter_style(self, colorname=DEFAULT):
        """Create style configuration for the meter"""
        
        STYLE = 'TMeter'

        if colorname == DEFAULT:
            ttkstyle = STYLE
            foreground = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get(colorname)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg
        )
        self.style.layout(
            ttkstyle,
            [
                ("Label.border", 
                    {"sticky": tk.NSEW, "border": "1", "children": [
                        ("Label.padding", 
                            {"sticky": tk.NSEW, "border": "1", "children": [
                                ("Label.label", {"sticky": tk.NSEW})]
                            },
                        )
                    ],
                })
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)        

    def create_label_style(self, colorname=DEFAULT):
        """Create style configuration for ttk label"""

        STYLE = 'TLabel'

        if colorname == DEFAULT:
            ttkstyle = STYLE
            foreground = self.colors.fg
            background = self.colors.bg
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get(colorname)
            background = self.colors.bg

        # standard label
        self.style.configure(
            ttkstyle, 
            foreground=foreground, 
            background=background
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_inverse_label_style(self, colorname=DEFAULT):
        """Create inverse style configuration for ttk label"""

        STYLE_INVERSE = 'Inverse.TLabel'

        if colorname == DEFAULT:
            ttkstyle = STYLE_INVERSE
            background = self.colors.fg
            foreground = self.colors.bg
        else:
            ttkstyle = f'{colorname}.{STYLE_INVERSE}'
            foreground = self.colors.selectfg
            background = self.colors.get(colorname)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=background
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_labelframe_style(self, colorname=DEFAULT):
        """Create style configuration for ttk labelframe"""
        
        STYLE = 'TLabelframe'

        background = self.colors.bg
        
        if colorname == DEFAULT:
            foreground = self.colors.fg
            ttkstyle = STYLE
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'

        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        # create widget style
        self.style.configure(
            f'{ttkstyle}.Label',
            foreground=foreground,
            background=background,
        )
        self.style.configure(
            ttkstyle,
            relief=tk.RAISED,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=background,
            darkcolor=background,
            background=background
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_checkbutton_style(self, colorname=DEFAULT):
        """Create style configuration for ttk checkbutton"""
        
        STYLE = 'TCheckbutton'
        
        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if colorname == DEFAULT:
            colorname = PRIMARY
            ttkstyle = STYLE
        else:
            ttkstyle = f'{colorname}.TCheckbutton'

        # ( off, on, disabled )
        images = self.create_checkbutton_assets(colorname)

        element = ttkstyle.replace('.TC', '.C')
        self.style.element_create(f'{element}.indicator', 'image', images[1],
            ('disabled', images[2]),
            ('!selected', images[0]),
            width=20, border=4, sticky=tk.W
        )
        self.style.configure(ttkstyle, foreground=self.colors.fg)
        self.style.map(ttkstyle, foreground=[('disabled', disabled_fg)])
        self.style.layout(
            ttkstyle, 
            [
                ("Checkbutton.padding", { "children": [
                    (f'{element}.indicator', {"side": tk.LEFT, "sticky": ""}),
                    ("Checkbutton.focus", {"children": [
                        ("Checkbutton.label", {"sticky": tk.NSEW})],
                            "side": tk.LEFT, "sticky": ""})],
                        "sticky": tk.NSEW}
                )
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_checkbutton_assets(self, colorname=DEFAULT):
        """Create radiobutton assets

        Parameters
        ----------
        colorname : str
            The name of the color to use for the button on state

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names.
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
        off_fill = self.colors.bg

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            disabled_bg = self.colors.inputbg
        else:
            disabled_fg = self.colors.inputbg
            disabled_bg = disabled_fg

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
            checkbutton_off.resize((14, 14), Image.LANCZOS)
        )
        off_name = get_image_name(off_img)
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
        draw.text((20, font_offset), "✓", font=fnt, fill=self.colors.selectfg)
        on_img = ImageTk.PhotoImage(
            checkbutton_on.resize((14, 14), Image.LANCZOS)
        )
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # checkbutton disabled
        checkbutton_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            fill=disabled_bg,
        )
        disabled_img = ImageTk.PhotoImage(
            checkbutton_disabled.resize((14, 14), Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name

    def create_menubutton_style(self, colorname=DEFAULT):
        """Apply a solid color style to ttk menubutton"""

        STYLE = 'TMenubutton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
            disabled_bg = self.colors.inputbg
            arrowcolor = self.colors.bg
        else:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(disabled_fg, vd=-0.2)
            arrowcolor = self.colors.selectfg            

        if colorname == DEFAULT:
            ttkstyle = STYLE
            background = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.1)                

        self.style.configure(
            ttkstyle,
            foreground=self.colors.selectfg,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            arrowsize=3,
            arrowcolor=arrowcolor,
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
                ("hover !disabled", hover)],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_outline_menubutton_style(self, colorname=DEFAULT):
        """Apply and outline style to ttk menubutton"""

        STYLE = 'Outline.TMenubutton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if colorname == DEFAULT:
            foreground = self.colors.primary
            ttkstyle = STYLE
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=foreground,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg)],
            background=[
                ("pressed !disabled", foreground),
                ("hover !disabled", foreground)],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed", foreground),
                ("hover", foreground)],
            darkcolor=[
                ("pressed !disabled", foreground),
                ("hover !disabled", foreground)],
            lightcolor=[
                ("pressed !disabled", foreground),
                ("hover !disabled", foreground)],
            arrowcolor=[
                ("disabled", disabled_fg),
                ("pressed", self.colors.selectfg),
                ("hover", self.colors.selectfg)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             

    def create_notebook_style(self, colorname=DEFAULT):
        """Create style configuration for ttk notebook"""
        
        STYLE = 'TNotebook'

        if self.is_light_theme:
            bordercolor = self.colors.border
            foreground = self.colors.inputfg
        else:
            bordercolor = self.colors.selectbg
            foreground = self.colors.selectfg

        if colorname == DEFAULT:
            background = self.colors.inputbg
            selectfg = self.colors.fg
            ttkstyle = STYLE
        else:
            selectfg = self.colors.selectfg
            background = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'

        ttkstyle_tab = f'{ttkstyle}.Tab'

        # create widget style
        self.style.configure(
            ttkstyle,
            background=self.colors.bg,
            bordercolor=bordercolor,
            lightcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            tabmargins=(0, 1, 1, 0),
        )
        self.style.configure(
            ttkstyle_tab,
            focuscolor='',
            foreground=foreground,
            padding=(6, 5)
        )
        self.style.map(
            ttkstyle_tab,
            background=[
                ('selected', self.colors.bg),
                ('!selected', background)],
            lightcolor=[
                ('selected', self.colors.bg),
                ('!selected', background)],
            bordercolor=[
                ('selected', bordercolor),
                ('!selected', bordercolor)],
            padding=[
                ('selected', (6, 5)),
                ('!selected', (6, 5))],
            foreground=[
                ('selected', foreground),
                ('!selected', selectfg)]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)     

    def create_panedwindow_style(self, colorname=DEFAULT):
        """Create style configuration for ttk paned window"""

        H_STYLE = 'Horizontal.TPanedwindow'
        V_STYLE = 'Vertical.TPanedwindow'

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if colorname == DEFAULT:
            sashcolor = default_color
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            sashcolor = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{H_STYLE}'
            v_ttkstyle = f'{colorname}.{V_STYLE}'

        self.style.configure('Sash', gripcount=0, sashthickness=3)
        self.style.configure(h_ttkstyle, background=sashcolor)
        self.style.configure(v_ttkstyle, background=sashcolor)

        # register ttkstyle
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_sizegrip_assets(self, color):
        """Create assets for size grip

        Parameters
        ----------
        color : str
            The name of the color to use for the sizegrip images

        Returns
        -------
        str
            The PhotoImage name.
        """
        im = Image.new("RGBA", (14, 14))
        draw = ImageDraw.Draw(im)
        draw.rectangle((9, 3, 10, 4), fill=color)  # top
        draw.rectangle((6, 6, 7, 7), fill=color)   # middle
        draw.rectangle((9, 6, 10, 7), fill=color)
        draw.rectangle((3, 9, 4, 10), fill=color)  # bottom
        draw.rectangle((6, 9, 7, 10), fill=color)
        draw.rectangle((9, 9, 10, 10), fill=color)

        _img = ImageTk.PhotoImage(im)
        _name = get_image_name(_img)
        self.theme_images[_name] = _img
        return _name

    def create_sizegrip_style(self, colorname=DEFAULT):
        """Create style configuration for ttk sizegrip"""
        
        STYLE = 'TSizegrip'

        if colorname == DEFAULT:
            ttkstyle = STYLE

            if self.is_light_theme:
                grip_color = self.colors.border
            else:
                grip_color = self.colors.inputbg
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            grip_color = self.colors.get(colorname)
        
        image = self.create_sizegrip_assets(grip_color)
        
        self.style.element_create(
            f'{ttkstyle}.Sizegrip.sizegrip', 'image', image
        )
        self.style.layout(
            ttkstyle, 
            [
                (f'{ttkstyle}.Sizegrip.sizegrip', 
                {'side': tk.BOTTOM, 'sticky': tk.SE})
            ]
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)             
