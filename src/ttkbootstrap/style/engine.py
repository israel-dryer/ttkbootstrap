"""The ttkbootstrap style engine.

`Style` is the process-wide singleton (subclasses `ttk.Style`): it owns the
theme definitions, the active theme, the version-stamped theme walk, and the
content-addressed image cache. Split out of the monolithic `style.py` in 2.0.
"""
import json
import warnings
from tkinter import TclError, ttk
from typing import Any, Optional

from ttkbootstrap.internal import utility as util
from ttkbootstrap.constants import *
from ttkbootstrap.themes.standard import LEGACY_THEME_ALIASES, STANDARD_THEMES

from ttkbootstrap.style.theme import ThemeDefinition
from ttkbootstrap.style.scaling import Scaling
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK


# Geometry/layout options a user's `style.configure(...)` may set that should
# SURVIVE variant builds and theme switches (the durable style-options layer,
# #1238/#1161). Colors are deliberately excluded: they stay theme-reactive, so a
# `configure(background=...)` applies once but is not replayed on rebuild. The
# set must cover every non-color option any recipe writes, or that option stays
# clobbered; `tests/test_durable_style_options.py` guards that by AST-scanning
# the recipes.
DURABLE_STYLE_OPTIONS = frozenset({
    "padding",
    "borderwidth",
    "focusthickness",
    "thickness",
    "rowheight",
    "sashthickness",
    "gripcount",
    "tabmargins",
    "arrowsize",
    "anchor",
    "font",
    "relief",
    "pbarrelief",
    "justify",
    "insertwidth",
    "indicatormargin",
    "indicatorsize",
})


class Style(ttk.Style):
    """A singleton class for creating and managing the application
    theme and widget styles.

    This class is meant to be a drop-in replacement for `ttk.Style` and
    inherits all of it's methods and properties. However, in
    ttkbootstrap, this class is implemented as a singleton. Subclassing
    is not recommended and may have unintended consequences.
    """

    instance = None

    def __new__(cls, *args, **kwargs):
        if Style.instance is None:
            return object.__new__(cls)
        else:
            return Style.instance

    def __init__(self, theme=None, default_button=None, *, themename=None,
                 light_theme=None, dark_theme=None):
        """
        Parameters:

            theme (str):
                The name of the theme to use when styling the widget.
                `themename` is a permanent, non-deprecated alias accepted for
                the same purpose (pre-2.0 spelling); pass either.

            light_theme, dark_theme (str):
                Optionally designate the themes that `toggle_theme()` /
                `theme_mode` switch between. If omitted, the counterpart
                is derived from the `<family>-light` / `<family>-dark` naming
                convention, so designation is only needed to pin a specific
                pair (e.g. a light theme from one family with a dark theme from
                another). Read once on the first `Style`/`App`; ignored on the
                existing singleton (set later via `set_theme_modes(...)`).

            default_button (str):
                The color a bare `Button`/`Menubutton` (no `bootstyle`) uses.
                Defaults to `"neutral"`; pass `"primary"` for the pre-2.0
                accented default. Read once when the base styles build, so set it
                on the first `Style`/`App`; ignored on the existing singleton. If
                omitted, a pre-root `ttk.set_default_button(...)` setting is used,
                else `"neutral"`; an explicit argument here wins over that setter.
        """
        # `theme` is canonical; `themename` is a permanent, non-deprecated alias
        # (the pre-2.0 spelling). Prefer `theme` when both are given.
        theme = theme if theme is not None else themename
        if theme is None:
            theme = DEFAULT_THEME

        if Style.instance is not None:
            if theme != DEFAULT_THEME:
                Style.instance.theme_use(theme)
            return
        self._theme_objects = {}
        self._theme_definitions = {}
        self._style_registry = set()  # all styles used
        self._theme_styles = {}  # styles used in theme
        # Durable style-options layer (#1238/#1161): user `configure()` overrides
        # keyed by style name, replayed after each build so they survive variant
        # builds and theme switches. Only DURABLE_STYLE_OPTIONS are recorded.
        self._user_options = {}
        # Styles the framework *derives* (e.g. the per-widget `Icon<hash>.<base>`
        # icon styles). They are excluded from the durable-options fan-out: they
        # already inherit a base-class `configure` through ttk's native dotted-name
        # resolution, and fanning a user override onto them would overwrite the
        # icon's own computed values (e.g. stretch a square `icon_only` control).
        # See #1284.
        self._derived_styles = set()
        self._theme_names = set()
        # Optional designated light/dark theme pair for the theme_mode setter /
        # toggle_theme(); None means "derive from the -light/-dark naming".
        self._light_theme = None
        self._dark_theme = None
        # Monotonic counter bumped on every theme switch. The theme walk
        # repaints (and restamps) only widgets stamped older than this, so a
        # widget is repainted at most once per switch. Replaces the old
        # Publisher broadcast.
        self._theme_version = 0
        # Content-addressed image cache shared across themes/builders. Keyed on
        # the pixel-determining inputs of each asset (resolved colors, scaled
        # size, geometry), NOT the theme name, so cross-theme-identical assets
        # dedupe and are rendered once. Replaces the per-builder theme_images
        # dicts that pinned a fresh PhotoImage per theme (the image leak).
        self._image_cache = {}
        # Callbacks run after every theme change (register via on_theme_change),
        # so a custom style can rebuild itself against the new theme's colors.
        self._theme_change_callbacks = []
        self._running_theme_callbacks = False
        self._load_themes()
        self._dynamic_foreground = False
        super().__init__()
        self.scaling = Scaling.for_widget(self.master)

        Style.instance = self

        # Resolve the default (no-color) button fill BEFORE theme_use() builds the
        # base TButton/TMenubutton styles that read it. Order: baseline NEUTRAL,
        # then any pre-root config queued before the root existed (Slice 5's
        # deferred-config seam -- default_button/locale/fonts), then an explicit
        # `default_button=` argument, which wins over the global pre-root setter.
        self.default_button = NEUTRAL
        from ttkbootstrap.utils import config
        config.flush_pending_config()
        if default_button is not None:
            self.default_button = default_button

        if light_theme is not None or dark_theme is not None:
            self.set_theme_modes(light=light_theme, dark=dark_theme)

        self.theme_use(theme)

        # apply localization
        from ttkbootstrap import localization
        localization.initialize_localities()

    @property
    def colors(self):
        """An object that contains the colors used for the current
        theme.

        Returns:

            Colors:
                The colors object for the current theme.
        """
        theme = self.theme.name
        if theme in list(self._theme_names):
            definition = self._theme_definitions.get(theme)
            if not definition:
                return []  # TODO refactor this
            else:
                return definition.colors
        else:
            return []  # TODO refactor this

    def configure(self, style, query_opt: Any = None, **kw):
        """Configure a ttk style, resolving `style` through the bootstyle
        parser if it is not already a registered ttk style name.

        Parameters:

            style (str):
                A ttk style name or a `bootstyle` string to resolve first.

            query_opt (Any):
                If given, query this single style option instead of setting
                options; forwarded to `ttk.Style.configure`.

            **kw:
                Style options to configure (forwarded to `ttk.Style.configure`).
        """
        if query_opt:
            return super().configure(style, query_opt=query_opt, **kw)

        # Capture durable geometry overrides so they survive later variant
        # builds / theme switches (see _reapply_user_options). Builders write via
        # _build_configure, NOT this public path, so recipe writes are not
        # recorded -- only genuine user calls are.
        if kw:
            self._record_user_options(style, kw)

        # local import breaks the engine<-bootstyle cycle (bootstyle imports engine)
        from ttkbootstrap.style.bootstyle import Bootstyle

        if not self.style_exists_in_theme(style):
            ttkstyle = Bootstyle.update_ttk_widget_style(None, style)
        else:
            ttkstyle = style

        if ttkstyle == style:
            # configure an existing ttkbootrap theme
            return super().configure(style, query_opt=query_opt, **kw)
        else:
            # subclass a ttkbootstrap theme
            result = super().configure(style, query_opt=query_opt, **kw)
            self._register_ttkstyle(style)
            return result

    def theme_names(self):
        """Return a list of all ttkbootstrap themes.

        Returns:

            list[str, ...]:
                A list of theme names.
        """
        return list(self._theme_definitions.keys())

    def register_theme(self, definition):
        """Register a theme definition for use by the `Style`
        object. This makes the definition and name available at
        run-time so that the assets and styles can be created when
        needed.

        Parameters:

            definition (ThemeDefinition):
                A `ThemeDefinition` object.
        """
        theme = definition.name
        self._theme_names.add(theme)
        self._theme_definitions[theme] = definition
        self._theme_styles[theme] = set()

    def _resolve_theme_alias(self, themename):
        """Map a pre-2.0 name that was adapted into the curated catalog to that
        theme's variant matching its ORIGINAL light/dark mode.

        Backwards compatibility: five legacy names carry over as curated
        families (``minty``/``pulse``/``sandstone``/``united``/``vapor``). A 1.x
        caller writing ``theme_use("minty")`` expects a *light* minty and
        ``theme_use("vapor")`` a *dark* vapor -- the legacy theme's own mode, not
        the app's current mode. Resolve to ``<name>-<legacy-mode>`` when that
        curated variant is registered; otherwise return the name unchanged, so a
        legacy name with no curated counterpart still falls through to the
        legacy-dict migration path in ``theme_use``.

        A spelling alias (``cerulean`` -> the misspelled-but-canonical
        ``cerculean``) is normalized first, so both spellings resolve.
        """
        themename = LEGACY_THEME_ALIASES.get(themename, themename)
        spec = STANDARD_THEMES.get(themename)
        if spec is not None:
            variant = f"{themename}-{spec.get('type', 'light')}"
            if variant in self._theme_names:
                return variant
        return themename

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set
        the current theme to themename, refreshes all widgets and emits
        a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during*
        runtime. Otherwise, pass the theme name into the Style
        constructor to instantiate the style with a theme.

        Parameters:

            themename (str):
                The name of the theme to apply when creating new widgets

        Returns:

            Union[str, None]:
                The name of the current theme if `themename` is None
                otherwise, `None`.
        """
        if not themename:
            # return current theme
            return super().theme_use()

        # change to an existing theme
        existing_themes = super().theme_names()
        # Backwards compat: a pre-2.0 name adapted into the curated catalog (and
        # not otherwise registered -- so an explicit install_legacy_themes()
        # still wins) resolves to its curated variant at the legacy mode, e.g.
        # theme_use("minty") -> "minty-light". Legacy names with no curated
        # counterpart pass through unchanged to the legacy-dict path below.
        if themename not in existing_themes and themename not in self._theme_names:
            themename = self._resolve_theme_alias(themename)
        if themename in existing_themes:
            self.theme = self._theme_definitions.get(themename)
            super().theme_use(themename)
        # setup a new theme
        elif themename in self._theme_names:
            self.theme = self._theme_definitions.get(themename)
            # Creating the builder also runs theme_create + theme_use for the
            # new theme and builds its default (".") styles.
            self._theme_objects[themename] = StyleBuilderTTK()
        elif themename in STANDARD_THEMES:
            # Legacy (pre-2.0) name: lazily adapt+register just this one theme
            # so the first line of ~every existing app
            # (Window(themename="darkly")) keeps working, warn once, then fall
            # through to the normal build path below. The full legacy catalog
            # stays opt-in via install_legacy_themes() (bulk register, so
            # theme_names()/ttkcreator can enumerate it).
            from ttkbootstrap.themes.legacy import theme_from_legacy_dict

            warnings.warn(
                f"{themename!r} is a legacy (pre-2.0) theme name, kept as a "
                f"migration convenience and planned for removal in 3.0; prefer "
                f"a 2.0 theme (see Style.theme_names()).",
                DeprecationWarning,
                stacklevel=2,
            )
            self.register_theme(
                theme_from_legacy_dict(themename, STANDARD_THEMES[themename])
            )
            self.theme = self._theme_definitions.get(themename)
            # Creating the builder also runs theme_create + theme_use for the
            # new theme and builds its default (".") styles.
            self._theme_objects[themename] = StyleBuilderTTK()
        else:
            raise TclError(themename, "is not a valid theme.")

        # Repaint the live widget tree for the new theme. Each theme has its
        # own clam-derived Tcl style DB, so a style configured under one theme
        # is invisible under another; the walk rebuilds the (theme, style)
        # pairs that mounted widgets actually reference -- O(mounted), not
        # O(all-styles-ever-used) -- and restyles legacy tk widgets inline.
        self._theme_version += 1
        self._theme_walk()

        # Let theme-aware custom styles rebuild against the new theme. Run after
        # the walk so the new theme's colors/styles are fully live. The guard
        # keeps a callback that itself calls theme_use from recursing forever --
        # a nested switch still repaints, it just doesn't re-enter this loop.
        if not self._running_theme_callbacks:
            self._running_theme_callbacks = True
            try:
                for callback in list(self._theme_change_callbacks):
                    self._run_theme_change_callback(callback)
            finally:
                self._running_theme_callbacks = False

    # ------------------------------------------------------------------ #
    # Light/dark theme mode toggling
    # ------------------------------------------------------------------ #
    @property
    def theme_mode(self) -> Optional[str]:
        """The active theme mode (`"light"` or `"dark"`).

        Read it, or assign `"light"`/`"dark"` to switch the current family to
        that mode (the designated theme, else the `-light`/`-dark` sibling)::

            style.theme_mode           # -> "light"
            style.theme_mode = "dark"  # switch

        Reads the active theme's mode; `None` before a theme is applied.
        """
        theme = getattr(self, "theme", None)
        return theme.mode if theme is not None else None

    @theme_mode.setter
    def theme_mode(self, mode: str) -> None:
        self._apply_theme_mode(mode)

    def set_theme_modes(self, light: str = None, dark: str = None) -> None:
        """Designate the light and/or dark theme that `theme_mode` /
        `toggle_theme()` switch between.

        By default the counterpart is derived from the `<family>-light` /
        `<family>-dark` naming convention, so this is only needed to pin a
        specific pair (e.g. a light theme from one family with a dark theme
        from another). Each name must be a registered theme; a name whose own
        type disagrees with the slot it is assigned to earns a warning.

        Parameters:

            light (str):
                Theme to use as the light-mode target.

            dark (str):
                Theme to use as the dark-mode target.
        """
        for mode, name in (("light", light), ("dark", dark)):
            if name is None:
                continue
            if name not in self._theme_names:
                raise ValueError(f"{name!r} is not a registered theme name.")
            definition = self._theme_definitions.get(name)
            if definition is not None and definition.mode != mode:
                warnings.warn(
                    f"designating {name!r} (a {definition.mode} theme) as the "
                    f"{mode} theme; toggling will not change appearance the way "
                    "a matching-type theme would.",
                    UserWarning,
                    stacklevel=2,
                )
            setattr(self, f"_{mode}_theme", name)

    def _theme_for_mode(self, mode: str) -> Optional[str]:
        """Resolve the theme name for `mode`: a designated theme if set, else
        the `<current-family>-<mode>` sibling if it is registered, else None.
        """
        designated = getattr(self, f"_{mode}_theme", None)
        if designated:
            return designated
        current = self.theme.name if getattr(self, "theme", None) else DEFAULT_THEME
        family = current
        for suffix in ("-light", "-dark"):
            if current.endswith(suffix):
                family = current[: -len(suffix)]
                break
        candidate = f"{family}-{mode}"
        return candidate if candidate in self._theme_names else None

    def _apply_theme_mode(self, mode: str) -> Optional[str]:
        """Switch to the light or dark theme (the designated one, else the
        current family's `-light`/`-dark` sibling); returns the resulting mode.

        Backs the `theme_mode` setter and `toggle_theme()`. No-ops with a
        warning if no counterpart exists (e.g. a single legacy theme).
        """
        mode = str(mode).lower()
        if mode not in ("light", "dark"):
            raise ValueError(f"mode must be 'light' or 'dark', got {mode!r}")
        target = self._theme_for_mode(mode)
        if target is None:
            warnings.warn(
                f"no {mode} theme for {self.theme.name!r}; designate one via "
                f"set_theme_modes({mode}=...) or use a theme that has a "
                f"'-{mode}' variant.",
                UserWarning,
                stacklevel=2,
            )
            return self.theme_mode
        if target != self.theme.name:
            self.theme_use(target)
        return self.theme_mode

    def toggle_theme(self) -> Optional[str]:
        """Toggle between the light and dark theme, returning the new mode."""
        other = "dark" if self.theme_mode == "light" else "light"
        return self._apply_theme_mode(other)

    # ------------------------------------------------------------------ #
    # Theme-change callbacks (theme-aware custom styles)
    # ------------------------------------------------------------------ #
    def on_theme_change(self, callback, *, call_now: bool = True):
        """Register ``callback(style)`` to run after every theme change.

        Use it to (re)build a custom style so it tracks the active theme: the
        callback re-runs on each ``theme_use`` / ``toggle_theme``. When
        ``call_now`` (the default), it also runs once immediately if a theme is
        already active, so the style exists before the first switch.

        Returns ``callback``, so it doubles as a decorator.

        Parameters:

            callback (Callable[[Style], None]):
                Called with this `Style`; typically rebuilds a style from
                `style.colors`.

            call_now (bool):
                Also run it once now (if a theme is active).
        """
        newly_added = callback not in self._theme_change_callbacks
        if newly_added:
            self._theme_change_callbacks.append(callback)
        # Only fire on first registration, so a duplicate register is a no-op
        # (idempotent) rather than re-running the callback's side effects.
        if call_now and newly_added and getattr(self, "theme", None) is not None:
            self._run_theme_change_callback(callback)
        return callback

    def remove_theme_change_callback(self, callback) -> None:
        """Unregister a callback previously passed to `on_theme_change`."""
        try:
            self._theme_change_callbacks.remove(callback)
        except ValueError:
            pass

    def _run_theme_change_callback(self, callback) -> None:
        """Run one theme-change callback; a failure warns but never breaks
        theming for the rest of the app."""
        try:
            callback(self)
        except Exception as exc:
            warnings.warn(
                f"theme-change callback "
                f"{getattr(callback, '__name__', callback)!r} raised {exc!r}; "
                "skipping it.",
                UserWarning,
                stacklevel=2,
            )

    def theme_create(self, themename: str, parent: str = None, settings: dict = None) -> None:
        """
        Create a new theme in the Tcl interpreter. If the parent is a registered
        ttkbootstrap theme, the new theme will be registered with a copied
        ThemeDefinition and builder. Duplicate registration is avoided.

        Parameters:

            themename (str):
                The name of the new theme.

            parent (str):
                The name of the parent theme to inherit from.

            settings (dict):
                A dictionary of style settings (Tcl-style).
        """
        from tkinter.ttk import _script_from_settings  # type: ignore[attr-defined]

        script = _script_from_settings(settings) if settings else ''

        # Lazy-load parent if it's a known bootstrap theme
        if parent:
            if parent not in super().theme_names():
                if parent in self._theme_names:
                    self.theme_use(parent)
                else:
                    raise TclError(f"{parent!r} is not a valid theme name or parent theme.")

        # Create the Tcl-level theme
        if parent:
            self.tk.call(
                self._name, "theme", "create", themename,
                "-parent", parent, "-settings", script)
        else:
            self.tk.call(
                self._name, "theme", "create", themename,
                "-settings", script)

        # Register the new theme if copying from a ttkbootstrap theme
        if parent in self._theme_definitions and themename not in self._theme_definitions:
            parent_def = self._theme_definitions[parent]
            copied_def = ThemeDefinition(
                name=themename,
                colors=parent_def.colors,
                mode=parent_def.mode
            )
            self._theme_definitions[themename] = copied_def
            self._theme_names.add(themename)
            self._theme_styles[themename] = set()

            if themename not in self._theme_objects:
                self._theme_objects[themename] = StyleBuilderTTK(build=False)

    def style_exists_in_theme(self, ttkstyle: str):
        """Check if a style exists in the current theme.

        Parameters:

            ttkstyle (str):
                The ttk style to check.

        Returns:

            bool:
                `True` if the style exists, otherwise `False`.
        """
        if self.theme is None:
            return False

        theme_styles = self._theme_styles.get(self.theme.name)
        if theme_styles is None:
            return False

        exists_in_theme = ttkstyle in theme_styles
        exists_in_registry = ttkstyle in self._style_registry
        return exists_in_theme and exists_in_registry

    def use_dynamic_foreground(self, enable: bool = True):
        """Enable or disable dynamic foreground color selection.

        When enabled, the foreground color of widgets will be decided
        between the `fg` and `selectfg` colors based on the
        contrast ratio with the widget's background color.
        At default, this is disabled.

        Parameters:

            enable (bool):
                If `True`, dynamic foreground selection is enabled.
                Otherwise, it is disabled.
        """
        self._dynamic_foreground = enable

    @property
    def dynamic_foreground(self):
        """Returns `True` if dynamic foreground selection is enabled,
        otherwise `False`.
        """
        return self._dynamic_foreground

    @staticmethod
    def get_instance():
        """Returns the singleton `Style` instance (or `None` if not yet created)."""
        return Style.instance

    @staticmethod
    def _get_builder():
        """Get the object that builds the widget styles for the current
        theme.

        Returns:

            StyleBuilderTTK:
                The theme builder object that builds the ttk styles for
                the current theme.
        """
        style: Style = Style.get_instance()
        theme_name = style.theme.name
        return style._theme_objects[theme_name]

    @staticmethod
    def _get_builder_tk():
        """Get the object that builds the widget styles for the current
        theme.

        Returns:

            StyleBuilderTK:
                The theme builder object that builds the ttk styles for
                the current theme.
        """
        builder = Style._get_builder()
        return builder.builder_tk

    def _build_configure(self, style, **kw):
        """Calls configure of superclass; used by style builder classes."""
        super().configure(style, **kw)

    def element_create(self, elementname, etype, *args, **kw):
        """Create a ttk element, idempotently within the current theme.

        ttk raises ``Duplicate element`` if the same element name is created
        twice in one theme. Every ttkbootstrap theme maps to a single
        clam-derived Tcl theme with fixed colors, so an element only ever needs
        to be created once per theme; the second run of a recipe -- whether a
        test that force-rebuilds a style, or a production theme-rebuild after
        the per-theme style registry (`_theme_styles`) desyncs from the Tcl
        theme -- must be a safe no-op, not a crash. The `configure`/`layout`/
        `map` steps that follow are already idempotent, so skipping the redundant
        element create makes the whole recipe re-runnable.
        """
        if elementname in self.element_names():
            return
        super().element_create(elementname, etype, *args, **kw)

    def _load_themes(self, EXTERNAL_THEMES=None):
        """Register the curated 2.0 theme catalog.

        The built-in catalog is the curated semantic-anchor `Theme` families
        (`themes/builtin.py`), each generating a `<name>-light`/`<name>-dark`
        pair. Legacy 16-key dicts passed as `EXTERNAL_THEMES` are adapted through
        the compat quarantine so they keep working. The full pre-2.0 name catalog
        is opt-in via `ttkbootstrap.install_legacy_themes()`.
        """
        from ttkbootstrap.themes.builtin import CURATED_THEMES

        for theme in CURATED_THEMES:
            for definition in theme.to_definitions():
                self.register_theme(definition)

        # Legacy 16-key dicts (caller-provided), cleaned through the compat adapter.
        if EXTERNAL_THEMES:
            from ttkbootstrap.themes.legacy import theme_from_legacy_dict

            for name, spec in EXTERNAL_THEMES.items():
                self.register_theme(theme_from_legacy_dict(name, spec))

    def _register_ttkstyle(self, ttkstyle):
        """Register that a ttk style name. This ensures that the
        builder will not attempt to build a style that has already
        been created.

        Parameters:

            ttkstyle (str):
                The name of the ttk style to register.
        """
        self._style_registry.add(ttkstyle)
        theme = self.theme.name
        self._theme_styles[theme].add(ttkstyle)
        # A recipe just (re)built this style, overwriting any user override with
        # its hardcoded defaults. Replay the durable overrides so the user wins.
        self._reapply_user_options(ttkstyle)

    # -- durable style options (#1238/#1161) -------------------------------- #

    def _record_user_options(self, style, kw):
        """Record the durable (geometry) subset of a user `configure()` call.

        Colors are intentionally skipped so they stay theme-reactive. Already-
        built descendant variants are updated now (retroactive fan-out), so the
        override reaches existing styles too and the result is independent of
        whether the override or the widget came first.
        """
        recorded = {k: v for k, v in kw.items() if k in DURABLE_STYLE_OPTIONS}
        if not recorded:
            return
        self._user_options.setdefault(style, {}).update(recorded)
        for built in list(self._theme_styles.get(self.theme.name, ())):
            # Derived styles are skipped inside _reapply_user_options (#1284), so
            # the retroactive path needs no separate guard here.
            if built != style and style in self._style_ancestors(built):
                self._reapply_user_options(built)

    @staticmethod
    def _style_ancestors(style):
        """ttk's dotted-name resolution chain, least- to most-specific.

        ``"danger.Outline.TButton"`` -> ``["TButton", "Outline.TButton",
        "danger.Outline.TButton"]``. Mirrors ttk stripping leading tokens, so an
        override set on the base class fans out to its variants (#1238).
        """
        parts = style.split(".")
        return [".".join(parts[i:]) for i in range(len(parts) - 1, -1, -1)]

    def _reapply_user_options(self, built_style=None):
        """Replay durable user overrides after a style (re)build.

        For ``built_style``, overrides recorded on it AND on its base-class
        ancestors are merged most-specific-wins and applied in one write (the
        base-class fan-out). Every other recorded override is restored onto its
        own name, which also covers un-namespaced globals like ``"Sash"`` that
        any build clobbers (#1161). Writes go through ``_build_configure`` (the
        internal path), so they are not re-recorded.
        """
        if not self._user_options:
            return
        # A framework-derived style (icon styles) is excluded from fan-out: it
        # inherits a base-class `configure` natively and owns its computed values
        # (#1284). It never carries its own recorded overrides, so there is
        # nothing else to replay onto it either.
        if built_style in self._derived_styles:
            return
        handled = set()
        if built_style:
            merged = {}
            for name in self._style_ancestors(built_style):
                opts = self._user_options.get(name)
                if opts:
                    merged.update(opts)
                    handled.add(name)
            if merged:
                self._build_configure(built_style, **merged)
        for name, opts in self._user_options.items():
            if name not in handled and opts:
                self._build_configure(name, **opts)

    def _effective_style_option(self, ttk_style, option, default=None):
        """The value `ttk_style` will end up with for `option`.

        Prefers a durable user override (most-specific ancestor wins) over the
        current Tcl lookup. A recipe that *derives* geometry from an option (e.g.
        treeview `rowheight` from `font`) must consult the registry rather than
        `lookup` alone: overrides are re-applied AFTER the recipe runs, so the
        lookup would still see the pre-override value.
        """
        for name in reversed(self._style_ancestors(ttk_style)):
            opts = self._user_options.get(name)
            if opts and option in opts:
                return opts[option]
        # `lookup` returns "" for an unset option; anything else is a real value
        # -- including falsy ones like 0, which must not fall through to
        # `default` (a `borderwidth` of 0 is a value, not an absence).
        looked_up = self.lookup(ttk_style, option)
        return default if looked_up == "" else looked_up

    def reset_style_options(self, style=None):
        """Drop durable style-option overrides recorded via ``configure()``.

        With no argument, clears every recorded override; with a style name,
        clears only that one. The recipe's default value returns the next time
        the affected style is rebuilt (a theme switch or a new variant build).

        Parameters:

            style (str, optional):
                The style name to reset; ``None`` (default) resets all.
        """
        if style is None:
            self._user_options.clear()
        else:
            self._user_options.pop(style, None)

    def _theme_walk(self):
        """Repaint the live widget tree for the current theme.

        Depth-first over `winfo_children()` from the root, repainting only
        widgets stamped older than `_theme_version` (so each widget is touched
        at most once per switch). ttk widgets get their `(theme, style)`
        rebuilt on demand; legacy tk widgets are restyled inline. Because the
        walk reaches every mounted widget through the tree, it replaces both
        the Publisher broadcast (legacy tk widgets) and the
        rebuild-every-registered-style scan (ttk widgets).
        """
        root = self.master
        if root is None:
            return

        version = self._theme_version
        stack = [root]
        while stack:
            widget = stack.pop()
            # Honor autostyle=False: such widgets opted out of theming and are
            # never repainted, but their (autostyled) descendants still are.
            if not getattr(widget, "_tb_no_autostyle", False):
                if getattr(widget, "_theme_version", None) != version:
                    self._repaint_widget(widget)
                    try:
                        widget._theme_version = version
                    except (AttributeError, TypeError):
                        # Builtin/extension widgets that forbid new attributes
                        # are simply repainted on every switch -- correct, just
                        # not skippable.
                        pass
            try:
                stack.extend(widget.winfo_children())
            except TclError:
                pass

    def _repaint_widget(self, widget):
        """Restyle a single widget for the current theme.

        ttk widgets ensure their style exists under the active theme (rebuilt
        lazily by the builder if stale); legacy tk widgets re-run their tk
        update method. The combobox popdown -- a Tcl toplevel the DFS cannot
        reach -- is refreshed inside `update_ttk_widget_style`.
        """
        # local import breaks the engine<-bootstyle cycle (bootstyle imports engine)
        from ttkbootstrap.style.bootstyle import Bootstyle

        if isinstance(widget, ttk.Widget):
            Bootstyle.update_ttk_widget_style(widget)
        else:
            Bootstyle.update_tk_widget_style(widget)

    def _get_or_create_image(self, key, factory):
        """Return the Tcl name of a cached asset image, building on a miss.

        Content-addressed memoization: `key` must capture every
        pixel-determining input of the asset (resolved colors, scaled pixel
        size, geometry/variant) so identical assets dedupe across themes and
        are rendered exactly once. The cache holds a strong reference to the
        `PhotoImage`, keeping its Tcl image alive for as long as styles
        reference it by name.

        Parameters:

            key:
                A hashable tuple of the asset's pixel-determining inputs.

            factory (Callable[[], ImageTk.PhotoImage]):
                A zero-arg builder that renders the image. Called only on a
                cache miss; must be pure with respect to `key`.

        Returns:

            str:
                The tcl/tk image name to use in the style.
        """
        cached = self._image_cache.get(key)
        if cached is not None:
            return cached[0]
        image = factory()
        name = util.get_image_name(image)
        self._image_cache[key] = (name, image)
        return name

    def clear_image_cache(self):
        """Drop all cached widget asset images.

        Releases the cached `PhotoImage` objects (and their underlying Tcl
        images). This is a memory-reclamation and diagnostics escape hatch, not
        a live refresh: styles are built once per `(theme, style)`, so styles
        built before the clear keep referencing the freed image names until
        they are rebuilt -- which happens when a not-yet-built theme is
        activated, not on a same-theme switch. Clear when image widgets for the
        affected styles are not currently displayed (e.g. before moving to a
        fresh theme), or to reclaim memory at shutdown.
        """
        self._image_cache.clear()

    def load_user_theme(self, theme: ThemeDefinition):
        """Load a user theme definition"""
        self.register_theme(theme)

    def load_user_themes(self, file):
        """Load user themes saved in json format"""
        with open(file, encoding='utf-8') as f:
            data = json.load(f)
            themes = data['themes']
        for theme in themes:
            for name, definition in theme.items():
                self.register_theme(
                    ThemeDefinition(
                        name=name,
                        mode=definition.get("mode") or definition["type"],
                        colors=definition["colors"],
                    )
                )
