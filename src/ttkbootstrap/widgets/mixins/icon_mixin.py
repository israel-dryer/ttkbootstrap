from typing import Union, TYPE_CHECKING
from ttkbootstrap.icons import Icon
from ttkbootstrap.logger import logger
from ttkbootstrap.style.theme_manager import get_theme_manager

if TYPE_CHECKING:
    from tkinter import PhotoImage


class IconMixin:
    """Mixin for widgets that support a themed icon with hover + theme change behavior."""

    _icon_image_normal: Union["PhotoImage", str, None] = None
    _icon_image_hover: Union["PhotoImage", str, None] = None
    _icon_name: str = None
    _icon_size: int = 16
    _variant: str = "default"
    _color: str = "default"

    def init_icon_support(self, kwargs: dict, default_compound: str = "left"):
        """Inject image and compound into kwargs before widget init."""
        if not self._icon_name:
            return

        try:
            self._build_icon_images()
            kwargs["image"] = self._icon_image_normal
            if "compound" not in kwargs:
                kwargs["compound"] = default_compound
        except Exception as e:
            logger.error("IconMixin", f"failed to load icon: '{self._icon_name}': {e}")

    def bind_icon_hover_events(self):
        self.bind("<Enter>", lambda e: self.configure(image=self._icon_image_hover))
        self.bind("<Leave>", lambda e: self.configure(image=self._icon_image_normal))

    def bind_theme_change_event(self):
        self.bind("<<ThemeChange>>", lambda e: self._on_theme_change())

    def _on_theme_change(self):
        self._build_icon_images()
        self.configure(image=self._icon_image_normal)

    def _build_icon_images(self):
        tm = get_theme_manager()
        token = "primary" if self._color == "default" else self._color
        base_color = tm.active_theme.get_color(token)

        if self._variant == "outline":
            normal_color = base_color
            hover_color = tm.active_theme.get_foreground(base_color)
        elif self._variant == "text":
            normal_color = tm.active_theme.foreground if self._color == "default" else base_color
            hover_color = normal_color
        else:
            normal_color = tm.active_theme.get_foreground(base_color)
            hover_color = normal_color

        normal_icon = Icon(self._icon_name, size=self._icon_size, color=normal_color)
        hover_icon = Icon(self._icon_name, size=self._icon_size, color=hover_color)

        self._icon_image_normal = normal_icon.image
        self._icon_image_hover = hover_icon.image
