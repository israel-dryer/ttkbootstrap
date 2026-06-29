"""TTK widget style builders for ttkbootstrap.

`StyleBuilderTTK` holds the ``create_*_style`` methods that build every ttk
style (and its image assets via the content-addressed cache). The largest module
in the package. Split out of the monolithic `style.py` in 2.0.
"""
import tkinter as tk
from math import ceil
from tkinter import font, ttk

from PIL import Image, ImageDraw, ImageTk
from PIL.Image import Resampling

from ttkbootstrap.constants import *
from ttkbootstrap.style.theme import Colors, ThemeDefinition
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.layout import (
    El, layout, image_element, state_map, StyleName,
)


class StyleBuilderTTK:
    """A class containing methods for building new ttk widget styles on
    demand.

    The methods in this classed are used internally to generate ttk
    widget styles on-demand and are not intended to be called by the end
    user.
    """

    def __init__(self, build: bool = True):
        # local import breaks the builders<-engine cycle (engine imports builders)
        from ttkbootstrap.style.engine import Style

        self.style: Style = Style.get_instance()
        self.builder_tk = StyleBuilderTK()

        if build:
            self.create_theme()

    @staticmethod
    def name_to_method(method_name):
        """Get a method by name.

        Parameters:

            method_name (str):
                The name of the style builder method.

        Returns:

            Callable:
                The method that is named by `method_name`
        """
        func = getattr(StyleBuilderTTK, method_name)
        return func

    @property
    def colors(self) -> Colors:
        """A reference to the `Colors` object of the current theme."""
        return self.style.theme.colors

    @property
    def theme(self) -> ThemeDefinition:
        """A reference to the `ThemeDefinition` object for the current
        theme."""
        return self.style.theme

    @property
    def is_light_theme(self) -> bool:
        """If the current theme is _light_, returns `True`, otherwise
        returns `False`."""
        return self.style.theme.type == LIGHT

    @property
    def assets(self) -> Assets:
        """A key-safe `Assets` facade bound to the engine image cache.

        Lazily constructed once per builder; the underlying cache lives on the
        shared `Style` singleton, so dedup is process-wide regardless of which
        builder created an asset.
        """
        cached = self.__dict__.get("_assets")
        if cached is None:
            cached = self.__dict__["_assets"] = Assets(self.style)
        return cached

    def configure(self, style, **options):
        """Configure a style without re-entering public bootstyle resolution.

        This is the builder-facing alias for the engine's raw configuration
        seam. Keeping the private call here prevents every recipe from coupling
        directly to `Style` internals.
        """
        self.style._build_configure(style, **options)

    def scale_size(self, size):
        """Scale the size of images and other assets based on the
        scaling factor of ttk to ensure that the image matches the
        screen resolution.

        Parameters:

            size (Union[int, List, Tuple]):
                A single integer or an iterable of integers
        """
        winsys = self.style.master.tk.call("tk", "windowingsystem")
        if winsys == "aqua":
            BASELINE = 1.000492368291482
        else:
            BASELINE = 1.33398982438864281
        scaling = self.style.master.tk.call("tk", "scaling")
        factor = scaling / BASELINE

        if isinstance(size, int) or isinstance(size, float):
            return ceil(size * factor)
        elif isinstance(size, tuple) or isinstance(size, list):
            return [ceil(x * factor) for x in size]

    def _create_indicator_spacer_asset(self):
        """Return the shared transparent image used between indicator and label."""
        size = self.scale_size((6, 1))

        def draw_spacer(_draw, _width, _height):
            pass

        return self.assets.image(size, draw_spacer, "indicator-spacer")

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal
        style methods.
        """
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self):
        """This method is called internally every time the theme is
        changed to update various components included in the body of
        the method."""
        self.create_default_style()

    def create_default_style(self):
        """Setup the default widget style configuration for the root
        ttk style "."; these defaults are applied to any widget that
        contains the configuration options updated by this style. This
        method should be called *first* before any other style is applied
        during theme creation.
        """
        self.configure(
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
            focuscolor="",
        )
        # build the default button style up front so that native ttk
        # widgets the application never instantiates directly -- e.g. the
        # ttk::button widgets in Tk's file/message dialogs on Linux -- pick
        # up the theme instead of falling back to the bare clam appearance.
        # Without this, an app that only creates styled buttons (e.g.
        # Outline.Toolbutton) would leave the base "TButton" unthemed and
        # any linked dialog would lose its button coloring (see #1062).
        self.create_button_style()

        # this is general style applied to the tableview
        self.create_link_button_style()
        self.style.configure("symbol.Link.TButton", font="-size 16")

        # this is the general style applied to the tooltip
        self.create_label_style()
        self.style.configure(
            style="tooltip.TLabel",
            background="#fffddd",
            foreground="#333",
            bordercolor="#888",
            borderwidth=1,
            darkcolor="#fffddd",
            lightcolor="#fffddd",
            relief=RAISED,
        )

    def create_combobox_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Combobox widget.

        Parameters:

            colorname (str):
                The color label to use as the primary widget color.
        """
        STYLE = "TCombobox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            element = f"{ttkstyle.replace('TC', 'C')}"
            focuscolor = self.colors.get(colorname)

        # Create custom arrow assets since the default ones don't work with Tcl/Tk bundled in python 3.13
        arrow_images = self.create_simple_arrow_assets(
            self.colors.inputfg,
            disabled_fg,
            focuscolor,
        )
        downarrow_image = arrow_images[0][1]
        downarrow_disabled_image = arrow_images[1][1]
        downarrow_focused_image = arrow_images[2][1]
        image_element(
            self.style, f"{element}.downarrow", default=downarrow_image,
            states={"disabled": downarrow_disabled_image,
                    "pressed !disabled": downarrow_focused_image,
                    "focus !disabled": downarrow_focused_image,
                    "hover !disabled": downarrow_focused_image},
            # right padding so the caret isn't flush against the border
            padding=(0, 0, self.scale_size(6), 0))
        #  self.style.element_create(f"{element}.downarrow", "from", TTK_DEFAULT)  # doesn't work in python 3.13
        self.style.element_create(f"{element}.padding", "from", TTK_CLAM)
        self.style.element_create(f"{element}.textarea", "from", TTK_CLAM)

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        self.configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            foreground=self.colors.inputfg,
            fieldbackground=self.colors.inputbg,
            background=self.colors.inputbg,
            insertcolor=self.colors.inputfg,
            relief=tk.FLAT,
            padding=5,
        )
        self.style.map(
            ttkstyle,
            background=[("readonly", readonly)],
            fieldbackground=[("readonly", readonly)],
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
                ("readonly", readonly),
            ],
        )
        layout(self.style, ttkstyle,
               El("combo.Spinbox.field", side=tk.TOP, sticky=tk.EW, children=[
                   El("Combobox.downarrow", side=tk.RIGHT, sticky=tk.S),
                   El("Combobox.padding", expand="1", sticky=tk.NSEW, children=[
                       El("Combobox.textarea", sticky=tk.NSEW)])]))
        self.style._register_ttkstyle(ttkstyle)
        try:
            self.create_scrollbar_style()
        except Exception:
            # style already created
            pass

    def create_separator_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Separator widget.

        Parameters:

            colorname (str):
                The primary widget color.
        """
        HSTYLE = "Horizontal.TSeparator"
        VSTYLE = "Vertical.TSeparator"

        hsize = [40, 1]
        vsize = [1, 40]

        # style colors
        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            background = default_color
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            background = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

        a = self.assets

        # horizontal separator
        h_element = h_ttkstyle.replace(".TS", ".S")
        h_name = a.rect(background, hsize)
        self.style.element_create(f"{h_element}.separator", "image", h_name)
        layout(self.style, h_ttkstyle,
               El(f"{h_element}.separator", sticky=tk.EW))

        # vertical separator
        v_element = v_ttkstyle.replace(".TS", ".S")
        v_name = a.rect(background, vsize)
        self.style.element_create(f"{v_element}.separator", "image", v_name)
        layout(self.style, v_ttkstyle,
               El(f"{v_element}.separator", sticky=tk.NS))
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_striped_progressbar_assets(self, thickness, colorname=DEFAULT):
        """Create the striped progressbar image and return as a
        `PhotoImage`

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            tuple[str]:
                A list of photoimage names.
        """
        if any([colorname == DEFAULT, colorname == ""]):
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
        a = self.assets

        # Diagonal stripe pattern over a barcolor_light field; the original
        # polygons were hand-fit to a 100-unit canvas, re-expressed here as
        # w/h-relative ratios. The vertical variant is the horizontal one
        # rotated 90 deg CCW.
        def draw_h(d, w, h):
            d.rectangle((0, 0, w, h), fill=barcolor_light)
            d.polygon([(0, 0), (0.48 * w, 0), (w, 0.52 * h), (w, h)], fill=barcolor)
            d.polygon([(0, 0.52 * h), (0.48 * w, h), (0, h)], fill=barcolor)

        def draw_v(d, w, h):
            d.rectangle((0, 0, w, h), fill=barcolor_light)
            d.polygon([(0, h), (0, 0.52 * h), (0.52 * w, 0), (w, 0)], fill=barcolor)
            d.polygon([(0.52 * w, h), (w, 0.52 * h), (w, h)], fill=barcolor)

        h_name = a.image((thickness, thickness), draw_h, barcolor, barcolor_light)
        v_name = a.image((thickness, thickness), draw_v, barcolor, barcolor_light)
        return h_name, v_name

    def create_striped_progressbar_style(self, colorname=DEFAULT):
        """Create a striped style for the ttk.Progressbar widget.

        Parameters:

            colorname (str):
                The primary widget color label.
        """
        HSTYLE = "Striped.Horizontal.TProgressbar"
        VSTYLE = "Striped.Vertical.TProgressbar"

        thickness = self.scale_size(12)

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"

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
        h_element = h_ttkstyle.replace(".TP", ".P")
        self.style.element_create(
            f"{h_element}.pbar",
            "image",
            images[0],
            width=thickness,
            sticky=tk.EW,
        )
        layout(self.style, h_ttkstyle,
               El(f"{h_element}.trough", sticky=tk.NSEW, children=[
                   El(f"{h_element}.pbar", side=tk.LEFT, sticky=tk.NS)]))
        self.configure(
            h_ttkstyle,
            troughcolor=troughcolor,
            thickness=thickness,
            bordercolor=bordercolor,
            borderwidth=1,
        )

        # vertical progressbar
        v_element = v_ttkstyle.replace(".TP", ".P")
        self.style.element_create(
            f"{v_element}.pbar",
            "image",
            images[1],
            width=thickness,
            sticky=tk.NS,
        )
        layout(self.style, v_ttkstyle,
               El(f"{v_element}.trough", sticky=tk.NSEW, children=[
                   El(f"{v_element}.pbar", side=tk.BOTTOM, sticky=tk.EW)]))
        self.configure(
            v_ttkstyle,
            troughcolor=troughcolor,
            bordercolor=bordercolor,
            thickness=thickness,
            borderwidth=1,
        )
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_progressbar_style(self, colorname=DEFAULT):
        """Create a solid ttk style for the ttk.Progressbar widget.

        Parameters:

            colorname (str):
                The primary widget color.
        """
        self._create_recolored_progressbar_style(
            colorname, asset_name="progressbar_default", type_name="")

    def create_thin_progressbar_style(self, colorname=DEFAULT):
        """Create the compact raster-backed ttk.Progressbar style."""
        self._create_recolored_progressbar_style(
            colorname, asset_name="progressbar_thin", type_name="Thin.")

    def _create_recolored_progressbar_style(
            self, colorname, *, asset_name, type_name):
        """Build horizontal and vertical progressbars from one source asset."""
        h_base = f"{type_name}Horizontal.TProgressbar"
        v_base = f"{type_name}Vertical.TProgressbar"
        if self.is_light_theme:
            troughcolor = (
                self.colors.bg if colorname == LIGHT else self.colors.light)
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        if colorname in (DEFAULT, ""):
            barcolor = self.colors.primary
            h_ttkstyle, v_ttkstyle = h_base, v_base
        else:
            barcolor = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{h_base}"
            v_ttkstyle = f"{colorname}.{v_base}"

        a = self.assets
        h_trough = a.recolor(
            asset_name, white=troughcolor, black=troughcolor)
        h_bar = a.recolor(asset_name, white=barcolor, black=barcolor)
        v_trough = a.recolor(
            asset_name, white=troughcolor, black=troughcolor,
            transform="rotate-90")
        v_bar = a.recolor(
            asset_name, white=barcolor, black=barcolor,
            transform="rotate-90")

        h_element = h_ttkstyle.replace(".TP", ".P")
        h_trough_name = f"{h_element}.trough"
        h_bar_name = f"{h_element}.pbar"
        image_element(
            self.style, h_trough_name, default=h_trough.image,
            border=h_trough.meta.border, padding=h_trough.meta.padding,
            sticky=tk.NSEW)
        image_element(
            self.style, h_bar_name, default=h_bar.image,
            border=h_bar.meta.border, padding=h_bar.meta.padding)
        layout(self.style, h_ttkstyle,
               El(h_trough_name, sticky=tk.NSEW, children=[
                   El(h_bar_name, side=tk.LEFT, sticky=tk.EW)]))

        v_element = v_ttkstyle.replace(".TP", ".P")
        v_trough_name = f"{v_element}.trough"
        v_bar_name = f"{v_element}.pbar"
        image_element(
            self.style, v_trough_name, default=v_trough.image,
            border=v_trough.meta.border, padding=v_trough.meta.padding,
            sticky=tk.NSEW)
        image_element(
            self.style, v_bar_name, default=v_bar.image,
            border=v_bar.meta.border, padding=v_bar.meta.padding)
        layout(self.style, v_ttkstyle,
               El(v_trough_name, sticky=tk.NSEW, children=[
                   El(v_bar_name, side=tk.BOTTOM, sticky=tk.NS)]))

        self.configure(
            h_ttkstyle, background=self.colors.bg, troughcolor=troughcolor,
            thickness=h_trough.meta.height, borderwidth=0)
        self.configure(
            v_ttkstyle, background=self.colors.bg, troughcolor=troughcolor,
            thickness=v_trough.meta.width, borderwidth=0)
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_scale_assets(self, colorname=DEFAULT):
        """Create the assets used for the ttk.Scale widget.

        The slider handle is automatically adjusted to fit the
        screen resolution.

        Parameters:

            colorname (str):
                The color label.

        Returns:

            tuple[RecolorResult, ...]:
                Recolored handle and track assets.
        """
        a = self.assets
        if self.is_light_theme:
            disabled_color = self.colors.border
            track_color = self.colors.bg if colorname == LIGHT else self.colors.light
        else:
            disabled_color = self.colors.selectbg
            track_color = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        if any([colorname == DEFAULT, colorname == ""]):
            normal_color = self.colors.primary
        else:
            normal_color = self.colors.get(colorname)
        pressed_color = Colors.update_hsv(normal_color, vd=-0.1)
        hover_color = Colors.update_hsv(normal_color, vd=0.1)

        # ( normal, pressed, hover, disabled thumbs; horizontal, vertical track )
        return (
            a.recolor("slider_handle", white=self.colors.bg,
                      black=disabled_color, magenta=normal_color),
            a.recolor("slider_handle", white=self.colors.bg,
                      black=disabled_color, magenta=pressed_color),
            a.recolor("slider_handle", white=self.colors.bg,
                      black=disabled_color, magenta=hover_color),
            a.recolor("slider_handle", white=self.colors.bg,
                      black=disabled_color, magenta=disabled_color),
            a.recolor("slider_track", white=track_color, black=track_color),
            a.recolor("slider_track", white=track_color, black=track_color,
                      transform="rotate-90"),
        )

    def create_scale_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Scale widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        h = StyleName("TScale", colorname, orient="Horizontal")
        v = StyleName("TScale", colorname, orient="Vertical")

        # ( normal, pressed, hover, disabled, htrack, vtrack )
        images = self.create_scale_assets(colorname)

        # horizontal scale
        image_element(
            self.style, f"{h.element}.slider", default=images[0].image,
            states={"disabled": images[3].image, "pressed": images[1].image,
                    "hover": images[2].image},
            border=images[0].meta.border, padding=images[0].meta.padding)
        self.style.element_create(
            f"{h.element}.track", "image", images[4].image,
            border=images[4].meta.border, padding=images[4].meta.padding)
        layout(
            self.style, h.ttkstyle,
            El(f"{h.element}.focus", expand=1, sticky=NSEW, children=[
                El(f"{h.element}.track", sticky=EW),
                El(f"{h.element}.slider", side=LEFT, sticky="")]))

        # vertical scale
        image_element(
            self.style, f"{v.element}.slider", default=images[0].image,
            states={"disabled": images[3].image, "pressed": images[1].image,
                    "hover": images[2].image},
            border=images[0].meta.border, padding=images[0].meta.padding)
        self.style.element_create(
            f"{v.element}.track", "image", images[5].image,
            border=images[5].meta.border, padding=images[5].meta.padding)
        layout(
            self.style, v.ttkstyle,
            El(f"{v.element}.focus", expand=1, sticky=NSEW, children=[
                El(f"{v.element}.track", sticky=NS),
                El(f"{v.element}.slider", side=TOP, sticky="")]))


        # register ttkstyles
        self.style._register_ttkstyle(h.ttkstyle)
        self.style._register_ttkstyle(v.ttkstyle)

    def create_floodgauge_style(self, colorname=DEFAULT):
        """Create a ttk style for the ttkbootstrap.widgets.Floodgauge
        widget. This is a custom widget style that uses components of
        the progressbar and label.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        HSTYLE = "Horizontal.TFloodgauge"
        VSTYLE = "Vertical.TFloodgauge"
        FLOOD_FONT = "-size 14"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = HSTYLE
            v_ttkstyle = VSTYLE
            background = self.colors.primary
        else:
            h_ttkstyle = f"{colorname}.{HSTYLE}"
            v_ttkstyle = f"{colorname}.{VSTYLE}"
            background = self.colors.get(colorname)

        if colorname == LIGHT:
            foreground = self.colors.fg
            troughcolor = self.colors.bg
        else:
            troughcolor = Colors.update_hsv(background, sd=-0.3, vd=0.8)
            foreground = self.colors.selectfg

        # horizontal floodgauge
        h_element = h_ttkstyle.replace(".TF", ".F")
        self.style.element_create(f"{h_element}.trough", "from", TTK_CLAM)
        self.style.element_create(f"{h_element}.pbar", "from", TTK_DEFAULT)
        layout(self.style, h_ttkstyle,
               El(f"{h_element}.trough", sticky=tk.NSEW, children=[
                   El(f"{h_element}.pbar", sticky=tk.NS),
                   El("Floodgauge.label", sticky="")]))
        self.configure(
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
        v_element = v_ttkstyle.replace(".TF", ".F")
        self.style.element_create(f"{v_element}.trough", "from", TTK_CLAM)
        self.style.element_create(f"{v_element}.pbar", "from", TTK_DEFAULT)
        layout(self.style, v_ttkstyle,
               El(f"{v_element}.trough", sticky=tk.NSEW, children=[
                   El(f"{v_element}.pbar", sticky=tk.EW),
                   El("Floodgauge.label", sticky="")]))
        self.configure(
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
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_simple_arrow_assets(self, arrowcolor: str, disabledcolor: str, activecolor: str, y_offset: int = 0):
        """Create caret arrow assets using Bootstrap Icons glyphs.

        Used for Combobox and Spinbox indicators. Uses the solid `caret-*-fill`
        triangles so the indicators read consistently with the filled-triangle
        arrows elsewhere in the app (menubutton, datepicker header).

        The `y_offset` parameter is accepted for API compatibility but is no
        longer used (it was specific to the old hand-drawn triangle approach).

        Args:
            arrowcolor: The color value to use as the arrow fill color.
            disabledcolor: A second color value to use when the arrow is disabled.
            activecolor: A third color value to use when the arrow has focus.
            y_offset: Accepted for API compatibility; ignored.
        Returns:
            A nested tuple (normal, disabled, active), each a 4-tuple of Tcl
            image names in the order (up, down, left, right).
        """
        a = self.assets
        size = self.scale_size([13, 11])

        def make_arrows(color):
            up = a.icon("caret-up-fill", size, color)
            down = a.icon("caret-down-fill", size, color)
            left = a.icon("caret-left-fill", size, color)
            right = a.icon("caret-right-fill", size, color)
            return up, down, left, right

        return make_arrows(arrowcolor), make_arrows(disabledcolor), make_arrows(activecolor)

    def create_arrow_assets(self, arrowcolor, pressed, active):
        """Create arrow assets used for various widget buttons.

        !!! note
            This method is currently not being utilized.

        Parameters:

            arrowcolor (str):
                The color value to use as the arrow fill color.

            pressed (str):
                The color value to use when the arrow is pressed.

            active (str):
                The color value to use when the arrow is active or
                hovered.
        """

        def draw_arrow(color: str):
            size = self.scale_size([11, 11])

            def render(rotate):
                img = Image.new("RGBA", (11, 11))
                draw = ImageDraw.Draw(img)
                draw.line([2, 6, 2, 9], fill=color)
                draw.line([3, 5, 3, 8], fill=color)
                draw.line([4, 4, 4, 7], fill=color)
                draw.line([5, 3, 5, 6], fill=color)
                draw.line([6, 4, 6, 7], fill=color)
                draw.line([7, 5, 7, 8], fill=color)
                draw.line([8, 6, 8, 9], fill=color)
                img = img.resize(size, Resampling.BICUBIC)
                if rotate:
                    img = img.rotate(rotate)
                return ImageTk.PhotoImage(img)

            base = ("arrow.chevron", color, tuple(size))
            up_name = self.style._get_or_create_image(
                base + ("up",), lambda: render(0))
            down_name = self.style._get_or_create_image(
                base + ("down",), lambda: render(180))
            left_name = self.style._get_or_create_image(
                base + ("left",), lambda: render(90))
            right_name = self.style._get_or_create_image(
                base + ("right",), lambda: render(-90))
            return up_name, down_name, left_name, right_name

        normal_names = draw_arrow(arrowcolor)
        pressed_names = draw_arrow(pressed)
        active_names = draw_arrow(active)

        return normal_names, pressed_names, active_names

    def create_round_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create image assets to be used when building the round
        scrollbar style.

        Parameters:

            thumbcolor (str):
                The color value of the thumb in normal state.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        return self.create_scrollbar_assets(thumbcolor, pressed, active)

    def create_round_scrollbar_style(self, colorname=DEFAULT):
        """Create a round style for the ttk.Scrollbar widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScrollbar"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = f"Round.Horizontal.{STYLE}"
            v_ttkstyle = f"Round.Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Round.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Round.Vertical.{STYLE}"
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_round_scrollbar_assets(
            background, pressed, active
        )
        # horizontal scrollbar
        self.configure(
            h_ttkstyle,
            troughcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            bordercolor=self.colors.bg,
            lightcolor=self.colors.bg,
            background=self.colors.bg,
            relief=tk.FLAT,
            borderwidth=0,
        )
        image_element(
            self.style, f"{h_ttkstyle}.thumb", default=scroll_images[0].image,
            states={"pressed": scroll_images[1].image,
                    "active": scroll_images[2].image},
            border=scroll_images[0].meta.border,
            padding=scroll_images[0].meta.padding)
        layout(self.style, h_ttkstyle,
               El("Horizontal.Scrollbar.trough", sticky="we", children=[
                   El(f"{h_ttkstyle}.thumb", expand="1", sticky="we")]))

        # vertical scrollbar
        self.configure(
            v_ttkstyle,
            troughcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            bordercolor=self.colors.bg,
            lightcolor=self.colors.bg,
            background=self.colors.bg,
            relief=tk.FLAT,
        )
        image_element(
            self.style, f"{v_ttkstyle}.thumb", default=scroll_images[3].image,
            states={"pressed": scroll_images[4].image,
                    "active": scroll_images[5].image},
            border=scroll_images[3].meta.border,
            padding=scroll_images[3].meta.padding)
        layout(self.style, v_ttkstyle,
               El("Vertical.Scrollbar.trough", sticky="ns", children=[
                   El(f"{v_ttkstyle}.thumb", expand="1", sticky="ns")]))

        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create the image assets used to build the standard scrollbar
        style.

        Parameters:

            thumbcolor (str):
                The primary color value used to color the thumb.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        a = self.assets
        h_normal = a.recolor(
            "scrollbar_thumb", white=thumbcolor, black=thumbcolor)
        h_pressed = a.recolor(
            "scrollbar_thumb", white=pressed, black=pressed)
        h_active = a.recolor(
            "scrollbar_thumb", white=active, black=active)
        v_normal = a.recolor(
            "scrollbar_thumb", white=thumbcolor, black=thumbcolor,
            transform="rotate-90")
        v_pressed = a.recolor(
            "scrollbar_thumb", white=pressed, black=pressed,
            transform="rotate-90")
        v_active = a.recolor(
            "scrollbar_thumb", white=active, black=active,
            transform="rotate-90")
        return h_normal, h_pressed, h_active, v_normal, v_pressed, v_active

    def create_scrollbar_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Scrollbar widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TScrollbar"

        if any([colorname == DEFAULT, colorname == ""]):
            h_ttkstyle = f"Horizontal.{STYLE}"
            v_ttkstyle = f"Vertical.{STYLE}"

            if self.is_light_theme:
                background = self.colors.border
            else:
                background = self.colors.selectbg

        else:
            h_ttkstyle = f"{colorname}.Horizontal.{STYLE}"
            v_ttkstyle = f"{colorname}.Vertical.{STYLE}"
            background = self.colors.get(colorname)

        pressed = Colors.update_hsv(background, vd=-0.05)
        active = Colors.update_hsv(background, vd=0.05)

        scroll_images = self.create_scrollbar_assets(
            background, pressed, active
        )
        # horizontal scrollbar
        self.configure(
            h_ttkstyle,
            troughcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            bordercolor=self.colors.bg,
            lightcolor=self.colors.bg,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=self.colors.bg,
            relief=tk.FLAT,
            borderwidth=0,
        )
        image_element(
            self.style, f"{h_ttkstyle}.thumb", default=scroll_images[0].image,
            states={"pressed": scroll_images[1].image,
                    "active": scroll_images[2].image},
            border=scroll_images[0].meta.border,
            padding=scroll_images[0].meta.padding)
        layout(self.style, h_ttkstyle,
               El("Horizontal.Scrollbar.trough", sticky="we", children=[
                   El(f"{h_ttkstyle}.thumb", expand="1", sticky="we")]))

        # vertical scrollbar
        self.configure(
            v_ttkstyle,
            troughcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            bordercolor=self.colors.bg,
            lightcolor=self.colors.bg,
            arrowcolor=background,
            arrowsize=self.scale_size(11),
            background=self.colors.bg,
            relief=tk.FLAT,
            borderwidth=0,
        )
        image_element(
            self.style, f"{v_ttkstyle}.thumb", default=scroll_images[3].image,
            states={"pressed": scroll_images[4].image,
                    "active": scroll_images[5].image},
            border=scroll_images[3].meta.border,
            padding=scroll_images[3].meta.padding)
        layout(self.style, v_ttkstyle,
               El("Vertical.Scrollbar.trough", sticky="ns", children=[
                   El(f"{v_ttkstyle}.thumb", expand="1", sticky="ns")]))

        # register ttkstyles
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_spinbox_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Spinbox widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TSpinbox"

        if self.is_light_theme:
            disabled_fg = self.colors.border
            bordercolor = self.colors.border
            readonly = self.colors.light
        else:
            disabled_fg = self.colors.selectbg
            bordercolor = self.colors.selectbg
            readonly = bordercolor

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            focuscolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get(colorname)

        if all([colorname, colorname != DEFAULT]):
            bordercolor = focuscolor

        if colorname == "light":
            arrowfocus = self.colors.fg
        else:
            arrowfocus = focuscolor

        element = ttkstyle.replace(".TS", ".S")
        arrow_images = self.create_simple_arrow_assets(
            self.colors.inputfg, disabled_fg, arrowfocus, y_offset=2
        )
        uparrow_image = arrow_images[0][0]
        uparrow_disabled_image = arrow_images[1][0]
        uparrow_focus_image = arrow_images[2][0]
        downarrow_image = arrow_images[0][1]
        downarrow_disabled_image = arrow_images[1][1]
        downarrow_focus_image = arrow_images[2][1]

        # right padding so the carets aren't flush against the border
        arrow_pad = (0, 0, self.scale_size(6), 0)
        image_element(
            self.style, f"{element}.uparrow", default=uparrow_image,
            states={"disabled": uparrow_disabled_image,
                    "pressed !disabled": uparrow_focus_image,
                    "hover !disabled": uparrow_focus_image},
            padding=arrow_pad)
        image_element(
            self.style, f"{element}.downarrow", default=downarrow_image,
            states={"disabled": downarrow_disabled_image,
                    "pressed !disabled": downarrow_focus_image,
                    "hover !disabled": downarrow_focus_image},
            padding=arrow_pad)
        layout(self.style, ttkstyle,
               El(f"{element}.field", side=tk.TOP, sticky=tk.EW, children=[
                   El("null", side=tk.RIGHT, sticky="", children=[
                       El(f"{element}.uparrow", side=tk.TOP, sticky=tk.E),
                       El(f"{element}.downarrow", side=tk.BOTTOM, sticky=tk.E)]),
                   El(f"{element}.padding", sticky=tk.NSEW, children=[
                       El(f"{element}.textarea", sticky=tk.NSEW)])]))
        self.configure(
            ttkstyle,
            bordercolor=bordercolor,
            darkcolor=self.colors.inputbg,
            lightcolor=self.colors.inputbg,
            fieldbackground=self.colors.inputbg,
            foreground=self.colors.inputfg,
            borderwidth=0,
            background=self.colors.inputbg,
            relief=tk.FLAT,
            insertcolor=self.colors.inputfg,
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
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
            bordercolor=[
                ("invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("hover !disabled", focuscolor),
            ],
        )
        # register ttkstyles
        self.style._register_ttkstyle(ttkstyle)

    def create_table_treeview_style(self, colorname=DEFAULT):
        """Create a style for the Tableview widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Table.Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
            hover = Colors.update_hsv(self.colors.light, vd=-0.1)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg
            hover = Colors.update_hsv(self.colors.dark, vd=0.1)

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = Colors.update_hsv(background, vd=-0.1)
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            hover = Colors.update_hsv(background, vd=0.1)

        # treeview header
        self.configure(
            header_style,
            background=background,
            foreground=foreground,
            relief=RAISED,
            borderwidth=1,
            darkcolor=background,
            bordercolor=bordercolor,
            lightcolor=background,
            padding=5,
        )
        self.style.map(
            header_style,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("active !disabled", hover),
            ],
            darkcolor=[
                ("active !disabled", hover),
            ],
            lightcolor=[
                ("active !disabled", hover),
            ],
        )
        self.configure(
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
            relief=tk.RAISED,
        )
        self.style.map(
            body_style,
            background=[("selected", self.colors.selectbg)],
            foreground=[
                ("disabled", disabled_fg),
                ("selected", self.colors.selectfg),
            ],
        )
        layout(self.style, body_style,
               El("Button.border", sticky=tk.NSEW, border="1", children=[
                   El("Treeview.padding", sticky=tk.NSEW, children=[
                       El("Treeview.treearea", sticky=tk.NSEW)])]))
        # register ttkstyles
        self.style._register_ttkstyle(body_style)

    def create_treeview_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Treeview widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Treeview"

        f = font.nametofont("TkDefaultFont")
        rowheight = f.metrics()["linespace"]

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            bordercolor = self.colors.border
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            bordercolor = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            foreground = self.colors.inputfg
            body_style = STYLE
            header_style = f"{STYLE}.Heading"
            focuscolor = self.colors.primary
        elif colorname == LIGHT and self.is_light_theme:
            background = self.colors.get(colorname)
            foreground = self.colors.fg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor
        else:
            background = self.colors.get(colorname)
            foreground = self.colors.selectfg
            body_style = f"{colorname}.{STYLE}"
            header_style = f"{colorname}.{STYLE}.Heading"
            focuscolor = background
            bordercolor = focuscolor

        # treeview header
        self.configure(
            header_style,
            background=background,
            foreground=foreground,
            relief=tk.FLAT,
            padding=5,
        )
        self.style.map(
            header_style,
            foreground=[("disabled", disabled_fg)],
            bordercolor=[("focus !disabled", background)],
        )
        # treeview body
        self.configure(
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
            relief=tk.RAISED,
        )
        self.style.map(
            body_style,
            background=[("selected", self.colors.selectbg)],
            foreground=[
                ("disabled", disabled_fg),
                ("selected", self.colors.selectfg),
            ],
            bordercolor=[
                ("disabled", bordercolor),
                ("focus", focuscolor),
                ("pressed", focuscolor),
                ("hover", focuscolor),
            ],
            lightcolor=[("focus", focuscolor)],
            darkcolor=[("focus", focuscolor)],
        )
        layout(self.style, body_style,
               El("Button.border", sticky=tk.NSEW, border="1", children=[
                   El("Treeview.padding", sticky=tk.NSEW, children=[
                       El("Treeview.treearea", sticky=tk.NSEW)])]))

        try:
            self.style.element_create("Treeitem.indicator", "from", TTK_ALT)
        except:
            pass

        # register ttkstyles
        self.style._register_ttkstyle(body_style)

    def create_frame_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Frame widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TFrame"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get(colorname)

        self.configure(ttkstyle, background=background)

        # register style
        self.style._register_ttkstyle(ttkstyle)

    def create_button_style(self, colorname=DEFAULT):
        """Create a solid style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TButton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)

        bordercolor = background
        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        self.configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=bordercolor,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            focuscolor=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[("disabled", disabled_bg)],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_button_style(self, colorname=DEFAULT):
        """Create an outline style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.TButton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=bordercolor,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            focuscolor=[
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_link_button_style(self, colorname=DEFAULT):
        """Create a link button style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Link.TButton"

        pressed = self.colors.info
        hover = self.colors.info

        if any([colorname == DEFAULT, colorname == ""]):
            foreground = self.colors.fg
            ttkstyle = STYLE
        elif colorname == LIGHT:
            foreground = self.colors.fg
            ttkstyle = f"{colorname}.{STYLE}"
        else:
            foreground = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        self.configure(
            ttkstyle,
            foreground=foreground,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
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
                ("hover !disabled", hover),
            ],
            focuscolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            background=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            bordercolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", self.colors.bg),
                ("hover !disabled", self.colors.bg),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_toggle_style(self, colorname=DEFAULT):
        """Create a round toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
        """
        self.create_round_toggle_style(colorname)

    def create_round_toggle_style(self, colorname=DEFAULT):
        """Create a round toggle style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Round.Toggle"
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        fg_muted = Colors.make_transparent(0.40, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # Resolve the "on" accent; LIGHT/DARK on their own background need a
        # contrasting indicator (visual-check item: verify toggle aspect ratio
        # and LIGHT-on-light on the human spot-check).
        if colorname == LIGHT:
            accent = self.colors.dark
        elif colorname == DARK:
            accent = self.colors.light
        else:
            accent = self.colors.get(colorname)

        self.configure(
            ttkstyle,
            relief=tk.FLAT,
            borderwidth=0,
            padding=0,
            foreground=self.colors.fg,
            background=self.colors.bg,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[("selected", self.colors.bg)],
        )
        a = self.assets
        on = a.recolor(
            "switch_round", white=accent, black=self.colors.bg)
        off = a.recolor(
            "switch_round", white=fg_muted, black=self.colors.bg,
            transform="flip-x")
        disabled_on = a.recolor(
            "switch_round", white=disabled_fg, black=self.colors.bg)
        disabled_off = a.recolor(
            "switch_round", white=disabled_fg, black=self.colors.bg,
            transform="flip-x")
        spacer_name = f"{ttkstyle}.spacer"
        try:
            image_element(
                self.style, f"{ttkstyle}.indicator", default=on.image,
                states={
                    "disabled selected": disabled_on.image,
                    "disabled": disabled_off.image,
                    "!selected": off.image,
                },
                border=on.meta.border, padding=on.meta.padding, sticky=W)
            image_element(
                self.style, spacer_name,
                default=self._create_indicator_spacer_asset(), sticky=EW)
        except Exception:
            """This method is used as the default Toggle style, so it is
            necessary to catch Tcl errors when it tries to create an element
            that was already created by the Toggle or Round Toggle style."""
            pass

        layout(self.style, ttkstyle,
            El("Toolbutton.border", sticky=NSEW, children=[
                El("Toolbutton.padding", sticky=NSEW, children=[
                    El(f"{ttkstyle}.indicator", side=LEFT),
                    El(spacer_name, side=LEFT),
                    El("Toolbutton.label", side=LEFT)])]))
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_square_toggle_style(self, colorname=DEFAULT):
        """Create a square toggle style for the ttk.Checkbutton widget.

        The square toggle uses its own recolorable raster template.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Square.Toggle"
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        fg_muted = Colors.make_transparent(0.40, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        # Resolve the "on" accent (same logic as round-toggle).
        if colorname == LIGHT:
            accent = self.colors.dark
        elif colorname == DARK:
            accent = self.colors.light
        else:
            accent = self.colors.get(colorname)

        self.configure(
            ttkstyle, relief=tk.FLAT, borderwidth=0, foreground=self.colors.fg
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("selected", self.colors.bg),
                ("!selected", self.colors.bg),
            ],
        )
        a = self.assets
        on = a.recolor(
            "switch_square", white=accent, black=self.colors.bg)
        off = a.recolor(
            "switch_square", white=fg_muted, black=self.colors.bg,
            transform="flip-x")
        disabled_on = a.recolor(
            "switch_square", white=disabled_fg, black=self.colors.bg)
        disabled_off = a.recolor(
            "switch_square", white=disabled_fg, black=self.colors.bg,
            transform="flip-x")
        spacer_name = f"{ttkstyle}.spacer"
        image_element(
            self.style, f"{ttkstyle}.indicator", default=on.image,
            states={
                "disabled selected": disabled_on.image,
                "disabled": disabled_off.image,
                "!selected": off.image,
            },
            border=on.meta.border, padding=on.meta.padding, sticky=W)
        image_element(
            self.style, spacer_name,
            default=self._create_indicator_spacer_asset(), sticky=EW)
        layout(self.style, ttkstyle,
            El("Toolbutton.border", sticky=NSEW, children=[
                El("Toolbutton.padding", sticky=NSEW, children=[
                    El(f"{ttkstyle}.indicator", side=LEFT),
                    El(spacer_name, side=LEFT),
                    El("Toolbutton.label", side=LEFT)])]))
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_toolbutton_style(self, colorname=DEFAULT):
        """Create a solid toolbutton style for the ttk.Checkbutton
        and ttk.Radiobutton widgets.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Toolbutton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            toggle_on = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            toggle_on = self.colors.get(colorname)

        foreground = self.colors.get_foreground(colorname)

        if self.is_light_theme:
            toggle_off = self.colors.border
        else:
            toggle_off = self.colors.selectbg

        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        self.configure(
            ttkstyle,
            foreground=self.colors.selectfg,
            background=toggle_off,
            bordercolor=toggle_off,
            darkcolor=toggle_off,
            lightcolor=toggle_off,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("hover", foreground),
                ("selected", foreground),
            ],
            focuscolor=[
                ("disabled", disabled_fg),
                ("hover", foreground),
                ("selected", foreground),
            ],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", toggle_on),
                ("selected !disabled", toggle_on),
                ("hover !disabled", toggle_on),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_outline_toolbutton_style(self, colorname=DEFAULT):
        """Create an outline toolbutton style for the ttk.Checkbutton
        and ttk.Radiobutton widgets.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.Toolbutton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.configure(
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
            arrowsize=3,
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("selected !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            darkcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", self.colors.bg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_entry_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Entry widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TEntry"

        # general default colors
        if self.is_light_theme:
            disabled_fg = self.colors.border
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
            ttkstyle = f"{colorname}.{STYLE}"
            focuscolor = self.colors.get(colorname)
            bordercolor = focuscolor

        self.configure(
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
                ("hover !disabled", focuscolor),
            ],
            lightcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
            darkcolor=[
                ("focus invalid", self.colors.danger),
                ("focus !disabled", focuscolor),
                ("readonly", readonly),
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_radiobutton_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Radiobutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        sn = StyleName("TRadiobutton", colorname)
        fg = self.colors.fg
        disabled = Colors.make_transparent(0.30, fg, self.colors.bg)
        fg_muted = Colors.make_transparent(0.40, fg, self.colors.bg)

        # Resolve the "on" accent; LIGHT/DARK on their own background need a
        # contrasting indicator so the knockout interior stays readable
        # (visual-check item: verify LIGHT-on-light reads on the human spot-check).
        if sn.colorname == LIGHT and self.is_light_theme:
            accent = self.colors.dark
        elif sn.colorname == DARK and not self.is_light_theme:
            accent = self.colors.light
        else:
            accent = self.colors.get(sn.colorname)

        self.configure(sn.ttkstyle, foreground=fg)
        state_map(self.style, sn.ttkstyle, foreground={"disabled": disabled})

        a = self.assets
        selected = a.recolor("radiobutton", white=accent, black=accent)
        unselected = a.recolor(
            "radiobutton", white=self.colors.bg, black=fg_muted)
        disabled_selected = a.recolor(
            "radiobutton", white=disabled, black=disabled)
        disabled_unselected = a.recolor(
            "radiobutton", white=self.colors.bg, black=disabled)
        image_element(
            self.style, f"{sn.ttkstyle}.indicator", default=selected.image,
            states={
                "disabled selected": disabled_selected.image,
                "disabled": disabled_unselected.image,
                "!selected": unselected.image,
            },
            border=selected.meta.border, padding=selected.meta.padding, sticky=W)
        spacer_name = f"{sn.ttkstyle}.spacer"
        image_element(
            self.style, spacer_name,
            default=self._create_indicator_spacer_asset(), sticky=EW)
        layout(
            self.style, sn.ttkstyle,
            El("Radiobutton.padding", sticky=NSEW, children=[
                El(f"{sn.ttkstyle}.indicator", side=LEFT, sticky=""),
                El(spacer_name, side=LEFT),
                El("Radiobutton.focus", side=LEFT, sticky="", children=[
                    El("Radiobutton.label", sticky=NSEW)])]))
        self.style._register_ttkstyle(sn.ttkstyle)

    def create_date_button_style(self, colorname=DEFAULT):
        """Create a date button style for the ttk.Button widget.

        Parameters:

            colorname (str):
                The color label used to style widget.
        """
        STYLE = "Date.TButton"

        if self.is_light_theme:
            disabled_fg = self.colors.border
        else:
            disabled_fg = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.get_foreground(PRIMARY)
            background = self.colors.primary
            btn_foreground = Colors.get_foreground(self.colors, PRIMARY)
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)
            btn_foreground = Colors.get_foreground(self.colors, colorname)

        # Calendar icon in the button foreground color.
        size = self.scale_size([21, 22])
        img_normal = self.assets.icon("calendar3", size, btn_foreground)

        pressed = Colors.update_hsv(background, vd=-0.1)
        hover = Colors.update_hsv(background, vd=0.10)

        self.configure(
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
            image=img_normal,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[("disabled", disabled_fg)],
            darkcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        self.style._register_ttkstyle(ttkstyle)

    def create_calendar_style(self, colorname=DEFAULT):
        """Create a style for the
        ttkbootstrap.dialogs.DatePickerPopup widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "TCalendar"

        if any([colorname == DEFAULT, colorname == ""]):
            prime_color = self.colors.primary
            ttkstyle = STYLE
            chevron_style = "Chevron.TButton"
        else:
            prime_color = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"
            chevron_style = f"Chevron.{colorname}.TButton"

        if self.is_light_theme:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.2)
            pressed = Colors.update_hsv(prime_color, vd=-0.1)
        else:
            disabled_fg = Colors.update_hsv(self.colors.inputbg, vd=-0.3)
            pressed = Colors.update_hsv(prime_color, vd=0.1)

        self.configure(
            ttkstyle,
            foreground=self.colors.fg,
            background=self.colors.bg,
            bordercolor=self.colors.bg,
            darkcolor=self.colors.bg,
            lightcolor=self.colors.bg,
            relief=tk.RAISED,
            focusthickness=1,
            focuscolor=self.colors.fg,
            borderwidth=1,
            padding=(10, 5),
            anchor=tk.CENTER,
        )
        layout(self.style, ttkstyle,
               El("Toolbutton.border", sticky=tk.NSEW, children=[
                   El("Toolbutton.focus", sticky=tk.NSEW, children=[
                       El("Toolbutton.padding", sticky=tk.NSEW, children=[
                           El("Toolbutton.label", sticky=tk.NSEW)])])]))

        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("selected !disabled", pressed),
                ("hover !disabled", pressed),
            ],
            focuscolor=[
                ("disabled", disabled_fg),
                ("pressed !disabled", self.colors.selectfg),
                ("selected !disabled", self.colors.selectfg),
                ("hover !disabled", self.colors.selectfg),
            ]
        )
        self.configure(chevron_style, font="-size 14")

        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)
        self.style._register_ttkstyle(chevron_style)

    def create_metersubtxt_label_style(self, colorname=DEFAULT):
        """Create a subtext label style for the
        ttkbootstrap.widgets.Meter widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Metersubtxt.TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            if self.is_light_theme:
                foreground = self.colors.secondary
            else:
                foreground = self.colors.light
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get(colorname)

        background = self.colors.bg

        self.configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_meter_label_style(self, colorname=DEFAULT):
        """Create a label style for the
        ttkbootstrap.widgets.Meter widget. This style also stores some
        metadata that is called by the Meter class to lookup relevant
        colors for the trough and bar when the new image is drawn.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """

        STYLE = "Meter.TLabel"

        # text color = `foreground`
        # trough color = `space`

        if self.is_light_theme:
            if colorname == LIGHT:
                troughcolor = self.colors.bg
            else:
                troughcolor = self.colors.light
        else:
            troughcolor = Colors.update_hsv(self.colors.selectbg, vd=-0.2)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.bg
            textcolor = self.colors.primary
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            textcolor = self.colors.get(colorname)
            background = self.colors.bg

        self.configure(
            ttkstyle,
            foreground=textcolor,
            background=background,
            space=troughcolor,
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_label_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Label widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            foreground = self.colors.fg
            background = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            foreground = self.colors.get(colorname)
            background = self.colors.bg

        # standard label
        self.configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_inverse_label_style(self, colorname=DEFAULT):
        """Create an inverted style for the ttk.Label.

        The foreground and background are inverted versions of that
        used in the standard label style.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE_INVERSE = "Inverse.TLabel"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE_INVERSE
            background = self.colors.fg
            foreground = self.colors.bg
        else:
            ttkstyle = f"{colorname}.{STYLE_INVERSE}"
            background = self.colors.get(colorname)
            foreground = self.colors.get_foreground(colorname)

        self.configure(
            ttkstyle, foreground=foreground, background=background
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_labelframe_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Labelframe widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TLabelframe"

        background = self.colors.bg

        if any([colorname == DEFAULT, colorname == ""]):
            foreground = self.colors.fg
            ttkstyle = STYLE

            if self.is_light_theme:
                bordercolor = self.colors.border
            else:
                bordercolor = self.colors.selectbg

        else:
            foreground = self.colors.get(colorname)
            bordercolor = foreground
            ttkstyle = f"{colorname}.{STYLE}"

        # create widget style
        self.configure(
            f"{ttkstyle}.Label",
            foreground=foreground,
            background=background,
        )
        self.configure(
            ttkstyle,
            relief=tk.RAISED,
            borderwidth=1,
            bordercolor=bordercolor,
            lightcolor=background,
            darkcolor=background,
            background=background,
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_checkbutton_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Checkbutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        sn = StyleName("TCheckbutton", colorname)
        fg = self.colors.fg
        disabled = Colors.make_transparent(0.3, fg, self.colors.bg)
        fg_muted = Colors.make_transparent(0.4, fg, self.colors.bg)

        # Resolve the "on" accent; LIGHT/DARK on their own background need a
        # contrasting indicator so the knockout interior stays readable
        # (visual-check item: verify LIGHT-on-light reads on the human spot-check).
        if sn.colorname == LIGHT and self.is_light_theme:
            accent = self.colors.dark
        elif sn.colorname == DARK and not self.is_light_theme:
            accent = self.colors.light
        else:
            accent = self.colors.get(sn.colorname)

        # Foreground map FIRST -- color-less icon specs resolve against it.
        self.configure(sn.ttkstyle, foreground=fg)
        state_map(self.style, sn.ttkstyle, foreground={"disabled": disabled})

        a = self.assets
        checked = a.recolor(
            "checkbox_checked", white=self.colors.bg, black=accent)
        unchecked = a.recolor(
            "checkbox_unchecked", white=self.colors.bg, black=fg_muted)
        indeterminate = a.recolor(
            "checkbox_indeterminate", white=self.colors.bg, black=accent)
        disabled_checked = a.recolor(
            "checkbox_checked", white=self.colors.bg, black=disabled)
        disabled_unchecked = a.recolor(
            "checkbox_unchecked", white=self.colors.bg, black=disabled)
        disabled_indeterminate = a.recolor(
            "checkbox_indeterminate", white=self.colors.bg, black=disabled)
        image_element(
            self.style, f"{sn.ttkstyle}.indicator", default=checked.image,
            states={
                "disabled selected": disabled_checked.image,
                "disabled alternate": disabled_indeterminate.image,
                "disabled": disabled_unchecked.image,
                "alternate": indeterminate.image,
                "!selected": unchecked.image,
            },
            border=checked.meta.border, padding=checked.meta.padding, sticky=W)
        spacer_name = f"{sn.ttkstyle}.spacer"
        image_element(
            self.style, spacer_name,
            default=self._create_indicator_spacer_asset(), sticky=EW)
        layout(self.style, sn.ttkstyle, El("Checkbutton.padding", sticky=NSEW, children=[
            El(f"{sn.ttkstyle}.indicator", side=LEFT, sticky=""),
            El(spacer_name, side=LEFT),
            El("Checkbutton.focus", side=LEFT, sticky="", children=[
                El("Checkbutton.label", sticky=NSEW)])]))
        # register ttkstyle
        self.style._register_ttkstyle(sn.ttkstyle)

    def create_menubutton_style(self, colorname=DEFAULT):
        """Create a solid style for the ttk.Menubutton widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TMenubutton"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            background = self.colors.primary
            foreground = self.colors.get_foreground(PRIMARY)
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            background = self.colors.get(colorname)
            foreground = self.colors.get_foreground(colorname)

        disabled_bg = Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        pressed = Colors.make_transparent(0.80, background, self.colors.bg)
        hover = Colors.make_transparent(0.90, background, self.colors.bg)

        self.configure(
            ttkstyle,
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=tk.RAISED,
            focusthickness=0,
            focuscolor=self.colors.selectfg,
            padding=(10, 5),
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled_fg)],
            background=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            darkcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("disabled", disabled_bg),
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # caret-down-fill indicator (replaces the native clam triangle); the
        # solid menubutton arrow keeps one color (only the background changes on
        # hover), so just a normal + disabled image.
        self._build_menubutton_arrow(ttkstyle, foreground, disabled_fg, foreground)
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def _build_menubutton_arrow(self, ttkstyle, normal, disabled, active):
        """Build the caret-down indicator element + layout for a Menubutton style.

        Replaces ttk's native `Menubutton.indicator` triangle with a Bootstrap
        `caret-down-fill` image element so the menubutton arrow matches the
        caret-fill arrows used elsewhere. `normal`/`disabled`/`active` are the
        arrow colors per state (`active` == `normal` when the arrow does not
        recolor on hover/press).
        """
        arrows = self.create_simple_arrow_assets(normal, disabled, active)
        down, down_disabled, down_active = arrows[0][1], arrows[1][1], arrows[2][1]
        image_element(
            self.style, f"{ttkstyle}.indicator", default=down,
            states={"disabled": down_disabled,
                    "pressed !disabled": down_active,
                    "hover !disabled": down_active},
            sticky="", padding=(0, 0, self.scale_size(10), 0))
        layout(self.style, ttkstyle,
            El("Menubutton.border", sticky=NSEW, children=[
                El("Menubutton.focus", sticky=NSEW, children=[
                    El(f"{ttkstyle}.indicator", side=tk.RIGHT, sticky=""),
                    El("Menubutton.padding", sticky=tk.EW, children=[
                        El("Menubutton.label", side=LEFT, sticky="")])])]))

    def create_outline_menubutton_style(self, colorname=DEFAULT):
        """Create an outline button style for the ttk.Menubutton widget

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "Outline.TMenubutton"

        disabled_fg = Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE
            colorname = PRIMARY
        else:
            ttkstyle = f"{colorname}.{STYLE}"

        foreground = self.colors.get(colorname)
        background = self.colors.get_foreground(colorname)
        foreground_pressed = background
        bordercolor = foreground
        pressed = foreground
        hover = foreground

        self.configure(
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
        )
        self.style.map(
            ttkstyle,
            foreground=[
                ("disabled", disabled_fg),
                ("pressed !disabled", foreground_pressed),
                ("hover !disabled", foreground_pressed),
            ],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            bordercolor=[
                ("disabled", disabled_fg),
                ("pressed", pressed),
                ("hover", hover),
            ],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover),
            ],
        )
        # caret-down-fill indicator; the outline arrow recolors on hover/press
        # (foreground -> the contrasting fill color), so pass that as `active`.
        self._build_menubutton_arrow(ttkstyle, foreground, disabled_fg, foreground_pressed)
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_notebook_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Notebook widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TNotebook"

        if self.is_light_theme:
            bordercolor = self.colors.border
            foreground = self.colors.inputfg
        else:
            bordercolor = self.colors.selectbg
            foreground = self.colors.selectfg

        if any([colorname == DEFAULT, colorname == ""]):
            background = self.colors.inputbg
            selectfg = self.colors.fg
            ttkstyle = STYLE
        else:
            selectfg = self.colors.get_foreground(colorname)
            background = self.colors.get(colorname)
            ttkstyle = f"{colorname}.{STYLE}"

        ttkstyle_tab = f"{ttkstyle}.Tab"

        # create widget style
        self.configure(
            ttkstyle,
            background=self.colors.bg,
            bordercolor=bordercolor,
            lightcolor=self.colors.bg,
            darkcolor=self.colors.bg,
            tabmargins=(0, 1, 1, 0),
        )
        self.configure(
            ttkstyle_tab, focuscolor="", foreground=foreground, padding=(6, 5)
        )
        self.style.map(
            ttkstyle_tab,
            background=[
                ("selected", self.colors.bg),
                ("!selected", background),
            ],
            lightcolor=[
                ("selected", self.colors.bg),
                ("!selected", background),
            ],
            bordercolor=[
                ("selected", bordercolor),
                ("!selected", bordercolor),
            ],
            padding=[("selected", (6, 5)), ("!selected", (6, 5))],
            foreground=[("selected", foreground), ("!selected", selectfg)],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def create_panedwindow_style(self, colorname=DEFAULT):
        """Create a standard style for the ttk.Panedwindow widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        H_STYLE = "Horizontal.TPanedwindow"
        V_STYLE = "Vertical.TPanedwindow"

        if self.is_light_theme:
            default_color = self.colors.border
        else:
            default_color = self.colors.selectbg

        if any([colorname == DEFAULT, colorname == ""]):
            sashcolor = default_color
            h_ttkstyle = H_STYLE
            v_ttkstyle = V_STYLE
        else:
            sashcolor = self.colors.get(colorname)
            h_ttkstyle = f"{colorname}.{H_STYLE}"
            v_ttkstyle = f"{colorname}.{V_STYLE}"

        self.configure(
            "Sash", gripcount=0, sashthickness=self.scale_size(2)
        )
        self.configure(h_ttkstyle, background=sashcolor)
        self.configure(v_ttkstyle, background=sashcolor)

        # register ttkstyle
        self.style._register_ttkstyle(h_ttkstyle)
        self.style._register_ttkstyle(v_ttkstyle)

    def create_sizegrip_style(self, colorname=DEFAULT):
        """Create a style for the ttk.Sizegrip widget.

        Parameters:

            colorname (str):
                The color label used to style the widget.
        """
        STYLE = "TSizegrip"

        if any([colorname == DEFAULT, colorname == ""]):
            ttkstyle = STYLE

            if self.is_light_theme:
                grip_color = self.colors.border
            else:
                grip_color = self.colors.inputbg
        else:
            ttkstyle = f"{colorname}.{STYLE}"
            grip_color = self.colors.get(colorname)

        # Visual-check item: `grip-horizontal` vs a corner-grip glyph -- settle
        # on the human spot-check.
        size = self.scale_size(16)
        image = self.assets.icon("grip-horizontal", size, grip_color)

        self.style.element_create(
            f"{ttkstyle}.Sizegrip.sizegrip", "image", image
        )
        self.style.layout(
            ttkstyle,
            [
                (
                    f"{ttkstyle}.Sizegrip.sizegrip",
                    {"side": tk.BOTTOM, "sticky": tk.SE},
                )
            ],
        )
        # register ttkstyle
        self.style._register_ttkstyle(ttkstyle)

    def update_combobox_popdown_style(self, widget):
        """Update the legacy ttk.Combobox elements. This method is
        called every time the theme is changed in order to ensure
        that the legacy tkinter components embedded in this ttk widget
        are styled appropriate to the current theme.

        The ttk.Combobox contains several elements that are not styled
        using the ttk theme engine. This includes the **popdownwindow**
        and the **scrollbar**. Both of these widgets are configured
        manually using calls to tcl/tk.

        Parameters:

            widget (ttk.Combobox):
                The combobox element to be updated.
        """
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
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)
