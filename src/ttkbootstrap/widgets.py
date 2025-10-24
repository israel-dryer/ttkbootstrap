# floodgauge imports
import math
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk
from tkinter import font
from tkinter.ttk import Button, Checkbutton, Combobox
from tkinter.ttk import Entry, Frame, Label
from tkinter.ttk import Labelframe, LabelFrame, Menubutton
from tkinter.ttk import Notebook, OptionMenu, PanedWindow
from tkinter.ttk import Panedwindow, Progressbar, Radiobutton
from tkinter.ttk import Scale, Scrollbar, Separator
from tkinter.ttk import Sizegrip, Spinbox, Treeview
from typing import Union
from warnings import warn

# meter imports
from PIL import Image, ImageDraw, ImageTk
from PIL.Image import Resampling

from ttkbootstrap import utility
from ttkbootstrap.colorutils import contrast_color
from ttkbootstrap.constants import *
# date entry imports
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.style import Bootstyle, Colors, Style

M = 3  # meter image scale, higher number increases resolution

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

    The <<DateEntrySelected>> event is generated when a date is
    selected.

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
            dateformat=r"%x",
            firstweekday=6,
            startdate=None,
            bootstyle="",
            popup_title: str = 'Select new date',
            raise_exception: bool = False,
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

            popup_title (str, optional):
                Title for PopUp window (Default: `Select new date`)

            raise_exception (bool, optional):
                If a `ValueError` should be raised, if the user enters an invalid date string. If this is set to `False`,
                faulty date strings will be ignored. Only a warning on the terminal/console will be printed. (Default: `False`)

            **kwargs (dict[str, Any], optional):
                Other keyword arguments passed to the frame containing the
                entry and date button.
        """
        self.__enabled = True  # User/Programmer should NOT be able to change this, therefore double underscores
        self.__dateformat = self._validate_dateformat(
            dateformat)  # User/Programmer should NOT be able to change this, therefore double underscores
        self._firstweekday = firstweekday

        self._startdate = startdate or datetime.today()
        self._bootstyle = bootstyle
        self._popup_title = popup_title
        self._raise_exception = raise_exception
        super().__init__(master, **kwargs)

        # add visual components
        entry_kwargs = {
            "bootstyle": self._bootstyle,
        }
        if "width" in kwargs:
            entry_kwargs["width"] = kwargs.pop("width")

        # Build date Widget button (this shows the date in the wanted format)
        self.entry = ttk.Entry(self, **entry_kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        # Build datepicker button & place it right to the date widget
        self.button = ttk.Button(
            master=self,
            command=self._on_date_ask,
            bootstyle=f"{self._bootstyle}-date",
        )
        self.button.pack(side=tk.LEFT)

        # Initialize this widget
        self.set_date(self._startdate)

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
            elif state in ("disabled", "normal"):
                self.entry.configure(state=state)
                self.button.configure(state=state)
            else:
                kwargs[state] = state
        if "dateformat" in kwargs:
            self.__dateformat = kwargs.pop("dateformat")
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
            return self.__dateformat
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

    @property
    def enabled(self) -> bool:
        """
        If ``True`` this date picker is enabled and user can pick a new date, if ``False`` user can't use this picker

        :return: ``True`` if usable, ``False`` otherwise
        """
        return self.__enabled

    @property
    def dateformat(self) -> str:
        """
        Returns date format string, that is used to convert from strings to datetime objects respectively vice versa

        :return: Date format as string
        """
        return self.__dateformat

    def get_date(self) -> datetime:
        """
        Returns currently selected date as datetime object

        :return: Currently selected date
        """
        return self.configure(cnf='startdate')

    @staticmethod
    def _validate_dateformat(dateformat: str) -> str:
        """
        Checks if given dateformat string is appropriate for dates. If not, a `ValueError` will be raised.

        @see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

        :param dateformat: Dateformat string
        :return: Given dateformat string
        :raise ValueError: If given dateformat string is not appropriate for dates
        """
        has_year: bool = any(y in dateformat for y in ('%Y', '%y', '%G'))
        has_month: bool = any(m in dateformat for m in ('%m', '%B', '%b'))
        has_day: bool = any(d in dateformat for d in ('%d',))
        is_full_format: bool = any(f in dateformat for f in ('%x', '%c'))

        if has_year and has_month and has_day:
            return dateformat

        if is_full_format:
            return dateformat

        # Special case: (day of the year & year)
        if '%j' in dateformat and has_year:
            return dateformat

        # Special case: (week day & week number & year)
        has_week_number: bool = any(w in dateformat for w in ('%U', '%W', '%V'))
        has_week_day: bool = any(w in dateformat for w in ('%a', '%A', '%w'))
        if has_week_number and has_week_day and has_year:
            return dateformat

        raise ValueError(
            f'Given formatting string ("{dateformat}"), cannot be used to validate a given strings for dates or display a given datetime object as a date!')

    @staticmethod
    def _clean_datetime(new_date: Union[datetime, date]) -> datetime:
        """This is a date picker, therefore erase all unnecessary elements: hours, minutes, seconds, ..."""
        if isinstance(new_date, datetime):
            return datetime(new_date.year, new_date.month, new_date.day, tzinfo=new_date.tzinfo)
        else:
            return datetime(new_date.year, new_date.month, new_date.day)

    def set_date(self, new_date: Union[datetime, date]) -> None:
        """
        Sets given date/datetime object as currently selected date.

        (NOTE: Hours, minutes, seconds, milliseconds, microseconds will be ignored)

        :param new_date: New date that will become the currently selected one
        """
        _date: datetime = self._clean_datetime(new_date)
        if self.__enabled:
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(END, new_date.strftime(self.__dateformat))
        else:
            self.enable()
            self.configure(startdate=_date)
            self.entry.delete(first=0, last=END)
            self.entry.insert(tk.END, new_date.strftime(self.__dateformat))
            self.disable()

    def disable(self) -> None:
        """ Disables this date picker """
        self.__enabled = False
        self.entry.state(['disabled'])
        self.button.state(['disabled'])

    def enable(self) -> None:
        """ Enables this date picker """
        self.__enabled = True
        self.entry.state(['!disabled'])
        self.button.state(['!disabled'])

    def _on_date_ask(self):
        """
        Callback for pushing the date button

        :raise ValueError: If entered string does NOT match with currently used date format
        """
        currently_selected_date: str = self.entry.get() or datetime.today().strftime(self.__dateformat)
        try:
            self._startdate: datetime = datetime.strptime(currently_selected_date, self.__dateformat)
        except ValueError as exc:
            warn(f"Date entry text does not match with date format: {self.__dateformat}\n")
            if self._raise_exception:
                raise exc
            return
        old_date = datetime.strptime(currently_selected_date, self.__dateformat)

        # get the new date and insert into the entry
        new_date = Querybox.get_date(
            parent=self.entry,
            title=self._popup_title,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.set_date(new_date)
        self.event_generate("<<DateEntrySelected>>")


class Floodgauge(tk.Canvas):
    """
    A canvas-based widget that displays progress in determinate or indeterminate mode,
    styled using ttkbootstrap's color system.

    This widget mimics the behavior of ttk.Progressbar with additional features:
    - Canvas-based drawing for full styling control
    - Bounce-style animation for indeterminate mode
    - Lightened trough color based on the bootstyle
    - Support for variable and textvariable bindings
    - Auto-updating label based on mask or textvariable
    - Theme-reactive color updates via <<ThemeChanged>> event

    Parameters:
        master (Widget, optional):
            Parent widget.

        value (int):
            Initial value of the progress bar.

        maximum (int):
            The maximum value for the determinate range.

        mode (str):
            'determinate' or 'indeterminate' mode.

        mask (str, optional):
            A string with a '{}' placeholder for formatted text output, e.g. 'Progress: {}%'.

        text (str, optional):
            A static fallback label (used if no mask is specified).

        font (Font or tuple):
            The font used for the label (default: Helvetica 14 bold).

        bootstyle (str):
            A ttkbootstrap style keyword such as 'primary', 'info', etc.

        orient (str):
            'horizontal' or 'vertical' orientation.

        length (int):
            The long dimension of the widget (width if horizontal, height if vertical). Defaults to 200.

        thickness (int):
            The short axis of the widget (height if horizontal, width if vertical). Defaults to 50.

        variable (tk.IntVar, optional):
            Bound variable for the current value.

        textvariable (tk.StringVar, optional):
            Bound variable for the display label.
    """

    def __init__(
            self,
            master=None,
            value=0,
            maximum=100,
            mode="determinate",
            mask=None,
            text="",
            font=("Helvetica", 12),
            bootstyle="primary",
            orient="horizontal",
            length=200,
            thickness=50,
            **kwargs
    ):
        self.variable = kwargs.pop("variable", tk.IntVar(value=value))
        self.textvariable = kwargs.pop("textvariable", tk.StringVar(value=text))

        self.length = length
        self.thickness = thickness
        self.orient = orient
        canvas_kwargs = dict(highlightthickness=0, **kwargs)

        if self.orient == "horizontal":
            canvas_kwargs.update(width=self.length, height=self.thickness)
        else:
            canvas_kwargs.update(width=self.thickness, height=self.length)

        super().__init__(master, **canvas_kwargs)

        self.variable.trace_add("write", lambda *_: self._on_var_change())
        self.textvariable.trace_add("write", lambda *_: self._on_text_change())

        self.value = self.variable.get()
        self.text = self.textvariable.get()
        self.maximum = maximum
        self.mode = mode
        self.mask = mask
        self.font = font
        self._step_size = 1
        self._running = False
        self._after_id = None
        self._pulse_pos = 0
        self._pulse_direction = 1
        self._bootstyle = bootstyle

        self._update_theme_colors()

        self.bind("<Configure>", self._on_resize)
        self.bind("<<ThemeChanged>>", lambda e: self._update_theme_colors())
        self._draw()

    def _update_theme_colors(self):
        style = Style.get_instance()
        self.bar_color = style.colors.get(self._bootstyle)
        self.trough_color = Colors.update_hsv(self.bar_color, 0, -0.5, 0.3)
        self.text_color = contrast_color(self.bar_color, 'hex')
        self._draw()

    def _on_resize(self, event):
        if self.orient == "horizontal":
            self.length = event.width
            self.thickness = event.height
        else:
            self.length = event.height
            self.thickness = event.width
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        self.create_rectangle(0, 0, w, h, fill=self.trough_color, width=0)

        if self.mode == "determinate":
            ratio = max(0, min(1, self.value / self.maximum))
            if self.orient == "horizontal":
                fill = int(ratio * w)
                self.create_rectangle(0, 0, fill, h, fill=self.bar_color, width=0)
            else:
                fill = int(ratio * h)
                self.create_rectangle(0, h - fill, w, h, fill=self.bar_color, width=0)
        else:
            if self.orient == "horizontal":
                pulse_width = max(10, int(w * 0.2))
                x = self._pulse_pos
                self.create_rectangle(x, 0, x + pulse_width, h, fill=self.bar_color, width=0)
            else:
                pulse_height = max(10, int(h * 0.2))
                y = self._pulse_pos
                self.create_rectangle(0, y - pulse_height, w, y, fill=self.bar_color, width=0)

        if self.mask:
            label = self.mask.format(int(self.value))
            self.textvariable.set(label)
        elif self.textvariable:
            label = self.textvariable.get()
        else:
            label = self.text

        if label:
            self.create_text(
                w // 2,
                h // 2,
                text=label,
                font=self.font,
                fill=self.text_color,
                anchor="center"
            )

    def _on_var_change(self):
        self.value = self.variable.get()
        self._draw()

    def _on_text_change(self):
        self.text = self.textvariable.get()
        self._draw()

    def step(self, amount=1):
        self.value = (self.value + amount) % (self.maximum + 1)
        self.variable.set(self.value)
        self._draw()

    def start(self, step_size=None, interval=None):
        if self.mode == "indeterminate":
            self._step_size = step_size if step_size is not None else 8
            interval = interval if interval is not None else 20
        else:
            self._step_size = step_size if step_size is not None else 1
            interval = interval if interval is not None else 50

        self._running = True
        self._pulse_direction = 1
        self._run_animation(interval)

    def stop(self):
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _run_animation(self, interval):
        if not self._running:
            return

        if self.mode == "indeterminate":
            self._animate_indeterminate(interval)
        else:
            self.step(self._step_size)
            self._after_id = self.after(interval, lambda: self._run_animation(interval))

    def _animate_indeterminate(self, interval):
        if not self._running:
            return

        if self.orient == "horizontal":
            w = self.winfo_width()
            pulse_width = max(10, int(w * 0.2))
            max_pos = w - pulse_width
            self._pulse_pos += self._step_size * self._pulse_direction
            if self._pulse_pos >= max_pos:
                self._pulse_pos = max_pos
                self._pulse_direction = -1
            elif self._pulse_pos <= 0:
                self._pulse_pos = 0
                self._pulse_direction = 1
        else:
            h = self.winfo_height()
            pulse_height = max(10, int(h * 0.2))
            max_pos = h
            self._pulse_pos += self._step_size * self._pulse_direction
            if self._pulse_pos >= max_pos:
                self._pulse_pos = max_pos
                self._pulse_direction = -1
            elif self._pulse_pos <= pulse_height:
                self._pulse_pos = pulse_height
                self._pulse_direction = 1

        self._draw()
        self._after_id = self.after(interval, lambda: self._animate_indeterminate(interval))

    def configure(self, cnf=None, **kwargs):
        if cnf is not None and not kwargs:
            custom = {
                "value": ("value", "value", "Value", self.variable.get()),
                "maximum": ("maximum", "maximum", "Maximum", self.maximum),
                "mask": ("mask", "mask", "Mask", self.mask),
                "text": ("text", "text", "Text", self.textvariable.get()),
                "font": ("font", "font", "Font", self.font),
                "bootstyle": ("bootstyle", "bootstyle", "Bootstyle", self._bootstyle),
                "variable": ("variable", "variable", "Variable", str(self.variable)),
                "textvariable": ("textvariable", "textvariable", "Textvariable", str(self.textvariable)),
                "length": ("length", "length", "Length", self.length),
                "thickness": ("thickness", "thickness", "Thickness", self.thickness),
            }
            if cnf in custom:
                return custom[cnf]
            else:
                raise tk.TclError(f"unknown option '{cnf}'")

        if "value" in kwargs:
            self.value = kwargs.pop("value")
            self.variable.set(self.value)
        if "maximum" in kwargs:
            self.maximum = kwargs.pop("maximum")
        if "mask" in kwargs:
            self.mask = kwargs.pop("mask")
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            self.textvariable.set(self.text)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.pop("bootstyle")
            self._update_theme_colors()
        if "length" in kwargs:
            self.length = kwargs.pop("length")
            if self.orient == "horizontal":
                self.configure(width=self.length)
            else:
                self.configure(height=self.length)
        if "thickness" in kwargs:
            self.thickness = kwargs.pop("thickness")
            if self.orient == "horizontal":
                self.configure(height=self.thickness)
            else:
                self.configure(width=self.thickness)
        if "variable" in kwargs:
            self.variable = kwargs.pop("variable")
            self.variable.trace_add("write", lambda *_: self._on_var_change())
        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
            self.textvariable.trace_add("write", lambda *_: self._on_text_change())

        super().configure(**kwargs)
        self._draw()

    def cget(self, key):
        if key == "value":
            return self.variable.get()
        if key == "text":
            return self.textvariable.get()
        if key == "maximum":
            return self.maximum
        if key == "mask":
            return self.mask
        if key == "bootstyle":
            return self._bootstyle
        if key == "font":
            return self.font
        if key == "length":
            return self.length
        if key == "thickness":
            return self.thickness
        if key == "variable":
            return str(self.variable)
        if key == "textvariable":
            return str(self.textvariable)
        return super().cget(key)

    def keys(self):
        return [
            "value", "maximum", "mask", "text", "font",
            "bootstyle", "length", "thickness", "variable", "textvariable"
        ]

    def items(self):
        return {k: self.cget(k) for k in self.keys()}.items()

    __getitem__ = lambda self, key: self.cget(key)
    __setitem__ = lambda self, key, value: self.configure(**{key: value})


class FloodgaugeLegacy(Progressbar):
    """
    DEPRECATED: This widget is retained for backward compatibility. You may
    use this is you have an issues with the canvas-based widget.

    Use the canvas-based `Floodgauge` widget instead for:
    - Full control over styling and draw order
    - Support for theme responsiveness
    - Animated indeterminate mode
    - Automatic label updates with `mask` or `textvariable`

    This legacy version is based on `ttk.Progressbar` and does not support
    the same level of styling or animation flexibility.
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
        # progress bar value variables
        if 'variable' in kwargs:
            self._variable = kwargs.pop('variable')
        else:
            self._variable = tk.IntVar(value=value)
        if 'textvariable' in kwargs:
            self._textvariable = kwargs.pop('textvariable')
        else:
            self._textvariable = tk.StringVar(value=text)

        self._textvariable.trace_add("write", self._set_widget_text)
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
            variable=self._variable,
            **kwargs,
        )
        self._set_widget_text(self._textvariable.get())
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)

        if self._mask is not None:
            self._set_mask()

    def _set_widget_text(self, *_):
        ttkstyle = self.cget("style")
        if self._mask is None:
            text = self._textvariable.get()
        else:
            value = self._variable.get()
            text = self._mask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._font)

    def _set_mask(self):
        if self._traceid is None:
            self._traceid = self._variable.trace_add(
                "write", self._set_widget_text
            )

    def _unset_mask(self):
        if self._traceid is not None:
            self._variable.trace_remove("write", self._traceid)
        self._traceid = None

    def _on_theme_change(self, *_):
        text = self._textvariable.get()
        self._set_widget_text(text)

    def _configure_get(self, cnf):
        if cnf == "value":
            return self._variable.get()
        if cnf == "text":
            return self._textvariable.get()
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
            self._variable.set(kwargs.pop("value"))
        if "text" in kwargs:
            self._textvariable.set(kwargs.pop("text"))
        if "bootstyle" in kwargs:
            self._bootstyle = kwargs.get("bootstyle")
        if "mask" in kwargs:
            self._mask = kwargs.pop("mask")
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        if "variable" in kwargs:
            self._variable = kwargs.get("variable")
            Progressbar.configure(self, cnf=None, **kwargs)
        if "textvariable" in kwargs:
            self.textvariable = kwargs.pop("textvariable")
        else:
            Progressbar.configure(self, cnf=None, **kwargs)

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

    @property
    def textvariable(self):
        """Returns the textvariable object"""
        return self._textvariable

    @textvariable.setter
    def textvariable(self, value):
        """Set the new textvariable property"""
        self._textvariable = value
        self._set_widget_text(self._textvariable.get())

    @property
    def variable(self):
        """Returns the variable object"""
        return self._variable

    @variable.setter
    def variable(self, value):
        """Set the new variable object"""
        self._variable = value
        if self.cget('variable') != value:
            self.configure(variable=self._variable)


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
            master=None,
            bootstyle=DEFAULT,
            arcrange=None,
            arcoffset=None,
            amountmin=0,
            amounttotal=100,
            amountused=0,
            amountformat="{:.0f}",
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
            stepsize=1,
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
        self.amountminvar = tk.IntVar(value=amountmin)
        self.amountusedvar = tk.IntVar(value=amountused)
        self.amountusedvar.trace_add("write", self._update_meter)
        self.amountuseddisplayvar = tk.StringVar(value=amountformat.format(amountused))
        self.amounttotalvar = tk.IntVar(value=amounttotal)
        self.labelvar = tk.StringVar(value=subtext)

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

    def _update_meter(self, *_):
        self._draw_meter()
        amount_used = self.amountusedvar.get()
        self.amountuseddisplayvar.set(self._amountformat.format(amount_used))

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
            textvariable=self.amountuseddisplayvar,
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
        if self._subtext:
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
            img.resize((self._metersize, self._metersize), Resampling.BICUBIC)
        )
        self.indicator.configure(image=self._meterimage)

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
            return super(ttk.Frame, self).configure(cnf)

    def _configure_set(self, **kwargs):
        """Override the configuration set method"""
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


class LabeledScale(ttk.Frame):
    """A Ttk Scale widget with a Ttk Label widget indicating its
    current value.

    The Ttk Scale can be accessed through instance.scale, and Ttk Label
    can be accessed through instance.label"""

    def __init__(self, master=None, variable=None, from_=0, to=10, bootstyle=DEFAULT, **kwargs):
        """Construct a horizontal LabeledScale with parent master, a
        variable to be associated with the Ttk Scale widget and its range.
        If variable is not specified, a tkinter.IntVar is created.

        WIDGET-SPECIFIC OPTIONS

            compound: 'top' or 'bottom'
                Specifies how to display the label relative to the scale.
                Defaults to 'top'.
        """
        super().__init__(master=master, **kwargs)
        self._label_top = kwargs.pop('compound', 'top') == 'top'

        ttk.Frame.__init__(self, master, **kwargs)
        self._variable = variable or tk.IntVar(master)
        self._variable.set(from_)
        self._last_valid = from_
        self._bootstyle = bootstyle

        self.label = ttk.Label(self, bootstyle=bootstyle)
        self.scale = ttk.Scale(self, variable=self._variable, from_=from_, to=to, bootstyle=bootstyle)
        self.scale.bind('<<RangeChanged>>', self._adjust)

        # position scale and label according to the compound option
        scale_side = 'bottom' if self._label_top else 'top'
        label_side = 'top' if scale_side == 'bottom' else 'bottom'
        self.scale.pack(side=scale_side, fill='x')
        # Dummy required to make frame correct height
        dummy = Label(self)
        dummy.pack(side=label_side)
        dummy.lower()
        self.label.place(anchor='n' if label_side == 'top' else 's')

        # update the label as scale or variable changes
        self.__tracecb = self._variable.trace_add('write', self._adjust)
        self.bind('<Configure>', self._adjust)
        self.bind('<Map>', self._adjust)

    def destroy(self):
        """Destroy this widget and possibly its associated variable."""
        try:
            self._variable.trace_remove('write', self.__tracecb)
        except AttributeError:
            pass
        else:
            del self._variable
        super().destroy()
        self.label = None
        self.scale = None

    def _to_number(self, x):
        if isinstance(x, str):
            if '.' in x:
                x = float(x)
            else:
                x = int(x)
        return x

    def _adjust(self, *args):
        """Adjust the label position according to the scale."""

        def adjust_label():
            self.update_idletasks()  # "force" scale redraw

            x, y = self.scale.coords()
            if self._label_top:
                y = self.scale.winfo_y() - self.label.winfo_reqheight()
            else:
                y = self.scale.winfo_reqheight() + self.label.winfo_reqheight()

            self.label.place_configure(x=x, y=y)

        from_ = self._to_number(self.scale['from'])
        to = self._to_number(self.scale['to'])
        if to < from_:
            from_, to = to, from_
        newval = self._variable.get()
        if not from_ <= newval <= to:
            # value outside range, set value back to the last valid one
            self.value = self._last_valid
            return

        self._last_valid = newval
        self.label['text'] = newval
        self.after_idle(adjust_label)

    @property
    def value(self):
        """Return current scale value."""
        return self._variable.get()

    @value.setter
    def value(self, val):
        """Set new scale value."""
        self._variable.set(val)
