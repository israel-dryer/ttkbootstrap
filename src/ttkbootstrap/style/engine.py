"""The ttkbootstrap style engine.

`Style` is the process-wide singleton (subclasses `ttk.Style`): it owns the
theme definitions, the active theme, the version-stamped theme walk, and the
content-addressed image cache. Split out of the monolithic `style.py` in 2.0.
"""
import json
import warnings
from tkinter import TclError, ttk
from typing import Any

from ttkbootstrap.internal import utility as util
from ttkbootstrap.constants import *
from ttkbootstrap.themes.standard import STANDARD_THEMES

from ttkbootstrap.style.theme import ThemeDefinition
from ttkbootstrap.style.scaling import Scaling
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK

try:
    # prevent app from failing if user.py gets corrupted
    from ttkbootstrap.themes.user import USER_THEMES
except (ImportError, ModuleNotFoundError):
    USER_THEMES = {}

try:
    from ttkbootstrap.themes.user import USER_THEME_SPECS
except (ImportError, ModuleNotFoundError):
    USER_THEME_SPECS = {}


class Style(ttk.Style):
    """A singleton class for creating and managing the application
    theme and widget styles.

    This class is meant to be a drop-in replacement for `ttk.Style` and
    inherits all of it's methods and properties. However, in
    ttkbootstrap, this class is implemented as a singleton. Subclassing
    is not recommended and may have unintended consequences.

    Examples:

        ```python
        # instantiate the style with default theme
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='bootstrap-dark')

        # check all available themes
        for theme in style.theme_names():
            print(theme)
        ```

    See the [Python documentation](https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Style)
    on this class for more details.
    """

    instance = None

    def __new__(cls, theme=None, default_button="neutral"):
        if Style.instance is None:
            return object.__new__(cls)
        else:
            return Style.instance

    def __init__(self, theme=DEFAULT_THEME, default_button="neutral"):
        """
        Parameters:

            theme (str):
                The name of the theme to use when styling the widget.

            default_button (str):
                The color a bare `Button`/`Menubutton` (no `bootstyle`) uses.
                Defaults to `"neutral"`; pass `"primary"` for the pre-2.0
                accented default. Read once when the base styles build, so set it
                on the first `Style`/`Window`; ignored on the existing singleton.
        """
        if Style.instance is not None:
            if theme != DEFAULT_THEME:
                Style.instance.theme_use(theme)
            return
        # Set before theme_use() below, which builds the base TButton/TMenubutton
        # styles that read this to resolve their default (no-color) fill.
        self.default_button = default_button
        self._theme_objects = {}
        self._theme_definitions = {}
        self._style_registry = set()  # all styles used
        self._theme_styles = {}  # styles used in theme
        self._theme_names = set()
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
        self._load_themes()
        self._dynamic_foreground = False
        super().__init__()
        self.scaling = Scaling.for_widget(self.master)

        Style.instance = self
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
                themetype=parent_def.type
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

    def _load_themes(self, EXTERNAL_THEMES=None):
        """Register the curated 2.0 theme catalog (and any user themes).

        The built-in catalog is the curated semantic-anchor `Theme` families
        (`themes/builtin.py`), each generating a `<name>-light`/`<name>-dark`
        pair. User-authored 16-key dicts (`USER_THEMES`, `EXTERNAL_THEMES`) are
        adapted through the legacy quarantine so they keep working and gain the
        plumbing cleanup. The full pre-2.0 name catalog is opt-in via
        `ttkbootstrap.install_legacy_themes()`.
        """
        from ttkbootstrap.themes.builtin import CURATED_THEMES
        from ttkbootstrap.style.theme import Theme

        for theme in CURATED_THEMES:
            for definition in theme.to_definitions():
                self.register_theme(definition)

        # 2.0 user themes: semantic-anchor Theme specs generate light/dark pairs.
        for name, spec in USER_THEME_SPECS.items():
            for definition in Theme(name=name, **spec).to_definitions():
                self.register_theme(definition)

        # Legacy 16-key user/external dicts, cleaned through the compat adapter.
        extra = {}
        if USER_THEMES:
            extra.update(USER_THEMES)
        if EXTERNAL_THEMES:
            extra.update(EXTERNAL_THEMES)
        if extra:
            from ttkbootstrap.themes.legacy import theme_from_legacy_dict

            for name, spec in extra.items():
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
                        themetype=definition["type"],
                        colors=definition["colors"],
                    )
                )
