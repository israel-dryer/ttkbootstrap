"""Meter widget for ttkbootstrap.

A radial progress indicator that shows progress as a full or semi circle, with
solid or striped fill and optional center/side text. Can be made interactive so
the user drags to set the value.
"""
import math
from tkinter import Event, Misc, TclError
from typing import Any, Optional, Union

from PIL import Image, ImageDraw, ImageTk
from PIL.Image import Resampling

from ttkbootstrap import DoubleVar, Frame, Label, StringVar, utility
from ttkbootstrap.constants import CENTER, DEFAULT, FULL, LEFT, RIGHT, S, Y
from ttkbootstrap.internal.configure_delegation import (
    ConfigureDelegationMixin,
    configure_delegate,
)
from ttkbootstrap.style import Bootstyle, Colors
from ttkbootstrap.style._compat import (
    normalize_meter_kwargs,
    normalize_meter_option,
    warn_deprecated,
)

M = 3  # meter image scale, higher number increases resolution


class Meter(ConfigureDelegationMixin, Frame):
    """A radial meter that can be used to show progress of long
    running operations or the amount of work completed; can also be
    used as a dial when set to `interactive=True`.

    This widget is very flexible. There are two primary meter types
    which can be set with the `meter_type` parameter: 'full' and
    'semi', which shows the arc of the meter in a full or
    semi-circle. You can also customize the arc of the circle with
    the `arc_range` and `arc_offset` parameters.

    The meter indicator can be displayed as a solid color or with
    stripes using the `stripe_thickness` parameter. By default, the
    `stripe_thickness` is 0, which results in a solid meter
    indicator. A higher `stripe_thickness` results in larger wedges
    around the arc of the meter.

    Various text and label options exist. The center text is
    formatted with the `amount_format` parameter. You can set text on
    the left and right of this center label using the `text_left` and
    `text_right` parameters. This is most commonly used for '$', '%',
    or other such symbols.

    The current value is available through the `value` property (and
    the `amount_used_var` variable); the value can also be retrieved
    or set via the `configure`/`cget` methods.

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.App()

        meter = ttk.Meter(
            meter_size=180,
            padding=5,
            amount_used=25,
            meter_type="semi",
            subtext="miles per hour",
            interactive=True,
        )
        meter.pack()

        # update the amount used directly
        meter.configure(amount_used=50)

        # update the amount used with another widget
        entry = ttk.Entry(textvariable=meter.amount_used_var)
        entry.pack(fill=X)

        # increment the amount by 10 steps
        meter.step(10)

        # decrement the amount by 15 steps
        meter.step(-15)

        # update the subtext
        meter.configure(subtext="loading...")

        app.mainloop()
        ```
    """

    # Options that affect the text labels — a `configure`/`__setitem__` that
    # touches one of these re-packs the labels; the others only redraw.
    _TEXT_OPTIONS = frozenset({"subtext", "text_left", "text_right", "show_text"})

    # Deprecated public-attribute spellings -> the 2.0 snake_case names. Served
    # via __getattr__ with a DeprecationWarning; removed in 3.0.
    _LEGACY_ATTRS = {
        "amountminvar": "amount_min_var",
        "amountusedvar": "amount_used_var",
        "amountuseddisplayvar": "amount_used_display_var",
        "amounttotalvar": "amount_total_var",
        "labelvar": "label_var",
        "meterframe": "meter_frame",
        "textframe": "text_frame",
        # The subtext/text-position Label handles kept their pre-2.0 spellings
        # while the sibling frames were snake_cased; give them collision-free
        # `*_label` names (the bare `subtext`/`text_left` names are the string
        # *options*) and deprecate the old attribute spellings.
        "subtext": "subtext_label",
        "textleft": "text_left_label",
        "textright": "text_right_label",
        "textcenter": "text_center_label",
    }

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            bootstyle: str = DEFAULT,
            arc_range: Optional[int] = None,
            arc_offset: Optional[int] = None,
            amount_min: Union[int, float] = 0,
            amount_total: Union[int, float] = 100,
            amount_used: Union[int, float] = 0,
            amount_format: str = "{:.0f}",
            wedge_size: int = 0,
            meter_size: int = 200,
            meter_type: str = FULL,
            meter_thickness: int = 10,
            show_text: bool = True,
            interactive: bool = False,
            stripe_thickness: int = 0,
            text_left: Optional[str] = None,
            text_right: Optional[str] = None,
            text_font: str = "-size 20 -weight bold",
            subtext: Optional[str] = None,
            subtext_style: str = DEFAULT,
            subtext_font: str = "-size 10",
            step_size: Union[int, float] = 1,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            master (Widget):
                The parent widget.

            arc_range (int):
                The range of the arc in degrees from start to end.

            arc_offset (int):
                The amount to offset the arc's starting position in degrees.
                0 is at 3 o'clock.

            amount_min (int):
                The minimum value of the meter. Defaults to 0. Can be set
                to a negative value to support negative ranges.

            amount_total (int):
                The maximum value of the meter.

            amount_used (int):
                The current value of the meter; displayed in a center label
                if the `show_text` property is set to True.

            amount_format (str):
                The format used to display the `amount_used` value. Default is
                "{:.0f}". Fractional formats such as "{:.1f}" are honored — the
                value is stored as a float.

            wedge_size (int):
                Sets the length of the indicator wedge around the arc. If
                greater than 0, this wedge is set as an indicator centered
                on the current meter value.

            meter_size (int):
                The meter is square. This represents the logical size of one
                side of the square in screen units (scaled for high-dpi).

            bootstyle (str):
                Sets the indicator and center text color. One of primary,
                secondary, success, info, warning, danger, light, dark.

            meter_type ('full', 'semi'):
                Displays the meter as a full circle or semi-circle.

            meter_thickness (int):
                The thickness of the indicator.

            show_text (bool):
                Indicates whether to show the left, center, and right text
                labels on the meter.

            interactive (bool):
                Indicates that the user may adjust the meter value with
                mouse interaction.

            stripe_thickness (int):
                The indicator can be displayed as a solid band or as
                striped wedges around the arc. If the value is greater than
                0, the indicator changes from a solid to striped, where the
                value is the thickness of the stripes (or wedges).

            text_left (str):
                A short string inserted to the left of the center text.

            text_right (str):
                A short string inserted to the right of the center text.

            text_font (Union[str, Font]):
                The font used to render the center text.

            subtext (str):
                Supplemental text that appears below the center text.

            subtext_style (str):
                The bootstyle color of the subtext. One of primary,
                secondary, success, info, warning, danger, light, dark.
                The default color is Theme specific and is a lighter
                shade based on whether it is a 'light' or 'dark' theme.

            subtext_font (Union[str, Font]):
                The font used to render the subtext.

            step_size (int):
                Sets the amount by which to change the meter indicator
                when incremented by mouse interaction.

            **kwargs:
                Other keyword arguments that are passed directly to the
                `Frame` widget that contains the meter components.
        """
        # Collect the option values, then fold in any legacy option names that
        # arrived through **kwargs (e.g. amountused=) so old callers keep working.
        opts = dict(
            bootstyle=bootstyle, arc_range=arc_range, arc_offset=arc_offset,
            amount_min=amount_min, amount_total=amount_total,
            amount_used=amount_used, amount_format=amount_format,
            wedge_size=wedge_size, meter_size=meter_size, meter_type=meter_type,
            meter_thickness=meter_thickness, show_text=show_text,
            interactive=interactive, stripe_thickness=stripe_thickness,
            text_left=text_left, text_right=text_right, text_font=text_font,
            subtext=subtext, subtext_style=subtext_style,
            subtext_font=subtext_font, step_size=step_size,
        )
        opts.update(normalize_meter_kwargs(kwargs))

        super().__init__(master=master, **kwargs)

        # widget variables (float-backed so fractional formats are honored)
        self.amount_min_var = DoubleVar(value=opts["amount_min"])
        self.amount_used_var = DoubleVar(value=opts["amount_used"])
        self._amount_used_traceid = self.amount_used_var.trace_add(
            "write", self._update_meter
        )
        self.amount_used_display_var = StringVar(
            value=opts["amount_format"].format(opts["amount_used"])
        )
        self.amount_total_var = DoubleVar(value=opts["amount_total"])
        self.label_var = StringVar(value=opts["subtext"])

        # misc settings — meter_size/meter_thickness are stored LOGICAL and only
        # scaled to physical pixels at the render seams (see _physical_size).
        self._amount_format = opts["amount_format"]
        self._set_arc_offset_range(
            opts["meter_type"], opts["arc_offset"], opts["arc_range"]
        )
        self._towards_maximum = True
        self._meter_size = opts["meter_size"]
        self._meter_thickness = opts["meter_thickness"]
        self._stripe_thickness = opts["stripe_thickness"]
        self._show_text = opts["show_text"]
        self._wedge_size = opts["wedge_size"]
        self._step_size = opts["step_size"]
        self._text_left = opts["text_left"]
        self._text_right = opts["text_right"]
        self._text_font = opts["text_font"]
        self._subtext = opts["subtext"]
        self._subtext_font = opts["subtext_font"]
        self._subtext_style = opts["subtext_style"]
        self._bootstyle = opts["bootstyle"]
        self._interactive = opts["interactive"]
        self._bindids = {}

        self._setup_widget()

    # -- value access -------------------------------------------------------- #
    @property
    def value(self) -> Union[int, float]:
        """The current meter value."""
        return self.amount_used_var.get()

    @value.setter
    def value(self, amount: Union[int, float]) -> None:
        self.amount_used_var.set(amount)

    def __getattr__(self, name: str) -> Any:
        # Only fires for missing attributes; map the deprecated spellings.
        new = self._LEGACY_ATTRS.get(name)
        if new is not None:
            warn_deprecated(f"Meter.{name}", f"Meter.{new}")
            return getattr(self, new)
        raise AttributeError(name)

    # -- scaling seam -------------------------------------------------------- #
    def _physical_size(self) -> int:
        """Physical (dpi-scaled) meter size in pixels from the logical size."""
        return utility.scale_size(self, self._meter_size)

    def _physical_thickness(self) -> int:
        """Physical (dpi-scaled) indicator thickness from the logical value."""
        return utility.scale_size(self, self._meter_thickness)

    def _update_meter(self, *_: Any) -> None:
        """Redraw the indicator and refresh the display text on value change."""
        self._draw_meter()
        amount_used = self.amount_used_var.get()
        self.amount_used_display_var.set(self._amount_format.format(amount_used))

    def destroy(self) -> None:
        """Detach the value-variable trace before teardown.

        The trace's write callback holds a reference back to the meter, so
        leaving it attached keeps the widget alive after destroy.
        """
        if self._amount_used_traceid is not None:
            try:
                self.amount_used_var.trace_remove(
                    "write", self._amount_used_traceid
                )
            except TclError:
                pass
            self._amount_used_traceid = None
        super().destroy()

    def _setup_widget(self) -> None:
        """Initialize and configure all meter components."""
        size = self._physical_size()
        self.meter_frame = Frame(master=self, width=size, height=size)
        self.indicator = Label(self.meter_frame)
        self.text_frame = Frame(self.meter_frame)
        self.text_left_label = Label(
            master=self.text_frame,
            text=self._text_left,
            font=self._subtext_font,
            bootstyle=f"{self._subtext_style}-metersubtxt",
            anchor=S,
            padding=(0, 5),
        )
        self.text_center_label = Label(
            master=self.text_frame,
            textvariable=self.amount_used_display_var,
            bootstyle=f"{self._bootstyle}-meter",
            font=self._text_font,
        )
        self.text_right_label = Label(
            master=self.text_frame,
            text=self._text_right,
            font=self._subtext_font,
            bootstyle=f"{self._subtext_style}-metersubtxt",
            anchor=S,
            padding=(0, 5),
        )
        self.subtext_label = Label(
            master=self.meter_frame,
            text=self._subtext,
            bootstyle=f"{self._subtext_style}-metersubtxt",
            font=self._subtext_font,
            textvariable=self.label_var,
        )

        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self._set_interactive_bind()
        self._draw_base_image()
        self._draw_meter()

        # set widget geometry
        self.indicator.place(x=0, y=0)
        self.meter_frame.pack()
        self._set_show_text()

    def _set_widget_colors(self) -> None:
        """Query the theme for the meter foreground/background/trough colors."""
        ttkstyle = Bootstyle.ttkstyle_name(
            string=f"{self._bootstyle}-meter-label"
        )
        textcolor = self._lookup_style_option(ttkstyle, "foreground")
        background = self._lookup_style_option(ttkstyle, "background")
        troughcolor = self._lookup_style_option(ttkstyle, "space")
        self._meterforeground = textcolor
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)
        self._metertrough = troughcolor

    def _set_meter_text(self) -> None:
        """Configure and position all text labels."""
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self) -> None:
        """Position the subtext label below the center text."""
        if self._subtext:
            if self._show_text:
                self.subtext_label.place(relx=0.5, rely=0.6, anchor=CENTER)
            else:
                self.subtext_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def _set_show_text(self) -> None:
        """Show or hide the text labels based on the show_text setting."""
        self.text_frame.pack_forget()
        self.text_center_label.pack_forget()
        self.text_left_label.pack_forget()
        self.text_right_label.pack_forget()
        self.subtext_label.pack_forget()

        if self._show_text:
            if self._subtext:
                self.text_frame.place(relx=0.5, rely=0.45, anchor=CENTER)
            else:
                self.text_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()
        self._set_subtext()

    def _set_text_left(self) -> None:
        """Pack the left text label if configured."""
        if self._show_text and self._text_left:
            self.text_left_label.pack(side=LEFT, fill=Y)

    def _set_text_center(self) -> None:
        """Pack the center text label showing the current value."""
        if self._show_text:
            self.text_center_label.pack(side=LEFT, fill=Y)

    def _set_text_right(self) -> None:
        """Pack the right text label if configured."""
        self.text_right_label.configure(text=self._text_right)
        if self._show_text and self._text_right:
            self.text_right_label.pack(side=RIGHT, fill=Y)

    def _set_interactive_bind(self) -> None:
        """Bind or unbind mouse events for interactive mode."""
        seq1 = "<B1-Motion>"
        seq2 = "<Button-1>"

        # Drop any existing binds first so repeated calls (e.g. toggling
        # `interactive` via configure) don't leak orphaned bind callbacks.
        for seq in (seq1, seq2):
            if seq in self._bindids:
                self.indicator.unbind(seq, self._bindids.pop(seq))

        if self._interactive:
            self._bindids[seq1] = self.indicator.bind(
                seq1, self._on_dial_interact
            )
            self._bindids[seq2] = self.indicator.bind(
                seq2, self._on_dial_interact
            )

    def _set_arc_offset_range(
        self, meter_type: str, arc_offset: Optional[int], arc_range: Optional[int]
    ) -> None:
        """Configure the arc parameters based on the meter type."""
        from ttkbootstrap.constants import SEMI

        if meter_type == SEMI:
            self._arc_offset = 135 if arc_offset is None else arc_offset
            self._arc_range = 270 if arc_range is None else arc_range
        else:
            self._arc_offset = -90 if arc_offset is None else arc_offset
            self._arc_range = 360 if arc_range is None else arc_range
        self._meter_type = meter_type

    def _draw_meter(self, *_: Any) -> None:
        """Draw the meter indicator on the base image."""
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._stripe_thickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)

        size = self._physical_size()
        self._meterimage = ImageTk.PhotoImage(
            img.resize((size, size), Resampling.BICUBIC)
        )
        self.indicator.configure(image=self._meterimage)

    def _draw_base_image(self) -> None:
        """Draw the meter background/trough (constant while the value changes)."""
        self._set_widget_colors()
        size = self._physical_size()
        self._base_image = Image.new(mode="RGBA", size=(size * M, size * M))
        draw = ImageDraw.Draw(self._base_image)

        x1 = y1 = size * M - 20
        width = self._physical_thickness() * M
        # striped meter
        if self._stripe_thickness > 0:
            _from = self._arc_offset
            _to = self._arc_range + self._arc_offset
            _step = 2 if self._stripe_thickness == 1 else self._stripe_thickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripe_thickness - 1,
                    fill=self._metertrough,
                    width=width,
                )
        # solid meter
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arc_offset,
                end=self._arc_range + self._arc_offset,
                fill=self._metertrough,
                width=width,
            )

    def _draw_solid_meter(self, draw) -> None:
        """Draw a solid meter indicator."""
        size = self._physical_size()
        x1 = y1 = size * M - 20
        width = self._physical_thickness() * M

        if self._wedge_size > 0:
            meter_value = self._meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedge_size,
                end=meter_value + self._wedge_size,
                fill=self._meterforeground,
                width=width,
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arc_offset,
                end=self._meter_value(),
                fill=self._meterforeground,
                width=width,
            )

    def _draw_striped_meter(self, draw) -> None:
        """Draw a striped meter indicator (discrete wedges)."""
        meter_value = self._meter_value()
        size = self._physical_size()
        x1 = y1 = size * M - 20
        width = self._physical_thickness() * M

        if self._wedge_size > 0:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedge_size,
                end=meter_value + self._wedge_size,
                fill=self._meterforeground,
                width=width,
            )
        else:
            _from = self._arc_offset
            _to = meter_value - 1
            _step = self._stripe_thickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripe_thickness - 1,
                    fill=self._meterforeground,
                    width=width,
                )

    def _meter_value(self) -> int:
        """Convert the current value to the arc degree used for drawing."""
        amount_min = self.amount_min_var.get()
        amount_total = self.amount_total_var.get()
        amount_used = self.amount_used_var.get()

        # Normalize to 0-1 range to handle negative values
        range_size = amount_total - amount_min
        if range_size == 0:
            normalized = 0
        else:
            normalized = (amount_used - amount_min) / range_size

        value = int(normalized * self._arc_range + self._arc_offset)
        return value

    def _on_theme_change(self, *_: Any) -> None:
        """Redraw the meter with updated colors from the new theme."""
        self._draw_base_image()
        self._draw_meter()

    def _on_dial_interact(self, e: Event) -> None:
        """Adjust the value based on the mouse position in interactive mode."""
        size = self._physical_size()
        dx = e.x - size // 2
        dy = e.y - size // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arc_offset - max(0, (360 - self._arc_range) / 2):
            factor = degs - self._arc_offset
        else:
            factor = 360 + degs - self._arc_offset

        # clamp the value between `amount_min` and `amount_total`
        amount_min = self.amount_min_var.get()
        amount_total = self.amount_total_var.get()
        lastused = self.amount_used_var.get()

        # Calculate the value based on the range
        range_size = amount_total - amount_min
        amount_used = (range_size / self._arc_range * factor) + amount_min

        # calculate amount used given step_size
        if self._step_size > 0:
            # Round to nearest step_size
            amount_used = round(amount_used / self._step_size) * self._step_size

        # if the number is the same, then do not redraw
        if lastused == amount_used:
            return
        # set the amount used variable
        if amount_used < amount_min:
            self.amount_used_var.set(amount_min)
        elif amount_used > amount_total:
            self.amount_used_var.set(amount_total)
        else:
            self.amount_used_var.set(amount_used)

    def _lookup_style_option(self, style: str, option: str) -> Any:
        """Query a ttk style option value."""
        value = self.tk.call(
            "ttk::style", "lookup", style, "-%s" % option, None, None
        )
        return value

    # -- configure delegates ------------------------------------------------- #
    # One get/set handler per custom option (value=None queries, else sets).
    # The ConfigureDelegationMixin wires these into configure/cget/keys/
    # __getitem__/__setitem__; the redraw is batched once in _refresh below.

    @configure_delegate("bootstyle")
    def _cfg_bootstyle(self, value):
        if value is None:
            return self._bootstyle
        self._bootstyle = value
        self.text_center_label.configure(bootstyle=f"{self._bootstyle}-meter")

    @configure_delegate("arc_range")
    def _cfg_arc_range(self, value):
        if value is None:
            return self._arc_range
        self._arc_range = value

    @configure_delegate("arc_offset")
    def _cfg_arc_offset(self, value):
        if value is None:
            return self._arc_offset
        self._arc_offset = value

    @configure_delegate("amount_min")
    def _cfg_amount_min(self, value):
        if value is None:
            return self.amount_min_var.get()
        self.amount_min_var.set(value)

    @configure_delegate("amount_total")
    def _cfg_amount_total(self, value):
        if value is None:
            return self.amount_total_var.get()
        self.amount_total_var.set(value)

    @configure_delegate("amount_used")
    def _cfg_amount_used(self, value):
        if value is None:
            return self.amount_used_var.get()
        self.amount_used_var.set(value)

    @configure_delegate("amount_format")
    def _cfg_amount_format(self, value):
        if value is None:
            return self._amount_format
        self._amount_format = value
        self.amount_used_display_var.set(
            self._amount_format.format(self.amount_used_var.get())
        )

    @configure_delegate("wedge_size")
    def _cfg_wedge_size(self, value):
        if value is None:
            return self._wedge_size
        self._wedge_size = value

    @configure_delegate("meter_size")
    def _cfg_meter_size(self, value):
        if value is None:
            return self._meter_size  # logical (round-trips without re-scaling)
        self._meter_size = value
        size = self._physical_size()
        self.meter_frame.configure(height=size, width=size)

    @configure_delegate("meter_type")
    def _cfg_meter_type(self, value):
        if value is None:
            return self._meter_type
        self._meter_type = value

    @configure_delegate("meter_thickness")
    def _cfg_meter_thickness(self, value):
        if value is None:
            return self._meter_thickness  # logical
        self._meter_thickness = value

    @configure_delegate("show_text")
    def _cfg_show_text(self, value):
        if value is None:
            return self._show_text
        self._show_text = value

    @configure_delegate("interactive")
    def _cfg_interactive(self, value):
        if value is None:
            return self._interactive
        self._interactive = value
        self._set_interactive_bind()

    @configure_delegate("stripe_thickness")
    def _cfg_stripe_thickness(self, value):
        if value is None:
            return self._stripe_thickness
        self._stripe_thickness = value

    @configure_delegate("text_left")
    def _cfg_text_left(self, value):
        if value is None:
            return self._text_left
        self._text_left = value
        self.text_left_label.configure(text=self._text_left)

    @configure_delegate("text_right")
    def _cfg_text_right(self, value):
        if value is None:
            return self._text_right
        self._text_right = value

    @configure_delegate("text_font")
    def _cfg_text_font(self, value):
        if value is None:
            return self._text_font
        self._text_font = value
        self.text_center_label.configure(font=self._text_font)

    @configure_delegate("subtext")
    def _cfg_subtext(self, value):
        if value is None:
            return self.label_var.get()
        self._subtext = value
        self.label_var.set(value)

    @configure_delegate("subtext_style")
    def _cfg_subtext_style(self, value):
        if value is None:
            return self._subtext_style
        self._subtext_style = value
        # Recolor every subtext label (not just the center subtext) with the
        # same style suffix used at construction.
        for label in (self.subtext_label, self.text_left_label, self.text_right_label):
            label.configure(bootstyle=f"{self._subtext_style}-metersubtxt")

    @configure_delegate("subtext_font")
    def _cfg_subtext_font(self, value):
        if value is None:
            return self._subtext_font
        self._subtext_font = value
        self.subtext_label.configure(font=self._subtext_font)
        self.text_left_label.configure(font=self._subtext_font)
        self.text_right_label.configure(font=self._subtext_font)

    @configure_delegate("step_size")
    def _cfg_step_size(self, value):
        if value is None:
            return self._step_size
        self._step_size = value

    # -- configure/setitem wrappers (batch one redraw per set) --------------- #
    def _refresh(self, redraw_text: bool = False) -> None:
        """Recompute the arc and redraw once after a batch of option changes."""
        try:
            if self._meter_type:
                self._set_arc_offset_range(
                    meter_type=self._meter_type,
                    arc_offset=self._arc_offset,
                    arc_range=self._arc_range,
                )
        except AttributeError:
            return

        self._draw_base_image()
        self._draw_meter()
        if redraw_text:
            self._set_meter_text()

    def configure(self, cnf: Any = None, **kwargs: Any) -> Any:
        # Accept legacy option spellings (kwargs, dict cnf, or a query string).
        if kwargs:
            kwargs.update(normalize_meter_kwargs(kwargs))
        if isinstance(cnf, dict):
            cnf = dict(cnf)
            cnf.update(normalize_meter_kwargs(cnf))
        elif isinstance(cnf, str):
            cnf = normalize_meter_option(cnf)

        keys = set(kwargs)
        if isinstance(cnf, dict):
            keys |= set(cnf)
        result = super().configure(cnf, **kwargs)
        if keys:  # it was a set
            self._refresh(redraw_text=bool(keys & self._TEXT_OPTIONS))
        return result

    config = configure

    def cget(self, key: str) -> Any:
        return super().cget(normalize_meter_option(key))

    def __setitem__(self, key: str, value: Any) -> None:
        key = normalize_meter_option(key)
        super().__setitem__(key, value)
        self._refresh(redraw_text=key in self._TEXT_OPTIONS)

    def __getitem__(self, key: str) -> Any:
        return super().__getitem__(normalize_meter_option(key))

    def step(self, delta: Union[int, float] = 1) -> None:
        """Increment or decrement the meter value.

        The indicator will bounce back when reaching the minimum or maximum
        values, reversing direction automatically.

        Parameters:
            delta (int, optional): The amount to change the indicator by.
                                  Positive values increase, negative values
                                  decrease. Defaults to 1.
        """
        amount_used = self.amount_used_var.get()
        amount_min = self.amount_min_var.get()
        amount_total = self.amount_total_var.get()

        if self._towards_maximum:
            amount_updated = amount_used + delta
        else:
            amount_updated = amount_used - delta

        if amount_updated >= amount_total:
            self._towards_maximum = False
            self.amount_used_var.set(
                amount_total - (amount_updated - amount_total)
            )
        elif amount_updated < amount_min:
            self._towards_maximum = True
            self.amount_used_var.set(amount_min + (amount_min - amount_updated))
        else:
            self.amount_used_var.set(amount_updated)
