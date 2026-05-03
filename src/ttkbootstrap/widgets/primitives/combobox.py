"""Themed combobox widget."""
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
    """Keyword-argument schema for `Combobox.__init__`."""

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
    """Themed single-line text entry combined with a dropdown list.

    Extends `ttk.Combobox` with theme-aware styling and text-signal
    binding. The entry shows the current value; the dropdown exposes
    choices from `values`. The `state` setting controls whether users
    can also type free-form values (`normal`) or only choose from the
    list (`readonly`).
    """

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

        # Set up popdown styling (also bound to theme changes)
        self._setup_postcommand()
        self._subscribe_theme_changes()

    @configure_delegate('density')
    def _delegate_density(self, value=None):
        if value is None:
            return self.configure_style_options(value)
        else:
            if value == 'compact':
                self.configure(font='caption')
            else:
                self.configure(font='body')
            self.configure_style_options(density=value)
            return self.rebuild_style()

    @configure_delegate('surface')
    def _delegate_surface(self, value=None):
        if value is None:
            return self._surface
        self.configure_style_options(surface=value)
        return self.rebuild_style()

    def _setup_postcommand(self) -> None:
        """Re-style the popdown each time it opens.

        The popdown is created lazily on first open and reused. Re-styling on
        every open ensures it picks up the current theme's colors, since the
        embedded Tk listbox/scrollbar aren't rebuilt by the ttk style engine.
        """

        def on_popdown():
            self._apply_popdown_style(create_if_missing=True)

            if self._original_postcommand:
                if callable(self._original_postcommand):
                    self._original_postcommand()
                else:
                    self.tk.eval(str(self._original_postcommand))

        self.configure(postcommand=on_popdown)

    def _apply_popdown_style(self, create_if_missing: bool = False) -> None:
        """Apply theme colors and density font to the embedded popdown.

        Args:
            create_if_missing: If True, force-create the popdown so we can
                style it before it's mapped (used from the postcommand). If
                False, no-op when the popdown doesn't exist yet (used from
                the theme-change subscriber).
        """
        popdown_path = f"{self}.popdown"
        try:
            popdown_exists = bool(int(self.tk.eval(f"winfo exists {popdown_path}")))
        except Exception:
            return

        if not popdown_exists:
            if not create_if_missing:
                return
            try:
                self.tk.eval(f"ttk::combobox::PopdownWindow {self}")
            except Exception:
                return

        try:
            from ttkbootstrap.style.bootstyle_builder_mixed import BootstyleBuilderMixed
            BootstyleBuilderMixed().update_combobox_popdown_style(self)
        except Exception:
            pass

        try:
            density = self.configure_style_options('density') or 'default'
            from ttkbootstrap.style.typography import get_font
            font_token = 'caption' if density == 'compact' else 'body'
            self.tk.call(f"{popdown_path}.f.l", "configure", "-font", str(get_font(font_token)))
        except Exception:
            pass

    def _subscribe_theme_changes(self) -> None:
        """Re-style any already-created popdown when the theme changes."""
        from ttkbootstrap.core.publisher import Channel, Publisher
        name = str(self)
        Publisher.subscribe(name=name, func=self._apply_popdown_style, channel=Channel.STD)
        self.bind('<Destroy>', lambda _e, n=name: Publisher.unsubscribe(n), '+')

