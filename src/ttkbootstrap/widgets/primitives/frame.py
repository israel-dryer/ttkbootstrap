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
    width: int
    height: int
    style: str
    cursor: str
    name: str
    takefocus: bool
    class_: str

    # ttkbootstrap-specific extensions
    accent: str
    variant: str
    surface: str
    input_background: str
    show_border: bool
    style_options: dict[str, Any]
    bootstyle: str  # DEPRECATED: Use accent and variant instead


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
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent token for styling, e.g. 'primary', 'secondary', 'success'.
            variant (str): Style variant (if applicable).
            bootstyle (str): DEPRECATED - Use `accent` and `variant` instead.
                Combined style tokens (e.g., 'secondary').
            surface (str): Optional surface token; otherwise inherited.
            input_background (str): Surface token used as the fill color for all input
                widgets (Entry, Combobox, Spinbox, Field) inside this container. Cascades
                to descendants the same way `surface` does. Input foreground, border,
                and focus-ring colors are all derived from this fill so contrast is always
                correct. Defaults to `'content'` (the app background), which keeps
                inputs visually distinct regardless of the container surface. Override
                with any surface token (e.g. `'card'`) to match the container.
            show_border (bool): Draw a border around the frame.
            style_options (dict): Optional dict forwarded to the style builder.
        """
        kwargs.update(style_options=self._capture_style_options(['show_border'], kwargs))
        super().__init__(master, **kwargs)

    def configure_style_options(self, value=None, **kwargs):
        """Set style options and refresh descendant surfaces if needed."""
        old_surface = getattr(self, "_surface", "background")
        old_input_bg = getattr(self, "_input_background", None)
        result = super().configure_style_options(value, **kwargs)
        if value is None:
            if "surface" in kwargs:
                new_surface = getattr(self, "_surface", "background")
                if old_surface != new_surface:
                    self.rebuild_style()
                    self._refresh_descendant_surfaces(old_surface, new_surface)
            if "input_background" in kwargs:
                new_input_bg = getattr(self, "_input_background", None)
                if old_input_bg != new_input_bg:
                    self._refresh_descendant_input_backgrounds(old_input_bg, new_input_bg)
        return result

    @configure_delegate("bootstyle")
    def _delegate_bootstyle(self, value: Any = None):
        old_surface = getattr(self, "_surface", "background")
        result = super()._delegate_bootstyle(value)
        new_surface = getattr(self, "_surface", "background")
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
                child_surface = getattr(child, "_surface", None)
            except Exception:
                child_surface = None

            explicit_surface = None
            try:
                explicit_surface = getattr(child, "_style_options", {}).get("surface")
            except Exception:
                explicit_surface = None

            if explicit_surface and explicit_surface != old_surface:
                continue

            if child_surface != old_surface:
                continue

            try:
                setattr(child, "_surface", new_surface)
            except Exception:
                continue

            if hasattr(child, "rebuild_style"):
                try:
                    child.rebuild_style()
                except Exception:
                    pass
            else:
                try:
                    builder_tk.call_builder(child, surface=new_surface)
                except Exception:
                    pass

    def _refresh_descendant_input_backgrounds(self, old_bg: str | None, new_bg: str | None) -> None:
        if old_bg == new_bg:
            return

        style = get_style()
        builder_tk = BootstyleBuilderBuilderTk(
            theme_provider=style.theme_provider if style else None,
            style_instance=style,
        )

        for child in self._iter_descendants():
            try:
                child_input_bg = getattr(child, "_input_background", None)
            except Exception:
                child_input_bg = None

            explicit_input_bg = None
            try:
                explicit_input_bg = getattr(child, "_style_options", {}).get("input_background")
            except Exception:
                explicit_input_bg = None

            if explicit_input_bg and explicit_input_bg != old_bg:
                continue

            if child_input_bg != old_bg:
                continue

            try:
                setattr(child, "_input_background", new_bg)
            except Exception:
                continue

            if hasattr(child, "rebuild_style"):
                try:
                    child.rebuild_style()
                except Exception:
                    pass
            else:
                try:
                    builder_tk.call_builder(child, input_background=new_bg)
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

