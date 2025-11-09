"""Bootstyle parsing and widget integration for ttkbootstrap.

Handles parsing of bootstyle strings and provides integration layer between
user-friendly bootstyle syntax and TTK style names.
"""

from __future__ import annotations

from typing import Optional

from ttkbootstrap.appconfig import AppConfig

# Standard ttkbootstrap color tokens
COLORS = {
    'primary', 'secondary', 'success', 'info',
    'warning', 'danger', 'light', 'dark'
}

# Widget class name mappings
WIDGET_CLASS_MAP = {
    'button': 'TButton',
    'label': 'TLabel',
    'entry': 'TEntry',
    'frame': 'TFrame',
    'labelframe': 'TLabelframe',
    'progressbar': 'TProgressbar',
    'scale': 'TScale',
    'scrollbar': 'TScrollbar',
    'checkbutton': 'TCheckbutton',
    'radiobutton': 'TRadiobutton',
    'combobox': 'TCombobox',
    'notebook': 'TNotebook',
    'treeview': 'Treeview',
    'separator': 'TSeparator',
    'sizegrip': 'TSizegrip',
    'panedwindow': 'TPanedwindow',
    'spinbox': 'TSpinbox',
    'menubutton': 'TMenubutton',
}

WIDGET_NAME_MAP = {v: k for k, v in WIDGET_CLASS_MAP.items()}

FRAME_SURFACE_CLASSES = {'TFrame', 'TLabelframe'}


def parse_bootstyle_v2(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using V2 syntax (dash-separated).

    Syntax: `color-variant-widget` where all parts are optional.
    Checks actual theme colors and registered variants. Unknown parts are
    treated as custom colors.

    Args:
        bootstyle: Bootstyle string (e.g., "success-outline", "primary")
        widget_class: TTK widget class name (e.g., "TButton")

    Returns:
        Dict with: color, variant, widget_class, cross_widget
    """
    if not bootstyle:
        return {
            'color': None,
            'variant': "default",
            'widget_class': widget_class,
            'cross_widget': False
        }

    from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
    from ttkbootstrap.style.theme_provider import ThemeProvider

    theme_colors = ThemeProvider.instance().colors
    parts = bootstyle.lower().split('-')

    color = None
    variant = None
    resolved_widget = widget_class
    cross_widget = False

    for part in parts:
        if part in theme_colors:
            color = part
        elif part in WIDGET_CLASS_MAP:
            resolved_widget = WIDGET_CLASS_MAP[part]
            if resolved_widget != widget_class:
                cross_widget = True
        elif BootstyleBuilder.has_builder(resolved_widget, part):
            variant = part
        elif '[' in part or '#' in part or part in COLORS:
            color = part
        else:
            color = part

    return {
        'color': color,
        'variant': variant,
        'widget_class': resolved_widget,
        'cross_widget': cross_widget
    }


def generate_ttk_style_name(
        color: Optional[str],
        variant: Optional[str],
        widget_class: str,
        custom_prefix: Optional[str] = None,
        surface_color: Optional[str] = None) -> str:
    """Generate TTK style name from parsed components.

    Returns style name in format: [surface].[custom_prefix].[color].[Variant].[Widget]
    """
    parts = []

    if surface_color and surface_color != 'background':
        parts.append(f"Surface[{surface_color}]")
    if custom_prefix:
        parts.append(custom_prefix)
    if color:
        parts.append(color)
    if variant:
        parts.append(variant.capitalize())

    parts.append(widget_class)
    return '.'.join(parts)


def parse_bootstyle_legacy(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle using legacy V1 regex syntax (deprecated).

    Currently falls back to V2 parsing. TODO: Extract actual legacy logic.
    """
    return parse_bootstyle_v2(bootstyle, widget_class)


def parse_bootstyle(bootstyle: str, widget_class: str) -> dict:
    """Parse bootstyle string using configured parsing method.

    Main entry point for bootstyle parsing. Checks AppConfig.legacy_bootstyle
    flag to determine parsing method (V1 legacy vs V2 new).
    """
    use_legacy = AppConfig.get('legacy_bootstyle', False)
    return parse_bootstyle_legacy(bootstyle, widget_class) if use_legacy else parse_bootstyle_v2(
        bootstyle, widget_class)


def extract_color_from_style(ttk_style: str, default: str = 'primary') -> str:
    """Extract color token from TTK style name."""
    parts = ttk_style.split('.')
    if parts and parts[0].startswith('custom_'):
        parts = parts[1:]

    for part in parts:
        if part.lower() in COLORS:
            return part.lower()

    return default


def extract_variant_from_style(ttk_style: str) -> Optional[str]:
    """Extract variant name from TTK style name."""
    parts = ttk_style.split('.')

    if parts and parts[0].startswith('custom_'):
        parts = parts[1:]

    for part in parts:
        part_lower = part.lower()
        if part_lower not in COLORS and not part.startswith('T'):
            return part_lower

    return None


def extract_widget_class_from_style(ttk_style: str) -> Optional[str]:
    """Extract widget class from TTK style name."""
    parts = ttk_style.split('.')

    for part in parts:
        if part.startswith('T'):
            return part

    return None


class Bootstyle:
    """Widget integration layer for bootstyle functionality.

    Wires ttkbootstrap into tkinter/ttk by overriding widget constructors and
    configure methods to accept `bootstyle` parameter.
    """

    @staticmethod
    def create_ttk_style(
            widget_class: str,
            bootstyle: Optional[str] = None,
            style_options: Optional[dict] = None,
            surface_color: Optional[str] = None) -> str:
        """Create or get TTK style name for a widget.

        Parses bootstyle string, generates TTK style name, and triggers style creation.
        """
        from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder

        if not bootstyle:
            return widget_class

        parsed = parse_bootstyle(bootstyle, widget_class)
        color = parsed['color']
        variant = parsed['variant']
        resolved_widget = parsed['widget_class']

        custom_prefix = None
        if style_options:
            import hashlib
            import json
            options_str = json.dumps(style_options, sort_keys=True)
            options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
            custom_prefix = f"custom_{options_hash}"

        builder_variant = variant if variant is not None else \
            BootstyleBuilder.get_default_variant(resolved_widget)

        if (surface_color is None or surface_color == 'background') and \
                resolved_widget in FRAME_SURFACE_CLASSES and color:
            surface_color = color

        ttk_style = generate_ttk_style_name(
            color=color,
            variant=variant,
            widget_class=resolved_widget,
            custom_prefix=custom_prefix,
            surface_color=surface_color
        )

        from ttkbootstrap.style.style import use_style
        style = use_style()

        options = dict(style_options or {})
        if surface_color and surface_color != 'background':
            options['surface_color'] = surface_color

        style.create_style(
            widget_class=resolved_widget,
            variant=builder_variant,
            ttkstyle=ttk_style,
            color=color,
            options=options
        )

        return ttk_style

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override ttk widget __init__ to accept bootstyle parameter."""

        def __init__wrapper(self, *args, **kwargs):
            had_style_kwarg = 'style' in kwargs

            bootstyle = kwargs.pop("bootstyle", "")
            bs_style = kwargs.pop("bs_style", "")
            style_options = kwargs.pop("style_options", None)
            inherit_flag_arg = kwargs.pop('inherit_surface_color', None)
            explicit_surface_arg = kwargs.pop('surface_color', None)

            func(self, *args, **kwargs)

            try:
                widget_class = self.winfo_class()
            except Exception:
                widget_class = None

            try:
                style_str = bootstyle or bs_style

                if hasattr(self, 'master') and self.master is not None:
                    parent_surface = getattr(self.master, '_surface_color', 'background')
                else:
                    parent_surface = 'background'

                inherit_flag = inherit_flag_arg
                if inherit_flag is None:
                    inherit_flag = AppConfig.get('inherit_surface_color', True)

                explicit_surface = explicit_surface_arg
                if explicit_surface:
                    effective_surface = explicit_surface
                elif inherit_flag:
                    effective_surface = parent_surface
                else:
                    effective_surface = 'background'

                if style_str and widget_class in FRAME_SURFACE_CLASSES and explicit_surface is None:
                    try:
                        parsed = parse_bootstyle(style_str, widget_class)
                        if parsed.get('color'):
                            effective_surface = parsed['color']
                    except Exception:
                        pass

                try:
                    setattr(self, '_surface_color', effective_surface)
                except Exception:
                    from ttkbootstrap.utility import debug_log_exception
                    debug_log_exception("autostyle: reading background color from Style failed")
                if style_str and widget_class:
                    ttkstyle = Bootstyle.create_ttk_style(
                        widget_class=widget_class,
                        bootstyle=style_str,
                        style_options=style_options,
                        surface_color=effective_surface,
                    )
                    try:
                        self.configure(style=ttkstyle)
                    except Exception:
                        pass
                elif widget_class and not had_style_kwarg:
                    from ttkbootstrap.style.bootstyle_builder import BootstyleBuilder
                    from ttkbootstrap.style.style import use_style
                    default_variant = BootstyleBuilder.get_default_variant(widget_class)
                    if BootstyleBuilder.has_builder(widget_class, default_variant):
                        ttkstyle = generate_ttk_style_name(
                            color=None,
                            variant=default_variant,
                            widget_class=widget_class,
                            surface_color=effective_surface,
                        )

                        style_instance = use_style()
                        if style_instance is not None:
                            options = dict(style_options or {})
                            if effective_surface and effective_surface != 'background':
                                options['surface_color'] = effective_surface
                            style_instance.create_style(
                                widget_class=widget_class,
                                variant=default_variant,
                                ttkstyle=ttkstyle,
                                options=options,
                            )
                            try:
                                self.configure(style=ttkstyle)
                            except Exception:
                                pass
                    else:
                        try:
                            self.configure(style=widget_class)
                        except Exception:
                            pass
            except Exception:
                pass

        return __init__wrapper

    @staticmethod
    def override_ttk_widget_configure(func):
        """Override ttk widget configure to accept bootstyle parameter."""

        def configure(self, cnf=None, **kwargs):
            if cnf in ("bootstyle", "style"):
                try:
                    return self.cget("style")
                except Exception:
                    return ""

            if cnf is not None:
                return func(self, cnf)

            style_options = kwargs.pop("style_options", None)
            inherit_flag = kwargs.pop('inherit_surface_color', None)
            explicit_surface = kwargs.pop('surface_color', None)

            style_str = None
            if "bootstyle" in kwargs and kwargs["bootstyle"]:
                style_str = kwargs.pop("bootstyle")
            elif "bs_style" in kwargs and kwargs["bs_style"]:
                style_str = kwargs.pop("bs_style")

            if style_str:
                try:
                    widget_class = self.winfo_class()
                    if explicit_surface is not None:
                        surface = explicit_surface
                    else:
                        if inherit_flag is None:
                            inherit_flag = AppConfig.get('inherit_surface_color', True)
                        if inherit_flag:
                            surface = 'background'
                            try:
                                if hasattr(self, 'master') and self.master is not None:
                                    surface = getattr(self.master, '_surface_color', 'background')
                            except Exception:
                                pass
                        else:
                            surface = getattr(self, '_surface_color', 'background')

                    if widget_class in FRAME_SURFACE_CLASSES and explicit_surface is None:
                        try:
                            parsed = parse_bootstyle(style_str, widget_class)
                            if parsed.get('color'):
                                surface = parsed['color']
                        except Exception:
                            pass

                    try:
                        setattr(self, '_surface_color', surface)
                    except Exception:
                        pass
                    ttkstyle = Bootstyle.create_ttk_style(
                        widget_class=widget_class,
                        bootstyle=style_str,
                        style_options=style_options,
                        surface_color=surface,
                    )
                    kwargs["style"] = ttkstyle
                except Exception:
                    from ttkbootstrap.utility import debug_log_exception
                    debug_log_exception("autostyle: apply tk builder failed")

            return func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def override_tk_widget_constructor(func):
        """Override Tk widget __init__ to apply theme background when autostyle=True."""

        def __init__wrapper(self, *args, **kwargs):
            autostyle = kwargs.pop("autostyle", True)

            inherit_flag = kwargs.pop('inherit_surface_color', None)
            if inherit_flag is None:
                inherit_flag = AppConfig.get('inherit_surface_color', True)
            explicit_surface = kwargs.pop('surface_color', None)

            func(self, *args, **kwargs)

            try:
                if hasattr(self, 'master') and self.master is not None:
                    parent_surface = getattr(self.master, '_surface_color', 'background')
                else:
                    parent_surface = 'background'

                if explicit_surface:
                    effective_surface = explicit_surface
                elif inherit_flag:
                    effective_surface = parent_surface
                else:
                    effective_surface = 'background'

                setattr(self, '_surface_color', effective_surface)
            except Exception:
                pass

            if autostyle:
                bg = None
                inst = None  # Active ttkbootstrap Style singleton
                try:
                    from ttkbootstrap.style.style import use_style
                    master = self.winfo_toplevel()
                    inst = use_style(master=master)
                    if inst is not None:
                        bg = inst.builder_manager.color('background')
                except Exception:
                    from ttkbootstrap.utility import debug_log_exception
                    debug_log_exception("autostyle: acquire Style instance or background failed")

                if bg is None:
                    try:
                        from ttkbootstrap.style.theme_provider import ThemeProvider
                        bg = ThemeProvider.instance().colors.get('background')
                    except Exception:
                        bg = None

                if bg is not None:
                    try:
                        self.configure(background=bg)
                    except Exception:
                        pass

                try:
                    from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderTk
                    # Use the same theme provider as the active Style instance
                    builder_tk = BootstyleBuilderTk(
                        theme_provider=inst.theme_provider if inst else None,
                        style_instance=inst)
                    surface = getattr(self, '_surface_color', 'background')
                    builder_tk.call_builder(self, surface_color=surface)
                except Exception:
                    pass

                try:
                    from ttkbootstrap.style.style import use_style
                    # Get the root window to pass as master
                    master = self.winfo_toplevel()
                    inst = use_style(master=master)
                    if inst is not None:
                        inst.register_tk_widget(self)
                except Exception:
                    pass

        return __init__wrapper

    @staticmethod
    def setup_ttkbootstrap_api():
        """Install bootstyle API into ttk/tk widgets via monkey patching."""
        try:
            from ttkbootstrap.widgets import TTK_WIDGETS, TK_WIDGETS
        except Exception:
            return

        try:
            import ttkbootstrap.style.builders_tk  # noqa: F401
        except Exception:
            pass

        for widget in TTK_WIDGETS:
            try:
                _init = Bootstyle.override_ttk_widget_constructor(widget.__init__)
                widget.__init__ = _init

                _configure = Bootstyle.override_ttk_widget_configure(widget.configure)
                widget.configure = _configure
                widget.config = widget.configure

                if getattr(widget, "__name__", "") != "OptionMenu":
                    _orig_getitem = getattr(widget, "__getitem__", None)
                    _orig_setitem = getattr(widget, "__setitem__", None)

                    if _orig_getitem and _orig_setitem:
                        def __setitem(self, key, val):
                            if key in ("bootstyle", "style"):
                                return _configure(self, **{key: val})
                            return _orig_setitem(self, key, val)

                        def __getitem(self, key):
                            if key in ("bootstyle", "style"):
                                return _configure(self, cnf=key)
                            return _orig_getitem(self, key)

                        widget.__setitem__ = __setitem
                        widget.__getitem__ = __getitem
            except Exception:
                continue

        for widget in TK_WIDGETS:
            try:
                _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
                widget.__init__ = _init
            except Exception:
                continue


__all__ = [
    'parse_bootstyle',
    'parse_bootstyle_v2',
    'parse_bootstyle_legacy',
    'generate_ttk_style_name',
    'extract_color_from_style',
    'extract_variant_from_style',
    'extract_widget_class_from_style',
    'Bootstyle',
    'COLORS',
    'WIDGET_CLASS_MAP',
    'WIDGET_NAME_MAP',
]
