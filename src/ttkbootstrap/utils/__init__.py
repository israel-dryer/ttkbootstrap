"""Public utilities for ttkbootstrap — the first-class home for the helpers an
app developer reaches for: color math, scaling / HiDPI, and platform checks.

This package replaces the pre-2.0 scatter (`ttkbootstrap.colorutils` +
`ttkbootstrap.utility`). Those old module paths still work as thin
warn-and-forward shims (removed in 3.0); new code should import from here (or
from the top-level `ttkbootstrap` namespace, where the whole surface is
re-exported for `ttk.<tab>` discovery).

Submodules:
    color     — color-model conversion and manipulation
    scaling   — `enable_high_dpi_awareness`, `scale_size`
    platform  — `windowing_system`

Later 2.0 slices add `fonts` (typography) and `config` (deferred-config seam)
here, and re-export the `localization` helpers through this namespace.
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
]
