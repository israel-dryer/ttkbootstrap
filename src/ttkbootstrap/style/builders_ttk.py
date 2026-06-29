"""Per-theme coordinator for private ttk widget-family style recipes."""

from math import ceil
from tkinter import ttk

from ttkbootstrap.constants import *
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.builders import load_builders
from ttkbootstrap.style.builders.registry import (
    DEFAULT_VARIANT,
    get_builder,
)
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.theme import Colors, ThemeDefinition


class StyleBuilderTTK:
    """Coordinate private ttk style recipes for one active theme.

    This class is internal to the style engine. Widget-family recipe bodies
    live in `ttkbootstrap.style.builders` and are selected through its private
    registry.
    """

    def __init__(self, build: bool = True):
        # local import breaks the builders<-engine cycle (engine imports builders)
        from ttkbootstrap.style.engine import Style

        self.style: Style = Style.get_instance()
        self.builder_tk = StyleBuilderTK()

        if build:
            self.create_theme()

    @property
    def colors(self) -> Colors:
        """A reference to the `Colors` object of the current theme."""
        return self.style.theme.colors

    @property
    def theme(self) -> ThemeDefinition:
        """A reference to the current theme definition."""
        return self.style.theme

    @property
    def is_light_theme(self) -> bool:
        """Whether the current theme is light."""
        return self.style.theme.type == LIGHT

    @property
    def assets(self) -> Assets:
        """A key-safe `Assets` facade bound to the engine image cache."""
        cached = self.__dict__.get("_assets")
        if cached is None:
            cached = self.__dict__["_assets"] = Assets(self.style)
        return cached

    def configure(self, style, **options):
        """Configure a style without re-entering public bootstyle resolution."""
        self.style._build_configure(style, **options)

    def scale_size(self, size):
        """Scale an integer or sequence using Tk's active scaling factor."""
        winsys = self.style.master.tk.call("tk", "windowingsystem")
        if winsys == "aqua":
            baseline = 1.000492368291482
        else:
            baseline = 1.33398982438864281
        scaling = self.style.master.tk.call("tk", "scaling")
        factor = scaling / baseline

        if isinstance(size, (int, float)):
            return ceil(size * factor)
        if isinstance(size, (tuple, list)):
            return [ceil(x * factor) for x in size]
        return None

    def build_style(
        self,
        variant: str,
        widget_family: str,
        colorname: str = DEFAULT,
        *,
        required: bool = False,
    ) -> bool:
        """Invoke one registered recipe, returning whether its key exists."""
        load_builders()
        recipe = (
            get_builder(variant, widget_family)
            if variant and widget_family
            else None
        )
        if recipe is None:
            if required:
                raise LookupError(
                    "required ttk style recipe is not registered: "
                    f"{(variant, widget_family)!r}"
                )
            return False
        recipe(self, colorname)
        return True

    def register_ttkstyle(self, style_name: str):
        """Register that a ttk style name. This ensures that the builder will not attempt to build a style
        that has already been created.
        """
        return self.style._register_ttkstyle(style_name)

    def create_theme(self):
        """Create the current ttk theme and establish its default settings."""
        self.style.theme_create(self.theme.name, TTK_CLAM)
        ttk.Style.theme_use(self.style, self.theme.name)
        self.update_ttk_theme_settings()

    def update_ttk_theme_settings(self):
        """Apply settings that are intentionally eager for a new theme."""
        self.create_default_style()

    def create_default_style(self):
        """Set root defaults and the small set of deliberately eager styles."""
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
            fieldbg=self.colors.bg,
            borderwidth=1,
            focuscolor="",
        )

        # Native dialog buttons need the base TButton even when an application
        # only instantiates styled variants.
        self.build_style(
            DEFAULT_VARIANT, "button", DEFAULT, required=True
        )

        # General styles used by Tableview and Tooltip internals.
        self.build_style("link", "button", DEFAULT, required=True)
        self.style.configure("symbol.Link.TButton", font="-size 16")

        self.build_style(
            DEFAULT_VARIANT, "label", DEFAULT, required=True
        )
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

    def update_combobox_popdown_style(self, widget):
        """Delegate Tcl-level Combobox popdown styling to its family module."""
        load_builders()
        from ttkbootstrap.style.builders.combobox import (
            update_combobox_popdown_style,
        )

        update_combobox_popdown_style(self, widget)
