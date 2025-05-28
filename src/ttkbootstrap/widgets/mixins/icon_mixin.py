from tkinter import Widget
from typing import Tuple, Union, TYPE_CHECKING
from ...icons import Icon
from ...logger import logger
from ...style.theme_manager import get_theme_manager
from ...ttk_types import StyleColor

if TYPE_CHECKING:
    from tkinter import PhotoImage


class IconMixin:
    """Mixin for widgets that support a themed icon with hover + theme change behavior."""

    widget: Widget

    _icon_image_normal: Union["PhotoImage", str, None] = None
    _icon_image_hover: Union["PhotoImage", str, None] = None
    _icon: Union[str, Tuple[str, int]]
    _variant: str = "default"
    _color: StyleColor = "default"
    _kwargs: dict = {}

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value: Union[str, Tuple[str, int]]):
        self._icon = value
        self._build_icon_images()
        self.widget.configure(image=self._icon_image_normal)

    @property
    def _icon_name(self):
        if isinstance(self._icon, str):
            return self._icon
        elif isinstance(self._icon, tuple):
            return self._icon[0]
        else:
            return None

    @property
    def _icon_size(self):
        if isinstance(self._icon, str):
            return 18
        elif isinstance(self._icon, tuple):
            return self._icon[1]
        else:
            return None

    def _inject_icon_support(self, default_compound: str = "left"):
        """Inject image and compound into kwargs before widget init."""
        if not self._icon:
            return

        try:
            self._build_icon_images()
            self._kwargs["image"] = self._icon_image_normal
            if "compound" not in self._kwargs:
                self._kwargs["compound"] = default_compound
        except Exception as e:
            logger.error("IconMixin", f"failed to load icon: '{self._icon_name}': {e}")

    def _bind_icon_events(self):
        """Bind all icon-related events (hover, theme change)."""
        if self._variant == "outline":
            self.widget.bind("<Enter>", lambda e: self.widget.configure(image=self._icon_image_hover))
            self.widget.bind("<Leave>", lambda e: self.widget.configure(image=self._icon_image_normal))
        self.widget.bind("<<ThemeChanged>>", lambda e: self._on_theme_change(), add=True)

    def _on_theme_change(self):
        if self._icon_name is None:
            return
        self._build_icon_images()

        # Determine current state
        state = set(self.widget.state())
        if "pressed" in state and self._icon_image_hover:
            self.widget.configure(image=self._icon_image_hover)
        elif "active" in state and self._icon_image_hover:
            self.widget.configure(image=self._icon_image_hover)
        else:
            self.widget.configure(image=self._icon_image_normal)

    def _build_icon_images(self):
        tm = get_theme_manager()
        token = "primary" if self._color == "default" else self._color
        base_color = tm.active_theme.get_color(token)
        if self._variant == "outline":
            normal_color = base_color
            hover_color = tm.active_theme.get_foreground(token)
        elif self._variant == "text":
            normal_color = tm.active_theme.foreground if self._color == "default" else base_color
            hover_color = normal_color
        else:
            normal_color = tm.active_theme.get_foreground(token)
            hover_color = normal_color

        icon_name = self._icon_name
        icon_size = self._icon_size
        if any([icon_name is None, icon_size is None]):
            return

        normal_icon = Icon(icon_name, self._icon_size, normal_color)
        hover_icon = Icon(icon_name, self._icon_size, hover_color)

        self._icon_image_normal = normal_icon.photo_image
        self._icon_image_hover = hover_icon.photo_image
