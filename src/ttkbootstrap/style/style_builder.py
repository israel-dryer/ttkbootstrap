import tkinter as tk
from tkinter import font
from tkinter import ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style.colors import Colors
from PIL import Image, ImageDraw, ImageTk, ImageFont
from math import ceil


def get_image_name(image):
    return image._PhotoImage__photo.name


class ThemeDefinition:
    """A class to provide defined name, colors, and font settings for a
    ttkbootstrap theme."""

    def __init__(
        self, name, colors, themetype=LIGHT):
        """
        Parameters
        ----------
        name : str
            The name of the theme.

        colors : Dict[str, str]
            A dictionary containing the theme colors.

        themetype : str
            The type of theme: *light* or *dark*; default='light'.
        """
        self.name = name
        self.colors = Colors(**colors)
        self.type = themetype

    def __repr__(self):

        return " ".join(
            [
                f"name={self.name},",
                f"type={self.type},",
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
        self.builder = builder
        self.master = builder.style.master

    @property
    def theme(self) -> ThemeDefinition:
        return self.builder.theme

    @property
    def colors(self) -> Colors:
        return self.builder.theme.colors

    @property
    def is_light_theme(self) -> bool:
        return self.builder.theme.type == LIGHT

    def update_tk_style(self, widget: tk.Tk):
        widget.configure(background=self.colors.bg)

    def update_toplevel_style(self, widget: tk.Toplevel):
        widget.configure(background=self.colors.bg)

    def update_canvas_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Canvas``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            background=self.colors.bg,
            highlightthickness=1,
            highlightbackground=bordercolor
        )

    def update_button_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Button``"""
        background = self.colors.primary
        foreground = self.colors.selectfg
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.1)

        widget.configure(
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            borderwidth=0,
            activebackground=activebackground,
            highlightbackground=self.colors.selectfg,
        )

    def update_label_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Label``"""
        widget.configure(
            foreground=self.colors.fg,
            background=self.colors.bg
        )

    def update_frame_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Frame"""
        widget.configure(background=self.colors.bg)

    def update_checkbutton_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Checkbutton``"""
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg
        )

    def update_radiobutton_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Radiobutton``"""
        widget.configure(
            activebackground=self.colors.bg,
            activeforeground=self.colors.primary,
            background=self.colors.bg,
            foreground=self.colors.fg,
            selectcolor=self.colors.bg
        )

    def update_entry_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Entry``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            relief=tk.FLAT,
            highlightthickness=1,
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=1
        )

    def update_scale_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Scale``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        activecolor = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            showvalue=False,
            sliderrelief=tk.FLAT,
            borderwidth=0,
            activebackground=activecolor,
            highlightthickness=1,
            highlightcolor=bordercolor,
            highlightbackground=bordercolor,
            troughcolor=self.colors.inputbg
        )

    def update_spinbox_style(self, widget: tk.Widget):
        """Apply style to `tkinter.Spinbox``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            relief=tk.FLAT,
            highlightthickness=1,
            foreground=self.colors.inputfg,
            highlightbackground=bordercolor,
            highlightcolor=self.colors.primary,
            background=self.colors.inputbg,
            buttonbackground=self.colors.inputbg,
            insertbackground=self.colors.inputfg,
            insertwidth=1,

            # these options should work, but do not have any affect
            buttonuprelief=tk.FLAT,
            buttondownrelief=tk.SUNKEN
        )

    def update_listbox_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Listbox``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            foreground=self.colors.inputfg,
            background=self.colors.inputbg,
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            highlightcolor=self.colors.primary,
            highlightbackground=bordercolor,
            highlightthickness=1,
            activestyle="none",
            relief=tk.FLAT
        )

    def update_menubutton_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Menubutton``"""
        activebackground = Colors.update_hsv(self.colors.primary, vd=-0.2)
        widget.configure(
            background=self.colors.primary,
            foreground=self.colors.selectfg,
            activebackground=activebackground,
            activeforeground=self.colors.selectfg,
            borderwidth=0
        )

    def update_menu_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Menu``"""
        widget.configure(
            tearoff=False,
            activebackground=self.colors.selectbg,
            activeforeground=self.colors.selectfg,
            foreground=self.colors.fg,
            selectcolor=self.colors.primary,
            background=self.colors.bg,
            relief=tk.FLAT,
            borderwidth=0
        )

    def update_labelframe_style(self, widget: tk.Widget):
        """Apply style to ``tkinter.Labelframe``"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        widget.configure(
            highlightcolor=bordercolor,
            foreground=self.colors.fg,
            borderwidth=1,
            highlightthickness=0,
            background=self.colors.bg
        )

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
            selectbackground=self.colors.selectbg,
            selectforeground=self.colors.selectfg,
            insertwidth=1,
            highlightthickness=1,
            relief=tk.FLAT,
            padx=5,
            pady=5,
            font='TkDefaultFont'
        )


class StyleBuilderTTK:
    """A class to create a new ttk theme"""

    def __init__(self, style):
        """Create a new ttk theme by using a combination of built-in
        themes and some image-based elements using ``pillow``. A theme
        is generated at runtime and is available to use with the
        ``Style`` class methods. The base theme of all **ttkbootstrap**
        themes is *clam*. In many cases, widget layouts are re-created
        using an assortment of elements from various styles such as
        *clam*, *alt*, *default*, etc...

        Parameters
        ----------
        style : BootStyle
            An instance of ``BootStyle``.

        definition : ThemeDefinition
            An instance of ``ThemeDefinition``; used to create the
            theme settings.
        """
        self.style = style
        self.theme_images = {}
        self.builder_tk = StyleBuilderTK(self)
        self.create_theme()

    @staticmethod
    def name_to_method(method_name):
        func = getattr(StyleBuilderTTK, method_name)
        return func

    @property
    def colors(self) -> Colors:
        return self.style.theme.colors

    @property
    def is_light_theme(self) -> bool:
        return self.style.theme.type == LIGHT

    @property
    def theme(self) -> ThemeDefinition:
        return self.style.theme

    def scale_size(self, size):
        """Scale the size based on the scaling factor of ttk
        
        size : Union[int, List, Tuple]
            A single integer or an iterable of integers
        """
        BASELINE = 1.33398982438864281
        scaling = self.style.master.tk.call('tk', 'scaling')
        factor = scaling / BASELINE

        if isinstance(size, int) or isinstance(size, float):
            return ceil(size * factor)
        elif isinstance(size, tuple) or isinstance(size, list):
            return [ceil(x * factor) for x in size]

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal
        style methods.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self):
        """Update the settings dictionary that is used to create a
        theme. This is a wrapper on all the `_style_widget` methods
        which define the layout, configuration, and styling mapping
        for each ttk widget.
        """
        self.create_default_style()

    def create_default_style(self):
        """Setup the default ``ttk.Style`` configuration. These
        defaults are applied to any widget that contains these
        element options. This method should be called *first* before
        any other style is applied during theme creation.
        """
        self.style.configure(
            style=".",
            background=self.colors.bg,
            darkcolor=self.colors.border,
            foreground=self.colors.fg,
            troughcolor=self.colors.bg,
            selectbg=self.colors.selectbg,
            selectfg=self.colors.selectfg,
            selectforeground=self.colors.selectfg,
            selectbackground=self.colors.selectbg,
            fieldbg="white",
            borderwidth=1,
            focuscolor=''
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
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == '']):
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

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        self.style.configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            arrowcolor=self.colors.inputfg,
            foreground=self.colors.inputfg,
            fieldbackground=self.colors.inputbg,
            background=self.colors.inputbg,
            insertcolor=self.colors.inputfg,
            relief=tk.FLAT,
            padding=5,
            arrowsize=self.scale_size(12)
        )
        self.style.map(
            ttkstyle,
            background=[('readonly', readonly)],
            fieldbackground=[('readonly', readonly)],
            foreground=[("disabled", disabled_fg)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("pressed !disabled", focuscolor),
                ("readonly", readonly)
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

        hsize = self.scale_size([40, 1])
        vsize = self.scale_size([1, 40])

        # style colors
        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == '']):
            background = default_color
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'

        # horizontal separator
        h_element = h_ttkstyle.replace('.TS', '.S')
        h_img = ImageTk.PhotoImage(Image.new("RGB", self.scale_size(hsize), background))
        h_name = get_image_name(h_img)
        self.theme_images[h_name] = h_img

        self.style.element_create(f'{h_element}.separator', 'image', h_name)
        self.style.layout(
            h_ttkstyle,
            [(f'{h_element}.separator', {'sticky': tk.EW})]
        )

        # vertical separator
        v_element = v_ttkstyle.replace('.TS', '.S')
        v_img = ImageTk.PhotoImage(Image.new("RGB", self.scale_size(vsize), background))
        v_name = get_image_name(v_img)
        self.theme_images[v_name] = v_img
        self.style.element_create(f'{v_element}.separator', 'image', v_name)
        self.style.layout(
            v_ttkstyle,
            [(f'{v_element}.separator', {'sticky': tk.NS})]
        )
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_striped_progressbar_assets(self, thickness, colorname=DEFAULT):
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
        if any([colorname == DEFAULT, colorname == '']):
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

        _resized = img.resize((thickness, thickness), Image.LANCZOS)
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

        thickness = self.scale_size(12)

        if any([colorname == DEFAULT, colorname == '']):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)
            bordercolor = troughcolor

        # ( horizontal, vertical )
        images = self.create_striped_progressbar_assets(thickness, colorname)

        # horizontal progressbar
        h_element = h_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{h_element}.pbar', 'image', images[0],
                                  width=thickness, sticky=tk.EW
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
            troughcolor=troughcolor,
            thickness=thickness,
            bordercolor=bordercolor,
            borderwidth=1
        )

        # vertical progressbar
        v_element = v_ttkstyle.replace('.TP', '.P')
        self.style.element_create(f'{v_element}.pbar', 'image', images[1],
                                  width=thickness, sticky=tk.NS
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
            troughcolor=troughcolor,
            bordercolor=bordercolor,
            thickness=thickness,
            borderwidth=1
        )
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_progressbar_style(self, colorname=DEFAULT):
        """Create style configuration for ttk progressbar"""
        H_STYLE = 'Horizontal.TProgressbar'
        V_STYLE = 'Vertical.TProgressbar'

        thickness = self.scale_size(10)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
                bordercolor = self.colors.light
            else:
                troughcolor = self.colors.light
                bordercolor = troughcolor
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)        
            bordercolor = troughcolor

        if any([colorname == DEFAULT, colorname == '']):
            background = self.colors.primary
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{H_STYLE}'
            v_ttkstyle = f'{colorname}.{V_STYLE}'

        self.style.configure(
            h_ttkstyle,
            thickness=thickness,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
        )
        existing_elements = self.style.element_names()

        self.style.configure(
            v_ttkstyle,
            thickness=thickness,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=self.colors.border,
            pbarrelief=tk.FLAT,
            troughcolor=troughcolor,
        )
        existing_elements = self.style.element_names()        

        # horizontal progressbar
        h_element = h_ttkstyle.replace('.TP', '.P')
        trough_element = f'{h_element}.trough'
        pbar_element = f'{h_element}.pbar'
        if trough_element not in existing_elements:
            self.style.element_create(trough_element, 'from', TTK_CLAM)
            self.style.element_create(pbar_element, 'from', TTK_DEFAULT)

        self.style.layout(
            h_ttkstyle,
            [(trough_element, {'sticky': 'nswe', 'children':
                               [(pbar_element, {'side': 'left', 'sticky': 'ns'})]})]
        )
        self.style.configure(h_ttkstyle, background=background)

        # vertical progressbar
        v_element = v_ttkstyle.replace('.TP', '.P')
        trough_element = f'{v_element}.trough'
        pbar_element = f'{v_element}.pbar'
        if trough_element not in existing_elements:
            self.style.element_create(trough_element, 'from', TTK_CLAM)
            self.style.element_create(pbar_element, 'from', TTK_DEFAULT)
            self.style.configure(v_ttkstyle, background=background)
        self.style.layout(
            v_ttkstyle,
            [(trough_element, {'sticky': 'nswe', 'children':
                               [(pbar_element, {'side': 'bottom', 'sticky': 'we'})]})]
        )

        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)

    def create_scale_assets(self, colorname=DEFAULT, size=14):
        """Create a circle slider image based on given size and color;
        used in the slider widget.

        Parameters
        ----------
        colorname : str
            The color name to use as the primary color

        size : int
            The size diameter of the slider circle; default=16.

        Returns
        -------
        Tuple[str]
            A tuple of PhotoImage names.
        """
        size = self.scale_size(size)
        if self.is_light_theme:
            disabled_color = self.colors.border
            if colorname == LIGHT:
                track_color = self.colors.bg
            else:
                track_color = self.colors.light
        else:
            disabled_color = self.colors.selectbg
            track_color = Colors.update_hsv(self.colors.selectbg, vd=-0.2) 

        if any([colorname == DEFAULT, colorname == '']):
            normal_color = self.colors.primary
        else:
            normal_color = self.colors.get(colorname)

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
            Image.new("RGB", self.scale_size((40, 5)), track_color)
        )
        h_track_name = get_image_name(h_track_img)
        self.theme_images[h_track_name] = h_track_img

        # horizontal track
        v_track_img = ImageTk.PhotoImage(
            Image.new("RGB", self.scale_size((5, 40)), track_color)
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

        if any([colorname == DEFAULT, colorname == '']):
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
        FLOOD_FONT = '-size 14'

        if any([colorname == DEFAULT, colorname == '']):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
            background = self.colors.primary
        else:
            h_ttkstyle = f'{colorname}.{HSTYLE}'
            v_ttkstyle = f'{colorname}.{VSTYLE}'
            background = self.colors.get(colorname)

        if colorname == LIGHT:
            foreground = self.colors.fg
            troughcolor = self.colors.bg
        else:
            troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)
            foreground = self.colors.selectfg
        
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
            foreground=foreground,
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
            foreground=foreground,
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
            size = self.scale_size([11, 11])

            draw.line([2, 6, 2, 9], fill=color)
            draw.line([3, 5, 3, 8], fill=color)
            draw.line([4, 4, 4, 7], fill=color)
            draw.line([5, 3, 5, 6], fill=color)
            draw.line([6, 4, 6, 7], fill=color)
            draw.line([7, 5, 7, 8], fill=color)
            draw.line([8, 6, 8, 9], fill=color)

            img = img.resize(size, Image.CUBIC)

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

    def create_round_scrollbar_assets(self, thumbcolor, pressed, active):
        vsize = self.scale_size([9, 28])
        hsize = self.scale_size([28, 9])
        
        def rounded_rect(size, fill):
            x = size[0] * 10
            y = size[1] * 10
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            radius = min([x, y]) // 2
            draw.rounded_rectangle([0, 0, x-1, y-1], radius, fill)
            image = ImageTk.PhotoImage(img.resize(size, Image.CUBIC))
            name = get_image_name(image)
            self.theme_images[name] = image
            return name

        # create images
        h_normal_img = rounded_rect(hsize, thumbcolor)
        h_pressed_img = rounded_rect(hsize, pressed)
        h_active_img = rounded_rect(hsize, active)

        v_normal_img = rounded_rect(vsize, thumbcolor)
        v_pressed_img = rounded_rect(vsize, pressed)
        v_active_img = rounded_rect(vsize, active)

        return (
            h_normal_img, h_pressed_img, h_active_img,
            v_normal_img, v_pressed_img, v_active_img
        )

    def create_round_scrollbar_style(self, colorname=DEFAULT):
        """Create style configuration for ttk scrollbar: *ttk.Scrollbar* 
        This theme uses elements from the *alt* theme to build the widget 
        layout.
        """
        STYLE = 'TScrollbar'
        
        if any([colorname == DEFAULT, colorname == '']):
            h_ttkstyle = f'Round.Horizontal.{STYLE}'
            v_ttkstyle = f'Round.Vertical.{STYLE}'

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f'{colorname}.Round.Horizontal.{STYLE}'
            v_ttkstyle = f'{colorname}.Round.Vertical.{STYLE}'
            background = self.colors.get(colorname)

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)                  

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_round_scrollbar_assets(
            background, pressed, active
        )

        # horizontal scrollbar
        self.style.configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.style.element_create(
            f'{h_ttkstyle}.thumb', 'image', scroll_images[0],
            ('pressed', scroll_images[1]),
            ('active', scroll_images[2]),
            border=self.scale_size(9),
            padding=0,
            sticky=tk.EW,
        )
        self.style.layout(h_ttkstyle, [
            ('Horizontal.Scrollbar.trough', {'sticky': 'we', 'children': [
                ('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}), 
                ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}), 
                (f'{h_ttkstyle}.thumb', {'expand': '1', 'sticky': 'nswe'})]})
            ]
        )
        self.style.configure(h_ttkstyle, arrowcolor=background)        
        self.style.map(h_ttkstyle, arrowcolor=[('pressed', pressed), ('active', active)])
        
        # vertical scrollbar
        self.style.configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
        )
        self.style.element_create(
            f'{v_ttkstyle}.thumb', 'image', scroll_images[3],
            ('pressed', scroll_images[4]),
            ('active', scroll_images[5]),
            border=self.scale_size(9),
            padding=0,
            sticky=tk.NS,
         )
        self.style.layout(v_ttkstyle, [
            ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
                ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), 
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), 
                (f'{v_ttkstyle}.thumb', {'expand': '1', 'sticky': 'nswe'})]})
            ]
        )
        self.style.configure(v_ttkstyle, arrowcolor=background)        
        self.style.map(v_ttkstyle, arrowcolor=[('pressed', pressed), ('active', active)])

        # register ttkstyles
        self.style.register_ttkstyle(h_ttkstyle)
        self.style.register_ttkstyle(v_ttkstyle)  

    # def create_scrollbar_assets(
    #     self, thumbcolor, pressed, active, troughcolor, thickness
    # ):
        
    #     x = self.scale_size(thickness * 10)
    #     y = int(thickness * 3.5 * 10)
        
    #     def rounded_rect(x: int, y: int, fill: str):
    #         _img = Image.new('RGBA', (x, y))
    #         draw = ImageDraw.Draw(_img)
    #         xy = (1, 1, x-1, y-1)
    #         draw.rectangle(xy, fill, troughcolor, 1)
    #         image = ImageTk.PhotoImage(_img.resize((x//10, y//10)), Image.CUBIC)
    #         name = get_image_name(image)
    #         self.theme_images[name] = image
    #         return name

    #     # create images
    #     h_normal_img = rounded_rect(x, y, thumbcolor)
    #     h_pressed_img = rounded_rect(x, y, pressed)
    #     h_active_img = rounded_rect(x, y, active)

    #     v_normal_img = rounded_rect(y, x, thumbcolor)
    #     v_pressed_img = rounded_rect(y, x, pressed)
    #     v_active_img = rounded_rect(y, x, active)

    #     return (
    #         h_normal_img, h_pressed_img, h_active_img,
    #         v_normal_img, v_pressed_img, v_active_img
    #     )

    def create_scrollbar_assets(self, thumbcolor, pressed, active):
        vsize = self.scale_size([9, 28])
        hsize = self.scale_size([28, 9])
        
        def draw_rect(size, fill):
            x = size[0] * 10
            y = size[1] * 10
            img = Image.new('RGBA', (x, y))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, x-1, y-1], fill)
            image = ImageTk.PhotoImage(img.resize(size), Image.CUBIC)
            name = get_image_name(image)
            self.theme_images[name] = image
            return name

        # create images
        h_normal_img = draw_rect(hsize, thumbcolor)
        h_pressed_img = draw_rect(hsize, pressed)
        h_active_img = draw_rect(hsize, active)

        v_normal_img = draw_rect(vsize, thumbcolor)
        v_pressed_img = draw_rect(vsize, pressed)
        v_active_img = draw_rect(vsize, active)

        return (
            h_normal_img, h_pressed_img, h_active_img,
            v_normal_img, v_pressed_img, v_active_img
        )

    def create_scrollbar_style(self, colorname=DEFAULT):
        """Create style configuration for ttk scrollbar: *ttk.Scrollbar* 
        This theme uses elements from the *alt* theme to build the widget 
        layout.
        """
        STYLE = 'TScrollbar'
        
        if any([colorname == DEFAULT, colorname == '']):
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

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)                  

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_scrollbar_assets(background, pressed, active)

        # horizontal scrollbar
        self.style.configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.style.element_create(
            f'{h_ttkstyle}.thumb', 'image', scroll_images[0],
            ('pressed', scroll_images[1]),
            ('active', scroll_images[2]),
            border=(3, 0),
            sticky=tk.NSEW,
        )
        self.style.layout(h_ttkstyle, [
            ('Horizontal.Scrollbar.trough', {'sticky': 'we', 'children': [
                ('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}), 
                ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}), 
                (f'{h_ttkstyle}.thumb', {'expand': '1', 'sticky': 'nswe'})]})
            ]
        )
        self.style.configure(h_ttkstyle, arrowcolor=background)        
        self.style.map(h_ttkstyle, arrowcolor=[('pressed', pressed), ('active', active)])
        
        # vertical scrollbar
        self.style.configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            darkcolor=troughcolor,
            bordercolor=troughcolor,
            lightcolor=troughcolor,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=troughcolor,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.style.element_create(
            f'{v_ttkstyle}.thumb', 'image', scroll_images[3],
            ('pressed', scroll_images[4]),
            ('active', scroll_images[5]),
            border=(0, 3),
            sticky=tk.NSEW,
         )
        self.style.layout(v_ttkstyle, [
            ('Vertical.Scrollbar.trough', {'sticky': 'ns', 'children': [
                ('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), 
                ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), 
                (f'{v_ttkstyle}.thumb', {'expand': '1', 'sticky': 'nswe'})]})
            ]
        )
        self.style.configure(v_ttkstyle, arrowcolor=background)        
        self.style.map(v_ttkstyle, arrowcolor=[('pressed', pressed), ('active', active)])

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
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            focuscolor = self.colors.get(colorname)

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        if colorname == 'light':
            arrowfocus = self.colors.fg
        else:
            arrowfocus = focuscolor

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
            arrowsize=self.scale_size(12),
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            fieldbackground=[("readonly", readonly)],
            background=[("readonly", readonly)],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly)],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)],
            arrowcolor=[
                ("disabled !disabled", disabled_fg),
                ("pressed !disabled", arrowfocus),
                ("hover !disabled", arrowfocus)],
        )
        # register ttkstyles
        self.style.register_ttkstyle(ttkstyle)

    def create_treeview_style(self, colorname=DEFAULT):
        """Create style configuration for ttk treeview"""
        STYLE = 'Treeview'

        f = font.nametofont('TkDefaultFont')
        rowheight = f.metrics()['linespace']

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == '']):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f'{STYLE}.Heading'
            focuscolor = self.colors.primary
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            body_style = f'{colorname}.{STYLE}'
            header_style = f'{colorname}.{STYLE}.Heading'
            focuscolor = background
            bordercolor = focuscolor
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f'{colorname}.{STYLE}'
            header_style = f'{colorname}.{STYLE}.Heading'
            focuscolor = background
            bordercolor = focuscolor

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
            borderwidth=2,
            padding=0,
            rowheight=rowheight,
            relief=tk.RAISED
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
        
        try:
            self.style.element_create('Treeitem.indicator', 'from', TTK_ALT)
        except:
            pass
                                  
        # register ttkstyles
        self.style.register_ttkstyle(body_style)

    def create_frame_style(self, colorname=DEFAULT):
        """Create style configuration for ttk frame"""
        STYLE = 'TFrame'

        if any([colorname == DEFAULT, colorname == '']):
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

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
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

        if any([colorname == DEFAULT, colorname == '']):
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
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed)],
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

        if any([colorname == DEFAULT, colorname == '']):
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
            focusthickness=0,
            focuscolor=foreground,
            anchor=tk.CENTER,
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
        size = self.scale_size([24, 15])
        if any([colorname == DEFAULT, colorname == '']):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = self.colors.border
        else:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

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
        
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
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
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # toggle disabled
        _disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled_fg, width=6)
        draw.rectangle([18, 18, 110, 110], fill=disabled_fg)
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Image.LANCZOS)
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
        size = self.scale_size([24, 15])

        if any([colorname == DEFAULT, colorname == '']):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg

        if self.is_light_theme:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = self.colors.border
        else:
            off_border = self.colors.selectbg
            off_indicator = self.colors.selectbg
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

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
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
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
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
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
            _disabled.resize(size, Image.LANCZOS)
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
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # ( off, on, disabled )
        images = self.create_round_toggle_assets(colorname)

        try:
            width = self.scale_size(28)
            borderpad = self.scale_size(4)
            self.style.element_create(
                f'{ttkstyle}.indicator', 'image', images[1],
                ('disabled', images[2]),
                ('!selected', images[0]),
                width=width, border=borderpad, sticky=tk.W
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
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
        else:
            ttkstyle = f'{colorname}.{STYLE}'

        # ( off, on, disabled )
        images = self.create_square_toggle_assets(colorname)

        width = self.scale_size(28)
        borderpad = self.scale_size(4)

        self.style.element_create(
            f'{ttkstyle}.indicator', 'image', images[1],
            ('disabled', images[2]),
            ('!selected', images[0]),
            width=width, border=borderpad, sticky=tk.W
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

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            toggle_on = self.colors.get(colorname)

        foreground=self.colors.get_foreground(colorname)

        if self.is_light_theme:
            toggle_off = self.colors.border
        else:
            toggle_off = self.colors.selectbg

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
            foreground=[
                ("disabled", disabled_fg),
                ("hover", foreground),
                ("selected", foreground)
            ],
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

        if any([colorname == DEFAULT, colorname == '']):
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
            anchor=tk.CENTER,
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            arrowsize=3
        )        
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("selected !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed)],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover)],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover)],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover)],
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)

    def create_entry_style(self, colorname=DEFAULT):
        """Create style configuration for ttk entry"""

        STYLE = 'TEntry'

        # general default colors
        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, not colorname]):
            # default style
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            # colored style
            ttkstyle = f'{colorname}.{STYLE}'
            focuscolor = self.colors.get(colorname)
            bordercolor = focuscolor

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
            fieldbackground=[("readonly", readonly)],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor)],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly)],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly)],
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
        prime_color = self.colors.get(colorname)
        on_fill = prime_color
        off_fill = self.colors.bg
        on_indicator = self.colors.selectfg
        size = self.scale_size([14, 14])

        if self.is_light_theme:
            off_border = self.colors.border
            disabled = self.colors.border
            if colorname == LIGHT:
                on_indicator =  self.colors.dark
        else:
            disabled = Colors.update_hsv(self.colors.selectbg, vd=-0.3)
            off_border = self.colors.selectbg

        # radio off
        _off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_off)
        draw.ellipse(
            xy=[1, 1, 133, 133],
            outline=off_border,
            width=6,
            fill=off_fill
        )
        off_img = ImageTk.PhotoImage(_off.resize(size, Image.LANCZOS))
        off_name = get_image_name(off_img)
        self.theme_images[off_name] = off_img

        # radio on
        _on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_on)
        if colorname == LIGHT and self.is_light_theme:
            draw.ellipse(xy=[1, 1, 133, 133], outline=off_border, width=6)
        else:
            draw.ellipse(xy=[1, 1, 133, 133], fill=on_fill)
        draw.ellipse([40, 40, 94, 94], fill=on_indicator)
        on_img = ImageTk.PhotoImage(_on.resize(size, Image.LANCZOS))
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # radio disabled
        _disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(_disabled)
        draw.ellipse(
            xy=[1, 1, 133, 133],
            outline=disabled,
            width=3,
            fill=off_fill
        )
        disabled_img = ImageTk.PhotoImage(
            _disabled.resize(size, Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name

    def create_radiobutton_style(self, colorname=DEFAULT):
        """Create style configuration for ttk radiobutton"""

        STYLE = 'TRadiobutton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.selectbg, vd=-0.3)

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f'{colorname}.{STYLE}'

        # ( off, on, disabled )
        images = self.create_radiobutton_assets(colorname)
        width = self.scale_size(20)
        borderpad = self.scale_size(4)
        self.style.element_create(
            f'{ttkstyle}.indicator', 'image', images[1],
            ('disabled', images[2]),
            ('!selected', images[0]),
            width=width, border=borderpad, sticky=tk.W
        )
        self.style.map(ttkstyle, foreground=[('disabled', disabled_fg)]
        )
        self.style.configure(ttkstyle)
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

    def create_date_button_assets(self, foreground):
        """Draw a calendar button image of the specified color

        Returns
        -------
        str
            The PhotoImage name.
        """
        fill = foreground
        image = Image.new('RGBA', (210, 220))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle([10, 30, 200, 210], radius=20, outline=fill, width=10)

        calendar_image_coordinates = [
            # page spirals
            [40, 10, 50, 50], [100, 10, 110, 50], [160, 10, 170, 50],
            # row 1
            [70, 90, 90, 110], [110, 90, 130, 110], [150, 90, 170, 110],
            # row 2
            [30, 130, 50, 150], [70, 130, 90, 150], [110, 130, 130, 150], [150, 130, 170, 150],
            # row 3
            [30, 170, 50, 190], [70, 170, 90, 190], [110, 170, 130, 190]
        ]
        for xy in calendar_image_coordinates:
            draw.rectangle(xy=xy, fill=fill)

        size = self.scale_size([21, 22])
        tk_img = ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))
        tk_name = get_image_name(tk_img)
        self.theme_images[tk_name] = tk_img
        return tk_name
        
        
    def create_date_button_style(self, colorname=DEFAULT):
        """Create a solid date button style"""

        STYLE = 'Date.TButton'

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = self.colors.selectbg

        btn_foreground = Colors.get_foreground(self.colors, colorname)
        
        img_normal = self.create_date_button_assets(btn_foreground)

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.10)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(2, 2),
            anchor=tk.CENTER,
            image=img_normal
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            bordercolor=[
                ("disabled", disabled_fg)],
            darkcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)]
        )

        self.style.register_ttkstyle(ttkstyle)

    def create_calendar_style(self, colorname=DEFAULT):
        """Create style configuration for the date chooser"""

        STYLE = 'TCalendar'

        if any([colorname == DEFAULT, colorname == '']):
            prime_color = self.colors.primary
            ttkstyle = STYLE
            chevron_style = "Chevron.TButton"
        else:
            prime_color = self.colors.get(colorname)
            ttkstyle = f'{colorname}.{STYLE}'
            chevron_style = f"Chevron.{colorname}.TButton"

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
        self.style.configure(chevron_style, font='-size 14', focuscolor='')

        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)
        self.style.register_ttkstyle(chevron_style)

    def create_metersubtxt_label_style(self, colorname=DEFAULT):
        """Create default style for meter subtext label"""
        STYLE = 'Metersubtxt.TLabel'

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            if self.is_light_theme:
                foreground = self.colors.secondary
            else:
                foreground = self.colors.light
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            foreground = self.colors.get(colorname)

        background = self.colors.bg

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=background
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)        

    def create_meter_label_style(self, colorname=DEFAULT):
        """Create label style for meter widget"""
        
        STYLE = 'Meter.TLabel'
        
        # text color = `foreground`
        # trough color = `space`

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)        

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            background = self.colors.bg
            textcolor = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            textcolor = self.colors.get(colorname)
            background = self.colors.bg

        self.style.configure(
            ttkstyle,
            foreground=textcolor,
            background=background,
            space=troughcolor,
        )
        # register ttkstyle
        self.style.register_ttkstyle(ttkstyle)        

    def create_label_style(self, colorname=DEFAULT):
        """Create style configuration for ttk label"""

        STYLE = 'TLabel'

        if any([colorname == DEFAULT, colorname == '']):
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

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE_INVERSE
            background = self.colors.fg
            foreground = self.colors.bg
        else:
            ttkstyle = f'{colorname}.{STYLE_INVERSE}'
            background = self.colors.get(colorname)
            foreground = self.colors.get_foreground(colorname)

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

        if any([colorname == DEFAULT, colorname == '']):
            foreground = self.colors.fg
            ttkstyle = STYLE

            if self.is_light_theme:
                bordercolor = self.colors.border
            else:
                bordercolor = self.colors.selectbg

        else:
            foreground = self.colors.get(colorname)
            bordercolor = foreground
            ttkstyle = f'{colorname}.{STYLE}'

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

        if any([colorname == DEFAULT, colorname == '']):
            colorname = PRIMARY
            ttkstyle = STYLE
        else:
            ttkstyle = f'{colorname}.TCheckbutton'

        # ( off, on, disabled )
        images = self.create_checkbutton_assets(colorname)

        element = ttkstyle.replace('.TC', '.C')
        width = self.scale_size(20)
        borderpad = self.scale_size(4)
        self.style.element_create(f'{element}.indicator', 'image', images[1],
                                  ('disabled', images[2]),
                                  ('!selected', images[0]),
                                  width=width, border=borderpad, sticky=tk.W
                                  )
        self.style.configure(ttkstyle, foreground=self.colors.fg)
        self.style.map(ttkstyle, foreground=[('disabled', disabled_fg)])
        self.style.layout(
            ttkstyle,
            [
                ("Checkbutton.padding", {"children": [
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
            disabled_bg = self.colors.border
        else:
            disabled_bg = self.colors.selectbg

        if colorname == LIGHT:
            check_color = self.colors.dark
            on_border = check_color
        elif colorname == DARK:
            check_color = self.colors.light
            on_border = check_color
        else:
            check_color = self.colors.selectfg

        size = self.scale_size([14, 14])

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
            checkbutton_off.resize(size, Image.LANCZOS)
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
        
        draw.text((20, font_offset), "✓", font=fnt, fill=check_color)
        on_img = ImageTk.PhotoImage(
            checkbutton_on.resize(size, Image.LANCZOS)
        )
        on_name = get_image_name(on_img)
        self.theme_images[on_name] = on_img

        # checkbutton disabled
        checkbutton_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(checkbutton_disabled)
        draw.rounded_rectangle(
            [2, 2, 132, 132],
            radius=16,
            outline=disabled_bg,
            width=3
        )
        disabled_img = ImageTk.PhotoImage(
            checkbutton_disabled.resize(size, Image.LANCZOS)
        )
        disabled_name = get_image_name(disabled_img)
        self.theme_images[disabled_name] = disabled_img

        return off_name, on_name, disabled_name

    def create_menubutton_style(self, colorname=DEFAULT):
        """Apply a solid color style to ttk menubutton"""

        STYLE = 'TMenubutton'

        foreground = self.colors.get_foreground(colorname)

        if self.is_light_theme:
            disabled_fg = self.colors.border
            disabled_bg = self.colors.inputbg
        else:
            disabled_fg = self.colors.selectbg
            disabled_bg = Colors.update_hsv(disabled_fg, vd=-0.2)

        if any([colorname == DEFAULT, colorname == '']):
            ttkstyle = STYLE
            background = self.colors.primary
        else:
            ttkstyle = f'{colorname}.{STYLE}'
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.1)

        self.style.configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            arrowsize=self.scale_size(4),
            arrowcolor=foreground,
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

        if any([colorname == DEFAULT, colorname == '']):
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
            arrowcolor=foreground,
            arrowpadding=(0, 0, 15, 0),
            arrowsize=self.scale_size(4)
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
                ("pressed", pressed),
                ("hover", hover)],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            arrowcolor=[
                ("disabled", disabled_fg),
                ("pressed", foreground_pressed),
                ("hover", foreground_pressed)],
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

        if any([colorname == DEFAULT, colorname == '']):
            background = self.colors.inputbg
            selectfg = self.colors.fg
            ttkstyle = STYLE
        else:
            selectfg = self.colors.get_foreground(colorname)
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

        if any([colorname == DEFAULT, colorname == '']):
            sashcolor = default_color
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            sashcolor = self.colors.get(colorname)
            h_ttkstyle = f'{colorname}.{H_STYLE}'
            v_ttkstyle = f'{colorname}.{V_STYLE}'

        self.style.configure('Sash', gripcount=0, sashthickness=self.scale_size(2))
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
        from math import ceil
        
        box = self.scale_size(1)
        pad = box * 2
        chunk = box + pad # 4

        w = chunk * 3 + pad # 14
        h = chunk * 3 + pad # 14

        size = [w, h]

        im = Image.new("RGBA", size)
        draw = ImageDraw.Draw(im)

        draw.rectangle((chunk*2+pad, pad, chunk*3, chunk), fill=color)
        draw.rectangle((chunk*2+pad, chunk+pad, chunk*3, chunk*2), fill=color)
        draw.rectangle((chunk*2+pad, chunk*2+pad, chunk*3, chunk*3), fill=color)

        draw.rectangle((chunk+pad, chunk+pad, chunk*2, chunk*2), fill=color)
        draw.rectangle((chunk+pad, chunk*2+pad, chunk*2, chunk*3), fill=color)

        draw.rectangle((pad, chunk*2+pad, chunk, chunk*3), fill=color)

        _img = ImageTk.PhotoImage(im)
        _name = get_image_name(_img)
        self.theme_images[_name] = _img
        return _name

    def create_sizegrip_style(self, colorname=DEFAULT):
        """Create style configuration for ttk sizegrip"""

        STYLE = 'TSizegrip'

        if any([colorname == DEFAULT, colorname == '']):
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

    def update_combobox_popdown_style(self, widget):
        """Update the combobox popdown list and scrollbar"""
        if self.is_light_theme:
            bordercolor = self.colors.border
        else:
            bordercolor = self.colors.selectbg

        tk_settings = []
        tk_settings.extend(["-borderwidth", 2])
        tk_settings.extend(["-highlightthickness", 1])
        tk_settings.extend(["-highlightcolor", bordercolor])
        tk_settings.extend(["-background", self.colors.inputbg])
        tk_settings.extend(["-foreground", self.colors.inputfg])
        tk_settings.extend(["-selectbackground", self.colors.selectbg])
        tk_settings.extend(["-selectforeground", self.colors.selectfg])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f'{popdown}.f.sb', 'configure', '-style', sb_style)
