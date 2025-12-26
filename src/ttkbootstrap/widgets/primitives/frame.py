from __future__ import annotations

from tkinter import ttk
from typing import Any, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core.mixins.ttk_state import TtkStateMixin
from ttkbootstrap.core.mixins.widget import WidgetCapabilitiesMixin
from ttkbootstrap.widgets.internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.style.style import get_style
from ttkbootstrap.style.bootstyle_builder_tk import BootstyleBuilderBuilderTk
from ..mixins import configure_delegate


class FrameKwargs(TypedDict, total=False):
    # Standard ttk.Frame options
    padding: Any
    relief: Any
    borderwidth: Any
    width: int
    height: int
    style: str
    class_: str
    cursor: str
    name: str
    takefocus: bool

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    show_border: bool
    style_options: dict[str, Any]


class Frame(TTKWrapperBase, WidgetCapabilitiesMixin, TtkStateMixin, ttk.Frame):
    """ttkbootstrap wrapper for `ttk.Frame` with bootstyle support."""

    _ttk_base = ttk.Frame

    def __init__(self, master: Master = None, **kwargs: Unpack[FrameKwargs]) -> None:
        """Create a themed ttkbootstrap Frame.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            padding (int | tuple): Extra padding inside the frame.
            relief (str): Border style.
            borderwidth (int): Border width.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
            takefocus (bool): Widget accepts focus during keyboard traversal.
            style (str): Explicit ttk style name (overrides bootstyle).
            bootstyle (str): ttkbootstrap style tokens (e.g., 'secondary').
            surface_color (str): Optional surface token; otherwise inherited.
            show_border (bool): If True, draws a border around the frame.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['show_border'], kwargs))
        super().__init__(master, **kwargs)

    def configure_style_options(self, value=None, **kwargs):
        """Set style options and refresh descendant surfaces if needed."""
        old_surface = getattr(self, "_surface_color", "background")
        result = super().configure_style_options(value, **kwargs)
        if value is None and "surface_color" in kwargs:
            new_surface = getattr(self, "_surface_color", "background")
            if old_surface != new_surface:
                self.rebuild_style()
                self._refresh_descendant_surfaces(old_surface, new_surface)
        return result

    @configure_delegate("bootstyle")
    def _delegate_bootstyle(self, value: Any = None):
        old_surface = getattr(self, "_surface_color", "background")
        result = super()._delegate_bootstyle(value)
        new_surface = getattr(self, "_surface_color", "background")
        if value is not None and old_surface != new_surface:
            self._refresh_descendant_surfaces(old_surface, new_surface)
        return result

    def _refresh_descendant_surfaces(self, old_surface: str, new_surface: str) -> None:
        if old_surface == new_surface:
            return

        style = get_style()
        builder_tk = BootstyleBuilderBuilderTk(
            theme_provider=style.theme_provider if style else None,
            style_instance=style,
        )

        for child in self._iter_descendants():
            try:
                child_surface = getattr(child, "_surface_color", None)
            except Exception:
                child_surface = None

            explicit_surface = None
            try:
                explicit_surface = getattr(child, "_style_options", {}).get("surface_color")
            except Exception:
                explicit_surface = None

            if explicit_surface and explicit_surface != old_surface:
                continue

            if child_surface != old_surface:
                continue

            try:
                setattr(child, "_surface_color", new_surface)
            except Exception:
                continue

            if hasattr(child, "rebuild_style"):
                try:
                    child.rebuild_style()
                except Exception:
                    pass
            else:
                try:
                    builder_tk.call_builder(child, surface_color=new_surface)
                except Exception:
                    pass

    def _iter_descendants(self):
        stack = list(self.winfo_children())
        while stack:
            widget = stack.pop()
            yield widget
            try:
                stack.extend(widget.winfo_children())
            except Exception:
                pass

    @configure_delegate('show_border')
    def _delegate_show_border(self, value=None):
        if value is not None:
            return self.configure_style_options('show_border')
        else:
            self.configure_style_options(show_border=True)
            return self.rebuild_style()

