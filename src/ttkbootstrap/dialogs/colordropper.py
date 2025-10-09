"""
    NOTE: https://stackoverflow.com/questions/25467288/pils-imagegrab-is-capturing-at-the-wrong-resolution

    !! This widget is not currently supported on Mac OS
"""
import tkinter as tk
from collections import namedtuple

from PIL import ImageGrab, ImageTk
from PIL.Image import Resampling

import ttkbootstrap as ttk
from ttkbootstrap import colorutils, utility
from ttkbootstrap.constants import *

ColorChoice = namedtuple('ColorChoice', 'rgb hsl hex')


class ColorDropperDialog:
    """A widget that displays an indicator and a zoom window for
    selecting a color on the screen.

    Left-click the mouse button to select a color. The result is 
    stored in the `result` property as a `ColorChoice` tuple which
    contains named fields for rgb, hsl, and hex color models.

    Zoom in and out on the zoom window by using the mouse wheel.

    This widget is implemented for **Windows** and **Linux** only.

    ![](../../assets/dialogs/color-dropper.png)       

    !!! warning "high resolution displays"
        This widget may not function properly on high resolution
        displays if you are not using the application in high
        resolution mode. This is enabled automatically on Windows.
    """

    def __init__(self):
        self.toplevel: ttk.Toplevel = None
        self.result = ttk.Variable()

    def build_screenshot_canvas(self):
        """Build the screenshot canvas"""
        self.screenshot_canvas = ttk.Canvas(
            self.toplevel, cursor='tcross', autostyle=False)
        self.screenshot_data = ImageGrab.grab()
        self.screenshot_image = ImageTk.PhotoImage(self.screenshot_data)
        self.screenshot_canvas.create_image(
            0, 0, image=self.screenshot_image, anchor=NW)
        self.screenshot_canvas.pack(fill=BOTH, expand=YES)

    def build_zoom_toplevel(self, master):
        """Build the toplevel widget that shows the zoomed version of
        the pixels underneath the mouse cursor."""
        height = utility.scale_size(self.toplevel, 100)
        width = utility.scale_size(self.toplevel, 100)
        text_xoffset = utility.scale_size(self.toplevel, 50)
        text_yoffset = utility.scale_size(self.toplevel, 50)
        toplevel = ttk.Toplevel(master)
        toplevel.transient(master)
        if self.toplevel.winsys == 'x11':
            toplevel.attributes('-type', 'tooltip')
        else:
            toplevel.overrideredirect(True)
        toplevel.geometry(f'{width}x{height}')
        toplevel.lift()
        self.zoom_canvas = ttk.Canvas(
            toplevel, borderwidth=1, height=self.zoom_height, width=self.zoom_width)
        self.zoom_canvas.create_image(0, 0, tags=['image'], anchor=NW)
        self.zoom_canvas.create_text(
            text_xoffset, text_yoffset, text="+", fill="white", tags=['indicator'])
        self.zoom_canvas.pack(fill=BOTH, expand=YES)
        self.zoom_toplevel = toplevel

    def on_mouse_wheel(self, event: tk.Event):
        """Zoom in and out on the image underneath the mouse
        TODO Cross platform testing needed
        """
        if self.toplevel.winsys.lower() == 'win32':
            delta = -int(event.delta / 120)
        elif self.toplevel.winsys.lower() == 'aqua':
            delta = -event.delta
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        self.zoom_level += delta
        self.on_mouse_motion()

    def on_left_click(self, _):
        """Capture the color underneath the mouse cursor and destroy
        the toplevel widget"""
        # add logic here to capture the image color
        hx = self.get_hover_color()
        hsl = colorutils.color_to_hsl(hx)
        rgb = colorutils.color_to_rgb(hx)
        self.result.set(ColorChoice(rgb, hsl, hx))
        self.toplevel.destroy()
        self.zoom_toplevel.destroy()
        self.toplevel.grab_release()
        return self.result.get()

    def on_right_click(self, _):
        """Close the color dropper without saving any color information"""
        self.zoom_toplevel.destroy()
        self.toplevel.grab_release()
        self.toplevel.destroy()

    def on_mouse_motion(self, event=None):
        """Callback for mouse motion"""
        if event is None:
            x, y = self.toplevel.winfo_pointerxy()
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
        self.zoom_image = ImageTk.PhotoImage(self.zoom_data)
        self.zoom_canvas.itemconfig('image', image=self.zoom_image)
        hover_color = self.get_hover_color()
        contrast_color = colorutils.contrast_color(hover_color, 'hex')
        self.zoom_canvas.itemconfig('indicator', fill=contrast_color)

    def get_hover_color(self):
        """Get the color that is hovered over by the mouse cursor."""
        x1, y1, x2, y2 = self.zoom_canvas.bbox('indicator')
        x = x1 + (x2 - x1) // 2
        y = y1 + (y2 - y2) // 2
        r, g, b = self.zoom_data.getpixel((x, y))
        hx = colorutils.color_to_hex((r, g, b))
        return hx

    def show(self):
        """Show the toplevel window"""
        self.toplevel = ttk.Toplevel(alpha=1)
        self.toplevel.wm_attributes('-fullscreen', True)
        self.build_screenshot_canvas()

        # event binding
        self.toplevel.bind("<Motion>", self.on_mouse_motion, "+")
        self.toplevel.bind("<Button-1>", self.on_left_click, "+")
        self.toplevel.bind("<Button-3>", self.on_right_click, "+")

        if self.toplevel.winsys.lower() == 'x11':
            self.toplevel.bind("<Button-4>", self.on_mouse_wheel, "+")
            self.toplevel.bind("<Button-5>", self.on_mouse_wheel, "+")
        else:
            self.toplevel.bind("<MouseWheel>", self.on_mouse_wheel, "+")

        # initial snip setup
        self.zoom_level = 2
        self.zoom_toplevel: ttk.Toplevel = None
        self.zoom_data = None
        self.zoom_image = None
        self.zoom_height = utility.scale_size(self.toplevel, 100)
        self.zoom_width = utility.scale_size(self.toplevel, 100)
        self.zoom_xoffset = utility.scale_size(self.toplevel, 10)
        self.zoom_yoffset = utility.scale_size(self.toplevel, 10)

        self.build_zoom_toplevel(self.toplevel)
        self.toplevel.grab_set()
        self.toplevel.lift('.')
        self.zoom_toplevel.lift(self.toplevel)

        self.on_mouse_motion()
