from __future__ import annotations

from typing import Any, Callable, Literal, Optional, TYPE_CHECKING, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.widgets.contextmenu import ContextMenu, ContextMenuItem
from ttkbootstrap.widgets.menubutton import Menubutton
from ttkbootstrap.widgets.mixins import configure_delegate

if TYPE_CHECKING:
    from ttkbootstrap.signals import Signal


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
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]
    popdown_options: dict[str, Any]
    show_dropdown_button: bool
    dropdown_button_icon: str | dict


class DropdownButton(Menubutton):

    def __init__(
            self,
            master=None,
            text: Any = None,
            items: list[ContextMenuItem] = None,
            **kwargs: Unpack[DropdownButtonKwargs],
    ):
        """Create a dropdown button backed by a ContextMenu.

        Args:
            master: Parent widget.
            text: Label text for the button.
            items: Initial list of ContextMenuItem entries.
            **kwargs: Menubutton and style options including:
                command: Callback when the button is activated.
                image/icon/icon_only/compound: Content display options.
                padding/width/underline/state/takefocus/style/class_/cursor/default/name: Standard ttk options.
                textvariable/textsignal: Bindings for the label text.
                bootstyle/surface_color: Bootstyle settings.
                style_options: Dict forwarded to the menubutton style builder.
                popdown_options: Dict forwarded to ContextMenu (e.g., anchor/attach/offset).
                show_dropdown_button: Show/hide the chevron.
                dropdown_button_icon: Icon name for the chevron.
        """
        style_options = kwargs.pop('style_options', {})
        style_options.update(
            self._capture_style_options(
                options=['icon', 'icon_only', 'show_dropdown_button', 'dropdown_button_icon'],
                source=kwargs
            )
        )
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

    def on_item_click(self, callback: Callable[[Any], Any]):
        """Bind a callback to menu item selections."""
        self._item_click_callback = callback
        self._context_menu.on_item_click(callback)

    def off_item_click(self):
        """Clear any bound item-click callback."""
        self._item_click_callback = None
        self._context_menu.on_item_click(None)

    def _build_context_menu(self):
        """Construct the ContextMenu with current items and options."""
        options = self._popdown_options.copy()
        options.update(anchor="nw", attach="sw", offset=(2, 0))
        cm = ContextMenu(self, target=self, items=self._items, **options)
        if self._item_click_callback:
            self.on_item_click(self._item_click_callback)
        return cm

    def show_menu(self):
        """Show the dropdown menu unless disabled or readonly."""
        if not self.instate(("!disabled", "!readonly")):
            return
        self._context_menu.show()

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
