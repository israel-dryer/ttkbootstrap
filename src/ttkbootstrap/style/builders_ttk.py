"""Per-theme coordinator for private ttk widget-family style recipes."""

from tkinter import ttk

from ttkbootstrap.constants import *
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.builders import load_builders
from ttkbootstrap.style.builders.registry import (
    DEFAULT_VARIANT,
    get_builder,
)
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.theme import (
    Colors,
    ThemeDefinition,
    _accent_on_color,
    _mix_colors,
    _state_color,
)


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
        """Convert logical UI units using the root-bound scaling service."""
        return self.style.scaling.logical(size)

    def active(self, color: str) -> str:
        """Return bootstack's luminance-directed active-state color."""
        return _state_color(color, "active")

    def pressed(self, color: str) -> str:
        """Return bootstack's stronger luminance-directed pressed color."""
        return _state_color(color, "pressed")

    def border(self, color: str) -> str:
        """Derive a local border by mixing a surface toward its on-color."""
        return _mix_colors(color, self.on_color(color), 0.84)

    def disabled(
        self, role: str = "background", surface: str | None = None
    ) -> str:
        """Return bootstack's mode-aware disabled text or surface color."""
        surface = surface or self.colors.bg
        if role == 'text':
            if self.is_light_theme:
                neutral, weight = '#6c757d', 0.35
            else:
                neutral, weight = '#adb5bd', 0.25
        elif role == 'background':
            if self.is_light_theme:
                neutral, weight = '#dee2e6', 0.15
            else:
                neutral, weight = '#495057', 0.20
        else:
            raise ValueError(
                f'Invalid role: {role}. Expected text or background.'
            )
        return _mix_colors(neutral, surface, weight)

    def on_color(self, color: str) -> str:
        """Return a readable foreground for a filled surface.

        White-preferred, saturation-aware: white wins whenever it clears the
        bold-text floor, and stays chosen for vivid non-warm accents where
        WCAG contrast understates it; black is used for pale, near-neutral,
        and warm (yellow/orange) fills. Identical in light and dark themes.
        See `_accent_on_color`.
        """
        return _accent_on_color(color)

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
            borderwidth=self.scale_size(1),
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
            borderwidth=self.scale_size(1),
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
