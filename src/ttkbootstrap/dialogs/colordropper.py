"""Screen color picker (dropper) dialog for ttkbootstrap.

This module provides a color dropper tool that allows users to select colors
directly from anywhere on the screen. It captures a screenshot and displays
a magnified view to help with precise color selection.

Example:
    Using the dropper directly:

    >>> from ttkbootstrap.dialogs.colordropper import ColorDropperDialog
    >>> dropper = ColorDropperDialog()
    >>> dropper.show()
    >>> color = dropper.result.get()
    >>> if color:
    ...     print(color.hex)
    ...     print(color.rgb)
    ...     print(color.hsl)
"""
import tkinter as tk
from collections import namedtuple
from types import SimpleNamespace
from typing import Any, Callable, Optional

from tkinter import Canvas, Variable
from PIL import ImageGrab, ImageTk
from PIL.Image import Resampling

from ttkbootstrap.api.app import Toplevel
import ttkbootstrap.core.colorutils as colorutils
import ttkbootstrap.runtime.utility as utility
from ttkbootstrap.core.constants import *

ttk = SimpleNamespace(Canvas=Canvas, Toplevel=Toplevel, Variable=Variable)

ColorChoice = namedtuple('ColorChoice', 'rgb hsl hex')


class ColorDropperDialog:
    """Screen color picker with zoom preview.

    Usage:
        Left-click anywhere on screen to pick a color; mouse wheel zooms the preview.
        Selected color is stored in ``result`` as a ColorChoice (rgb, hsl, hex).

    Platforms:
        Windows and Linux supported; macOS not supported (ImageGrab limitation).

    Notes:
        On high-DPI displays, ensure the app runs in high-DPI mode (automatic on Windows).
    """

    def __init__(self) -> None:
        self.zoom_yoffset = None
        self.zoom_xoffset = None
        self.zoom_width = None
        self.zoom_height = None
        self.zoom_image = None
        self.zoom_data = None
        self.zoom_level = None
        self.screenshot_image = None
        self.screenshot_data = None
        self.screenshot_canvas = None
        self.toplevel: Optional[ttk.Toplevel] = None
        self.zoom_toplevel: Optional[ttk.Toplevel] = None
        self.result: ttk.Variable = ttk.Variable()
        self._emitted_result = False

    def build_screenshot_canvas(self) -> None:
        """Build the screenshot canvas"""
        self.screenshot_canvas: ttk.Canvas = ttk.Canvas(self.toplevel, cursor='tcross')
        self.screenshot_data = ImageGrab.grab()
        self.screenshot_image: ImageTk.PhotoImage = ImageTk.PhotoImage(self.screenshot_data)
        self.screenshot_canvas.create_image(
            0, 0, image=self.screenshot_image, anchor=NW)
        self.screenshot_canvas.pack(fill=BOTH, expand=YES)

    def build_zoom_toplevel(self, master) -> None:
        """Build the toplevel widget that shows the zoomed version of
        the pixels underneath the mouse cursor."""
        height = utility.scale_size(self.toplevel, 100)
        width = utility.scale_size(self.toplevel, 100)
        text_xoffset = utility.scale_size(self.toplevel, 50)
        text_yoffset = utility.scale_size(self.toplevel, 50)
        toplevel = ttk.Toplevel(master=master)
        toplevel.transient(master=master)
        if self.toplevel and self.toplevel.winsys == 'x11':
            toplevel.attributes('-type', 'tooltip')
        else:
            toplevel.overrideredirect(True)
        toplevel.geometry(f'{width}x{height}')
        toplevel.lift()
        self.zoom_canvas: ttk.Canvas = ttk.Canvas(
            toplevel, borderwidth=1, height=self.zoom_height, width=self.zoom_width)
        self.zoom_canvas.create_image(0, 0, tags=['image'], anchor=NW)
        self.zoom_canvas.create_text(
            text_xoffset, text_yoffset, text="+", fill="white", tags=['indicator'])
        self.zoom_canvas.pack(fill=BOTH, expand=YES)
        self.zoom_toplevel = toplevel

    def _cleanup(self) -> None:
        """Destroy zoom and main toplevels."""
        if self.zoom_toplevel and self.zoom_toplevel.winfo_exists():
            try:
                self.zoom_toplevel.destroy()
            except Exception:
                pass
        if self.toplevel and self.toplevel.winfo_exists():
            try:
                self.toplevel.destroy()
            except Exception:
                pass

    def on_mouse_wheel(self, event: tk.Event) -> None:
        """Zoom in and out on the image underneath the mouse"""
        delta = 0
        if self.toplevel and self.toplevel.winsys.lower() == 'win32':
            delta = -int(event.delta / 120)
        elif self.toplevel and self.toplevel.winsys.lower() == 'aqua':
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        self.zoom_level += delta
        self._on_mouse_motion()

    def on_left_click(self, _: tk.Event) -> Optional[ColorChoice]:
        """Capture the color underneath the mouse cursor and destroy
        the toplevel widget"""
        # add logic here to capture the image color
        hx = self.get_hover_color()
        hsl = colorutils.color_to_hsl(hx)
        rgb = colorutils.color_to_rgb(hx)
        self.result.set(ColorChoice(rgb, hsl, hx))
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel.grab_release()
        if self.zoom_toplevel:
            self.zoom_toplevel.destroy()
        return self.result.get()

    def on_right_click(self, _: tk.Event) -> None:
        """Close the color dropper without saving any color information"""
        if self.zoom_toplevel:
            self.zoom_toplevel.destroy()
        if self.toplevel:
            self.toplevel.grab_release()
            self.toplevel.destroy()

    def _on_mouse_motion(self, event: Optional[tk.Event] = None) -> None:
        """Callback for mouse motion"""
        if event is None:
            x, y = self.toplevel.winfo_pointerxy()  # type: ignore[union-attr]
        else:
            x = event.x
            y = event.y
        # move snip window
        self.zoom_toplevel.geometry(
            f'+{x + self.zoom_xoffset}+{y + self.zoom_yoffset}')
        # update the snip image
        bbox = (x - self.zoom_level, y - self.zoom_level,
                x + self.zoom_level + 1, y + self.zoom_level + 1)
        size = (self.zoom_width, self.zoom_height)
        self.zoom_data = self.screenshot_data.crop(
            bbox).resize(size, Resampling.BOX)
        self.zoom_image: ImageTk.PhotoImage = ImageTk.PhotoImage(self.zoom_data)
        self.zoom_canvas.itemconfig('image', image=self.zoom_image)
        hover_color = self.get_hover_color()
        contrast_color = colorutils.contrast_color(hover_color, 'hex')
        self.zoom_canvas.itemconfig('indicator', fill=contrast_color)

    def get_hover_color(self) -> str:
        """Get the color that is hovered over by the mouse cursor."""
        x1, y1, x2, y2 = self.zoom_canvas.bbox('indicator')
        x = x1 + (x2 - x1) // 2
        y = y1 + (y2 - y2) // 2
        r, g, b = self.zoom_data.getpixel((x, y))
        hx = colorutils.color_to_hex((r, g, b))
        return hx

    # event helpers -----------------------------------------------------------
    def on_dialog_result(self, callback: Callable[[Any], None]) -> Optional[str]:
        """Bind a callback fired when the dropper produces a result."""
        target = self.toplevel
        if target is None:
            return None

        def handler(event):
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_dialog_result(self, funcid: str) -> None:
        """Unbind a previously bound dialog result callback."""
        target = self.toplevel
        if target is None:
            return
        target.unbind("<<DialogResult>>", funcid)

    def _emit_result(self, confirmed: bool) -> None:
        """Emit the dialog result event once."""
        if self._emitted_result:
            return
        payload = {"result": self.result.get() if hasattr(self.result, "get") else None, "confirmed": confirmed}
        target = self.toplevel
        if not target:
            return
        try:
            target.event_generate("<<DialogResult>>", data=payload)
        except Exception:
            try:
                target.event_generate("<<DialogResult>>")
            except Exception:
                pass
        self._emitted_result = True

    def show(self) -> None:
        """Show the toplevel window"""
        self._emitted_result = False
        self.toplevel = ttk.Toplevel(alpha=1)
        self.toplevel.wm_attributes('-fullscreen', True)
        self.build_screenshot_canvas()

        # event binding
        self.toplevel.bind("<Motion>", self._on_mouse_motion, "+")
        self.toplevel.bind("<Button-1>", self._on_left_click, "+")
        self.toplevel.bind("<Button-3>", self._on_right_click, "+")
        self.toplevel.bind("<Escape>", self._on_cancel, "+")

        if self.toplevel.winsys.lower() == 'x11':
            self.toplevel.bind("<Button-4>", self.on_mouse_wheel, "+")
            self.toplevel.bind("<Button-5>", self.on_mouse_wheel, "+")
        else:
            self.toplevel.bind("<MouseWheel>", self.on_mouse_wheel, "+")

        # initial snip setup
        self.zoom_level: int = 2
        self.zoom_toplevel: Optional[ttk.Toplevel] = None
        self.zoom_data: Any = None
        self.zoom_image: Optional[ImageTk.PhotoImage] = None
        self.zoom_height: int = utility.scale_size(self.toplevel, 100)
        self.zoom_width: int = utility.scale_size(self.toplevel, 100)
        self.zoom_xoffset: int = utility.scale_size(self.toplevel, 10)
        self.zoom_yoffset: int = utility.scale_size(self.toplevel, 10)

        self.build_zoom_toplevel(self.toplevel)
        self.toplevel.grab_set()
        self.toplevel.lift('.')
        self.zoom_toplevel.lift(self.toplevel)

        self._on_mouse_motion()

    def _on_left_click(self, _: tk.Event) -> Optional[ColorChoice]:
        """Capture the color underneath the mouse cursor and close."""
        hx = self.get_hover_color()
        hsl = colorutils.color_to_hsl(hx)
        rgb = colorutils.color_to_rgb(hx)
        self.result.set(ColorChoice(rgb, hsl, hx))
        self._emit_result(confirmed=True)
        self._cleanup()
        return self.result.get()

    def _on_right_click(self, _: tk.Event) -> None:
        """Close without saving any color information."""
        self.result.set(None)
        self._emit_result(confirmed=False)
        self._cleanup()

    def _on_cancel(self, _: tk.Event) -> None:
        """Close without selection (Escape)."""
        self._on_right_click(_)
