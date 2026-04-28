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
        # Match the entry field: surface = 'content', selection = primary
        surface = self.color('content')
        on_surface = self.on_color(surface)
        select = self.color('primary')
        on_select = self.on_color(select)

        # Listbox has no border of its own — the popdown frame already draws
        # the outer border, and stacking a listbox highlight on top creates a
        # visible double-border effect.
        tk_settings = [
            "-borderwidth", 0,
            "-highlightthickness", 0,
            "-background", surface,
            "-foreground", on_surface,
            "-selectbackground", select,
            "-selectforeground", on_select,
            "-activestyle", "none",
            "-relief", "flat",
        ]

        try:
            # Skip if the popdown hasn't been created yet (lazy construction).
            # The postcommand handler will style it on first open.
            popdown_path = f"{widget}.popdown"
            if not int(widget.tk.eval(f"winfo exists {popdown_path}")):
                return
            widget.tk.call(f"{popdown_path}.f.l", "configure", *tk_settings)

            # Build a themed scrollbar style and apply it to the popdown
            # scrollbar. Bootstyle.create_ttk_style returns a hashed style
            # name (e.g. bs[xxx].Default.Vertical.TScrollbar) that is rebuilt
            # automatically on theme change.
            from ttkbootstrap.style.bootstyle import Bootstyle
            sb_style = Bootstyle.create_ttk_style(
                'TScrollbar', variant='default',
                style_options={'orient': 'vertical', 'show_arrows': False},
            )
            widget.tk.call(f"{popdown_path}.f.sb", "configure", "-style", sb_style)
        except Exception:
            # Silently fail if widget isn't fully initialized or mapped yet
            pass