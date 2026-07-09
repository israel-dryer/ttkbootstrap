"""Deprecated location for ttkbootstrap's color utilities.

The color helpers have moved to `ttkbootstrap.utils` (implemented in
`ttkbootstrap.utils.color`). This shim re-exports them for backward
compatibility and will be removed in 3.0. Import from `ttkbootstrap.utils`
(or the top-level `ttkbootstrap` namespace) instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.colorutils has moved to ttkbootstrap.utils; this shim will "
    "be removed in 3.0.",
    DeprecationWarning,
    stacklevel=2,
)

from ttkbootstrap.utils.color import (  # noqa: F401,E402
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
