from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict

from typing_extensions import Unpack

from ._internal.wrapper_base import TTKWrapperBase


class ComboboxKwargs(TypedDict, total=False):
    # Standard ttk.Combobox options
    values: Any
    textvariable: Any
    state: Literal['normal', 'readonly', 'disabled'] | str
    width: int
    height: int
    postcommand: Any
    justify: Any
    exportselection: bool
    xscrollcommand: Any
    font: Any
    foreground: str
    background: str
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class Combobox(TTKWrapperBase, ttk.Combobox):
    """ttkbootstrap wrapper for `ttk.Combobox` with bootstyle support."""

    _ttk_base = ttk.Combobox

    def __init__(self, master=None, **kwargs: Unpack[ComboboxKwargs]) -> None:
        """Create a themed ttkbootstrap Combobox.

        Keyword Args:
            values: Sequence of values to display.
            textvariable: Tk variable linked to the selected value.
            state: Widget state; 'readonly' restricts to list items.
            width: Width in characters.
            height: Maximum rows shown in the drop-down list.
            postcommand: Callback executed before showing the drop-down.
            justify: Text justification within the entry field.
            exportselection: Whether selection is exported to X clipboard.
            xscrollcommand: Scroll callback for horizontal scrolling.
            font: Font for the entry field.
            foreground: Text color.
            background: Background color for the entry field.
            style: Explicit ttk style name (overrides bootstyle).
            bootstyle: ttkbootstrap style tokens (e.g., 'primary').
            surface_color: Optional surface token; otherwise inherited.
            style_options: Optional dict forwarded to the style builder.
        """
        super().__init__(master, **kwargs)

        # Store original postcommand if provided
        self._original_postcommand = kwargs.get('postcommand')

        # Set up our postcommand to style popdown on first open
        self._popdown_styled = False
        self._setup_postcommand()

        # Subscribe to theme changes to re-apply popdown styling
        root = self.nametowidget('.')
        root.bind('<<ThemeChanged>>', lambda _: self._on_theme_changed(), add='+')

    def _setup_postcommand(self) -> None:
        """Set up postcommand to style popdown when first opened."""

        def on_popdown():
            # Apply popdown styling if not done yet
            if not self._popdown_styled:
                self._apply_popdown_style()
                self._popdown_styled = True

            # Call original postcommand if it exists
            if self._original_postcommand:
                if callable(self._original_postcommand):
                    self._original_postcommand()
                else:
                    # It might be a string command
                    self.tk.eval(str(self._original_postcommand))

        # Configure the postcommand
        self.configure(postcommand=on_popdown)

    def _on_theme_changed(self) -> None:
        """Handle theme change event."""
        # Reset styled flag so popdown gets restyled on next open
        self._popdown_styled = False

        # If popdown has been opened before, restyle it immediately
        try:
            # Try to get the popdown window - if it exists, style it now
            popdown = self.tk.eval(f"ttk::combobox::PopdownWindow {self}")
            if popdown:
                self._apply_popdown_style()
        except Exception:
            # Popdown doesn't exist yet, will be styled on next open
            pass

    def _apply_popdown_style(self) -> None:
        """Apply theme-appropriate styling to the popdown listbox."""
        from ttkbootstrap.style.bootstyle_builder_mixed import BootstyleBuilderMixed
        from ttkbootstrap.style.style import use_style

        try:
            style = use_style()
            builder = BootstyleBuilderMixed(
                theme_provider=style.theme_provider,
                style_instance=style
            )
            # Apply immediately - popdown should exist now
            builder.update_combobox_popdown_style(self)
            self._popdown_styled = True
        except Exception:
            pass
