"""Install-time patching for Tk widgets only.

This module applies ttkbootstrap's Tk autostyle behavior to Tk widgets by
wrapping their constructors. It does not affect ttk widgets, which are
provided as explicit subclasses in the ttkbootstrap.widgets package.
"""

from __future__ import annotations

from ttkbootstrap.style.bootstyle import Bootstyle


def install_tk_autostyle() -> None:
    """Patch Tk widgets to enable autostyle via Bootstyle.

    - Wraps Tk widget `__init__` with surface color inheritance and theme
      background application using registered Tk builders.
    - Leaves ttk widgets untouched; ttk integration is done via wrappers.
    """
    # Ensure Tk builders are registered
    import ttkbootstrap.style.builders_tk  # noqa: F401

    # Import Tk widget classes list
    from ttkbootstrap.widgets import TK_WIDGETS

    for widget in TK_WIDGETS:
        _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
        widget.__init__ = _init


__all__ = ["install_tk_autostyle"]
