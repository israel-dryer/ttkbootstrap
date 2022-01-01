import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.ttk import Button, Checkbutton, Combobox
from tkinter.ttk import Entry, Frame, Label
from tkinter.ttk import Labelframe, LabelFrame, Menubutton
from tkinter.ttk import Notebook, OptionMenu, PanedWindow
from tkinter.ttk import Panedwindow, Progressbar, Radiobutton
from tkinter.ttk import Scale, Scrollbar, Separator
from tkinter.ttk import Sizegrip, Spinbox, Treeview
from ttkbootstrap.constants import *
from math import ceil

# date entry imports
from ttkbootstrap.dialogs import Querybox
from datetime import datetime

# floodgauge imports
import math

# meter imports
from PIL import Image, ImageTk, ImageDraw
from ttkbootstrap.style import Colors
from ttkbootstrap import utility
from ttkbootstrap.style import Bootstyle

TTK_WIDGETS = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Labelframe,
    ttk.Label,
    ttk.Menubutton,
    ttk.Notebook,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview,
    ttk.OptionMenu,
)

TK_WIDGETS = (
    tk.Tk,
    tk.Toplevel,
    tk.Button,
    tk.Label,
    tk.Text,
    tk.Frame,
    tk.Checkbutton,
    tk.Radiobutton,
    tk.Entry,
    tk.Scale,
    tk.Listbox,
    tk.Menu,
    tk.Menubutton,
    tk.LabelFrame,
    tk.Canvas,
    tk.OptionMenu,
    tk.Spinbox,
)


class DateEntry(ttk.Frame):
    """A date entry widget combines the `Combobox` and a `Button`
    with a callback attached to the `get_date` function.

    When pressed, a date chooser popup is displayed. The returned
    value is inserted into the combobox.

    The date chooser popup will use the date in the combobox as the
    date of focus if it is in the format specified by the
    `dateformat` parameter. By default, this format is "%Y-%m-%d".

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.

    The starting weekday on the date chooser popup can be changed
    with the `firstweekday` parameter. By default this value is
    `6`, which represents "Sunday".

    The `Entry` and `Button` widgets are accessible from the
    `DateEntry.Entry` and `DateEntry.Button` properties.

    ![](../../assets/widgets/date-entry.png)
    """

    def __init__(
        self,
        master=None,
        dateformat=r"%Y-%m-%d",
        firstweekday=6,
        startdate=None,
        bootstyle="",
        **kwargs,
    ):
        """
        Parameters:

            master (Widget, optional):
                The parent widget.

            dateformat (str, optional):
                The format string used to render the text in the entry
                widget. For more information on acceptable formats, see https://strftime.org/

            firstweekday (int, optional):
                Specifies the first day of the week. 0=Monday, 1=Tuesday,
                etc...

            startdate (datetime, optional):
                The date that is in focus when the widget is displayed. Default is
                current date.

            bootstyle (str, optional):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            **kwargs (Dict[str, Any], optional):
                Other keyword arguments passed to the frame containing the
                entry and date button.
        """
        self._dateformat = dateformat
        self._firstweekday = firstweekday

        self._startdate = startdate or datetime.today()
        self._bootstyle = bootstyle
        super().__init__(master, **kwargs)

        # add visual components
        entry_kwargs = {"bootstyle": self._bootstyle}
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.button = ttk.Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=f"{self._bootstyle}-date",
        )
        self.button.pack(side=tk.LEFT)

        # starting value
        self.entry.insert(tk.END, self._startdate.strftime(self._dateformat))

    def __getitem__(self, key: str):
        return self.configure(cnf=key)

    def __setitem__(self, key: str, value):
        self.configure(cnf=None, **{key: value})

    def _configure_set(self, **kwargs):
        """Override configure method to allow for setting custom
        DateEntry parameters"""

        if "state" in kwargs:
            state = kwargs.pop("state")
            if state in ["readonly", "invalid"]:
                self.entry.configure(state=state)
            elif state == "disabled":
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state
        if "dateformat" in kwargs:
            self._dateformat = kwargs.pop("dateformat")
        if "firstweekday" in kwargs:
            self._firstweekday = kwargs.pop("firstweekday")
        if "startdate" in kwargs:
            self._startdate = kwargs.pop("startdate")
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.entry.configure(bootstyle=self._bootstyle)
            self.button.configure(bootstyle=[self._bootstyle, "date"])
        if "width" in kwargs:
            width = kwargs.pop("width")
            self.entry.configure(width=width)

        super(ttk.Frame, self).configure(**kwargs)

    def _configure_get(self, cnf):
        """Override the configure get method"""
        if cnf == "state":
            entrystate = self.entry.cget("state")
            buttonstate = self.button.cget("state")
            return {"Entry": entrystate, "Button": buttonstate}
        if cnf == "dateformat":
            return self._dateformat
        if cnf == "firstweekday":
            return self._firstweekday
        if cnf == "startdate":
            return self._startdate
        if cnf == "bootstyle":
            return self._bootstyle
        else:
            return super(ttk.Frame, self).configure(cnf=cnf)

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:

            cnf (Dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            return self._configure_set(**kwargs)

    def _on_date_ask(self):
        """Callback for pushing the date button"""
        _val = self.entry.get()
        try:
            self._startdate = datetime.strptime(_val, self._dateformat)
        except Exception as e:
            print("Date entry text does not match", self._dateformat)
            self._startdate = datetime.today()
            self.entry.delete(first=0, last=tk.END)
            self.entry.insert(
                tk.END, self._startdate.strftime(self._dateformat)
            )

        old_date = datetime.strptime(_val or self._startdate, self._dateformat)

        # get the new date and insert into the entry
        new_date = Querybox.get_date(
            parent=self.entry,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.entry.delete(first=0, last=tk.END)
        self.entry.insert(tk.END, new_date.strftime(self._dateformat))
        self.entry.focus_force()


class Floodgauge(Progressbar):
    """A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `ttk.Progressbar`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.

    Variable are generated automatically for this widget and can be
    linked to other widgets by referencing them via the
    `textvariable` and `variable` attributes.

    ![](../../assets/widgets/floodgauge.gif)
    """

    def __init__(
        self,
        master=None,
        cursor=None,
        font=None,
        length=None,
        maximum=100,
        mode=DETERMINATE,
        orient=HORIZONTAL,
        bootstyle=PRIMARY,
        takefocus=False,
        text=None,
        value=0,
        mask=None,
        **kwargs,
    ):
        """
        Parameters:

            master (Widget, optional):
                Parent widget. Defaults to None.

            cursor (str, optional):
                The cursor that will appear when the mouse is over the
                progress bar. Defaults to None.

            font (Union[Font, str], optional):
                The font to use for the progress bar label.

            length (int, optional):
                Specifies the length of the long axis of the progress bar
                (width if orient = horizontal, height if if vertical);

            maximum (float, optional):
                A floating point number specifying the maximum `value`.
                Defaults to 100.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Floodgauge.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

            orient ('horizontal', 'vertical'):
                Specifies the orientation of the widget.

            bootstyle (str, optional):
                The style used to render the widget. Options include
                primary, secondary, success, info, warning, danger, light,
                dark.

            takefocus (bool, optional):
                This widget is not included in focus traversal by default.
                To add the widget to focus traversal, use
                `takefocus=True`.

            text (str, optional):
                A string of text to be displayed in the Floodgauge label.
                This is assigned to the attribute `Floodgauge.textvariable`

            value (float, optional):
                The current value of the progressbar. In `determinate`
                mode, this represents the amount of work completed. In
                `indeterminate` mode, it is interpreted modulo `maximum`;
                that is, the progress bar completes one "cycle" when the
                `value` increases by `maximum`.

            mask (str, optional):
                A string format that can be used to update the Floodgauge
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Floodgauge label. If a
                mask is set, then the `text` option is ignored.

            **kwargs:
                Other configuration options from the option database.
        """
        # progress bar value variable
        self.variable = tk.IntVar(value=value)
        self.textvariable = tk.StringVar(value=text)
        self._bootstyle = bootstyle
        self._font = font or "helvetica 10"
        self._mask = mask
        self._traceid = None

        super().__init__(
            master=master,
            class_="Floodgauge",
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            bootstyle=bootstyle,
            takefocus=takefocus,
            variable=self.variable,
            **kwargs,
        )
        self._set_widget_text(self.textvariable.get())
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        if self._mask is not None:
            self._set_mask()

    def _set_widget_text(self, *_):
        ttkstyle = self.cget("style")
        if self._mask is None:
            text = self.textvariable.get()
        else:
            value = self.variable.get()
            text = self._mask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._font)

    def _set_mask(self):
        if self._traceid is None:
            self._traceid = self.variable.trace_add(
                "write", self._set_widget_text
            )

    def _unset_mask(self):
        if self._traceid is not None:
            self.variable.trace_remove("write", self._traceid)
        self._traceid = None

    def _on_theme_change(self, *_):
        text = self.textvariable.get()
        self._set_widget_text(text)

    def _configure_get(self, cnf):
        if cnf == "value":
            return self.variable.get()
        if cnf == "text":
            return self.textvariable.get()
        if cnf == "bootstyle":
            return self._bootstyle
        if cnf == "mask":
            return self._mask
        if cnf == "font":
            return self._font
        else:
            return super(Progressbar, self).configure(cnf=cnf)

    def _configure_set(self, **kwargs):
        if "value" in kwargs:
            self.variable.set(kwargs.pop("value"))
        if "text" in kwargs:
            self.textvariable.set(kwargs.pop("text"))
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.get("bootstyle")
        if "mask" in kwargs:
            self._mask = kwargs.pop("mask")
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        else:
            super(Progressbar, self).configure(cnf=None, **kwargs)

    def __getitem__(self, key: str):
        return self._configure_get(cnf=key)

    def __setitem__(self, key: str, value):
        self._configure_set(**{key: value})

    def configure(self, cnf=None, **kwargs):
        """Configure the options for this widget.

        Parameters:

            cnf (Dict[str, Any], optional):
                A dictionary of configuration options.

            **kwargs:
                Optional keyword arguments.
        """
        if cnf is not None:
            return self._configure_get(cnf)
        else:
            self._configure_set(**kwargs)


class Meter(ttk.Frame):
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
    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        arcrange=None,
        arcoffset=None,
        amounttotal=100,
        amountused=0,
        wedgesize=0,
        metersize=200,
        metertype=FULL,
        meterthickness=10,
        showtext=True,
        interactive=False,
        stripethickness=0,
        textleft=None,
        textright=None,
        textfont="-size 20 -weight bold",
        subtext=None,
        subtextstyle=DEFAULT,
        subtextfont="-size 10",
        **kwargs,
    ):
        """
        Parameters:

            master (Widget):
                The parent widget.

            arcrange (int):
                The range of the arc if degrees from start to end.

            arcoffset (int):
                The amount to offset the arc's starting position in degrees.
                0 is at 3 o'clock.

            amounttotal (int):
                The maximum value of the meter.

            amountused (int):
                The current value of the meter; displayed in a center label
                if the `showtext` property is set to True.

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

            **kwargs:
                Other keyword arguments that are passed directly to the
                `Frame` widget that contains the meter components.
        """
        super().__init__(master=master, **kwargs)

        # widget variables
        self.amountusedvar = tk.IntVar(value=amountused)
        self.amountusedvar.trace_add("write", self._draw_meter)
        self.amounttotalvar = tk.IntVar(value=amounttotal)
        self.labelvar = tk.StringVar(value=subtext)

        # misc settings
        self._set_arc_offset_range(metertype, arcoffset, arcrange)
        self._towardsmaximum = True
        self._metersize = utility.scale_size(self, metersize)
        self._meterthickness = utility.scale_size(self, meterthickness)
        self._stripethickness = stripethickness
        self._showtext = showtext
        self._wedgesize = wedgesize

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

    def _setup_widget(self):
        self.meterframe = ttk.Frame(
            master=self, width=self._metersize, height=self._metersize
        )
        self.indicator = ttk.Label(self.meterframe)
        self.textframe = ttk.Frame(self.meterframe)
        self.textleft = ttk.Label(
            master=self.textframe,
            text=self._textleft,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=tk.S,
            padding=(0, 5),
        )
        self.textcenter = ttk.Label(
            master=self.textframe,
            textvariable=self.amountusedvar,
            bootstyle=(self._bootstyle, "meter"),
            font=self._textfont,
        )
        self.textright = ttk.Label(
            master=self.textframe,
            text=self._textright,
            font=self._subtextfont,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            anchor=tk.S,
            padding=(0, 5),
        )
        self.subtext = ttk.Label(
            master=self.meterframe,
            text=self._subtext,
            bootstyle=(self._subtextstyle, "metersubtxt"),
            font=self._subtextfont,
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

    def _set_widget_colors(self):
        bootstyle = (self._bootstyle, "meter", "label")
        ttkstyle = Bootstyle.ttkstyle_name(string="-".join(bootstyle))
        textcolor = self._lookup_style_option(ttkstyle, "foreground")
        background = self._lookup_style_option(ttkstyle, "background")
        troughcolor = self._lookup_style_option(ttkstyle, "space")
        self._meterforeground = textcolor
        self._meterbackground = Colors.update_hsv(background, vd=-0.1)
        self._metertrough = troughcolor

    def _set_meter_text(self):
        """Setup and pack the widget labels in the appropriate order"""
        self._set_show_text()
        self._set_subtext()

    def _set_subtext(self):
        if self._subtextfont:
            if self._showtext:
                self.subtext.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
            else:
                self.subtext.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _set_show_text(self):
        self.textframe.pack_forget()
        self.textcenter.pack_forget()
        self.textleft.pack_forget()
        self.textright.pack_forget()
        self.subtext.pack_forget()

        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._set_text_left()
        self._set_text_center()
        self._set_text_right()
        self._set_subtext()

    def _set_text_left(self):
        if self._showtext and self._textleft:
            self.textleft.pack(side=tk.LEFT, fill=tk.Y)

    def _set_text_center(self):
        if self._showtext:
            self.textcenter.pack(side=tk.LEFT, fill=tk.Y)

    def _set_text_right(self):
        self.textright.configure(text=self._textright)
        if self._showtext and self._textright:
            self.textright.pack(side=tk.RIGHT, fill=tk.Y)

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
        if metertype == SEMI:
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

        self._meterimage = ImageTk.PhotoImage(
            img.resize((self._metersize, self._metersize), Image.CUBIC)
        )
        self.indicator.configure(image=self._meterimage)

    def _draw_base_image(self):
        """Draw base image to be used for subsequent updates"""
        self._set_widget_colors()
        self._base_image = Image.new(
            mode="RGBA", size=(self._metersize * 5, self._metersize * 5)
        )
        draw = ImageDraw.Draw(self._base_image)

        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5
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

    def _draw_solid_meter(self, draw: ImageDraw.Draw):
        """Draw a solid meter"""
        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5

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

    def _draw_striped_meter(self, draw: ImageDraw.Draw):
        """Draw a striped meter"""
        meter_value = self._meter_value()
        x1 = y1 = self._metersize * 5 - 20
        width = self._meterthickness * 5

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

    def _on_dial_interact(self, e: tk.Event):
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
        amountused = int(amounttotal / self._arcrange * factor)
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
        else:
            return super(ttk.Frame, self).configure(cnf)

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
            self.subtext.configure(font=self._subtextfont)
            self.textleft.configure(font=self._subtextfont)
            self.textright.configure(font=self._subtextfont)
        if "subtextstyle" in kwargs:
            self._subtextstyle = kwargs.pop("subtextstyle")
            self.subtext.configure(bootstyle=[self._subtextstyle, "meter"])
        if "metersize" in kwargs:
            self._metersize = utility.scale_size(kwargs.pop("metersize"))
            self.meterframe.configure(
                height=self._metersize, width=self._metersize
            )
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self.textcenter.configure(bootstyle=[self._bootstyle, "meter"])
        if "metertype" in kwargs:
            self._metertype = kwargs.pop("metertype")
        if "meterthickness" in kwargs:
            self._meterthickness = self.scale_size(
                kwargs.pop("meterthickness")
            )
        if "stripethickness" in kwargs:
            self._stripethickness = kwargs.pop("stripethickness")
        if "subtext" in kwargs:
            self._subtext = kwargs.pop("subtext")
            self.subtext.configure(text=self._subtext)
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
        super(ttk.Frame, self).configure(**kwargs)

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
            self._configure_set(**kwargs)

    def step(self, delta=1):
        """Increase the indicator value by `delta`

        The indicator will reverse direction and count down once it
        reaches the maximum value.

        Parameters:

            delta (int):
                The amount to change the indicator.
        """
        amountused = self.amountusedvar.get()
        amounttotal = self.amounttotalvar.get()
        if amountused >= amounttotal:
            self._towardsmaximum = True
            self.amountusedvar.set(amountused - delta)
        elif amountused <= 0:
            self._towardsmaximum = False
            self.amountusedvar.set(amountused + delta)
        elif self._towardsmaximum:
            self.amountusedvar.set(amountused - delta)
        else:
            self.amountusedvar.set(amountused + delta)


UPARROW = "⯅"
DOWNARROW = "⯆"
ASCENDING = 0
DESCENDING = 1


class Tableview(ttk.Frame):
    """A class for arranging data in rows and columns. A Tableview
    object contains various features such has striped rows, pagination,
    and autosized and autoaligned columns.

    The pagination option is recommended when loading a lot of data as
    the table records are inserted on-demand. Table records are only
    created when requested to be in a page view. This allows the table
    to be loaded very quickly even with hundreds of thousands of
    records.

    All table columns are sortable. Clicking a column header will toggle
    between sorting "ascending" and "descending".

    Columns are configurable by passing a simple list of header names or
    by passing in a dictionary of column names with settings. You can
    use both as well, as in the example below, where a column header
    name is use for one column, and a dictionary of settings is used
    for another.

    The object has a right-click menu on the header and the cells that
    allow you to configure various settings.

    ![](../../assets/widgets/tableview.gif)

    Examples:

        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()
        colors = app.style.colors

        coldata = [
            {"text": "LicenseNumber", "stretch": False},
            "CompanyName",
            {"text": "UserCount", "stretch": False},
        ]

        rowdata = [
            ('A123', 'IzzyCo', 12),
            ('A136', 'Kimdee Inc.', 45),
            ('A158', 'Farmadding Co.', 36)
        ]

        dt = ttk.Tableview(
            master=app,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(colors.light, None),
        )
        dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        app.mainloop()
        ```
    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        coldata=[],
        rowdata=[],
        paginated=False,
        searchable=False,
        autosize=True,
        autoalign=True,
        stripecolor=None,
        pagesize=15,
        height=10,
    ):
        """
        Parameters:

            master (Widget):
                The parent widget.

            bootstyle (str):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            coldata (List[str | Dict]):
                An iterable containing either the heading name or a
                dictionary of column settings. Configurable settings
                include >> text, image, command, anchor, width, minwidth,
                maxwidth, stretch

            rowdata (List):
                An iterable of row data. The lenth of each row of data
                must match the number of columns.

            paginated (bool):
                Specifies that the data is to be paginated. A pagination
                frame will be created below the table with controls that
                enable the user to page forward and backwards in the
                data set.

            pagesize (int):
                When `paginated=True`, this specifies the number of rows
                to show per page. This is the same as setting `height`
                for non-paginated tables.

            searchable (bool):
                If `True`, a searchbar will be created above the table.
                Press the <Return> key to initiate a search. Searching
                with an empty string will reset the search criteria, or
                pressing the reset button to the right of the search
                bar. Currently, the search method looks for any row
                that contains the search text. The filtered results
                are displayed in the table view.

            autosize (bool):
                If `True`, the table columns will be automatically sized
                based on the records presently in the viewport. You
                may also initiate an adhoc autosize by double-clicking
                the separator between each column header.

            autoalign (bool):
                If `True`, the column headers and data are automatically
                aligned. Numbers and number headers are right-aligned
                and all other data types are left-aligned. The auto
                align method evaluates the first record in each column
                to determine the data type for alignment.

            stripecolor (Tuple[str, str]):
                If provided, even numbered rows will be color using the
                (background, foreground) specified. You may specify one
                or the other by passing in **None**. For example,
                `stripecolor=('green', None)` will set the stripe
                background as green, but the foreground will remain as
                default. You may use standand color names, hexadecimal
                color codes, or bootstyle color keywords. For example,
                ('light', '#222') will set the background to the "light"
                themed ttkbootstrap color and the foreground to the
                specified hexadecimal color.

            height (int):
                Specifies how many rows will appear in the table's viewport.
                If the number of records extends beyond the table height,
                the user may use the mousewheel or scrollbar to navigate
                the data.
        """
        super().__init__(master)
        self.tablecols = []
        self.tablerows = []
        self.tablerows_filtered = []
        self.viewdata = []
        self.rowindex = tk.IntVar(value=0)
        self.pageindex = tk.IntVar(value=1)
        self.pagelimit = tk.IntVar(value=0)
        self.height = height
        self.pagesize = pagesize
        self.paginated = paginated
        self.searchable = searchable
        self.stripecolor = stripecolor
        self.autosize = autosize
        self.autoalign = autoalign
        self.filtered = False
        self.criteria = tk.StringVar()
        self.rightclickmenu_cell = None

        if not paginated:
            self.pagesize = len(rowdata)
        else:
            self.height = self.pagesize

        self._build_table(coldata, rowdata, bootstyle)

    # DATA LOADING

    def unload_table_data(self):
        """Unload all data from the table"""
        for row in self.viewdata:
            row.hide()
        self.viewdata.clear()

    def load_table_data(self):
        """Load all data into the table"""
        self.unload_table_data()
        page_start = self.rowindex.get()
        page_end = self.rowindex.get() + self.pagesize

        if self.filtered:
            rowdata = self.tablerows_filtered[page_start:page_end]
            rowcount = len(self.tablerows_filtered)
        else:
            rowdata = self.tablerows[page_start:page_end]
            rowcount = len(self.tablerows)

        self.pagelimit.set(ceil(rowcount / self.pagesize))

        pageindex = ceil(page_end / self.pagesize)
        pagelimit = self.pagelimit.get()
        self.pageindex.set(min([pagelimit, pageindex]))

        for i, row in enumerate(rowdata):
            if self.stripecolor is not None and i % 2 == 0:
                row.show(True)
            else:
                row.show(False)
            self.viewdata.append(row)

    def _get_event_objects(self, event):
        iid = self.tableview.identify_row(event.y)
        item = self.tableview.item(iid)
        col = self.tableview.identify_column(event.x)
        cid = int(self.tableview.column(col, "id"))
        values = item.get("values")
        data = {
            'iid': iid,
            'cid': cid,
            'col': col,
            'item': item,
            'values': values,
        }
        if values:
            data['value'] = values[cid]
        return data

    # WIDGET BUILDERS

    def _build_table(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self.searchable:
            self._build_search_frame()

        self.tableview = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self.height,
            selectmode=EXTENDED,
            show=HEADINGS,
            bootstyle=f"{bootstyle}-table",
        )
        self.tableview.pack(fill=BOTH, expand=YES, side=TOP)

        self._build_table_columns(coldata)
        self._build_table_rows(rowdata)
        # self.build_horizontal_scrollbar()

        self.load_table_data()

        if self.autosize:
            self.autosize_columns()

        if self.autoalign:
            self.autoalign_columns()

        if self.paginated:
            self._build_pagination_frame()

        if self.stripecolor is not None:
            self.configure_table_stripes(self.stripecolor)

        self.rightclickmenu_cell = TableCellRightClickMenu(self)
        self.rightclickmenu_head = TableHeaderRightClickMenu(self)
        self._set_widget_binding()

    def _build_search_frame(self):
        """Build the search frame containing the search widgets. This
        frame is only created if `searchable=True` when creating the
        widget.
        """
        frame = ttk.Frame(self, padding=5)
        frame.pack(fill=X, side=TOP)
        ttk.Label(frame, text="Search").pack(side=LEFT, padx=5)
        searchterm = ttk.Entry(frame, textvariable=self.criteria)
        searchterm.pack(fill=X, side=LEFT, expand=YES)
        searchterm.bind("<Return>", self._search_table_data)
        searchterm.bind("<KP_Enter>", self._search_table_data)
        ttk.Button(
            frame,
            text="⎌",
            command=self.clear_table_filters,
            style="symbol.Link.TButton",
        ).pack(side=LEFT)

    def _build_pagination_frame(self):
        """Build the frame containing the pagination widgets. This
        frame is only built if `pagination=True` when creating the
        widget.
        """
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, anchor=N)

        ttk.Button(
            master=pageframe,
            text="»",
            command=self.goto_last_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="›",
            command=self.goto_next_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)
        lbl = ttk.Label(pageframe, textvariable=self.pagelimit)
        lbl.pack(side=RIGHT, padx=(0, 5))
        ttk.Label(pageframe, text="of").pack(side=RIGHT, padx=(5, 0))

        index = ttk.Entry(pageframe, textvariable=self.pageindex, width=6)
        index.pack(side=RIGHT)
        index.bind("<Return>", self.goto_page, "+")
        index.bind("<KP_Enter>", self.goto_page, "+")

        ttk.Label(pageframe, text="Page").pack(side=RIGHT, padx=5)
        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)

        ttk.Button(
            master=pageframe,
            text="‹",
            command=self.goto_prev_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="«",
            command=self.goto_first_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

    def _build_table_rows(self, rowdata):
        """Build, load, and configure the DataTableRow objects

        Parameters:

            rowdata (List):
                An iterable of row data
        """
        for row in rowdata:
            self.tablerows.append(TableRow(self.tableview, row))

    def _build_table_columns(self, coldata):
        """Build, load, and configure the DataTableColumn objects

        Parameters:

            coldata (List[str|Dict[str, Any]]):
                An iterable of column names or a dictionary of column
                configuration settings.
        """
        for cid, col in enumerate(coldata):
            if isinstance(col, str):
                self.tablecols.append(
                    TableColumn(
                        table=self.tableview,
                        cid=cid,
                        text=col,
                    )
                )
            else:
                if "text" not in col:
                    col["text"] = f"Column {cid}"
                self.tablecols.append(
                    TableColumn(
                        table=self.tableview,
                        cid=cid,
                        **col,
                    )
                )

    # PAGE NAVIGATION

    def goto_first_page(self):
        """Update table with first page of data"""
        self.rowindex.set(0)
        self.load_table_data()

    def goto_last_page(self):
        """Update table with the last page of data"""
        self.rowindex.set(self.pagesize * (self.pagelimit.get() - 1))
        self.load_table_data()

    def goto_next_page(self):
        """Update table with next page of data"""
        if self.pageindex.get() >= self.pagelimit.get():
            return
        rowindex = self.rowindex.get()
        self.rowindex.set(rowindex + self.pagesize)
        self.load_table_data()

    def goto_prev_page(self):
        """Update table with prev page of data"""
        if self.pageindex.get() <= 1:
            return
        rowindex = self.rowindex.get()
        self.rowindex.set(rowindex - self.pagesize)
        self.load_table_data()

    def goto_page(self, *_):
        """Go to a specific page indicated by the page entry widget."""
        pageindex = self.pageindex.get() - 1
        self.rowindex.set(pageindex * self.pagesize)
        self.load_table_data()

    # COLUMN SORTING

    def sort_column_data(self, event=None, cid=None, sort=None):
        """Sort the table rows by the specified column. This method 
        may be trigged by an event or manually.
        
        Parameters:

            event (Event):
                A window event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column relative to the original data set.

            sort (int):
                Determines the sort direction. 0 = ASCENDING. 1 = DESCENDING.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get('cid')
        elif cid is None:
            return

        # update table data
        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        if sort is not None:
            colsort = sort
        else:
            colsort = self.tablecols[cid].sort

        if colsort == ASCENDING:
            self.tablecols[cid].sort = DESCENDING
        else:
            self.tablecols[cid].sort = ASCENDING

        sortedrows = sorted(
            tablerows, reverse=colsort, key=lambda x: x.values[cid]
        )
        if self.filtered:
            self.tablerows_filtered = sortedrows
        else:
            self.tablerows = sortedrows

        # update headers
        self._column_sort_header_reset()
        self._column_sort_header_update(cid)

        self.unload_table_data()
        self.load_table_data()

    def _column_sort_header_reset(self):
        """Remove the sort character from the column headers"""
        for col in self.tablecols:
            self.tableview.heading(col.cid, text=col.headertext)

    def _column_sort_header_update(self, cid):
        """Add sort character to the sorted column"""
        col = self.tablecols[cid]
        arrow = UPARROW if col.sort == ASCENDING else DOWNARROW
        headertext = f"{col.headertext} {arrow}"
        self.tableview.heading(col.cid, text=headertext)

    # DATA SEARCH & FILTERING

    def clear_table_filters(self):
        """Remove all filters from table data and reset the filtered 
        flag.
        """
        self.filtered = False
        self.criteria.set("")
        self.unload_table_data()
        self.load_table_data()

    def filter_column_to_value(self, event=None, cid=None, value=None):
        """Hide all records except for records where the current
        column exactly matches the provided value. This method may 
        be triggered by a window event or by specifying the column id.
        
        Parameters:

            event (Event):
                A window event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.

            value (Any):
                The criteria used to filter the column.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get('cid')
            value = eo.get('value') or value
        elif cid is None:
            return
        self.filtered = True
        self.tablerows_filtered.clear()
        self.unload_table_data()
        data = self.tablerows
        for row in data:
            if row.values[cid] == value:
                self.tablerows_filtered.append(row)
        self.rowindex.set(0)
        self.load_table_data()

    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows"""
        criteria = self.tableview.selection()
        if len(criteria) == 0:
            return # nothing is selected

        if self.filtered:
            for row in self.viewdata:
                if row.iid not in criteria:
                    row.hide()
                    self.tablerows_filtered.remove(row)
        else:
            self.filtered = True
            self.tablerows_filtered.clear()
            for row in self.viewdata:
                if row.iid in criteria:
                    self.tablerows_filtered.append(row)
        self.rowindex.set(0)
        self.load_table_data()

    def hide_selected_rows(self):
        """Hide the currently selected rows"""
        selected = self.tableview.selection()
        self.tableview.detach(*selected)
        tablerows = [row for row in self.viewdata if row.iid in selected]

        if not self.filtered:
            self.filtered = True
            self.tablerows_filtered = self.tablerows

        for row in tablerows:
            if self.filtered:
                self.tablerows_filtered.remove(row)

        self.load_table_data()

    def hide_selected_column(self, event=None, cid=None):
        """Detach the selected column from the tableview. This method
        may be triggered by a window event or by specifying the column
        id.
        
        Parameters:

            event (Event):
                A window event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get('cid')
        elif cid is None:
            return
        displaycols = list(self.tableview.configure("displaycolumns"))
        cols = list(self.tableview.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        displaycols.remove(str(cid))
        self.tableview.configure(displaycolumns=displaycols)

    def show_selected_column(self, event=None, cid=None):
        """Attach the selected column to the tableview. This method
        may be triggered by a window event or by specifying the column
        id. The column is reinserted at the index in the original data
        set.
        
        Parameters:

            event (Event):
                A window event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get('cid')
        elif cid is None:
            return
        displaycols = list(self.tableview.configure("displaycolumns"))
        if "#all" in displaycols:
            return
        if str(cid) in displaycols:
            return
        columns = list(self.tableview.configure("columns"))        
        index = columns.index(str(cid))
        displaycols.insert(index, str(cid))
        self.tableview.configure(displaycolumns=displaycols)

    def _search_table_data(self, _):
        """Search the table data for records that meet search criteria.
        Currently, this search locates any records that contain the
        specified text; it is also case insensitive.
        """
        criteria = self.criteria.get()
        self.filtered = True
        self.tablerows_filtered.clear()
        self.unload_table_data()
        data = self.tablerows
        for row in data:
            for col in row.values:
                if str(criteria).lower() in str(col).lower():
                    self.tablerows_filtered.append(row)
                    break
        self.rowindex.set(0)
        self.load_table_data()

    # DATA EXPORT

    def export_all_records(self):
        """Export all records to a csv file"""
        headers = [col.headertext for col in self.tablecols]
        records = [row.values for row in self.tablerows]
        self.save_data_to_csv(headers, records)

    def export_current_page(self):
        """Export records on current page to csv file"""
        headers = [col.headertext for col in self.tablecols]
        records = [row.values for row in self.viewdata]
        self.save_data_to_csv(headers, records)

    def export_current_selection(self):
        """Export rows currently selected to csv file"""
        headers = [col.headertext for col in self.tablecols]
        selected = self.tableview.selection()
        records = []
        for iid in selected:
            records.append(self.tableview.item(iid)["values"])
        self.save_data_to_csv(headers, records)

    def export_records_in_filter(self):
        """Export rows currently filtered to csv file"""
        headers = [col.headertext for col in self.tablecols]
        if not self.filtered:
            return
        records = [row.values for row in self.tablerows_filtered]
        self.save_data_to_csv(headers, records)

    def save_data_to_csv(self, headers, records):
        """Save data records to a csv file.

        Parameters:

            headers (List[str]):
                A list of header labels.

            records (List[Tuple[...]]):
                A list of table records.
        """
        from tkinter.filedialog import asksaveasfilename
        import csv

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        initialfile = f"tabledata_{timestamp}.csv"
        filetypes = [
            ("CSV UTF-8 (Comma delimited)", "*.csv"),
            ("All file types", "*.*"),
        ]
        filename = asksaveasfilename(
            confirmoverwrite=True,
            filetypes=filetypes,
            defaultextension="csv",
            initialfile=initialfile,
        )
        if filename:
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(records)

    # ROW MOVEMENT

    def move_selected_rows_to_top(self):
        """Move the selected rows to the top of the data set"""
        selected = self.tableview.selection()
        if len(selected) == 0:
            return

        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        row_items = []       
        
        for iid in selected:
            for row in tablerows:
                if row.iid == iid:
                    row_items.append(row)
                    break

        for i, item in enumerate(row_items):
            tablerows.remove(item)
            tablerows.insert(i, item)

        if self.filtered:
            self.tablerows_filtered = tablerows
        else:
            self.tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_selected_rows_to_bottom(self):
        """Move the selected rows to the bottom of the dataset"""
        selected = self.tableview.selection()
        if len(selected) == 0:
            return

        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        row_items = []       
        
        for iid in selected:
            for row in tablerows:
                if row.iid == iid:
                    row_items.append(row)
                    break

        for item in row_items:
            tablerows.remove(item)
            tablerows.append(item)

        if self.filtered:
            self.tablerows_filtered = tablerows
        else:
            self.tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_selected_row_up(self):
        """Move the selected rows up one position in the dataset"""
        selected = self.tableview.selection()
        if len(selected) == 0:
            return

        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        row_items = []       
        
        for iid in selected:
            for i, row in enumerate(tablerows):
                if row.iid == iid:
                    row_items.append([i, row])
                    break

        for index, item in row_items:
            tablerows.remove(item)
            tablerows.insert(index-1, item)

        if self.filtered:
            self.tablerows_filtered = tablerows
        else:
            self.tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_row_down(self):
        """Move the selected rows down one position in the dataset"""
        selected = self.tableview.selection()
        if len(selected) == 0:
            return

        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        row_items = []       
        
        for iid in selected:
            for i, row in enumerate(tablerows):
                if row.iid == iid:
                    row_items.append([i, row])
                    break

        for index, item in reversed(row_items):
            tablerows.remove(item)
            tablerows.insert(index+1, item)

        if self.filtered:
            self.tablerows_filtered = tablerows
        else:
            self.tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    # COLUMN MOVEMENT

    def move_column_left(self, event):
        """Move column one position to the left
        
        Parameters:
        
            event (Event):
                A window event.
        """
        eo = self._get_event_objects(event)
        cid = str(eo.get('cid'))
        displaycols = list(self.tableview.configure("displaycolumns"))
        cols = list(self.tableview.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == 0:
            return
        new_index = old_index - 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.tableview.configure(displaycolumns=displaycols)

    def move_column_right(self, event):
        """Move column one position to the right
        
        Parameters:
        
            event (Event):
                A window event.
        """
        eo = self._get_event_objects(event)
        cid = str(eo.get('cid'))
        displaycols = list(self.tableview.configure("displaycolumns"))
        cols = list(self.tableview.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == len(cols) - 1:
            return
        new_index = old_index + 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.tableview.configure(displaycolumns=displaycols)

    def move_column_to_first(self, event):
        """Move column to leftmost position
        
        Parameters:
        
            event (Event):
                A window event.
        """
        eo = self._get_event_objects(event)
        cid = str(eo.get('cid'))
        displaycols = list(self.tableview.configure("displaycolumns"))
        cols = list(self.tableview.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == 0:
            return
        displaycols.insert(0, displaycols.pop(old_index))
        self.tableview.configure(displaycolumns=displaycols)

    def move_column_to_last(self, event):
        """Move column to the rightmost position
        
        Parameters:
        
            event (Event):
                A window event.
        """
        eo = self._get_event_objects(event)
        cid = str(eo.get('cid'))
        displaycols = list(self.tableview.configure("displaycolumns"))
        cols = list(self.tableview.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == len(cols) - 1:
            return
        new_index = len(cols) - 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.tableview.configure(displaycolumns=displaycols)    

    # OTHER FORMATTING

    def configure_table_stripes(self, stripecolor):
        """Add stripes to even-numbered table rows as indicated by the
        `stripecolor` of (background, foreground). Either element may be
        specified as `None`, but both elements must be present.
        
        Parameters:

            stripecolor (Tuple[str, str]):
                A tuple of colors to apply to the table stripe. The
                tuple represents (background, foreground).
        """
        if len(stripecolor) == 2:
            self.stripecolor = stripecolor
            bg, fg = stripecolor
            kw = {}
            if bg is not None:
                kw["background"] = bg
            if fg is not None:
                kw["foreground"] = fg
            self.tableview.tag_configure("striped", **kw)

    def autosize_columns(self):
        """Fit the column to the data in the current view, bounded by the
        maxsize and minsize"""
        f = font.Font()
        column_widths = []

        for i, row in enumerate(self.viewdata):
            if i == 0:
                for col in self.tablecols:
                    column_widths.append(
                        f.measure(f"{col.headertext} {DOWNARROW}")
                    )

            for j, value in enumerate(row.values):
                measure = f.measure(str(value) + " ")
                if column_widths[j] > measure:
                    pass
                elif measure < self.tablecols[j].colmaxwidth:
                    column_widths[j] = measure

        for i, width in enumerate(column_widths):
            self.tableview.column(i, width=width)

    # COLUMN AND HEADER ALIGNMENT

    def autoalign_columns(self):
        """Align the columns and headers based on the data type of the
        values. Text is left-aligned; numbers are right-aligned."""
        values = self.tablerows[0].values
        for i, value in enumerate(values):
            if str(value).isnumeric():
                self.tableview.column(i, anchor=E)
                self.tableview.heading(i, anchor=E)

    def align_column_left(self, event=None, cid=None):
        """Left align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.column(cid, anchor=W)

    def align_column_right(self, event=None, cid=None):
        """Right align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.column(cid, anchor=E)

    def align_column_center(self, event=None, cid=None):
        """Center align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.column(cid, anchor=CENTER)

    def align_heading_left(self, event=None, cid=None):
        """Left align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.heading(cid, anchor=W)

    def align_heading_right(self, event=None, cid=None):
        """Right align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.heading(cid, anchor=E)

    def align_heading_center(self, event=None, cid=None):
        """Center align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.tableview.heading(cid, anchor=CENTER)       

    # WIDGET BINDING

    def _set_widget_binding(self):
        """Setup the widget binding"""
        self.tableview.bind("<Double-Button-1>", self._header_double_leftclick)
        self.tableview.bind("<Button-1>", self._header_leftclick)
        self.tableview.bind("<Button-3>", self._table_rightclick)

    def _header_double_leftclick(self, event):
        """Callback for double-click events on the tableview header"""
        region = self.tableview.identify_region(event.x, event.y)
        if region == "separator":
            self.autosize_columns()

    def _header_leftclick(self, event):
        """Callback for left-click events"""
        region = self.tableview.identify_region(event.x, event.y)
        if region == "heading":
            col = self.tableview.identify_column(event.x)
            cid = int(self.tableview.column(col, "id"))
            self.sort_column_data(event)

    def _table_rightclick(self, event):
        """Callback for right-click events"""
        region = self.tableview.identify_region(event.x, event.y)
        if region == "heading":
            self.rightclickmenu_head.post(event)
        elif region != "separator":
            self.rightclickmenu_cell.post(event)


class TableColumn:
    """Represents a column in a Tableview object - INTERNAL"""

    def __init__(
        self,
        table,
        cid,
        text,
        image="",
        command="",
        anchor=W,
        width=None,
        minwidth=None,
        maxwidth=400,
        stretch=True,
    ):
        """
        Parameters:

            table (Treeview):
                The internal Treeview object of the Tableview.

            cid (str):
                The column id.

            text (str):
                The header text.

            image (PhotoImage):
                An image that is displayed to the left of the header text.

            command (Callable):
                A function called whenever the header button is clicked.

            anchor (str):
                The position of the header text within the header. One
                of "e", "w", "center".

            width (int):
                Specifies the width of the column in pixels.

            minwidth (int):
                Specifies the minimum width of the column in pixels.

            maxwidth (int):
                Specifies the maximum width of the column in pixels.

            stretch (bool):
                Specifies whether or not the column width should be
                adjusted whenever the widget is resized or the user
                drags the column separator.
        """
        self.cid = cid
        self.headertext = text
        self.table: ttk.Treeview = table
        self.colmaxwidth = maxwidth
        self.sort = ASCENDING
        self.tableview = None
        self.hbar = None
        self.table.column(
            self.cid,
            width=width or 200,
            minwidth=minwidth or 20,
            stretch=stretch,
            anchor=anchor,
        )
        self.table.heading(
            self.cid,
            text=text,
            anchor=anchor,
            image=image,
            command=command,
        )


class TableRow:
    """Represents a row in a Tableview object - INTERNAL"""

    def __init__(self, table, values):
        """
        Parameters:

            table (Treeview):
                The inner Treeview object within the Tableview

            values (List[Any, ...]):
                A list of values to display in the row
        """
        self.table: ttk.Treeview = table
        self.values = values
        self.iid = None

    def show(self, striped=False):
        """Show the row in the data table view"""
        if self.iid is None:
            self.build_row()
        self.table.reattach(self.iid, "", END)

        # remove existing stripes
        tags = list(self.table.item(self.iid, "tags"))
        # TODO where is the `table.tag_remove` method?
        try:
            tags.remove("striped")
        except ValueError:
            pass

        # add stripes (if needed)
        if striped:
            tags.append("striped")
        self.table.item(self.iid, tags=tags)

    def hide(self):
        """Remove the row from the data table view"""
        self.table.detach(self.iid)

    # def cell_configure(self, index, value):
    #     """Modify the value of a specific cell"""
    #     self.values[index] = value
    #     self.table.item(self.iid, values=self.values)

    def build_row(self):
        """Create the row object in the `Treeview` and capture
        the resulting item id (iid).
        """
        self.iid = self.table.insert("", END, values=self.values)


class TableCellRightClickMenu(tk.Menu):
    """A right-click menu object for the tableview cells - INTERNAL"""

    def __init__(self, master: Tableview):
        """
        Parameters:

            master (Tableview):
                The parent object
        """
        super().__init__(master, tearoff=False)
        self.tableview: Tableview = master
        self.treeview: ttk.Treeview = master.tableview
        self.cid = None
        self.iid = None

        config = {
            "sortascending": {
                "label": "⬆  Sort Ascending",
                "command": self.sort_column_ascending,
            },
            "sortdescending": {
                "label": "⬇  Sort Descending",
                "command": self.sort_column_descending,
            },
            "clearfilter": {
                "label": "Clear filter",
                "command": self.tableview.clear_table_filters,
            },
            "filterbyvalue": {
                "label": "Filter by cell's value",
                "command": self.filter_to_cell_value,
            },
            "hiderows": {
                "label": "Hide select rows",
                "command": self.hide_selected_rows,
            },
            "showrows": {
                "label": "Show only select rows",
                "command": self.filter_to_selected_rows,
            },
            "exportall": {
                "label": "Export all records",
                "command": self.export_all_records,
            },
            "exportpage": {
                "label": "Export current page",
                "command": self.export_current_page,
            },
            "exportselection": {
                "label": "Export current selection",
                "command": self.export_current_selection,
            },
            "exportfiltered": {
                "label": "Export records in filter",
                "command": self.export_records_in_filter,
            },
            "moveup": {
                "label": "↑ Move up", 
                "command": self.move_row_up
            },
            "movedown": {
                "label": "↓ Move down",
                "command": self.move_row_down,
            },
            "movetotop": {
                "label": "⤒ Move to top",
                "command": self.move_row_to_top,
            },
            "movetobottom": {
                "label": "⤓ Move to bottom",
                "command": self.move_row_to_bottom,
            },
            "alignleft": {
                "label": "◧  Align left",
                "command": self.align_column_left,
            },
            "aligncenter": {
                "label": "◫  Align center",
                "command": self.align_column_center,
            },
            "alignright": {
                "label": "◨  Align right",
                "command": self.align_column_right,
            },
        }
        sort_menu = tk.Menu(self, tearoff=False)
        sort_menu.add_command(cnf=config["sortascending"])
        sort_menu.add_command(cnf=config["sortdescending"])
        self.add_cascade(menu=sort_menu, label="⇅ Sort")

        filter_menu = tk.Menu(self, tearoff=False)
        filter_menu.add_command(cnf=config["clearfilter"])
        filter_menu.add_separator()
        filter_menu.add_command(cnf=config["filterbyvalue"])
        filter_menu.add_command(cnf=config["hiderows"])
        filter_menu.add_command(cnf=config["showrows"])
        self.add_cascade(menu=filter_menu, label="⧨  Filter")

        export_menu = tk.Menu(self, tearoff=False)
        export_menu.add_command(cnf=config["exportall"])
        export_menu.add_command(cnf=config["exportpage"])
        export_menu.add_command(cnf=config["exportselection"])
        export_menu.add_command(cnf=config["exportfiltered"])
        self.add_cascade(menu=export_menu, label="↔  Export")

        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config["moveup"])
        move_menu.add_command(cnf=config["movedown"])
        move_menu.add_command(cnf=config["movetotop"])
        move_menu.add_command(cnf=config["movetobottom"])
        self.add_cascade(menu=move_menu, label="⇵  Move")

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label="↦  Align")

    def post(self, event):
        """Display the menu below the selected cell.

        Parameters:

            event (Event):
                The click event that triggers menu.
        """
        # capture the column and item that invoked the menu
        self.event = event
        iid = self.treeview.identify_row(event.y)
        col = self.treeview.identify_column(event.x)

        # show the menu below the invoking cell
        rootx = self.treeview.winfo_rootx()
        rooty = self.treeview.winfo_rooty()
        bbox = self.treeview.bbox(iid, col)
        super().post(rootx + bbox[0], rooty + bbox[1] + bbox[3])

    def sort_column_ascending(self):
        """Sort the column in ascending order."""
        self.tableview.sort_column_data(self.event, sort=ASCENDING)

    def sort_column_descending(self):
        """Sort the column in descending order."""
        self.tableview.sort_column_data(self.event, sort=DESCENDING)

    def filter_to_cell_value(self):
        """Hide all records except for records where the current
        column exactly matches the current cell value."""
        self.tableview.filter_column_to_value(self.event)

    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows."""
        self.tableview.filter_to_selected_rows()

    def export_all_records(self):
        """Export all records to a csv file"""
        self.tableview.export_all_records()

    def export_current_page(self):
        """Export records on current page"""
        self.tableview.export_current_page()

    def export_current_selection(self):
        """Export rows currently selected"""
        self.tableview.export_current_selection()

    def export_records_in_filter(self):
        """Export rows currently filtered"""
        self.tableview.export_records_in_filter()

    def hide_selected_rows(self):
        """Hide the selected rows"""
        self.tableview.hide_selected_rows()

    def move_row_to_top(self):
        """Move the row to the top of the data set"""
        self.tableview.move_selected_rows_to_top()

    def move_row_to_bottom(self):
        """Move the row to the bottom of the dataset"""
        self.tableview.move_selected_rows_to_bottom()

    def move_row_up(self):
        """Move the selected above the previous sibling"""
        self.tableview.move_selected_row_up()

    def move_row_down(self):
        """Move the selected row below the next sibling"""
        self.tableview.move_row_down()

    def align_column_left(self):
        "Left align the column text"
        self.tableview.align_column_left(self.event)

    def align_column_right(self):
        """Right align the column text"""
        self.tableview.align_column_right(self.event)

    def align_column_center(self):
        """Center align the column text"""
        self.tableview.align_column_center(self.event)


class TableHeaderRightClickMenu(tk.Menu):
    """A right-click menu object for the tableview header - INTERNAL"""

    def __init__(self, master: Tableview):
        """
        Parameters:

            master (Tableview):
                The parent object
        """
        super().__init__(master, tearoff=False)
        self.tableview: Tableview = self.master
        self.table: ttk.Treeview = master.tableview
        self.event = None

        # HIDE & SHOW
        show_menu = tk.Menu(self, tearoff=False)
        for column in self.master.tablecols:
            variable = f"column_{column.cid}"
            self.table.setvar(variable, True)
            show_menu.add_checkbutton(
                label=column.headertext,
                command=lambda w=column: self.toggle_columns(w.cid),
                variable=variable,
                indicatoron=True,
                onvalue=True,
                offvalue=False,
            )
        self.add_cascade(menu=show_menu, label="±  Columns")

        config = {
            'movetoright': {
                "label": "→  Move to right", 
                "command": self.move_column_right
            },
            'movetoleft': {
                "label": "←  Move to left", 
                "command": self.move_column_left
            },
            'movetofirst': {
                "label": "⇤  Move to first", 
                "command": self.move_column_to_first
            },
            'movetolast': {
                "label": "⇥  Move to last", 
                "command": self.move_column_to_last
            },
            'alignleft': {
                "label": "◧  Align left", 
                "command": self.align_heading_left
            },
            'alignright': {
                "label": "◨  Align right", 
                "command": self.align_heading_right                
            },
            'aligncenter': {
                "label": "◫  Align center", 
                "command": self.align_heading_center
            }
        }

        # MOVE MENU
        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config['movetoleft'])
        move_menu.add_command(cnf=config['movetoright'])
        move_menu.add_command(cnf=config['movetofirst'])
        move_menu.add_command(cnf=config['movetolast'])
        self.add_cascade(menu=move_menu, label="⇄  Move")

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label="↦  Align")

    def post(self, event):
        # capture the column and item that invoked the menu
        self.event = event

        # show the menu below the invoking cell
        rootx = self.table.winfo_rootx()
        rooty = self.table.winfo_rooty()
        super().post(rootx + event.x, rooty + event.y + 10)

    def toggle_columns(self, cid):
        """Toggles the visibility of the selected column"""
        variable = f"column_{cid}"
        toggled = self.getvar(variable)
        if toggled:
            self.tableview.show_selected_column(cid=cid)
        else:
            self.tableview.hide_selected_column(cid=cid)

    def move_column_left(self):
        """Move column one position to the left"""
        self.tableview.move_column_left(self.event)

    def move_column_right(self):
        """Move column on position to the right"""
        self.tableview.move_column_right(self.event)

    def move_column_to_first(self):
        """Move column to leftmost position"""
        self.tableview.move_column_to_first(self.event)

    def move_column_to_last(self):
        """Move column to rightmost position"""
        self.tableview.move_column_to_last(self.event)

    def align_heading_left(self):
        """Left align the column header"""
        self.tableview.align_heading_left(self.event)

    def align_heading_right(self):
        """Right align the column header"""
        self.tableview.align_heading_right(self.event)

    def align_heading_center(self):
        """Center align the column header"""
        self.tableview.align_heading_center(self.event)
