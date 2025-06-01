from tkinter import Widget
from typing import Tuple, Union, TYPE_CHECKING
from ...icons import Icon
from ...logger import logger
from ...style.theme_manager import get_theme_manager
from ...ttk_types import StyleColor

if TYPE_CHECKING:
    from tkinter import PhotoImage


class IconMixin:
    """Mixin for widgets that support themed icons with state-based styling."""

    widget: Widget

    _icon: Union[str, Tuple[str, int]]
    _variant: str = "default"
    _color: StyleColor = "default"
    _kwargs: dict = {}

    _icon_image_dynamic: Union["PhotoImage", None] = None

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value: Union[str, Tuple[str, int]]):
        self._icon = value
        self._update_icon_image_from_foreground()

    def _parse_icon(self) -> Tuple[str | None, int]:
        """Extract the icon name and size from self._icon."""
        if isinstance(self._icon, str):
            return self._icon, 24
        elif isinstance(self._icon, tuple) and len(self._icon) == 2:
            return self._icon[0], self._icon[1]
        return None, 0

    def _prepare_icon_kwargs(self, default_compound: str = "left"):
        """Inject image and compound keys into widget kwargs."""
        if not self._icon:
            return
        try:
            self._update_icon_image_from_foreground()
            self._kwargs["image"] = self._icon_image_dynamic
            self._kwargs.setdefault("compound", default_compound)
        except Exception as e:
            logger.error("IconMixin", f"Failed to load icon '{self._icon}': {e}")

    def _bind_icon_events(self):
        """Bind icon color updates to widget state and theme changes."""
        self.widget.bind("<Enter>", lambda e: self._update_icon_image_from_foreground(), add=True)
        self.widget.bind("<Leave>", lambda e: self._update_icon_image_from_foreground(), add=True)
        self.widget.bind("<FocusIn>", lambda e: self._update_icon_image_from_foreground(), add=True)
        self.widget.bind("<FocusOut>", lambda e: self._update_icon_image_from_foreground(), add=True)
        self.widget.bind("<ButtonPress>", lambda e: self._update_icon_image_from_foreground(), add=True)
        self.widget.bind("<ButtonRelease-1>", self._delayed_icon_update, add=True)
        self.widget.bind("<<ThemeChanged>>", self._delayed_icon_update, add=True)

    def _delayed_icon_update(self, event):
        """Defer icon update to allow state to settle after click."""
        self.widget.after(10, self._update_icon_image_from_foreground)

    def _update_icon_image_from_foreground(self):
        """Generate and apply a new icon image using the current foreground color."""
        if not self._icon or not hasattr(self, "widget") or not self.widget.winfo_exists():
            return

        style = self.widget.cget("style")
        tm = get_theme_manager()
        fg = tm.ttk.lookup(style, "foreground", state=self.widget.state())  # fallback-safe

        icon_name, icon_size = self._parse_icon()
        if not icon_name or not icon_size or not fg:
            return

        self._icon_image_dynamic = Icon(icon_name, icon_size, fg).photo_image
        self.widget.configure(image=self._icon_image_dynamic)
