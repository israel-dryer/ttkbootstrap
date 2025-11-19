"""Builder utilities for TTK widgets with embedded Tk components.

This module handles styling for TTK widgets that contain legacy Tk components
that aren't styled by the TTK theme engine, such as:
- ttk.Combobox (contains Tk listbox and scrollbar in popdown)
- Other hybrid widgets as needed

These widgets require manual Tcl/Tk calls to style their embedded components.
"""

from __future__ import annotations

from typing import Any, Optional

from ttkbootstrap.style.bootstyle_builder_base import BootstyleBuilderBase
from ttkbootstrap.style.theme_provider import ThemeProvider


class BootstyleBuilderMixed(BootstyleBuilderBase):
    """Builder for TTK widgets containing legacy Tk components.

    This class provides methods to style embedded Tk components within
    TTK widgets that aren't handled by the standard TTK theme engine.
    """

    def __init__(
        self,
        theme_provider: Optional[ThemeProvider] = None,
        style_instance: Optional[Any] = None
    ):
        """Initialize the mixed builder.

        Args:
            theme_provider: Optional ThemeProvider instance
            style_instance: Optional Style instance
        """
        super().__init__(theme_provider, style_instance)

    def update_combobox_popdown_style(self, widget: Any) -> None:
        """Update styling for legacy Tk components in ttk.Combobox.

        The ttk.Combobox contains embedded Tk components (popdown listbox
        and scrollbar) that aren't styled by the TTK theme engine and must
        be configured manually via Tcl/Tk calls.

        This method configures:
        - The popdown listbox window (colors, borders, selection)
        - The scrollbar within the popdown

        Args:
            widget: ttk.Combobox widget to update
        """
        # Determine border color based on theme mode
        surface = self.color('background')
        on_surface = self.on_color(surface)
        select = self.color('primary')
        on_select = self.on_color(select)
        border = self.color('border')

        # Build Tk configuration settings for the listbox
        tk_settings = []
        tk_settings.extend(["-borderwidth", 2])
        tk_settings.extend(["-highlightthickness", 1])
        tk_settings.extend(["-highlightcolor", border])
        tk_settings.extend(["-background", surface])
        tk_settings.extend(["-foreground", on_surface])
        tk_settings.extend(["-selectbackground", select])
        tk_settings.extend(["-selectforeground", on_select])

        try:
            # Get the popdown window path via Tcl
            popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {widget}")

            # Configure the listbox within the popdown
            widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

            # Configure the scrollbar style
            sb_style = "Vertical.TScrollbar"
            widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)
        except Exception:
            # Silently fail if widget isn't fully initialized or mapped yet
            pass