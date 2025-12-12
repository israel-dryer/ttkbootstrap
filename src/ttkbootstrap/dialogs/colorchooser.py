"""Color chooser widget for ttkbootstrap dialogs.

This module provides a comprehensive color selection widget with multiple
selection methods including RGB sliders, HSL controls, standard color palette,
hex input, and screen color picker (color dropper).

Classes:
    ColorChooser: Main color chooser widget with tabbed interface
    ColorValues: Named tuple for color value storage
    ColorChoice: Named tuple for final color selection result

Features:
    - Multiple color selection methods via tabbed interface
    - RGB color model with R, G, B sliders (0-255 range)
    - HSL color model with H (0-360), S, L (0-100) sliders
    - Standard color palette with common colors and shades
    - Hex color input with validation
    - Color dropper for selecting colors from screen
    - Live color preview
    - Integration with Querybox for dialog usage

Color Models:
    - RGB: Red, Green, Blue (0-255 each)
    - HSL: Hue (0-360), Saturation (0-100), Luminance (0-100)
    - HEX: Hexadecimal color string (#RRGGBB)

Example:
    Using ColorChooser in a dialog:

    >>> from ttkbootstrap.dialogs import QueryBox
    >>> color = QueryBox.get_color(title="Pick", value="#FF0000")
    >>> if color:
    ...     print(color.hex)
    ...     print(color.rgb)
    ...     print(color.hsl)

    Using ColorChooser widget directly:

    >>> import ttkbootstrap as ttk
    >>> from ttkbootstrap.dialogs.colorchooser import ColorChooser
    >>> root = ttk.Window()
    >>> chooser = ColorChooser(root, initial_color="#00FF00")
    >>> chooser.pack(padx=10, pady=10)
    >>> root.mainloop()
"""
import tkinter
from collections import namedtuple
from tkinter import Canvas, IntVar, StringVar
from tkinter import Frame as tkFrame, Label as tkLabel
from types import SimpleNamespace
from typing import Any, Callable, List, Optional, Tuple

from PIL import ImageColor

from ttkbootstrap.constants import *
from ttkbootstrap.core import colorutils
from ttkbootstrap.core.colorutils import HEX, HSL, HUE, LUM, RGB, SAT
from ttkbootstrap.core.localization import MessageCatalog
from ttkbootstrap.runtime import utility
from ttkbootstrap.style.style import get_style
from ttkbootstrap.widgets.composites.tooltip import ToolTip
from ttkbootstrap.widgets.primitives import Button, Entry, Frame, Label, Notebook, Spinbox
# from ttkbootstrap.validation import add_range_validation, add_validation, validator
from .colordropper import ColorDropperDialog

ttk = SimpleNamespace(
    Button=Button,
    Canvas=Canvas,
    Entry=Entry,
    Frame=Frame,
    IntVar=IntVar,
    Label=Label,
    Notebook=Notebook,
    Spinbox=Spinbox,
    StringVar=StringVar,
    use_style=get_style,
)

STD_SHADES: List[float] = [0.9, 0.8, 0.7, 0.4, 0.3]
STD_COLORS: List[str] = [
    '#FF0000', '#FFC000', '#FFFF00', '#00B050',
    '#0070C0', '#7030A0', '#FFFFFF', '#000000'
]

ColorValues = namedtuple('ColorValues', 'h s l r g b hex')
ColorChoice = namedtuple('ColorChoice', 'rgb hsl hex')

PEN = '✛'


# @validator
# def validate_color(event: Any) -> bool:
#     try:
#         ImageColor.getrgb(event.postchangetext)
#         return True
#     except:
#         return False


class ColorChooser(ttk.Frame):
    """Color chooser widget with multiple selection modes."""

    def __init__(
            self, master: Optional[tkinter.Misc], initial_color: Optional[str] = None,
            padding: Optional[int] = None) -> None:
        """Create a color chooser widget.

        The chooser offers:
        - Advanced tab: spectrum with hue/saturation and luminance slider.
        - Themed tab: swatches for theme colors and shades.
        - Standard tab: common colors and shades.

        Includes RGB/HSL/Hex inputs, live preview, and optional dropper.

        Args:
            master: Parent widget.
            initial_color: Initial color string; defaults to theme background.
            padding: Padding around the chooser.
        """
        super().__init__(master, padding=padding)
        self.tframe = ttk.Frame(self, padding=5)
        self.tframe.pack(fill=X)
        self.bframe = ttk.Frame(self, padding=(5, 0, 5, 5))
        self.bframe.pack(fill=X)

        self.notebook = ttk.Notebook(self.tframe)
        self.notebook.pack(fill=BOTH)

        self.style = ttk.use_style()
        self.colors = self.style.colors
        fallback_bg = (
                          self.colors.get("bg")
                          if isinstance(self.colors, dict)
                          else getattr(self.colors, "bg", None)
                      ) or "#ffffff"
        self.initial_color = initial_color or fallback_bg

        # color variables
        r, g, b = ImageColor.getrgb(self.initial_color)
        h, s, l = colorutils.color_to_hsl((r, g, b), RGB)
        hx = colorutils.color_to_hex((r, g, b), RGB)

        self.hue = ttk.IntVar(value=h)
        self.sat = ttk.IntVar(value=s)
        self.lum = ttk.IntVar(value=l)
        self.red = ttk.IntVar(value=r)
        self.grn = ttk.IntVar(value=g)
        self.blu = ttk.IntVar(value=b)
        self.hex = ttk.StringVar(value=hx)

        # widget sizes (adjusted by widget scaling)
        self.spectrum_height = utility.scale_size(self, 240)
        self.spectrum_width = utility.scale_size(self, 530)  # looks better on Mac OS
        # self.spectrum_width = utility.scale_size(self, 480)
        self.spectrum_point = utility.scale_size(self, 12)

        # build widgets
        spectrum_frame = ttk.Frame(self.notebook)
        self.color_spectrum = self.create_spectrum(spectrum_frame)
        self.color_spectrum.pack(fill=X, side=TOP)
        self.luminance_scale = self.create_luminance_scale(self.tframe)
        self.luminance_scale.pack(fill=X)
        self.notebook.add(spectrum_frame, text='color.advanced')

        palette_keys = ("primary", "secondary", "success", "info", "warning", "danger", "light", "dark")
        themed_colors = [
            (self.colors.get(c) if isinstance(self.colors, dict) else getattr(self.colors, c, None))
            for c in palette_keys
        ]
        themed_colors = [c or "#ffffff" for c in themed_colors]
        self.themed_swatches = self.create_swatches(
            self.notebook, themed_colors)
        self.standard_swatches = self.create_swatches(
            self.notebook, STD_COLORS)
        self.notebook.add(self.themed_swatches, text='color.themed')
        self.notebook.add(self.standard_swatches, text='color.standard')
        preview_frame = self.create_preview(self.bframe)
        preview_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))
        self.color_entries = self.create_value_inputs(self.bframe)
        self.color_entries.pack(side=RIGHT)

        self.create_spectrum_indicator()
        self.create_luminance_indicator()

    def create_spectrum(self, master: tkinter.Misc) -> ttk.Canvas:
        """Create the color spectrum canvas"""
        # canvas and point dimensions
        width = self.spectrum_width
        height = self.spectrum_height
        xf = yf = self.spectrum_point

        # create canvas widget and binding
        canvas = ttk.Canvas(master, width=width, height=height, cursor='tcross')
        canvas.bind("<B1-Motion>", self.on_spectrum_interaction, add="+")
        canvas.bind("<Button-1>", self.on_spectrum_interaction, add="+")

        # add color points
        for x, colorx in enumerate(range(0, width, xf)):
            for y, colory in enumerate(range(0, height, yf)):
                values = self.color_from_coords(colorx, colory)
                fill = values.hex
                bbox = [x * xf, y * yf, (x * xf) + xf, (y * yf) + yf]
                canvas.create_rectangle(*bbox, fill=fill, width=0)
        return canvas

    def create_spectrum_indicator(self) -> None:
        """Create a square indicator that displays in the position of
        the selected color"""
        s = utility.scale_size(self, 10)
        width = utility.scale_size(self, 2)
        values = self.get_variables()
        x1, y1 = self.coords_from_color(values.hex)
        colorutils.contrast_color(values.hex, 'hex')
        tag = ['spectrum-indicator']
        self.color_spectrum.create_rectangle(
            x1, y1, x1 + s, y1 + s, width=width, tags=[tag])
        self.color_spectrum.tag_lower('spectrum-indicator')

    # widget builder methods
    def create_swatches(self, master: tkinter.Misc, colors: List[str]) -> ttk.Frame:
        """Create a grid of color swatches"""
        box_padx = 2
        box_pady = 0
        padx_total = (box_padx * 15)
        box_width = int((self.spectrum_width - padx_total)) / len(STD_COLORS)
        box_height = int((self.spectrum_height - box_pady) / (len(STD_SHADES) + 1))
        container = ttk.Frame(master)

        # create color combinations
        color_rows = [colors]
        last_col = len(colors) - 1
        for l in STD_SHADES:
            lum = int(l * LUM)
            row = []
            for color in colors:
                color = colorutils.update_hsl_value(
                    color=color,
                    lum=lum,
                    inmodel='hex',
                    outmodel='hex'
                )
                row.append(color)
            color_rows.append(row)

        # themed colors - regular colors
        for row in color_rows:
            row_frame = ttk.Frame(container)
            for j, color in enumerate(row):
                swatch = tkFrame(
                    master=row_frame,
                    bg=color,
                    width=box_width,
                    height=box_height,
                    autostyle=False
                )
                swatch.bind('<Button-1>', self.on_press_swatch)
                if j == 0:
                    swatch.pack(side=LEFT, padx=(0, box_padx))
                elif j == last_col:
                    swatch.pack(side=LEFT, padx=(box_padx, 0))
                else:
                    swatch.pack(side=LEFT, padx=box_padx)
            row_frame.pack(fill=X, expand=YES)

        return container

    def create_preview(self, master: tkinter.Misc) -> ttk.Frame:
        """Create the preview frame for original and new colors"""
        ng_style = self.notebook.cget('style')
        # set the border color to match the notebook border color
        border_color = self.style.lookup(ng_style, 'bordercolor') or "#000000"
        container = ttk.Frame(master)

        # the frame and label for the original color (current)
        old = tkFrame(
            master=container,
            relief=FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=border_color,
            bg=self.initial_color,
            autostyle=False
        )
        old.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 2))
        constrast_fg = colorutils.contrast_color(
            color=self.initial_color,
            model='hex',
        )
        tkLabel(
            master=old,
            text=MessageCatalog.translate("color.current"),
            background=self.initial_color,
            foreground=constrast_fg,
            autostyle=False,
            width=7
        ).pack(anchor=NW)

        # the frame and label for the new color
        self.preview = tkFrame(
            master=container,
            relief=FLAT,
            bd=2,
            highlightthickness=1,
            highlightbackground=border_color,
            bg=self.initial_color,
            autostyle=False
        )
        self.preview.pack(side=LEFT, fill=BOTH, expand=YES, padx=(2, 0))
        self.preview_lbl = tkLabel(
            master=self.preview,
            text=MessageCatalog.translate("color.new"),
            background=self.initial_color,
            foreground=constrast_fg,
            autostyle=False,
            width=7
        )
        self.preview_lbl.pack(anchor=NW)

        return container

    def create_value_inputs(self, master: tkinter.Misc) -> ttk.Frame:
        """Create color value input widgets"""
        container = ttk.Frame(master)
        for x in range(4):
            container.columnconfigure(x, weight=1)

        # value labels - use semantic keys with built-in localization
        lbl_cnf = {'master': container, 'anchor': E}
        ttk.Label(**lbl_cnf, text='color.hue:').grid(row=0, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='color.sat:').grid(row=1, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='color.lum:').grid(row=2, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='color.hex:').grid(row=3, column=0, sticky=E)
        ttk.Label(**lbl_cnf, text='color.red:').grid(row=0, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text='color.green:').grid(row=1, column=2, sticky=E)
        ttk.Label(**lbl_cnf, text='color.blue:').grid(row=2, column=2, sticky=E)

        # value spinners and entry widgets
        rgb_cnf = {'master': container, 'from_': 0, 'to': 255, 'width': 3}
        sl_cnf = {'master': container, 'from_': 0, 'to': 100, 'width': 3}
        hue_cnf = {'master': container, 'from_': 0, 'to': 360, 'width': 3}
        sb_hue = ttk.Spinbox(**hue_cnf, textvariable=self.hue)
        sb_hue.grid(row=0, column=1, padx=4, pady=2, sticky=EW)
        sb_sat = ttk.Spinbox(**sl_cnf, textvariable=self.sat)
        sb_sat.grid(row=1, column=1, padx=4, pady=2, sticky=EW)
        sb_lum = ttk.Spinbox(**sl_cnf, textvariable=self.lum)
        sb_lum.grid(row=2, column=1, padx=4, pady=2, sticky=EW)
        sb_red = ttk.Spinbox(**rgb_cnf, textvariable=self.red)
        sb_red.grid(row=0, column=3, padx=4, pady=2, sticky=EW)
        sb_grn = ttk.Spinbox(**rgb_cnf, textvariable=self.grn)
        sb_grn.grid(row=1, column=3, padx=4, pady=2, sticky=EW)
        sb_blu = ttk.Spinbox(**rgb_cnf, textvariable=self.blu)
        sb_blu.grid(row=2, column=3, padx=4, pady=2, sticky=EW)
        ent_hex = ttk.Entry(container, textvariable=self.hex)
        ent_hex.grid(row=3, column=1, padx=4, columnspan=3, pady=2, sticky=EW)

        # event binding for updating colors on value change
        for sb in [sb_hue, sb_sat, sb_lum]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence,
                    func=lambda _, w=sb: self.on_entry_value_change(
                        w, HSL),
                    add="+"
                )
        for sb in [sb_red, sb_grn, sb_blu]:
            for sequence in ['<<Increment>>', '<<Decrement>>', '<Return>', '<KP_Enter>']:
                sb.bind(
                    sequence=sequence,
                    func=lambda _, w=sb: self.on_entry_value_change(
                        w, RGB),
                    add="+"
                )
        for sequence in ['<Return>', '<KP_Enter>']:
            ent_hex.bind(
                sequence=sequence,
                func=lambda _, w=ent_hex: self.on_entry_value_change(
                    w, HEX),
                add="+"
            )

        return container

    def create_luminance_scale(self, master: tkinter.Misc) -> ttk.Canvas:
        """Create the color luminance canvas"""
        # widget dimensions
        height = xf = self.spectrum_point
        width = self.spectrum_width

        values = self.get_variables()
        canvas = ttk.Canvas(master, height=height, width=width)

        # add color points to scale
        for x, l in enumerate(range(0, width, xf)):
            lum = l / width * LUM
            fill = colorutils.update_hsl_value(
                color=values.hex,
                lum=lum,
                inmodel='hex',
                outmodel='hex'
            )
            bbox = [x * xf, 0, (x * xf) + xf, height]
            tag = f'color{x}'
            canvas.create_rectangle(*bbox, fill=fill, width=0, tags=[tag])
            canvas.bind("<B1-Motion>", self.on_luminance_interaction, add="+")
            canvas.bind("<Button-1>", self.on_luminance_interaction, add="+")
        return canvas

    def create_luminance_indicator(self) -> None:
        """Create an indicator that displays in the position of the
        luminance value"""
        lum = 50
        x1 = int(lum / LUM * self.spectrum_width) - \
             ((self.spectrum_point - 2) // 2)
        y1 = 0
        x2 = x1 + self.spectrum_point
        y2 = self.spectrum_point - 3
        tag = 'luminance-indicator'
        bbox = [x1, y1, x2, y2]
        self.luminance_scale.create_rectangle(
            *bbox, fill='white', outline='black', tags=[tag])
        self.luminance_scale.tag_lower(tag)

    def coords_from_color(self, hexcolor: str) -> Tuple[float, float]:
        """Get the coordinates on the color spectrum from the color
        value"""
        h, s, _ = colorutils.color_to_hsl(hexcolor)
        x = (h / HUE) * self.spectrum_width
        y = (1 - (s / SAT)) * self.spectrum_height
        return x, y

    def color_from_coords(self, x: int, y: int):
        """Get the color value from the mouse position in the color
        spectrum"""
        HEIGHT = self.spectrum_height
        WIDTH = self.spectrum_width
        h = int(min(HUE, max(0, (HUE / WIDTH) * x)))
        s = int(min(SAT, max(0, SAT - ((SAT / HEIGHT) * y))))
        l = 50
        hx = colorutils.color_to_hex([h, s, l], 'hsl')
        r, g, b = colorutils.color_to_rgb(hx)
        return ColorValues(h, s, l, r, g, b, hx)

    def set_variables(self, h: int, s: int, l: int, r: int, g: int, b: int, hx: str) -> None:
        """Update the color value variables"""
        self.hue.set(h)
        self.sat.set(s)
        self.lum.set(l)
        self.red.set(r)
        self.grn.set(g)
        self.blu.set(b)
        self.hex.set(hx)

    def get_variables(self):
        """Get the values of all color models and return a
        tuple of color values"""
        h = self.hue.get()
        s = self.sat.get()
        l = self.lum.get()
        r = self.red.get()
        g = self.grn.get()
        b = self.blu.get()
        hx = self.hex.get()
        return ColorValues(h, s, l, r, g, b, hx)

    def update_preview(self) -> None:
        """Update the color in the preview frame"""
        hx = self.hex.get()
        fg = colorutils.contrast_color(
            color=hx,
            model='hex',
        )
        self.preview.configure(bg=hx)
        self.preview_lbl.configure(bg=hx, fg=fg)

    def update_luminance_scale(self) -> None:
        """Update the luminance scale with the change in hue and saturation"""
        values = self.get_variables()
        width = self.spectrum_width
        xf = self.spectrum_point
        for x, l in enumerate(range(0, width, xf)):
            lum = l / width * LUM
            fill = colorutils.update_hsl_value(
                color=values.hex,
                lum=lum,
                inmodel='hex',
                outmodel='hex'
            )
            tag = f'color{x}'
            self.luminance_scale.itemconfig(tag, fill=fill)

    def update_luminance_indicator(self) -> None:
        """Update the position of the luminance indicator"""
        lum = self.lum.get()
        x = int(lum / LUM * self.spectrum_width) - \
            ((self.spectrum_point - 2) // 2)
        self.luminance_scale.moveto('luminance-indicator', x, 0)
        self.luminance_scale.tag_raise('luminance-indicator')

    def update_spectrum_indicator(self) -> None:
        """Move the spectrum indicator to a new location"""
        values = self.get_variables()
        x, y = self.coords_from_color(values.hex)
        # move to the new color location
        self.color_spectrum.moveto('spectrum-indicator', x, y)
        self.color_spectrum.tag_raise('spectrum-indicator')
        # adjust the outline color based on contrast of background
        color = colorutils.contrast_color(values.hex, 'hex')
        self.color_spectrum.itemconfig('spectrum-indicator', outline=color)

    # color events
    def sync_color_values(self, model):
        """Callback for when a color value changes. A change in one
        value will automatically update the other values so that all
        color models remain in sync."""
        values = self.get_variables()
        if model == HEX:
            hx = values.hex
            r, g, b = colorutils.color_to_rgb(hx)
            h, s, l = colorutils.color_to_hsl(hx)
        elif model == RGB:
            r, g, b = values.r, values.g, values.b
            h, s, l = colorutils.color_to_hsl([r, g, b], 'rgb')
            hx = colorutils.color_to_hex([r, g, b])
        elif model == HSL:
            h, s, l = values.h, values.s, values.l
            r, g, b = colorutils.color_to_rgb([h, s, l], 'hsl')
            hx = colorutils.color_to_hex([h, s, l], 'hsl')
        self.set_variables(h, s, l, r, g, b, hx)
        self.update_preview()
        self.update_luminance_indicator()

    def on_entry_value_change(self, widget: ttk.Spinbox, model: Any) -> None:
        """Update the widget colors when the color value input is
        changed"""
        is_valid = widget.validate()
        if is_valid:
            self.sync_color_values(model)
            self.update_luminance_scale()
            self.update_spectrum_indicator()

    def on_press_swatch(self, event: tkinter.Event) -> None:
        """Update the widget colors when a color swatch is clicked."""
        button: tkFrame = self.nametowidget(event.widget)
        color = button.cget('background')
        self.hex.set(color)
        self.sync_color_values(HEX)
        self.update_luminance_scale()
        self.update_spectrum_indicator()

    def on_spectrum_interaction(self, event: tkinter.Event) -> None:
        """Update the widget colors when the color spectrum canvas is
        pressed"""
        values = self.color_from_coords(event.x, event.y)
        self.hue.set(values.h)
        self.sat.set(values.s)
        self.lum.set(values.l)
        self.sync_color_values(HSL)
        self.update_luminance_scale()
        self.update_spectrum_indicator()

    def on_luminance_interaction(self, event: tkinter.Event) -> None:
        """Update the widget colors when the color luminance scale is
        pressed"""
        l = max(0, min(LUM, int((event.x / self.spectrum_width) * LUM)))
        self.lum.set(l)
        self.sync_color_values(HSL)


from ttkbootstrap.dialogs.dialog import Dialog


class ColorChooserDialog:
    """Dialog wrapper for the ColorChooser widget.

    Args:
        master: Parent widget used for positioning and event binding.
        title: Dialog window title (localized).
        initial_color: Initial color shown in the chooser; defaults to theme background.

    Events:
        ``<<DialogResult>>`` with ``event.data = {"result": ColorChoice|None, "confirmed": bool}``.
    """

    def __init__(
            self,
            master: Optional[tkinter.Misc] = None,
            title: str = "color.chooser",
            initial_color: Optional[str] = None,
    ) -> None:
        self._master = master
        # Title is now automatically localized by BaseWindow._setup_window
        self._title = title
        self._initial_color = initial_color
        self.result: Optional[ColorChoice] = None
        self._emitted_result = False

        self._dropper = ColorDropperDialog()
        self._dropper.result.trace_add('write', self._trace_dropper_color)

        self._dialog = Dialog(
            master=master,
            title=self._title,
            content_builder=self._build_content,
            footer_builder=self._build_footer,
        )
        self._chooser: Optional[ColorChooser] = None

    # builders -----------------------------------------------------------------
    def _build_content(self, master: tkinter.Widget) -> None:
        self._chooser = ColorChooser(master, self._initial_color)
        self._chooser.pack(fill=BOTH, expand=YES)

    def _build_footer(self, master: tkinter.Widget) -> None:
        frame = ttk.Frame(master, padding=(5, 5))

        # color dropper (not supported on macOS)
        winsys = ""
        try:
            winsys = master.tk.call("tk", "windowingsystem")
        except Exception:
            winsys = ""
        if winsys != 'aqua':
            dropper = ttk.Label(frame, text=PEN, font=('-size 16'))
            ToolTip(dropper, 'color.dropper')
            dropper.pack(side=LEFT, padx=2)
            dropper.bind("<Button-1>", self._on_show_color_dropper)

        ok = ttk.Button(
            frame,
            bootstyle=PRIMARY,
            text='button.ok',
            command=self._on_ok,
        )
        ok.pack(padx=2, side=RIGHT)

        cancel = ttk.Button(
            frame,
            bootstyle=SECONDARY,
            text='button.cancel',
            command=self._on_cancel,
        )
        cancel.pack(padx=2, side=RIGHT)

        frame.pack(side=BOTTOM, fill=X, anchor=S)

    # callbacks ----------------------------------------------------------------
    def _on_show_color_dropper(self, _: tkinter.Event) -> None:
        self._dropper.show()

    def _trace_dropper_color(self, *_: Any) -> None:
        values = self._dropper.result.get()
        if self._chooser:
            self._chooser.hex.set(values[2])
            self._chooser.sync_color_values('hex')

    def _on_ok(self) -> None:
        if self._chooser:
            values = self._chooser.get_variables()
            self.result = ColorChoice(
                rgb=(values.r, values.g, values.b),
                hsl=(values.h, values.s, values.l),
                hex=values.hex
            )
        self._emit_result(confirmed=True)
        if self._dialog.toplevel:
            self._dialog.toplevel.after_idle(self._dialog.toplevel.destroy)

    def _on_cancel(self) -> None:
        self.result = None
        self._emit_result(confirmed=False)
        if self._dialog.toplevel:
            self._dialog.toplevel.after_idle(self._dialog.toplevel.destroy)

    # API ----------------------------------------------------------------------
    def show(self, position: Optional[tuple[int, int]] = None, modal: bool = True) -> None:
        """Display the dialog."""
        self.result = None
        self._emitted_result = False
        self._dialog.show(position=position, modal=modal)
        # Ensure result event fires even if consumers prefer post-show access
        if not self._emitted_result:
            self._emit_result(confirmed=self.result is not None)

    def on_dialog_result(self, callback: Callable[[Any], None]) -> Optional[str]:
        """Bind a callback fired when the dialog produces a result."""
        target = self._master or self._dialog.toplevel
        if target is None:
            return None

        def handler(event):
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_dialog_result(self, funcid: str) -> None:
        """Unbind a previously bound dialog result callback."""
        target = self._master or self._dialog.toplevel
        if target is None:
            return
        target.unbind("<<DialogResult>>", funcid)

    # helpers ------------------------------------------------------------------
    def _emit_result(self, confirmed: bool) -> None:
        payload = {"result": self.result, "confirmed": confirmed}
        target = self._master or self._dialog.toplevel
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
