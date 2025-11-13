"""Meter widget for ttkbootstrap.

This module provides the Meter widget, a radial progress indicator that can
display progress in various styles (full circle, semi-circle, solid, striped).
The meter can be interactive, allowing users to adjust values with mouse input.

Module Constants:
    M (int): Meter image scale factor (3). Higher values increase resolution
             of the rendered meter image.

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    root = ttk.Window()

    # Create a meter
    meter = ttk.Meter(
        root,
        metersize=200,
        amountused=65,
        amounttotal=100,
        metertype="semi",
        subtext="CPU Usage",
        interactive=True,
        bootstyle="success"
    )
    meter.pack(padx=10, pady=10)

    # Update the value
    meter.configure(amountused=75)

    # Access the value via variable
    print(meter.amountusedvar.get())

    root.mainloop()
    ```
"""
import math
from tkinter import Event, Misc
from typing import Any, Optional, Union

from PIL import Image, ImageDraw, ImageTk
from PIL.Image import Resampling

from ttkbootstrap import Frame, IntVar, Label, StringVar, utility
from ttkbootstrap.constants import CENTER, DEFAULT, FULL, LEFT, RIGHT, S, Y
from ttkbootstrap.style import Bootstyle, Colors

M = 3  # meter image scale, higher number increases resolution


class Meter(Frame):
    """A radial meter that can be used to show progress of long
    running operations or the amount of work completed; can also be
    used as a dial when set to `interactive=True`.

    This widget is very flexible. There are two primary meter types
    which can be set with the `metertype` parameter: 'full' and
    'semi', which shows the arc of the meter in a full or
    semi-circle. You can also customize the arc of the circle with
    the `arcrange` and `arcoffset` parameters.

    The meter indicator can be displayed as a solid color or with
    stripes using the `stripethickness` parameter. By default, the
    `stripethickness` is 0, which results in a solid meter
    indicator. A higher `stripethickness` results in larger wedges
    around the arc of the meter.

    Various text and label options exist. The center text and
    meter indicator is formatted with the `meterstyle` parameter.
    You can set text on the left and right of this center label
    using the `textleft` and `textright` parameters. This is most
    commonly used for '$', '%', or other such symbols.

    If you need access to the variables that update the meter, you
    you can access these via the `amountusedvar`, `amounttotalvar`,
    and the `labelvar`. The value of these properties can also be
    retrieved via the `configure` method.

    ![](../../assets/widgets/meter.gif)

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()

        meter = ttk.Meter(
            metersize=180,
            padding=5,
            amountused=25,
            metertype="semi",
            subtext="miles per hour",
            interactive=True,
        )
        meter.pack()

        # update the amount used directly
        meter.configure(amountused = 50)

        # update the amount used with another widget
        entry = ttk.Entry(textvariable=meter.amountusedvar)
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

    def __init__(
            self,
            master: Optional[Misc] = None,
            bootstyle: str = DEFAULT,
            arcrange: Optional[int] = None,
            arcoffset: Optional[int] = None,
            amountmin: Union[int, float] = 0,
            amounttotal: Union[int, float] = 100,
            amountused: Union[int, float] = 0,
            amountformat: str = "{:.0f}",
            wedgesize: int = 0,
            metersize: int = 200,
            metertype: str = FULL,
            meterthickness: int = 10,
            showtext: bool = True,
            interactive: bool = False,
            stripethickness: int = 0,
            textleft: Optional[str] = None,
            textright: Optional[str] = None,
            textfont: str = "-size 20 -weight bold",
            subtext: Optional[str] = None,
            subtextstyle: str = DEFAULT,
            subtextfont: str = "-size 10",
            stepsize: Union[int, float] = 1,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            master (Widget):
                The parent widget.

            arcrange (int):
                The range of the arc if degrees from start to end.

            arcoffset (int):
                The amount to offset the arc's starting position in degrees.
                0 is at 3 o'clock.

            amountmin (int):
                The minimum value of the meter. Defaults to 0. Can be set
                to a negative value to support negative ranges.

            amounttotal (int):
                The maximum value of the meter.

            amountused (int):
                The current value of the meter; displayed in a center label
                if the `showtext` property is set to True.

            amountformat (str):
                The format used to display the `amountused` value. Default is "{:.0f}"

            wedgesize (int):
                Sets the length of the indicator wedge around the arc. If
                greater than 0, this wedge is set as an indicator centered
                on the current meter value.

            metersize (int):
                The meter is square. This represents the size of one side
                if the square as measured in screen units.

            bootstyle (str):
                Sets the indicator and center text color. One of primary,
                secondary, success, info, warning, danger, light, dark.

            metertype ('full', 'semi'):
                Displays the meter as a full circle or semi-circle.

            meterthickness (int):
                The thickness of the indicator.

            showtext (bool):
                Indicates whether to show the left, center, and right text
                labels on the meter.

            interactive (bool):
                Indicates that the user may adjust the meter value with
                mouse interaction.

            stripethickness (int):
                The indicator can be displayed as a solid band or as
                striped wedges around the arc. If the value is greater than
                0, the indicator changes from a solid to striped, where the
                value is the thickness of the stripes (or wedges).

            textleft (str):
                A short string inserted to the left of the center text.

            textright (str):
                A short string inserted to the right of the center text.

            textfont (Union[str, Font]):
                The font used to render the center text.

            subtext (str):
                Supplemental text that appears below the center text.

            subtextstyle (str):
                The bootstyle color of the subtext. One of primary,
                secondary, success, info, warning, danger, light, dark.
                The default color is Theme specific and is a lighter
                shade based on whether it is a 'light' or 'dark' theme.

            subtextfont (Union[str, Font]):
                The font used to render the subtext.

            stepsize (int):
                Sets the amount by which to change the meter indicator
                when incremented by mouse interaction.

            **kwargs:
                Other keyword arguments that are passed directly to the
                `Frame` widget that contains the meter components.
        """
        super().__init__(master=master, **kwargs)

        # widget variables
        self.amountminvar = IntVar(value=amountmin)
        self.amountusedvar = IntVar(value=amountused)
        self.amountusedvar.trace_add("write", self._update_meter)
        self.amountuseddisplayvar = StringVar(value=amountformat.format(amountused))
        self.amounttotalvar = IntVar(value=amounttotal)
        self.labelvar = StringVar(value=subtext)

        # misc settings
        self._amountformat = amountformat
        self._set_arc_offset_range(metertype, arcoffset, arcrange)
        self._towards_maximum = True
        self._metersize = utility.scale_size(self, metersize)
        self._meterthickness = utility.scale_size(self, meterthickness)
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
        self._bootstyle = bootstyle
        self._interactive = interactive
        self._bindids = {}

        self._setup_widget()

    def _update_meter(self, *_: Any) -> None:
        """Update the meter display when the value changes.

        Redraws the meter and updates the display text according to
        the amountformat string.
        """
        self._draw_meter()
        amount_used = self.amountusedvar.get()
        self.amountuseddisplayvar.set(self._amountformat.format(amount_used))

    def _setup_widget(self) -> None:
        """Initialize and configure all meter components.

        Creates the meter frame, indicator label, text labels, and binds
        event handlers for theme changes and interactivity.
        """
        self.meterframe = Frame(
            master=self, width=self._metersize, height=self._metersize
        )
        self.indicator = Label(self.meterframe)
        self.textframe = Frame(self.meterframe)
        self.textleft = Label(
            master=self.textframe,
            text=self._textleft,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=S,
            padding=(0, 5),
        )
        self.textcenter = Label(
            master=self.textframe,
            textvariable=self.amountuseddisplayvar,
            bootstyle=(self._bootstyle, "meter"),
            font=self._textfont,
        )
        self.textright = Label(
            master=self.textframe,
            text=self._textright,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=S,
            padding=(0, 5),
        )
        self.subtext = Label(
            master=self.meterframe,
            text=self._subtext,
            bootstyle=(self._subtextstyle, "metersubtxt"),
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
        self.meterframe.pack()
        self._set_show_text()

    def _set_widget_colors(self) -> None:
        """Query the theme for meter colors.

        Sets the meter foreground, background, and trough colors based on
        the current theme and bootstyle.
        """
        bootstyle = (self._bootstyle, "meter", "label")
        ttkstyle = Bootstyle.ttkstyle_name(string="-".join(bootstyle))
        textcolor = self._lookup_style_option(ttkstyle, "foreground")
        background = self._lookup_style_option(ttkstyle, "background")
        troughcolor = self._lookup_style_option(ttkstyle, "space")
        self._meterforeground = textcolor
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)
        self._metertrough = troughcolor

    def _set_meter_text(self) -> None:
        """Configure and position all text labels.

        Arranges the text labels (left, center, right, and subtext) according
        to the current configuration.
        """
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self) -> None:
        """Position the subtext label below the center text."""
        if self._subtext:
            if self._showtext:
                self.subtext.place(relx=0.5, rely=0.6, anchor=CENTER)
            else:
                self.subtext.place(relx=0.5, rely=0.5, anchor=CENTER)

    def _set_show_text(self) -> None:
        """Show or hide the text labels based on showtext setting."""
        self.textframe.pack_forget()
        self.textcenter.pack_forget()
        self.textleft.pack_forget()
        self.textright.pack_forget()
        self.subtext.pack_forget()

        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.45, anchor=CENTER)
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor=CENTER)

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()
        self._set_subtext()

    def _set_text_left(self) -> None:
        """Pack the left text label if configured."""
        if self._showtext and self._textleft:
            self.textleft.pack(side=LEFT, fill=Y)

    def _set_text_center(self) -> None:
        """Pack the center text label showing the current value."""
        if self._showtext:
            self.textcenter.pack(side=LEFT, fill=Y)

    def _set_text_right(self) -> None:
        """Pack the right text label if configured."""
        self.textright.configure(text=self._textright)
        if self._showtext and self._textright:
            self.textright.pack(side=RIGHT, fill=Y)

    def _set_interactive_bind(self) -> None:
        """Bind or unbind mouse events for interactive mode."""
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

    def _set_arc_offset_range(
        self, metertype: str, arcoffset: Optional[int], arcrange: Optional[int]
    ) -> None:
        """Configure the arc parameters based on meter type.

        Sets default arc offset and range values for full or semi-circle meters
        if not explicitly provided.
        """
        from ttkbootstrap.constants import SEMI

        if metertype == SEMI:
            self._arcoffset = 135 if arcoffset is None else arcoffset
            self._arcrange = 270 if arcrange is None else arcrange
        else:
            self._arcoffset = -90 if arcoffset is None else arcoffset
            self._arcrange = 360 if arcrange is None else arcrange
        self._metertype = metertype

    def _draw_meter(self, *_: Any) -> None:
        """Draw the meter indicator on the base image.

        Creates a copy of the base image and draws either a solid or striped
        meter indicator based on the current value and stripethickness setting.
        """
        img = self._base_image.copy()
        draw = ImageDraw.Draw(img)
        if self._stripethickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)

        self._meterimage = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Resampling.BICUBIC)
        )
        self.indicator.configure(image=self._meterimage)

    def _draw_base_image(self) -> None:
        """Draw the meter background/trough.

        Creates the base image showing the meter trough (background arc)
        which remains constant while the indicator changes.
        """
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
                    fill=self._metertrough,
                    width=width,
                )
        # solid meter
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._arcrange + self._arcoffset,
                fill=self._metertrough,
                width=width,
            )

    def _draw_solid_meter(self, draw) -> None:
        """Draw a solid meter indicator.

        Draws a continuous arc representing the current value, either as a
        full arc from start to value, or as a wedge centered on the value.
        """
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
                width=width,
            )
        else:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=self._arcoffset,
                end=self._meter_value(),
                fill=self._meterforeground,
                width=width,
            )

    def _draw_striped_meter(self, draw) -> None:
        """Draw a striped meter indicator.

        Draws the meter as a series of discrete wedges/stripes rather than
        a continuous arc.
        """
        meter_value = self._meter_value()
        x1 = y1 = self._metersize * M - 20
        width = self._meterthickness * M

        if self._wedgesize > 0:
            draw.arc(
                xy=(0, 0, x1, y1),
                start=meter_value - self._wedgesize,
                end=meter_value + self._wedgesize,
                fill=self._meterforeground,
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
                    fill=self._meterforeground,
                    width=width,
                )

    def _meter_value(self) -> int:
        """Calculate the arc degree value for drawing.

        Converts the current meter value to degrees along the arc,
        handling negative ranges and normalizing to the configured
        arc offset and range.

        Returns:
            int: The degree value for the meter indicator position.
        """
        amountmin = self["amountmin"]
        amounttotal = self["amounttotal"]
        amountused = self["amountused"]

        # Normalize to 0-1 range to handle negative values
        range_size = amounttotal - amountmin
        if range_size == 0:
            normalized = 0
        else:
            normalized = (amountused - amountmin) / range_size

        value = int(normalized * self._arcrange + self._arcoffset)
        return value

    def _on_theme_change(self, *_: Any) -> None:
        """Handle theme change events.

        Redraws the meter with updated colors from the new theme.
        """
        self._draw_base_image()
        self._draw_meter()

    def _on_dial_interact(self, e: Event) -> None:
        """Handle mouse interaction for changing meter value.

        Calculates the new meter value based on mouse position when the
        meter is in interactive mode. Converts mouse coordinates to degrees
        and updates the value accordingly.

        Parameters:
            e (tk.Event): The mouse event containing position information.
        """
        dx = e.x - self._metersize // 2
        dy = e.y - self._metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arcoffset:
            factor = degs - self._arcoffset
        else:
            factor = 360 + degs - self._arcoffset

        # clamp the value between `amountmin` and `amounttotal`
        amountmin = self.amountminvar.get()
        amounttotal = self.amounttotalvar.get()
        lastused = self.amountusedvar.get()

        # Calculate the value based on the range
        range_size = amounttotal - amountmin
        amountused = (range_size / self._arcrange * factor) + amountmin

        # calculate amount used given stepsize
        if self._stepsize > 0:
            # Round to nearest stepsize
            amountused = round(amountused / self._stepsize) * self._stepsize

        # if the number is the same, then do not redraw
        if lastused == amountused:
            return
        # set the amount used variable
        if amountused < amountmin:
            self.amountusedvar.set(amountmin)
        elif amountused > amounttotal:
            self.amountusedvar.set(amounttotal)
        else:
            self.amountusedvar.set(amountused)

    def _lookup_style_option(self, style: str, option: str) -> Any:
        """Query a ttk style option value.

        Parameters:
            style (str): The ttk style name to query.
            option (str): The option name to retrieve.

        Returns:
            The value of the specified style option.
        """
        value = self.tk.call(
            "ttk::style", "lookup", style, "-%s" % option, None, None
        )
        return value

    def _configure_get(self, cnf: str) -> Any:
        """Get the value of a configuration option.

        Parameters:
            cnf (str): The option name to query.

        Returns:
            The current value of the specified option.
        """
        if cnf == "arcrange":
            return self._arcrange
        elif cnf == "arcoffset":
            return self._arcoffset
        elif cnf == "amountmin":
            return self.amountminvar.get()
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
            return self.labelvar.get()
        elif cnf == "metersize":
            return self._metersize
        elif cnf == "bootstyle":
            return self._bootstyle
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

    def _configure_set(self, **kwargs: Any) -> None:
        """Set widget configuration options.

        Handles all meter-specific configuration options and updates
        the widget display accordingly.

        Parameters:
            **kwargs: Configuration options to set.
        """
        meter_text_changed = False

        if "arcrange" in kwargs:
            self._arcrange = kwargs.pop("arcrange")
        if "arcoffset" in kwargs:
            self._arcoffset = kwargs.pop("arcoffset")
        if "amountmin" in kwargs:
            amountmin = kwargs.pop("amountmin")
            self.amountminvar.set(amountmin)
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
            self.subtext.configure(font=self._subtextfont)
            self.textleft.configure(font=self._subtextfont)
            self.textright.configure(font=self._subtextfont)
        if "subtextstyle" in kwargs:
            self._subtextstyle = kwargs.pop("subtextstyle")
            self.subtext.configure(bootstyle=(self._subtextstyle, "meter"))
        if "metersize" in kwargs:
            self._metersize = utility.scale_size(self, kwargs.pop("metersize"))
            self.meterframe.configure(
                height=self._metersize, width=self._metersize
            )
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.textcenter.configure(bootstyle=(self._bootstyle, "meter"))
        if "metertype" in kwargs:
            self._metertype = kwargs.pop("metertype")
        if "meterthickness" in kwargs:
            self._meterthickness = kwargs.pop("meterthickness")
        if "stripethickness" in kwargs:
            self._stripethickness = kwargs.pop("stripethickness")
        if "subtext" in kwargs:
            self._subtext = kwargs.pop("subtext")
            self.labelvar.set(self._subtext)
            meter_text_changed = True
        if "textleft" in kwargs:
            self._textleft = kwargs.pop("textleft")
            self.textleft.configure(text=self._textleft)
            meter_text_changed = True
        if "textright" in kwargs:
            self._textright = kwargs.pop("textright")
            meter_text_changed = True
        if "showtext" in kwargs:
            self._showtext = kwargs.pop("showtext")
            meter_text_changed = True
        if "textfont" in kwargs:
            self._textfont = kwargs.pop("textfont")
            self.textcenter.configure(font=self._textfont)
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

    def __getitem__(self, key: str) -> Any:
        return self._configure_get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._configure_set(**{key: value})

    def configure(self, cnf: Optional[str] = None, **kwargs: Any) -> Any:
        """Configure the options for this widget.

        Parameters:
            cnf (str, optional):
                Option name to query. If provided without kwargs, returns
                the current value of that option.

            **kwargs: Configuration options to set (arcrange, arcoffset,
                     amountmin, amounttotal, amountused, interactive,
                     subtextfont, subtextstyle, metersize, bootstyle,
                     metertype, meterthickness, stripethickness, subtext,
                     textleft, textright, showtext, textfont, wedgesize,
                     stepsize).
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    def step(self, delta: Union[int, float] = 1) -> None:
        """Increment or decrement the meter value.

        The indicator will bounce back when reaching the minimum or maximum
        values, reversing direction automatically.

        Parameters:
            delta (int, optional): The amount to change the indicator by.
                                  Positive values increase, negative values
                                  decrease. Defaults to 1.
        """
        amount_used = self.amountusedvar.get()
        amount_min = self.amountminvar.get()
        amount_total = self.amounttotalvar.get()

        if self._towards_maximum:
            amount_updated = amount_used + delta
        else:
            amount_updated = amount_used - delta

        if amount_updated >= amount_total:
            self._towards_maximum = False
            self.amountusedvar.set(amount_total - (amount_updated - amount_total))
        elif amount_updated < amount_min:
            self._towards_maximum = True
            self.amountusedvar.set(amount_min + (amount_min - amount_updated))
        else:
            self.amountusedvar.set(amount_updated)
