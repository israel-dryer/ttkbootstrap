from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master
from ..mixins import TextSignalMixin

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class ComboboxKwargs(TypedDict, total=False):
    # Standard ttk.Combobox options
    values: Any
    textvariable: Any
    textsignal: Signal[Any]
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
    bootstyle: str  # DEPRECATED: Use color and variant instead
    color: str
    surface_color: str
    style_options: dict[str, Any]


class Combobox(TextSignalMixin, TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Combobox):
    """ttkbootstrap wrapper for `ttk.Combobox` with bootstyle support."""

    _ttk_base = ttk.Combobox

    def __init__(self, master: Master = None, **kwargs: Unpack[ComboboxKwargs]) -> None:
        """Create a themed ttkbootstrap Combobox.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            values (list): Sequence of values to display.
            textvariable (Variable): Tk variable linked to the selected value.
            textsignal (Signal): Reactive Signal linked to the text (auto-synced with textvariable).
            state (str): Widget state; 'readonly' restricts to list items.
            width (int): Width in characters.
            height (int): Maximum rows shown in the drop-down list.
            postcommand (Callable): Callback executed before showing the drop-down.
            justify (str): Text justification within the entry field.
            exportselection (bool): Whether selection is exported to X clipboard.
            xscrollcommand (Callable): Scroll callback for horizontal scrolling.
            font (str | Font): Font for the entry field.
            foreground (str): Text color.
            background (str): Background color for the entry field.
            style (str): Explicit ttk style name (overrides color/variant).
            color (str): Color token for styling, e.g. 'primary', 'danger', 'success'.
            bootstyle (str): DEPRECATED - Use `color` and `variant` instead.
                Combined style tokens (e.g., 'primary').
            surface_color (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
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
        from ttkbootstrap.style.style import get_style

        try:
            style = get_style()
            builder = BootstyleBuilderMixed(
                theme_provider=style.theme_provider,
                style_instance=style
            )
            # Apply immediately - popdown should exist now
            builder.update_combobox_popdown_style(self)
            self._popdown_styled = True
        except Exception:
            pass

