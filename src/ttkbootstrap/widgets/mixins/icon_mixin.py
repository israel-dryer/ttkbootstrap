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

    _icon_image_normal: Union["PhotoImage", None] = None
    _icon_image_hover: Union["PhotoImage", None] = None
    _icon_image_pressed: Union["PhotoImage", None] = None
    _icon_image_focus: Union["PhotoImage", None] = None
    _icon_image_disabled: Union["PhotoImage", None] = None

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value: Union[str, Tuple[str, int]]):
        self._icon = value
        self._build_icon_images()
        self._update_icon_image_for_state()

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
            self._build_icon_images()
            self._kwargs["image"] = self._icon_image_normal
            self._kwargs.setdefault("compound", default_compound)
        except Exception as e:
            logger.error("IconMixin", f"Failed to load icon '{self._icon}': {e}")

    def _bind_icon_events(self):
        """Bind icon hover and theme change events."""
        if self._variant == "outline":
            self.widget.bind("<Enter>", lambda e: self.widget.configure(image=self._icon_image_hover))
            self.widget.bind("<Leave>", lambda e: self.widget.configure(image=self._icon_image_normal))
        self.widget.bind("<<ThemeChanged>>", lambda e: self._on_theme_change(), add=True)

    def _on_theme_change(self):
        if not self._icon:
            return
        self._build_icon_images()
        self._update_icon_image_for_state()

    def _update_icon_image_for_state(self):
        """Apply appropriate icon image based on widget state."""
        state = set(self.widget.state())
        if "disabled" in state:
            self.widget.configure(image=self._icon_image_disabled)
        elif "pressed" in state:
            self.widget.configure(image=self._icon_image_pressed)
        elif "active" in state:
            self.widget.configure(image=self._icon_image_hover)
        elif "focus" in state:
            self.widget.configure(image=self._icon_image_focus)
        else:
            self.widget.configure(image=self._icon_image_normal)

    def _build_icon_images(self):
        icon_name, icon_size = self._parse_icon()
        if not icon_name or not icon_size:
            return

        tm = get_theme_manager()
        colors = tm.active_theme.get_color_states(self._color, self._variant, tm.active_theme.surface.color)

        def create(name, color):
            return Icon(name, icon_size, color).photo_image

        self._icon_image_normal = create(icon_name, colors.normal.on_color)
        self._icon_image_hover = create(icon_name, colors.hover.on_color)
        self._icon_image_pressed = create(icon_name, colors.pressed.on_color)
        self._icon_image_focus = create(icon_name, colors.focused.on_color)
        self._icon_image_disabled = create(icon_name, colors.disabled.on_color)
