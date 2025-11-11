"""Bootstyle parsing and widget integration for ttkbootstrap.

Handles parsing of bootstyle strings and provides integration layer between
user-friendly bootstyle syntax and TTK style names.
"""

from __future__ import annotations

from typing import Optional

from ttkbootstrap.appconfig import AppConfig
from ttkbootstrap.exceptions import BootstyleParsingError
from ttkbootstrap.style.token_maps import COLOR_TOKENS, FRAME_SURFACE_CLASSES, WIDGET_CLASS_MAP


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

    from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk
    from ttkbootstrap.style.theme_provider import use_theme

    theme_colors = use_theme().colors
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
        elif BootstyleBuilderBuilderTTk.has_builder(resolved_widget, part):
            variant = part
        elif '[' in part or part in COLOR_TOKENS:
            color = part
        else:
            message = f"Unrecognized variant or color token: '{part}'"
            raise BootstyleParsingError(message)

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
        custom_prefix: Optional[str] = None) -> str:
    """Generate TTK style name from parsed components.

    Returns style name in format: [custom_prefix].[color].[Variant].[Widget]
    """
    parts = []

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

    for part in parts:
        if part.lower() in COLOR_TOKENS:
            return part.lower()

    return default


def extract_variant_from_style(ttk_style: str) -> Optional[str]:
    """Extract variant name from TTK style name."""
    parts = ttk_style.split('.')

    for part in parts:
        part_lower = part.lower()
        if part_lower not in COLOR_TOKENS and not part.startswith('T'):
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
        from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk

        if not bootstyle:
            return widget_class

        parsed = parse_bootstyle(bootstyle, widget_class)
        color = parsed['color']
        variant = parsed['variant']
        resolved_widget = parsed['widget_class']

        builder_variant = variant if variant is not None else \
            BootstyleBuilderBuilderTTk.get_default_variant(resolved_widget)

        if (surface_color is None or surface_color == 'background') and \
                resolved_widget in FRAME_SURFACE_CLASSES and color:
            surface_color = color

        options = dict(style_options or {})
        if surface_color and surface_color != 'background':
            options['surface_color'] = surface_color

        custom_prefix = None

        if style_options or surface_color != 'background':
            import hashlib
            import json
            options_str = json.dumps(options, sort_keys=True)
            options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
            custom_prefix = f"bs[{options_hash}]"

        ttk_style = generate_ttk_style_name(
            color=color,
            variant=variant,
            widget_class=resolved_widget,
            custom_prefix=custom_prefix
        )

        from ttkbootstrap.style.style import use_style
        style = use_style()

        style.create_style(
            widget_class=resolved_widget,
            variant=builder_variant,
            ttk_style=ttk_style,
            color=color,
            options=options
        )

        return ttk_style

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override ttk widget __init__ to accept bootstyle parameter."""

        def __init__wrapper(self, *args, **kwargs):

            # extract bootstyle & style arguments
            had_style_kwarg = 'style' in kwargs
            bootstyle = kwargs.pop("bootstyle", "")
            style_options = kwargs.pop("style_options", None)
            inherit_surface_color = kwargs.pop('inherit_surface_color', None)
            surface_color_token = kwargs.pop('surface_color', None)
            # Capture an optional icon spec for image-capable widgets
            icon_spec = kwargs.pop('icon', None)

            func(self, *args, **kwargs)  # the actual widget constructor

            widget_class = self.winfo_class()
            style_str = bootstyle

            # ===== Surface color inheritance =====

            if hasattr(self, 'master') and self.master is not None:
                parent_surface_token = getattr(self.master, '_surface_color', 'background')
            else:
                parent_surface_token = 'background'

            if inherit_surface_color is None:
                inherit_surface_color = AppConfig.get('inherit_surface_color', True)

            if surface_color_token:
                effective_surface_token = surface_color_token
            elif inherit_surface_color:
                effective_surface_token = parent_surface_token
            else:
                effective_surface_token = 'background'

            # frame widgets can take their surface color from the bootstyle
            if style_str and widget_class in FRAME_SURFACE_CLASSES and surface_color_token is None:
                parsed = parse_bootstyle(style_str, widget_class)
                if parsed.get('color'):
                    effective_surface_token = parsed['color']

            setattr(self, '_surface_color', effective_surface_token)

            # ==== Create actual ttk style & assign to widget =====

            if style_str and widget_class:
                # If this widget supports images and an icon was provided, pass to builder
                try:
                    supports_image = 'image' in self.keys()
                except Exception:
                    supports_image = False
                if icon_spec is not None and supports_image:
                    # Merge icon into style_options
                    _opts = dict(style_options or {})
                    _opts['icon'] = icon_spec
                    style_options = _opts
                ttk_style = Bootstyle.create_ttk_style(
                    widget_class=widget_class,
                    bootstyle=style_str,
                    style_options=style_options,
                    surface_color=effective_surface_token,
                )
                self.configure(style=ttk_style)

            elif widget_class and not had_style_kwarg:
                from ttkbootstrap.style.bootstyle_builder_ttk import BootstyleBuilderBuilderTTk
                from ttkbootstrap.style.style import use_style
                default_variant = BootstyleBuilderBuilderTTk.get_default_variant(widget_class)

                if BootstyleBuilderBuilderTTk.has_builder(widget_class, default_variant):
                    ttk_style = generate_ttk_style_name(
                        color=None,
                        variant=default_variant,
                        widget_class=widget_class
                    )

                    style_instance = use_style()
                    if style_instance is not None:
                        options = dict(style_options or {})
                        # Include icon for image-capable widgets
                        try:
                            supports_image = 'image' in self.keys()
                        except Exception:
                            supports_image = False
                        if icon_spec is not None and supports_image:
                            options['icon'] = icon_spec
                        if effective_surface_token and effective_surface_token != 'background':
                            options['surface_color'] = effective_surface_token
                        style_instance.create_style(
                            widget_class=widget_class,
                            variant=default_variant,
                            ttk_style=ttk_style,
                            options=options,
                        )
                        self.configure(style=ttk_style)
                else:
                    self.configure(style=widget_class)

        return __init__wrapper

    @staticmethod
    def override_ttk_widget_configure(func):
        """Override ttk widget configure to accept bootstyle parameter."""

        def configure(self, cnf=None, **kwargs):
            if cnf in ("bootstyle", "style"):
                return self.cget("style")

            if cnf is not None:
                return func(self, cnf)

            style_options = kwargs.pop("style_options", None)
            inherit_flag = kwargs.pop('inherit_surface_color', None)
            explicit_surface = kwargs.pop('surface_color', None)
            # Capture an optional icon spec for image-capable widgets
            icon_spec = kwargs.pop('icon', None)

            style_str = None
            if "bootstyle" in kwargs and kwargs["bootstyle"]:
                style_str = kwargs.pop("bootstyle")

            if style_str:
                widget_class = self.winfo_class()
                if explicit_surface is not None:
                    surface = explicit_surface
                else:
                    if inherit_flag is None:
                        inherit_flag = AppConfig.get('inherit_surface_color', True)
                    if inherit_flag:
                        surface = 'background'
                        if hasattr(self, 'master') and self.master is not None:
                            surface = getattr(self.master, '_surface_color', 'background')
                    else:
                        surface = getattr(self, '_surface_color', 'background')

                if widget_class in FRAME_SURFACE_CLASSES and explicit_surface is None:
                    parsed = parse_bootstyle(style_str, widget_class)
                    if parsed.get('color'):
                        surface = parsed['color']
                    setattr(self, '_surface_color', surface)
                # If this widget supports images and an icon was provided, pass to builder
                try:
                    supports_image = 'image' in self.keys()
                except Exception:
                    supports_image = False
                if icon_spec is not None and supports_image:
                    _opts = dict(style_options or {})
                    _opts['icon'] = icon_spec
                    style_options = _opts
                ttk_style = Bootstyle.create_ttk_style(
                    widget_class=widget_class,
                    bootstyle=style_str,
                    style_options=style_options,
                    surface_color=surface,
                )
                kwargs["style"] = ttk_style

            return func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def override_tk_widget_constructor(func):
        """Override Tk widget __init__ to apply theme background when autostyle=True."""

        def __init__wrapper(self, *args, **kwargs):

            # capture bootstrap arguments
            auto_style = kwargs.pop("autostyle", True)
            inherit_surface_color = kwargs.pop('inherit_surface_color', None)
            if inherit_surface_color is None:
                inherit_surface_color = AppConfig.get('inherit_surface_color', True)
            surface_token = kwargs.pop('surface_color', None)

            func(self, *args, **kwargs)  # the actual constructor

            # ===== Surface color inheritance =====

            if hasattr(self, 'master') and self.master is not None:
                parent_surface_token = getattr(self.master, '_surface_color', 'background')
            else:
                parent_surface_token = 'background'

            if inherit_surface_color:
                surface_token = parent_surface_token
            else:
                surface_token = surface_token or 'background'

            setattr(self, '_surface_color', surface_token)

            if not auto_style:
                return

            # ==== Update widget style & register for theme changes =====

            from ttkbootstrap.style.style import use_style
            from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderBuilderTk
            style = use_style()
            builder_tk = BootstyleBuilderBuilderTk(
                theme_provider=style.theme_provider if style else None,
                style_instance=style
            )
            surface = getattr(self, '_surface_color', 'background')
            builder_tk.call_builder(self, surface_color=surface)

            style.register_tk_widget(self)

        return __init__wrapper

    @staticmethod
    def install_ttkbootstrap():
        """Install bootstyle API into ttk/tk widgets via monkey patching."""
        from ttkbootstrap.widgets import TTK_WIDGETS, TK_WIDGETS
        import ttkbootstrap.style.builders_tk  # noqa: F401

        for widget in TTK_WIDGETS:
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

        for widget in TK_WIDGETS:
            _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
            widget.__init__ = _init


__all__ = [
    'parse_bootstyle',
    'parse_bootstyle_v2',
    'parse_bootstyle_legacy',
    'generate_ttk_style_name',
    'extract_color_from_style',
    'extract_variant_from_style',
    'extract_widget_class_from_style',
    'Bootstyle',
]
