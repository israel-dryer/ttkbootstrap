"""Deprecated location for ttkbootstrap's public utility functions.

The public helpers have moved to `ttkbootstrap.utils` (`enable_high_dpi_awareness`
and `scale_size` in `ttkbootstrap.utils.scaling`; `windowing_system` in
`ttkbootstrap.utils.platform`). This shim re-exports them for backward
compatibility and will be removed in 3.0. Import from `ttkbootstrap.utils` (or
the top-level `ttkbootstrap` namespace) instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.utility has moved to ttkbootstrap.utils; this shim will be "
    "removed in 3.0.",
    DeprecationWarning,
    stacklevel=2,
)

from ttkbootstrap.utils.scaling import (  # noqa: F401,E402
    enable_high_dpi_awareness,
    scale_size,
)
from ttkbootstrap.utils.platform import windowing_system  # noqa: F401,E402

# Two helpers that used to live here are implementation details and moved to
# ttkbootstrap.internal.utility; accessing them through this module still works
# (and this whole module is deprecated anyway), removed in 3.0.
_MOVED_TO_INTERNAL = ("get_image_name", "center_on_parent")


def __getattr__(name):
    if name in _MOVED_TO_INTERNAL:
        from ttkbootstrap.internal import utility as internal_utility
        return getattr(internal_utility, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
