from __future__ import annotations

from tkinter import ttk
from typing import Any, Literal, TypedDict, TYPE_CHECKING

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master
from ..mixins import TextSignalMixin, configure_delegate

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
    bootstyle: str  # DEPRECATED: Use accent and variant instead
    accent: str
    density: Literal['default', 'compact']
    surface: str
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
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'danger', 'success'.
            density (str): The vertical and horizontal compactness, e.g. 'default', 'compact'.
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens (e.g., 'primary').
            surface (str): Optional surface token; otherwise inherited.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        # Store density for popdown positioning
        if kwargs.get('density') == 'compact':
            kwargs['font'] = 'caption'
        kwargs.update(style_options=self._capture_style_options(['density'], kwargs))
        super().__init__(master, **kwargs)

        # Store original postcommand if provided
        self._original_postcommand = kwargs.get('postcommand')

        # Set up popdown position adjustment
        self._popdown_bound = False
        self._setup_postcommand()

    @configure_delegate('density')
    def _delegate_density(self, value=None):
        if value is None:
            return self.configure_style_options(value)
        else:
            if value == 'compact':
                self.configure(font='caption')
            else:
                self.configure(font='body')
            return self.configure_style_options(density=value)

    def _setup_postcommand(self) -> None:
        """Set up postcommand to bind popdown position adjustment."""

        def on_popdown():
            # Bind position adjustment on first open
            if not self._popdown_bound:
                self._bind_popdown_position()
                self._popdown_bound = True

            # Call original postcommand if it exists
            if self._original_postcommand:
                if callable(self._original_postcommand):
                    self._original_postcommand()
                else:
                    self.tk.eval(str(self._original_postcommand))

        self.configure(postcommand=on_popdown)

    def _bind_popdown_position(self) -> None:
        """Bind position adjustment to popdown Map event and configure font."""
        try:
            popdown = self.tk.eval(f"ttk::combobox::PopdownWindow {self}")
            if not popdown:
                return

            listbox = f"{popdown}.f.l"

            # Configure listbox font based on density
            density = self.configure_style_options('density') or 'default'
            try:
                from ttkbootstrap.style.typography import get_font
                font_token = 'caption' if density == 'compact' else 'body'
                font = get_font(font_token)
                self.tk.call(listbox, "configure", "-font", str(font))
            except Exception:
                pass  # Font config failed, continue with offset

            # Offset to align popdown with entry border (accounts for focus ring)
            offset = 1 if density == 'compact' else 2

            def adjust_position(event=None):
                def do_adjust():
                    try:
                        geom = str(self.tk.call("wm", "geometry", popdown))
                        size_part, pos_part = geom.split('+', 1)
                        width, height = size_part.split('x')
                        x, y = pos_part.split('+')
                        new_x = int(x) + offset
                        self.tk.call("wm", "geometry", popdown,
                                     f"{width}x{height}+{new_x}+{y}")
                    except Exception:
                        pass
                self.after(1, do_adjust)

            self.tk.call("bind", popdown, "<Map>", self.register(adjust_position))
        except Exception:
            pass

