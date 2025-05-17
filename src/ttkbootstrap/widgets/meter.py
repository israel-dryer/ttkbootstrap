import math
from tkinter import Event, IntVar, Misc, StringVar
from typing import Literal

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

from PIL import ImageDraw, ImageTk, Image
from PIL.Image import Resampling

from ttkbootstrap.ttk_types import FrameOptions, StyleColor
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.style import Bootstyle, Colors
from ttkbootstrap.utility import scale_size

M = 3  # meter image scale, higher number increases resolution
MeterType = Literal['full', 'semi']


class Meter(Frame):
    """
    A radial meter widget for displaying progress, values, or usage in a visual arc form.

    Supports solid and striped arc indicators, full or semi-circle display types,
    and optional interactive adjustment by dragging. Also includes configurable labels
    and subtext in the center of the meter.

    Args:
        master (Misc | None):
            The parent widget.

        color (StyleColor):
            The style color used for the meter indicator and center label.

        arcrange (int):
            The span of the arc in degrees (e.g., 270 for a semi-circle).

        arcoffset (int):
            The starting angle of the arc in degrees (0 is 3 o'clock).

        amounttotal (int):
            The total maximum value of the meter.

        amountused (int):
            The current value to be represented on the meter.

        amountformat (str):
            Format string to convert `amountused` into displayable text.

        wedgesize (int):
            Size of the arc segment to use as an indicator wedge.

        metersize (int):
            Diameter of the meter display in pixels.

        metertype (Literal['full', 'semi']):
            Choose between a full-circle or semi-circle display.

        meterthickness (int):
            Thickness of the meter's arc.

        showtext (bool):
            Whether to display the text labels.

        interactive (bool):
            If True, allows user interaction to modify value.

        stripethickness (int):
            If > 0, draw striped segments instead of a solid arc.

        textleft (str):
            Text label shown to the left of the numeric value.

        textright (str):
            Text label shown to the right of the numeric value.

        textfont (str):
            Font specification for the center text label.

        subtext (str):
            Additional subtext shown beneath the center label.

        subtextstyle (StyleColor):
            Color used for the subtext label.

        subtextfont (str):
            Font specification for the subtext label.

        stepsize (int):
            Amount to increment or decrement when stepping or dragging.

        **kwargs (Unpack[FrameOptions]):
            Additional options passed to the `ttk.Frame` constructor.

    Example:
        >>> import ttkbootstrap as ttk
        >>> from ttkbootstrap.constants import *
        >>> app = ttk.Window()
        >>> meter = ttk.Meter(metersize=180, amountused=25, metertype="semi", subtext="mph")
        >>> meter.pack()
        >>> app.mainloop()
    """

    def __init__(
        self,
        master: Misc | None = None,
        color: StyleColor = "default",
        arcrange: int = None,
        arcoffset: int = None,
        amounttotal=100,
        amountused=0,
        amountformat="{:.0f}",
        wedgesize=0,
        metersize=200,
        metertype: MeterType = 'full',
        meterthickness=10,
        showtext=True,
        interactive=False,
        stripethickness=0,
        textleft=None,
        textright=None,
        textfont="-size 20 -weight bold",
        subtext=None,
        subtextstyle: StyleColor = "default",
        subtextfont="-size 10",
        stepsize=1,
        **kwargs: Unpack[FrameOptions],
    ):
        """
        Args:
            master (Misc | None):
                The parent widget.

            color (StyleColor):
                The style color used for the meter indicator and center label.

            arcrange (int):
                The span of the arc in degrees (e.g., 270 for a semi-circle).

            arcoffset (int):
                The starting angle of the arc in degrees (0 is 3 o'clock).

            amounttotal (int):
                The total maximum value of the meter.

            amountused (int):
                The current value to be represented on the meter.

            amountformat (str):
                Format string to convert `amountused` into displayable text.

            wedgesize (int):
                Size of the arc segment to use as an indicator wedge.

            metersize (int):
                Diameter of the meter display in pixels.

            metertype (Literal['full', 'semi']):
                Choose between a full-circle or semi-circle display.

            meterthickness (int):
                Thickness of the meter's arc.

            showtext (bool):
                Whether to display the text labels.

            interactive (bool):
                If True, allows user interaction to modify value.

            stripethickness (int):
                If > 0, draw striped segments instead of a solid arc.

            textleft (str):
                Text label shown to the left of the numeric value.

            textright (str):
                Text label shown to the right of the numeric value.

            textfont (str):
                Font specification for the center text label.

            subtext (str):
                Additional subtext shown beneath the center label.

            subtextstyle (StyleColor):
                Color used for the subtext label.

            subtextfont (str):
                Font specification for the subtext label.

            stepsize (int):
                Amount to increment or decrement when stepping or dragging.

            **kwargs (Unpack[FrameOptions]):
                Additional options passed to the `ttk.Frame` constructor.
        """
        super().__init__(master=master, **kwargs)

        # widget variables
        self.amountusedvar = IntVar(value=amountused)
        self.amountusedvar.trace_add("write", self._update_meter)
        self.amountuseddisplayvar = StringVar(value=amountformat.format(amountused))
        self.amounttotalvar = IntVar(value=amounttotal)
        self.labelvar = StringVar(value=subtext)

        # misc settings
        self._amountformat = amountformat
        self._set_arc_offset_range(metertype, arcoffset, arcrange)
        self._towards_maximum = True
        self._metersize = scale_size(self, metersize)
        self._meterthickness = scale_size(self, meterthickness)
        self._stripethickness = stripethickness
        self._showtext = showtext
        self._wedgesize = wedgesize
        self._stepsize = stepsize
        self._textleft = textleft
        self._textright = textright
        self._textfont = textfont
        self._subtext = subtext
        self._subtextfont = subtextfont
        self._subtextstyle = subtextstyle
        self._color = color
        self._interactive = interactive
        self._bindids = {}

        self._setup_widget()

    def _update_meter(self, *_):
        self._draw_meter()
        amount_used = self.amountusedvar.get()
        self.amountuseddisplayvar.set(self._amountformat.format(amount_used))

    def _setup_widget(self):
        self.meter_frame = Frame(master=self, width=self._metersize, height=self._metersize)
        self.indicator = Label(self.meter_frame)
        self.textframe = Frame(self.meter_frame)
        self.text_left = Label(
            master=self.textframe,
            text=self._textleft,
            font=self._subtextfont,
            color=self._subtextstyle,
            variant="metersubtxt",
            anchor="s",
            padding=(0, 5),
        )
        self.text_center = Label(
            master=self.textframe,
            textvariable=self.amountuseddisplayvar,
            color=self._color,
            variant="meter",
            font=self._textfont,
        )
        self.text_right = Label(
            master=self.textframe,
            text=self._textright,
            font=self._subtextfont,
            color=self._subtextstyle,
            variant="metersubtxt",
            anchor="s",
            padding=(0, 5),
        )
        self.sub_text = Label(
            master=self.meter_frame,
            text=self._subtext,
            color=self._subtextstyle,
            variant="metersubtxt",
            font=self._subtextfont,
            textvariable=self.labelvar,
        )

        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)
        self._set_interactive_bind()
        self._draw_base_image()
        self._draw_meter()

        # set widget geometery
        self.indicator.place(x=0, y=0)
        self.meter_frame.pack()
        self._set_show_text()

    def _set_widget_colors(self):
        style_string = (self._color, "meter", "label")
        ttkstyle = Bootstyle.ttkstyle_name(string="-".join(style_string))
        textcolor = self._lookup_style_option(ttkstyle, "foreground")
        background = self._lookup_style_option(ttkstyle, "background")
        trough_color = self._lookup_style_option(ttkstyle, "space")
        self._meter_foreground = textcolor
        self._meter_background = Colors.update_hsv(background, vd=-0.1)
        self._meter_trough = trough_color

    def _set_meter_text(self):
        """Setup and pack the widget labels in the appropriate order"""
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self):
        if self._subtextfont:
            if self._showtext:
                self.sub_text.place(relx=0.5, rely=0.6, anchor="center")
            else:
                self.sub_text.place(relx=0.5, rely=0.5, anchor="center")

    def _set_show_text(self):
        self.textframe.pack_forget()
        self.text_center.pack_forget()
        self.text_left.pack_forget()
        self.text_right.pack_forget()
        self.sub_text.pack_forget()

        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.45, anchor="center")
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor="center")

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()
        self._set_subtext()

    def _set_text_left(self):
        if self._showtext and self._textleft:
            self.text_left.pack(side="left", fill="y")

    def _set_text_center(self):
        if self._showtext:
            self.text_center.pack(side="left", fill="y")

    def _set_text_right(self):
        self.text_right.configure(text=self._textright)
        if self._showtext and self._textright:
            self.text_right.pack(side="right", fill="y")

    def _set_interactive_bind(self):
        seq1 = "<B1-Motion>"
        seq2 = "<Button-1>"

        if self._interactive:
            self._bindids[seq1] = self.indicator.bind(
                seq1, self._on_dial_interact
            )
            self._bindids[seq2] = self.indicator.bind(
                seq2, self._on_dial_interact
            )
            return

        if seq1 in self._bindids:
            self.indicator.unbind(seq1, self._bindids.get(seq1))
            self.indicator.unbind(seq2, self._bindids.get(seq2))
            self._bindids.clear()

    def _set_arc_offset_range(self, metertype, arcoffset, arcrange):
        if metertype == "semi":
            self._arcoffset = 135 if arcoffset is None else arcoffset
            self._arcrange = 270 if arcrange is None else arcrange
        else:
            self._arcoffset = -90 if arcoffset is None else arcoffset
            self._arcrange = 360 if arcrange is None else arcrange
        self._metertype = metertype

    def _draw_meter(self, *_):
        """Draw a meter"""
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._stripethickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)

        self._meter_image = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Resampling.BICUBIC)
        )
        self.indicator.configure(image=self._meter_image)

    def _draw_base_image(self):
        """Draw base image to be used for subsequent updates"""
        self._set_widget_colors()
        self._base_image = Image.new(
            mode="RGBA", size=(self._metersize * M, self._metersize * M)
        )
        draw = ImageDraw.Draw(self._base_image)

        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M
        # striped meter
        if self._stripethickness > 0:
            _from = self._arcoffset
            _to = self._arcrange + self._arcoffset
            _step = 2 if self._stripethickness == 1 else self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._meter_trough,
                    width=width,
                )
        # solid meter
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._arcrange + self._arcoffset,
                fill=self._meter_trough,
                width=width,
            )

    def _draw_solid_meter(self, draw: ImageDraw.Draw):
        """Draw a solid meter"""
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meter_foreground,
                width=width,
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._meter_value(),
                fill=self._meter_foreground,
                width=width,
            )

    def _draw_striped_meter(self, draw: ImageDraw.Draw):
        """Draw a striped meter"""
        meter_value = self._meter_value()
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meter_foreground,
                width=width,
            )
        else:
            _from = self._arcoffset
            _to = meter_value - 1
            _step = self._stripethickness
            for x in range(_from, _to, _step):
                draw.arc(
                    xy=(0, 0, x1, y1),
                    start=x,
                    end=x + self._stripethickness - 1,
                    fill=self._meter_foreground,
                    width=width,
                )

    def _meter_value(self) -> int:
        """Calculate the value to be used to draw the arc length of the
        progress meter."""
        value = int(
            (self["amountused"] / self["amounttotal"]) * self._arcrange
            + self._arcoffset
        )
        return value

    def _on_theme_change(self, *_):
        self._draw_base_image()
        self._draw_meter()

    def _on_dial_interact(self, e: Event):
        """Callback for mouse drag motion on meter indicator"""
        dx = e.x - self._metersize // 2
        dy = e.y - self._metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arcoffset:
            factor = degs - self._arcoffset
        else:
            factor = 360 + degs - self._arcoffset

        # clamp the value between 0 and `amounttotal`
        amounttotal = self.amounttotalvar.get()
        lastused = self.amountusedvar.get()
        amountused = (amounttotal / self._arcrange * factor)

        # calculate amount used given stepsize
        if amountused > self._stepsize // 2:
            amountused = amountused // self._stepsize * self._stepsize + self._stepsize
        else:
            amountused = 0
        # if the number is the name, then do not redraw
        if lastused == amountused:
            return
        # set the amount used variable
        if amountused < 0:
            self.amountusedvar.set(0)
        elif amountused > amounttotal:
            self.amountusedvar.set(amounttotal)
        else:
            self.amountusedvar.set(amountused)

    def _lookup_style_option(self, style: str, option: str):
        """Wrapper around the tcl style lookup command"""
        value = self.tk.call(
            "ttk::style", "lookup", style, "-%s" % option, None, None
        )
        return value

    def _configure_get(self, cnf):
        """Override the configuration get method"""
        if cnf == "arcrange":
            return self._arcrange
        elif cnf == "arcoffset":
            return self._arcoffset
        elif cnf == "amounttotal":
            return self.amounttotalvar.get()
        elif cnf == "amountused":
            return self.amountusedvar.get()
        elif cnf == "interactive":
            return self._interactive
        elif cnf == "subtextfont":
            return self._subtextfont
        elif cnf == "subtextstyle":
            return self._subtextstyle
        elif cnf == "subtext":
            return self._subtext
        elif cnf == "metersize":
            return self._metersize
        elif cnf == "color":
            return self._color
        elif cnf == "metertype":
            return self._metertype
        elif cnf == "meterthickness":
            return self._meterthickness
        elif cnf == "showtext":
            return self._showtext
        elif cnf == "stripethickness":
            return self._stripethickness
        elif cnf == "textleft":
            return self._textleft
        elif cnf == "textright":
            return self._textright
        elif cnf == "textfont":
            return self._textfont
        elif cnf == "wedgesize":
            return self._wedgesize
        elif cnf == "stepsize":
            return self._stepsize
        else:
            return super(Frame, self).configure(cnf)

    def _configure_set(self, **kwargs):
        """Override the configuration set method"""
        meter_text_changed = False

        if "arcrange" in kwargs:
            self._arcrange = kwargs.pop("arcrange")
        if "arcoffset" in kwargs:
            self._arcoffset = kwargs.pop("arcoffset")
        if "amounttotal" in kwargs:
            amounttotal = kwargs.pop("amounttotal")
            self.amounttotalvar.set(amounttotal)
        if "amountused" in kwargs:
            amountused = kwargs.pop("amountused")
            self.amountusedvar.set(amountused)
        if "interactive" in kwargs:
            self._interactive = kwargs.pop("interactive")
            self._set_interactive_bind()
        if "subtextfont" in kwargs:
            self._subtextfont = kwargs.pop("subtextfont")
            self.sub_text.configure(font=self._subtextfont)
            self.text_left.configure(font=self._subtextfont)
            self.text_right.configure(font=self._subtextfont)
        if "subtextstyle" in kwargs:
            self._subtextstyle = kwargs.pop("subtextstyle")
            self.sub_text.configure(color=self._subtextstyle, variant="meter")
        if "metersize" in kwargs:
            self._metersize = scale_size(kwargs.pop("metersize"))
            self.meter_frame.configure(
                height=self._metersize, width=self._metersize
            )
        if "color" in kwargs:
            self._color = kwargs.pop("color")
            self.text_center.configure(color=self._color, variant="meter")
        if "metertype" in kwargs:
            self._metertype = kwargs.pop("metertype")
        if "meterthickness" in kwargs:
            self._meterthickness = kwargs.pop("meterthickness")
        if "stripethickness" in kwargs:
            self._stripethickness = kwargs.pop("stripethickness")
        if "subtext" in kwargs:
            self._subtext = kwargs.pop("subtext")
            self.sub_text.configure(text=self._subtext)
            meter_text_changed = True
        if "textleft" in kwargs:
            self._textleft = kwargs.pop("textleft")
            self.text_left.configure(text=self._textleft)
            meter_text_changed = True
        if "textright" in kwargs:
            self._textright = kwargs.pop("textright")
            meter_text_changed = True
        if "showtext" in kwargs:
            self._showtext = kwargs.pop("showtext")
            meter_text_changed = True
        if "textfont" in kwargs:
            self._textfont = kwargs.pop("textfont")
            self.text_center.configure(font=self._textfont)
        if "wedgesize" in kwargs:
            self._wedgesize = kwargs.pop("wedgesize")
        if "stepsize" in kwargs:
            self._stepsize = kwargs.pop("stepsize")
        if meter_text_changed:
            self._set_meter_text()

        try:
            if self._metertype:
                self._set_arc_offset_range(
                    metertype=self._metertype,
                    arcoffset=self._arcoffset,
                    arcrange=self._arcrange,
                )
        except AttributeError:
            return

        self._draw_base_image()
        self._draw_meter()

        # pass remaining configurations to `ttk.Frame.configure`
        super(Frame, self).configure(**kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(key)

    def __setitem__(self, key: str, value) -> None:
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:
            cnf (Dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs: Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    def step(self, delta=1):
        """Increase the indicator value by `delta`

        The indicator will reverse direction and count down once it
        reaches the maximum value.

        Parameters:

            delta (int):
                The amount to change the indicator.
        """
        amount_used = self.amountusedvar.get()
        amount_total = self.amounttotalvar.get()

        if self._towards_maximum:
            amount_updated = amount_used + delta
        else:
            amount_updated = amount_used - delta

        if amount_updated >= amount_total:
            self._towards_maximum = False
            self.amountusedvar.set(amount_total - (amount_updated - amount_total))
        elif amount_updated < 0:
            self._towards_maximum = True
            self.amountusedvar.set(abs(amount_updated))
        else:
            self.amountusedvar.set(amount_updated)
