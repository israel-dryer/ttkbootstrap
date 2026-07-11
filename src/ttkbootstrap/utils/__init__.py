"""Public utilities for ttkbootstrap — the first-class home for the helpers an
app developer reaches for: color math, scaling / HiDPI, and platform checks.

This package replaces the pre-2.0 scatter (`ttkbootstrap.colorutils` +
`ttkbootstrap.utility`). Those old module paths still work as thin
warn-and-forward shims (removed in 3.0); new code should import from here (or
from the top-level `ttkbootstrap` namespace, where the whole surface is
re-exported for `ttk.<tab>` discovery).

Submodules:
    color     — color-model conversion and manipulation
    fonts     — typography over the standard Tk named fonts
    scaling   — `enable_high_dpi_awareness`, `scale_size`
    platform  — `windowing_system`
    config    — the deferred-config seam (pre-root setters)

The `localization` helpers are also re-exported through this namespace.
"""
from ttkbootstrap.utils.color import (
    # color-model selector constants (usable as the `model=` argument). Not in
    # `__all__` (they weren't in colorutils' `__all__` either -- semi-internal),
    # but re-exported so `from ttkbootstrap.utils import RGB` resolves for anyone
    # migrating off the deprecated `ttkbootstrap.colorutils` path.
    RGB,
    HSL,
    HEX,
    NAME,
    HUE,
    SAT,
    LUM,
    color_to_rgb,
    color_to_hex,
    color_to_hsl,
    update_hsl_value,
    contrast_color,
    conform_color_model,
)
from ttkbootstrap.utils.scaling import (
    enable_high_dpi_awareness,
    scale_size,
)
from ttkbootstrap.utils.platform import windowing_system
from ttkbootstrap.utils.config import (
    set_default_button,
    on_theme_change,
    theme_aware,
    remove_theme_change_callback,
)
from ttkbootstrap.utils.fonts import Fonts, set_global_family

# Localization helpers live in the `localization` package (the i18n engine stays
# there); they are surfaced here for discoverability. Imported lazily via
# module `__getattr__` so that importing `utils` -- which happens during style/
# package init -- does not pull in the localization -> window import chain before
# window is ready.
_LOCALIZATION_EXPORTS = ("L", "LocaleVar", "set_locale")


def __getattr__(name):
    if name in _LOCALIZATION_EXPORTS:
        from ttkbootstrap import localization

        return getattr(localization, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # color
    "color_to_rgb",
    "color_to_hex",
    "color_to_hsl",
    "update_hsl_value",
    "contrast_color",
    "conform_color_model",
    # scaling
    "enable_high_dpi_awareness",
    "scale_size",
    # platform
    "windowing_system",
    # fonts (typography over the standard Tk named fonts)
    "Fonts",
    "set_global_family",
    # deferred config (pre-root setters)
    "set_default_button",
    "on_theme_change",
    "theme_aware",
    "remove_theme_change_callback",
    # localization (surfaced lazily from the localization package)
    "L",
    "LocaleVar",
    "set_locale",
]
