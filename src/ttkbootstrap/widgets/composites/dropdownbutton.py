from __future__ import annotations

from typing import Any, Callable, Literal, Optional, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.widgets.composites.contextmenu import ContextMenu, ContextMenuItem
from ttkbootstrap.widgets.primitives.menubutton import MenuButton
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.core.signals import Signal


class DropdownButtonKwargs(TypedDict, total=False):
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
    bootstyle: str  # DEPRECATED: Use color and variant instead
    color: str
    variant: str
    surface_color: str
    style_options: dict[str, Any]
    popdown_options: dict[str, Any]
    show_dropdown_button: bool
    dropdown_button_icon: str | dict


class DropdownButton(MenuButton):

    def __init__(
            self,
            master: Master = None,
            text: Any = None,
            items: list[ContextMenuItem] = None,
            **kwargs: Unpack[DropdownButtonKwargs],
    ):
        """Create a dropdown button backed by a ContextMenu.

        Args:
            master: Parent widget. If None, uses the default root window.
            text (str): Label text for the button.
            items (list): Initial list of ContextMenuItem entries.

        Other Parameters:
            command (Callable): Callback when the button is activated.
            image (PhotoImage): Tk image to display.
            icon (str | dict): Bootstyle icon spec for the button content.
            icon_only (bool): Whether to reserve label padding when showing only an icon.
            compound (str): Placement of image relative to text.
            padding (int | tuple): Extra padding around the button content.
            width (int): Width of the button.
            underline (int): Index of underlined character in text.
            state (str): Widget state ('normal', 'active', 'disabled', 'readonly').
            takefocus (bool): Participation in focus traversal.
            style (str): Explicit ttk style name.
            textvariable (Variable): Existing Tk variable for the label text.
            textsignal (Signal[str]): Signal bound to the textvariable.
            color (str): Color token for styling (e.g., 'primary', 'danger').
            variant (str): Style variant (e.g., 'outline', 'ghost').
            bootstyle (str): DEPRECATED - Use `color` and `variant` instead.
            surface_color (str): Surface token for style.
            style_options (dict): Dict forwarded to the menubutton style builder.
            popdown_options (dict): Dict forwarded to ContextMenu (e.g., anchor, attach, offset).
            show_dropdown_button (bool): Show/hide the chevron.
            dropdown_button_icon (str | dict): Icon name for the chevron.
        """
        style_options = kwargs.pop('style_options', {})
        style_options.update(
            self._capture_style_options(
                options=['icon', 'icon_only', 'show_dropdown_button', 'dropdown_button_icon'],
                source=kwargs
            )
        )
        kwargs['style_options'] = style_options
        self._item_click_callback = None
        self._items = items if items else []
        self._popdown_options = kwargs.pop('popdown_options', {})

        # Store the textvariable if provided, or create a new one
        super().__init__(master, text=text, **kwargs)

        # Create menu items that update the shared variable
        self._context_menu = self._build_context_menu()

        # Bind menu display to button events
        self.bind('<Button-1>', lambda _: self.show_menu(), add="+")
        self.bind('<Return>', lambda _: self.show_menu(), add="+")
        self.bind('<KP_Enter>', lambda _: self.show_menu(), add="+")

        # passthrough methods
        self.on_item_click = self._context_menu.on_item_click
        self.add_radiobutton = self._context_menu.add_radiobutton
        self.add_command = self._context_menu.add_command
        self.add_checkbutton = self._context_menu.add_checkbutton
        self.add_separator = self._context_menu.add_separator
        self.add_item = self._context_menu.add_item
        self.add_items = self._context_menu.add_items
        self.insert_item = self._context_menu.insert_item
        self.remove_item = self._context_menu.remove_item
        self.move_item = self._context_menu.move_item
        self.configure_item = self._context_menu.configure_item
        self.items = self._context_menu.items

    def on_item_click(self, callback: Callable) -> None:
        """Set item click callback. Callback receives ``item_info = {'type': str, 'text': str, 'value': Any}``."""
        self._item_click_callback = callback
        self._context_menu.on_item_click(callback)

    def off_item_click(self) -> None:
        """Remove the item click callback."""
        self._item_click_callback = None
        self._context_menu.on_item_click(None)

    def _build_context_menu(self):
        """Construct the ContextMenu with current items and options."""
        options = {"anchor": "nw", "attach": "sw", "offset": (2, 0)}
        options.update(self._popdown_options)
        cm = ContextMenu(self, target=self, items=self._items, **options)
        if self._item_click_callback:
            self.on_item_click(self._item_click_callback)
        return cm

    @property
    def context_menu(self):
        """Returns the context menu widget"""
        return self._context_menu

    def show_menu(self):
        """Show the dropdown menu unless disabled or readonly."""
        if not self.instate(("!disabled", "!readonly")):
            return
        self._context_menu.show()

    @configure_delegate('popdown_options')
    def _delegate_popdown_options(self, value=None):
        if value is None:
            return self._popdown_options
        else:
            self._popdown_options = value
            return self.context_menu.configure(**value)

    @configure_delegate('show_dropdown_button')
    def _delegate_show_dropdown_button(self, value=None):
        """Get or set visibility of the dropdown chevron."""
        if value is None:
            return self.configure_style_options('show_dropdown_button')
        else:
            self.configure_style_options(show_dropdown_button=value)
            return self.rebuild_style()

    @configure_delegate('dropdown_button_icon')
    def _delegate_dropdown_button_icon(self, value=None):
        """Get or set the dropdown chevron icon name."""
        if value is None:
            return self.configure_style_options('dropdown_button_icon')
        else:
            self.configure_style_options(dropdown_button_icon=value)
            return self.rebuild_style()

