"""DatePickerDialog implementation (calendar popup)."""

import calendar
import tkinter
from datetime import date, datetime
from typing import Any, List, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.internal.positioning import (
    below_widget,
    center_on_screen,
    ensure_on_screen,
)
from ttkbootstrap.utility import windowing_system
from ttkbootstrap.style._compat import normalize_datepicker_kwargs


class DatePickerDialog:
    """A dialog that displays a calendar popup and returns the
    selected date as a datetime object.

    The current date is displayed by default unless the `start_date`
    parameter is provided.

    Use the single chevrons on either side of the month-year title to
    move the calendar by one month, and the double chevrons to move it
    by one year. Click the title to reset to the start date.

    The starting weekday can be changed with the `first_weekday`
    parameter for geographies that do not start the calendar on
    Sunday, which is the default.

    The popup is a frameless (borderless) window that stays above its
    parent. Clicking a day selects it and closes the popup; clicking
    anywhere outside the popup, or pressing ``Escape``, cancels the
    selection and closes it.

    The bootstyle api may be used to change the style of the widget.
    The available colors include -> primary, secondary, success,
    info, warning, danger, light, dark.
    """

    def __init__(
            self,
            parent: Optional[tkinter.Misc] = None,
            title: str = " ",
            first_weekday: int = 6,
            start_date: Optional[date] = None,
            bootstyle: str = PRIMARY,
            autoshow: bool = True,
            show_outside_days: bool = True,
            **kwargs: Any,
    ) -> None:
        """Create a date picker dialog with a calendar popup.

        The dialog displays a calendar that allows the user to select a date.
        The selected date can be accessed via the `date_selected` attribute
        after the dialog is closed. The dialog is modal and grabs focus until
        dismissed.

        Parameters:

            parent (Widget):
                Parent widget. If provided, the dialog will be positioned
                relative to it. Otherwise, it will be centered on screen.

            title (str):
                The dialog window title (default=' ').

            first_weekday (int):
                First day of the week (0=Monday, 6=Sunday). Adjust this for
                different geographical conventions (default=6).

            start_date (date):
                Initial date to display in the calendar. If None, uses today's
                date. The calendar will open to the month containing this date.

            bootstyle (str):
                The color theme for the calendar (primary, secondary, success,
                info, warning, danger, light, dark) (default=PRIMARY).

            autoshow (bool):
                If True (default, back-compatible), the dialog grabs focus and
                blocks during construction, so ``date_selected`` is readable as
                soon as the constructor returns. If False, construction does not
                block; call :meth:`show` explicitly and read :attr:`result`
                afterward (the path :meth:`Querybox.get_date` uses so it can
                position the popup and detect cancellation).

            show_outside_days (bool):
                If True (default), the leading/trailing days that belong to the
                previous/next month are shown as muted, non-selectable labels. If
                False, those cells are left blank so only the current month's days
                are visible.

        Interaction:
            - Month arrows (single chevron): Move calendar by one month
            - Year arrows (double chevron): Move calendar by one year
            - Click title: Reset to start date
            - Click date: Select date and close dialog
            - Click outside or press Escape: Cancel and close dialog
        """
        # Accept the pre-2.0 `firstweekday`/`startdate` spellings through 2.x
        # (warn-and-normalize; removed in 3.0). Coordinated with DateEntry /
        # Querybox.get_date, which were snake_cased in the same PR.
        aliases = normalize_datepicker_kwargs(kwargs)
        first_weekday = aliases.get("first_weekday", first_weekday)
        start_date = aliases.get("start_date", start_date)
        if kwargs:
            raise TypeError(
                f"DatePickerDialog got unexpected keyword arguments: "
                f"{', '.join(sorted(kwargs))}"
            )

        # NOTE: deliberately no `locale.setlocale(LC_TIME, "")` here. It mutated
        # the process-global locale, which (a) desynced `DateEntry`'s `%x`
        # format/parse round-trip (text written under one locale failed to parse
        # under another, raising a spurious "does not match" warning), and (b) is
        # counterproductive for this dialog's own i18n -- month/weekday names are
        # localized via `MessageCatalog`, keyed on the *English* `strftime`
        # output, so the ambient (C) locale is exactly what's wanted.

        self.parent = parent
        self.root = ttk.Toplevel(
            title=title,
            transient=self.parent,
            resizable=(False, False),
            topmost=True,
            minsize=(226, 1),
            iconify=True,
            override_redirect=True
        )
        # Outside-click / Escape dismissal bookkeeping. The popup is frameless
        # (no titlebar 'X'), so a click outside its bounds -- or Escape -- cancels
        # the selection. Bindings live on the parent's toplevel (Tk events don't
        # bubble past it) and are armed after a short delay so the click that
        # opened the popup isn't caught, then torn down on <Destroy>.
        self._dismiss_after_id: Optional[str] = None
        self._dismiss_binding_root: Optional[tkinter.Misc] = None
        self._dismiss_handler_ids: List[Tuple[str, str]] = []
        self.first_weekday = first_weekday
        self.start_date = start_date or datetime.today().date()
        self.bootstyle = bootstyle or PRIMARY
        self.show_outside_days = show_outside_days

        self.date_selected = self.start_date
        self.date = start_date or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=first_weekday)
        # Track whether the user actually picked a day, so cancellation
        # (closing the window without a selection) is distinguishable from a
        # real selection -- `date_selected` alone cannot tell them apart because
        # it defaults to `start_date`/today. Read via the `result` property.
        self._selection_made = False

        self.titlevar = ttk.StringVar()
        self.datevar = ttk.IntVar()

        self._setup_calendar()
        if autoshow:
            self.show()

    def show(self, position: Optional[Tuple[int, int]] = None, wait_for_result: bool = True) -> None:
        """Show the frameless popup and (optionally) block until it closes.

        The popup dismisses on an outside click or ``Escape``; there is no modal
        grab, so the parent window stays interactive (clicking it cancels the
        popup). ``wait_for_result`` still blocks the caller until the popup is
        closed so the selection can be read from :attr:`result`.

        Parameters:

            position (tuple[int, int]):
                Optional ``(x, y)`` screen coordinates for the popup. If omitted,
                the default placement (directly below the parent target, else
                centered) set up during construction is kept.

            wait_for_result (bool):
                If True (default), block until the dialog is closed; read the
                selection from :attr:`result` afterward.
        """
        if position is not None:
            self._set_window_position(position)
        self.root.lift()
        self.root.focus_force()
        self._arm_dismiss()
        if wait_for_result:
            self.root.wait_window()

    @property
    def result(self) -> Optional[date]:
        """The selected ``date``, or ``None`` if the dialog was cancelled."""
        return self.date_selected if self._selection_made else None

    # -- frameless popup dismissal ------------------------------------------- #

    def _cancel(self, *_: Any) -> None:
        """Dismiss the popup without recording a selection."""
        if self.root.winfo_exists():
            self.root.destroy()
        self._return_focus()

    def _return_focus(self) -> None:
        """Hand input focus back to the parent after the popup closes.

        A frameless (override-redirect) popup that grabbed focus via
        ``focus_force`` does not return focus to the parent when destroyed --
        on Windows this leaves the app with *no* focused widget, so a later
        click on the entry doesn't land focus. Reactivate the parent's toplevel
        (``focus_force``) and then put keyboard focus on the parent widget
        itself (the ``DateEntry`` field, for that widget's popup).
        """
        target = self.parent
        if target is None:
            return
        try:
            if not target.winfo_exists():
                return
            # Reclaim window activation for the parent's toplevel first --
            # focus_set on a child is a no-op while the toplevel isn't the
            # focused window.
            target.winfo_toplevel().focus_force()
            target.focus_set()
        except tkinter.TclError:
            pass

    def _arm_dismiss(self) -> None:
        """Bind Escape + outside-click so the frameless popup can be dismissed."""
        self.root.bind("<Escape>", self._cancel, "+")
        self.root.bind("<Destroy>", self._on_root_destroy, "+")
        # Delay the outside-click binding so the mouse press that opened the
        # popup (still being dispatched) doesn't immediately dismiss it.
        self._dismiss_after_id = self.root.after(100, self._bind_outside_click)

    def _bind_outside_click(self) -> None:
        """Watch the parent's toplevel for clicks (or moves) outside the popup."""
        self._dismiss_after_id = None
        if not (self.root.winfo_exists() and self.root.winfo_viewable()):
            return
        root = self._dismiss_root()
        if root is None or not root.winfo_exists():
            return
        self._dismiss_binding_root = root
        # A child's bindtags include its toplevel, so a press anywhere inside
        # the parent window reaches this binding; the handler dismisses only
        # when the press lands outside the popup's screen bounds.
        for seq in ("<Button-1>", "<Button-2>", "<Button-3>"):
            handler_id = root.bind(seq, self._on_outside_click, "+")
            self._dismiss_handler_ids.append((seq, handler_id))
        # Dragging/resizing/minimizing the parent fires no click, so also
        # dismiss on its geometry changes -- otherwise the frameless popup
        # would hang at its old screen position.
        for seq in ("<Configure>", "<Unmap>"):
            handler_id = root.bind(seq, self._on_root_geometry_change, "+")
            self._dismiss_handler_ids.append((seq, handler_id))

    def _dismiss_root(self) -> Optional[tkinter.Misc]:
        """The toplevel to watch for outside clicks (the parent's, if any)."""
        candidate = self.parent or self.root.master
        if candidate is None:
            return None
        try:
            return candidate.winfo_toplevel()
        except tkinter.TclError:
            return None

    def _on_outside_click(self, event: Any) -> None:
        """Cancel when a press lands outside the popup's screen bounds."""
        if not self.root.winfo_exists():
            return
        x, y = event.x_root, event.y_root
        rx, ry = self.root.winfo_rootx(), self.root.winfo_rooty()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()
        if not (rx <= x <= rx + rw and ry <= y <= ry + rh):
            self._cancel()

    def _on_root_geometry_change(self, event: Any) -> None:
        """Cancel when the watched toplevel itself moves, resizes, or unmaps."""
        if str(event.widget) != str(self._dismiss_binding_root):
            return
        if self.root.winfo_exists() and self.root.winfo_viewable():
            self._cancel()

    def _on_root_destroy(self, event: Any) -> None:
        """Tear down the dismissal bindings when the popup is destroyed."""
        if event.widget is not self.root:
            return
        if self._dismiss_after_id is not None:
            try:
                self.root.after_cancel(self._dismiss_after_id)
            except tkinter.TclError:
                pass
            self._dismiss_after_id = None
        root = self._dismiss_binding_root
        if root is not None:
            try:
                if root.winfo_exists():
                    for seq, handler_id in self._dismiss_handler_ids:
                        root.unbind(seq, handler_id)
            except tkinter.TclError:
                pass
        self._dismiss_handler_ids = []
        self._dismiss_binding_root = None

    def _setup_calendar(self) -> None:
        """Setup the calendar widget"""
        # create the widget containers
        frm_style = "Card.TFrame" if windowing_system(self.root) != 'aqua' else "TFrame"
        self.frm_calendar = ttk.Frame(master=self.root, padding=2, style=frm_style).pack(fill=BOTH, expand=YES)
        self.frm_title = ttk.Frame(self.frm_calendar, padding=(3, 3)).pack(fill=X)
        self.frm_header = ttk.Frame(self.frm_calendar).pack(fill=X)

        # setup the toplevel widget
        self.root.withdraw()  # reset the iconify state
        self.frm_calendar.update_idletasks()  # actualize geometry

        # create visual components
        self._draw_titlebar()
        self._draw_calendar()

        # make toplevel visible
        self.root.update_idletasks()
        self.root.deiconify()
        self._set_window_position()

    def _draw_calendar(self) -> None:
        self._set_title()
        self._current_month_days()
        self.frm_dates = ttk.Frame(self.frm_calendar).pack(fill=BOTH, expand=YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    # A cell for a day in the previous/next month. When
                    # show_outside_days is off, leave it blank (empty label keeps
                    # the grid geometry intact); otherwise show the muted number.
                    text = self.monthdates[row][col].day if self.show_outside_days else ""
                    ttk.Label(
                        master=self.frm_dates,
                        text=text,
                        anchor=CENTER,
                        padding=5,
                        state=DISABLED,
                    ).grid(row=row, column=col, sticky=NSEW)
                else:
                    if all(
                            [
                                day == self.date_selected.day,
                                self.date.month == self.date_selected.month,
                                self.date.year == self.date_selected.year,
                            ]
                    ):
                        day_style = f"{self.bootstyle}-toolbutton"
                        # Put this day in the ttk "selected" state so the
                        # toolbutton renders its ON look. Without this the day
                        # sits in the (now quiet + muted) OFF state and reads as
                        # a disabled button.
                        self.datevar.set(day)
                    else:
                        day_style = f"{self.bootstyle}-calendar"

                    def selected(x=row, y=col):
                        self._on_date_selected(x, y)

                    btn = ttk.Radiobutton(
                        master=self.frm_dates,
                        variable=self.datevar,
                        value=day,
                        text=day,
                        takefocus=True,
                        bootstyle=day_style,
                        padding=4,
                        command=selected,
                    )
                    btn.grid(row=row, column=col, sticky=NSEW)

    def _draw_titlebar(self) -> None:
        """Draw the calendar title bar and navigation controls."""
        # create and pack the title and action buttons
        self.prev_year = ttk.Button(
            master=self.frm_title,
            command=self.on_prev_year,
            bootstyle="ghost",
            icon="chevron-double-left",
            padding=4,
        )
        self.prev_year.pack(side=LEFT, fill=Y)
        self.prev_period = ttk.Button(
            master=self.frm_title,
            command=self.on_prev_month,
            bootstyle="ghost",
            icon="chevron-left",
            padding=4
        )
        self.prev_period.pack(side=LEFT, fill=Y)

        self.title = ttk.Label(
            master=self.frm_title,
            textvariable=self.titlevar,
            anchor=CENTER,
            font="TkHeadingFont",
        )
        self.title.pack(side=LEFT, fill=X, expand=YES)

        self.next_period = ttk.Button(
            master=self.frm_title,
            command=self.on_next_month,
            bootstyle="ghost",
            icon="chevron-right",
            padding=4
        )
        self.next_period.pack(side=LEFT, fill=Y)

        self.next_year = ttk.Button(
            master=self.frm_title,
            command=self.on_next_year,
            bootstyle="ghost",
            icon="chevron-double-right",
            padding=4
        )
        self.next_year.pack(side=LEFT, fill=Y)

        self.title.bind("<Button-1>", self.on_reset_date)

        # create and pack days of the week header
        for col in self._header_columns():
            ttk.Label(
                master=self.frm_header,
                text=col,
                anchor=CENTER,
                padding=4,
                font="-size 8 -weight bold",
                bootstyle="secondary"
            ).pack(side=LEFT, fill=X, expand=YES)

    def _set_title(self) -> None:
        _titledate_month = MessageCatalog.translate(f'{self.date.strftime("%B")}')
        _titledate_year = f'{self.date.strftime("%Y")}'
        _titledate = f'{_titledate_month} {_titledate_year}'
        self.titlevar.set(value=_titledate.capitalize())

    def _current_month_days(self) -> None:
        """Fetch day numbers and dates for current month."""
        self.monthdays = self.calendar.monthdayscalendar(year=self.date.year, month=self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(year=self.date.year, month=self.date.month)

    def _header_columns(self) -> List[str]:
        """Create weekday headers based on `first_weekday`."""
        weekdays = [
            MessageCatalog.translate("Mo"),
            MessageCatalog.translate("Tu"),
            MessageCatalog.translate("We"),
            MessageCatalog.translate("Th"),
            MessageCatalog.translate("Fr"),
            MessageCatalog.translate("Sa"),
            MessageCatalog.translate("Su"),
        ]
        header = weekdays[self.first_weekday:] + weekdays[: self.first_weekday]
        return header

    def _on_date_selected(self, row: int, col: int) -> None:
        """Callback for selecting a date."""
        self.date_selected = self.monthdates[row][col]
        self._selection_made = True
        self.root.destroy()
        self._return_focus()

    def _selection_callback(func):
        """Calls the decorated `func` and redraws the calendar."""

        def inner(self, *args):
            func(self, *args)
            self.frm_dates.destroy()
            self._draw_calendar()

        return inner

    @_selection_callback
    def on_next_month(self) -> None:
        year, month = self._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_next_year(self, *_: Any) -> None:
        year = self.date.year + 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_month(self) -> None:
        year, month = self._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_prev_year(self, *_: Any) -> None:
        year = self.date.year - 1
        month = self.date.month
        self.date = datetime(year=year, month=month, day=1).date()

    @_selection_callback
    def on_reset_date(self, *_: Any) -> None:
        self.date = self.start_date

    def _set_window_position(self, position: Optional[Tuple[int, int]] = None) -> None:
        """Position the popup, clamped to stay fully on its monitor.

        An explicit ``(x, y)`` wins; otherwise the popup drops directly below the
        parent (target) widget, left-aligned to it -- standard dropdown placement,
        so a ``DateEntry`` (whose target is the entry field) shows the calendar
        beneath the input, flipping *above* the target when there is no room
        below. With no parent it centers on screen. Every path is clamped by
        :func:`ensure_on_screen` so the popup never overflows off-screen (most
        visible on a target near the screen edge).
        """
        # titlebar_height=0: the popup is frameless, so no decoration to reserve.
        if position is not None:
            x, y = ensure_on_screen(self.root, *position, titlebar_height=0)
        elif self.parent:
            x, y = below_widget(self.root, self.parent)
        else:
            x, y = ensure_on_screen(self.root, *center_on_screen(self.root), titlebar_height=0)
        self.root.geometry(f"+{x}+{y}")

    @staticmethod
    def _nextmonth(year: int, month: int) -> Tuple[int, int]:
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    @staticmethod
    def _prevmonth(year: int, month: int) -> Tuple[int, int]:
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1
