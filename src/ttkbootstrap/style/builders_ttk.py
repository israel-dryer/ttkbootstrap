"""Per-theme coordinator for private ttk widget-family style recipes."""

from difflib import get_close_matches
from tkinter import ttk

from ttkbootstrap.constants import *
from ttkbootstrap.style._compat import report_invalid
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
    _border_color,
    _mix_colors,
    _shade,
    _state_color,
    _tint,
)

# Mix-based surface tuning, retiring the ad-hoc HSV/alpha color math. Weights
# are fractions mixed toward black (shade), white (tint), or a surface (mute),
# chosen to preserve each recipe's current appearance; gate-tunable.
_TROUGH_SHADE = 0.2    # recessed dark-theme track/trough behind a filled bar
_STRIPE_TINT = 0.2     # lighter diagonal highlight over a progress bar
_MUTE_AMOUNT = 0.4     # unchecked-indicator muting
_CARD_ELEVATION = 0.06  # mode-aware raise of the background for the `card` surface


class StyleBuilderTTK:
    """Coordinate private ttk style recipes for one active theme.

    This class is internal to the style engine. Widget-family recipe bodies
    live in `ttkbootstrap.style.builders` and are selected through its private
    registry.
    """

    def __init__(self, build: bool = True):
        """Bind to the active `Style` instance and build the theme unless `build` is False."""
        # local import breaks the builders<-engine cycle (engine imports builders)
        from ttkbootstrap.style.engine import Style

        self.style: Style = Style.get_instance()
        self.builder_tk = StyleBuilderTK()
        # transient surface token for the recipe currently building (2.0
        # surface-color); set/restored by `build_style`, read by surface-aware
        # recipes via `surface_prefix`/`resolve_surface`.
        self._surface = ""

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
        return _border_color(color)

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

    def shade(self, color: str, weight: float = _TROUGH_SHADE) -> str:
        """Return `color` darkened by mixing `weight` of black into it.

        The default weight matches the recessed dark-theme track/trough recipes.
        """
        return _shade(color, weight)

    def tint(self, color: str, weight: float = _STRIPE_TINT) -> str:
        """Return `color` lightened by mixing `weight` of white into it.

        Used for forward highlights that must read lighter than the fill they
        sit on (progress stripe, pale floodgauge trough) in either mode.
        """
        return _tint(color, weight)

    def mute(
        self, color: str, surface: str | None = None,
        amount: float = _MUTE_AMOUNT,
    ) -> str:
        """Return `color` alpha-blended onto a surface to mute an indicator."""
        return _mix_colors(color, surface or self.colors.bg, amount)

    def on_color(self, color: str) -> str:
        """Return a readable foreground for a filled surface.

        White-preferred, saturation-aware: white wins whenever it clears the
        bold-text floor, and stays chosen for vivid non-warm accents where
        WCAG contrast understates it; black is used for pale, near-neutral,
        and warm (yellow/orange) fills. Identical in light and dark themes.
        See `_accent_on_color`.
        """
        return _accent_on_color(color)

    def card_surface(self) -> str:
        """Return the `card` surface: a mode-aware raise of the background.

        Darkens the background in a light theme, lightens it in a dark theme, so
        a card reads as a subtly raised panel in either mode. Derived from
        `colors.bg` at build time, so it follows theme switches.
        """
        bg = self.colors.bg
        if self.is_light_theme:
            return self.shade(bg, _CARD_ELEVATION)
        return self.tint(bg, _CARD_ELEVATION)

    def resolve_surface(self, surface: str | None = None) -> str:
        """Resolve a surface token to a concrete background color.

        The *surface* is the background a widget is placed on. Accepts:

          - `None` / `""` / `"background"` -- the application background
            (`colors.bg`); the default, and the only surface that produces no
            style-name segment.
          - `"card"` -- a mode-aware raised surface (`card_surface`).
          - an accent color name (`primary`, `success`, ..., `neutral`) -- that
            color, so a ghost/outline/link control can blend into an accent
            container (e.g. an accent toolbar).

        Named and accent surfaces are theme-reactive: they re-resolve on a theme
        switch. An unknown token routes through the shared strictness gate --
        warn-and-fall-back-to-background by default, raise under strict mode
        (`set_bootstyle_strict` / `TTKBOOTSTRAP_STRICT`), matching how the
        resolver treats an unknown bootstyle token. Raw-hex surfaces are not yet
        accepted (deferred).
        """
        if not surface or surface == DEFAULT_SURFACE:
            return self.colors.bg
        if surface == "card":
            return self.card_surface()
        if surface in BOOTSTYLE_COLORS:
            if surface == NEUTRAL:
                # local import breaks the builders<-utils cycle
                from ttkbootstrap.style.builders.utils import neutral_fill
                return neutral_fill(self)
            return self.colors.get(surface)
        report_invalid(
            "surface", surface, surface,
            suggestions=get_close_matches(surface, BOOTSTYLE_SURFACE_TOKENS, n=2),
        )
        return self.colors.bg

    def build_style(
        self,
        variant: str,
        widget_family: str,
        colorname: str = DEFAULT,
        surface: str = "",
        *,
        required: bool = False,
    ) -> bool:
        """Invoke one registered recipe, returning whether its key exists.

        `surface` (2.0 surface-color) is the background the widget sits on; it is
        exposed to the recipe as transient state (`self._surface`) for the
        duration of the build and restored afterward (save/restore, so a recipe
        that itself builds another style does not clobber it).
        """
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
        prev_surface = self._surface
        self._surface = surface or ""
        try:
            recipe(self, colorname)
        finally:
            self._surface = prev_surface
        return True

    def surface_prefix(self, name: str) -> str:
        """Prefix a style name with the active `@<surface>.` segment, if any.

        Recipes build their style name normally (`f"{color}.{ttk_class}"`) and
        wrap it here. Uses the shared `surface_segment` (constants) that the
        resolver's `_build_ttkstyle_name` also uses, so the *built* name and the
        *looked-up* name cannot drift; a default/empty surface adds nothing.
        """
        return f"{surface_segment(self._surface)}{name}"

    def on_surface_fg(self) -> str:
        """Foreground that reads against the active surface (2.0 surface-color).

        A genuine accent surface (primary/success/light/dark/...) needs a
        contrast flip to `on_color`; the near-background neutral surfaces
        (`background`/`card`/`neutral`) keep the theme's soft `fg`, so a control
        on a card does not harden its text vs the same control on the app
        background. No surface -> the theme `fg`.
        """
        surface = self._surface
        if surface and surface in BOOTSTYLE_COLORS and surface != NEUTRAL:
            return self.on_color(self.resolve_surface(surface))
        return self.colors.fg

    def register_ttkstyle(self, style_name: str):
        """Mark `style_name` as built so the builder will not recreate it."""
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
