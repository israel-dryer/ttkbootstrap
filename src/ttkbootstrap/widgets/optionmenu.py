from __future__ import annotations

from tkinter import StringVar
from typing import Any, Callable, Literal, Optional, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.widgets.contextmenu import ContextMenu, ContextMenuItem
from ttkbootstrap.widgets.menubutton import Menubutton
from ttkbootstrap.widgets.mixins import configure_delegate

if TYPE_CHECKING:
    from ttkbootstrap.signals import Signal


class OptionMenuKwargs(TypedDict, total=False):
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    icon_only: bool
    compound: Literal['text', 'image', 'top', 'bottom', 'left', 'right', 'center', 'none'] | str
    padding: Any
    width: int
    underline: int
    state: Literal['normal', 'active', 'disabled', 'readonly'] | str
    takefocus: Any
    style: str
    class_: str
    cursor: str
    default: Any
    name: str
    textvariable: Any
    textsignal: Signal[str]
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]
    show_dropdown_button: bool
    dropdown_button_icon: str | dict


class OptionMenu(Menubutton):

    def __init__(
            self,
            master=None,
            value: Any = None,
            options: list[Any] = None,
            **kwargs: Unpack[OptionMenuKwargs],
    ):
        """Create an OptionMenu backed by a ContextMenu.

        Args:
            master: Parent widget.
            value: Initial selected value.
            options: List of values to populate the menu.
            **kwargs: Additional options forwarded to Menubutton and the style builder:
                command: Callback invoked when the value changes via menu selection.
                image: Tk image to display.
                icon: Bootstyle icon spec for the label content.
                icon_only: Whether to reserve label padding when showing only an icon.
                compound: Placement of image relative to text.
                padding: Extra padding around the menubutton content.
                width: Width of the menubutton.
                underline: Index of underlined character in text.
                state: Widget state ('normal', 'active', 'disabled', 'readonly').
                takefocus: Participation in focus traversal.
                style: Explicit ttk style name.
                class_: Tk class name.
                cursor: Mouse cursor when hovering.
                default: Default ttk state.
                name: Tk widget name.
                textvariable: Existing tk variable to bind; new StringVar created if omitted.
                textsignal: Signal bound to the textvariable.
                bootstyle: Bootstyle string (e.g., 'primary-outline').
                surface_color: Surface token for style.
                style_options: Dict forwarded to the style builder (e.g., icon_only, surface_color).
                show_dropdown_button: Toggle visibility of the dropdown chevron.
                dropdown_button_icon: Icon name for the chevron; defaults to 'caret-down-fill'.
        """
        style_options = kwargs.pop('style_options', {})
        style_options.update(
            self._capture_style_options(
                options=['icon_only', 'icon', 'show_dropdown_button', 'dropdown_button_icon'],
                source=kwargs
            )
        )

        self._bind_id = None
        self._menu_options = options if options is not None else []

        # Store the textvariable if provided, or create a new one
        self._textvariable = kwargs.pop('textvariable', None)
        if self._textvariable is None:
            self._textvariable = StringVar(value=str(value) if value is not None else "")

        super().__init__(master, text=value, **kwargs)

        # Configure the menubutton to use the textvariable
        self.configure(textvariable=self._textvariable)

        # Bind signal to change event
        self._bind_id = self._bind_change_event()

        # Create menu items that update the shared variable
        self._context_menu = self._build_context_menu()

        # Bind menu display to button events
        self.bind('<Button-1>', lambda _: self.show_menu(), add="+")
        self.bind('<Return>', lambda _: self.show_menu(), add="+")
        self.bind('<KP_Enter>', lambda _: self.show_menu(), add="+")

    def _bind_change_event(self):
        """(Re)bind textsignal to emit <<Changed>> Tk events."""
        if self._bind_id is not None:
            self.textsignal.unsubscribe(self._bind_id)
        return self.textsignal.subscribe(lambda v: self.event_generate('<<Changed>>', data={"value": v}))

    def _build_context_menu(self):
        # Create menu items that update the shared variable
        menu_items = [
            ContextMenuItem(
                type="radiobutton",
                text=str(item),
                variable=self._textvariable,
                value=str(item)
            )
            for item in self._menu_options
        ]
        return ContextMenu(self, target=self, items=menu_items, anchor="nw", attach="sw", offset=(2, 2))

    def show_menu(self):
        """Show the dropdown menu unless disabled or readonly."""
        if not self.instate(("!disabled", "!readonly")):
            return
        self._context_menu.show()

    @property
    def value(self):
        """Return the current value."""
        return self._textvariable.get()

    @value.setter
    def value(self, value):
        """Set the current value (coerced to string)."""
        self._textvariable.set(str(value))

    def on_changed(self, callback: Callable[[Any], Any]):
        """Bind a callback to <<Changed>>; event.data contains {"value": v}."""
        return self.bind('<<Changed>>', callback, add="+")

    def off_changed(self, bind_id: str):
        """Unbind a previously registered <<Changed>> callback."""
        self.unbind('<<Changed>>', bind_id)

    @configure_delegate('options')
    def _delegate_options(self, value=None):
        """Get or set the menu options list."""
        if value is None:
            return self._menu_options
        else:
            self._menu_options = value
            if self._context_menu:
                self._context_menu.destroy()
            self._context_menu = self._build_context_menu()
        return None

    @configure_delegate('value')
    def _delegate_value(self, value):
        """Get or set the current value."""
        if value is None:
            return self.value
        else:
            self.value = value
        return None

    @configure_delegate('textsignal')
    def _delegate_textsignal(self, value=None):
        """Get or set the textsignal binding."""
        if value is None:
            return super()._delegate_textsignal()
        else:
            super()._delegate_textsignal(value)
            self._bind_change_event()
        return None

    @configure_delegate('show_dropdown_button')
    def _delegate_show_dropdown_button(self, value=None):
        """Get or set visibility of the dropdown chevron."""
        if value is None:
            return self.configure_style_options('show_dropdown_button')
        else:
            self.configure_style_options(show_dropdown_button=value)
            return self.rebuild_style()

    @configure_delegate('dropdown_button_icon')
    def _delegate_dropdown_button_icon(self, value):
        """Get or set the dropdown chevron icon name."""
        if value is None:
            return self.configure_style_options('dropdown_button_icon')
        else:
            self.configure_style_options(dropdown_button_icon=value)
            return self.rebuild_style()
