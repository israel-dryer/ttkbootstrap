"""ttkbootstrap 2.0 pre-release visual review harness (Track B).

A single-window "everything bagel" that constructs one of every native ttk
widget and every shipped ttkbootstrap widget, in their common states, plus a
launcher for every dialog. Built for the human-gated visual / cross-platform
pass of the 2.0 pre-release review (`development/2_0_prerelease_review_plan.md`,
Track B): the eyeball pass is one window, not thirty.

Run it once per cell of the matrix:

    Platforms : win32 (primary), macOS/aqua, Linux/x11 (if reachable)
    Modes     : light + dark (use the "Toggle light/dark" button, or the theme
                picker for the full catalog)
    DPI       : 100 / 125 / 150 / 200 %  (set the OS display scaling, or launch
                with `TK_SCALING` / `Window(scaling=...)`)

What to look for (non-exhaustive):
  - button family: solid / outline / ghost / link / toolbutton / toggle read
    correctly incl. the `neutral` default; 1px hairline borders are crisp.
  - inputs: focus ring shows on focus only (not hover); disabled/readonly fills.
  - indicators: check / radio / switch / scale / scrollbar / progressbar glyphs
    are sharp at every DPI; striped progressbar trough is flat.
  - icons: date caret, spinbox/combobox/menubutton arrows, Messagebox glyphs,
    Tableview sort + pagination glyphs follow the theme foreground.
  - theme switch repaints every mounted widget (no stale colors / leftover art).
  - dialogs: open each one light + dark; DatePicker highlights the *selected*
    day only (watch the parked "stale highlight while browsing months" issue).

Known parked bug to confirm here (memory `center-on-screen-negative-origin-bug`):
  on a multi-monitor layout, `place_window_center` / `center_on_screen` can put
  the window at a negative origin off-screen. Use "Recenter window" after moving
  the app onto a secondary monitor.
"""
import datetime

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox, Querybox
from ttkbootstrap.dialogs import (
    MessageDialog, DatePickerDialog, FontDialog, ColorChooserDialog,
)
from ttkbootstrap.widgets import ToolTip, ToastNotification

COLORS = ("primary", "secondary", "success", "info", "warning", "danger",
          "light", "dark", "neutral")


def _labeled(parent, text):
    lf = ttk.Labelframe(parent, text=text, padding=8)
    lf.pack(fill=X, pady=4, padx=4, anchor=N)
    return lf


def build_button_family(parent):
    lf = _labeled(parent, "Button family (solid / outline / ghost / link)")
    for variant, suffix in (("solid", ""), ("outline", "-outline"),
                            ("ghost", "-ghost")):
        row = ttk.Frame(lf)
        row.pack(fill=X, pady=1)
        ttk.Label(row, text=variant, width=8).pack(side=LEFT)
        for c in COLORS:
            ttk.Button(row, text=c, bootstyle=f"{c}{suffix}").pack(
                side=LEFT, padx=1, fill=X, expand=YES)
    row = ttk.Frame(lf)
    row.pack(fill=X, pady=1)
    ttk.Label(row, text="link", width=8).pack(side=LEFT)
    for c in COLORS:
        ttk.Button(row, text=c, bootstyle=f"{c}-link").pack(
            side=LEFT, padx=1, fill=X, expand=YES)
    # a disabled + a default (neutral) button
    row = ttk.Frame(lf)
    row.pack(fill=X, pady=(4, 1))
    ttk.Button(row, text="default (neutral)").pack(side=LEFT, padx=2)
    ttk.Button(row, text="disabled", state=DISABLED).pack(side=LEFT, padx=2)
    b = ttk.Button(row, text="hover me for a tooltip", bootstyle="info-outline")
    b.pack(side=LEFT, padx=2)
    ToolTip(b, text="This is a ToolTip.", bootstyle="info-inverse")

    # icon-only buttons: square, same height as a normal button; compare against
    # a normal button and an icon+text button on the same row.
    row = ttk.Frame(lf)
    row.pack(fill=X, pady=(6, 1))
    ttk.Label(row, text="icon-only", width=8).pack(side=LEFT)
    ttk.Button(row, text="Normal").pack(side=LEFT, padx=2)
    ttk.Button(row, icon="floppy", text="Save").pack(side=LEFT, padx=2)
    for glyph, style in (("gear-fill", "primary"), ("bell-fill", "info"),
                         ("trash-fill", "danger-outline"), ("search", "ghost"),
                         ("three-dots", "secondary")):
        ttk.Button(row, icon=glyph, icon_only=True, bootstyle=style).pack(
            side=LEFT, padx=2)
    ttk.Button(row, icon="x-lg", icon_only=True, state=DISABLED).pack(
        side=LEFT, padx=2)
    # explicit overrides (deliberately a different size): a bigger glyph, then a
    # dense small-padding toolbar button -- separated so the default set above
    # reads as one uniform height.
    ttk.Label(row, text="overrides:").pack(side=LEFT, padx=(12, 2))
    ttk.Button(row, icon="plus-lg", icon_only=True, icon_size=24,
               bootstyle="success").pack(side=LEFT, padx=2)
    ttk.Button(row, icon="list", icon_only=True, padding=2,
               bootstyle="dark").pack(side=LEFT, padx=2)


def build_toggles(parent):
    lf = _labeled(parent, "Check / radio / toolbutton / toggle")
    row = ttk.Frame(lf)
    row.pack(fill=X)
    c1 = ttk.Checkbutton(row, text="checked")
    c1.pack(side=LEFT, padx=6)
    c1.invoke()
    ttk.Checkbutton(row, text="unchecked").pack(side=LEFT, padx=6)
    ttk.Checkbutton(row, text="disabled", state=DISABLED).pack(side=LEFT, padx=6)
    r1 = ttk.Radiobutton(row, text="radio on", value=1)
    r1.pack(side=LEFT, padx=6)
    r1.invoke()
    ttk.Radiobutton(row, text="radio off", value=2).pack(side=LEFT, padx=6)

    row = ttk.Frame(lf)
    row.pack(fill=X, pady=(6, 0))
    t1 = ttk.Checkbutton(row, text="success toolbutton",
                         bootstyle="success-toolbutton")
    t1.pack(side=LEFT, padx=6)
    t1.invoke()
    t2 = ttk.Checkbutton(row, text="round toggle",
                         bootstyle="success-round-toggle")
    t2.pack(side=LEFT, padx=6)
    t2.invoke()
    ttk.Checkbutton(row, text="square toggle",
                    bootstyle="square-toggle").pack(side=LEFT, padx=6)


def build_inputs(parent):
    lf = _labeled(parent, "Inputs (focus ring on focus only; readonly/disabled)")
    e = ttk.Entry(lf)
    e.insert(END, "entry — click to focus")
    e.pack(fill=X, pady=2)
    ro = ttk.Entry(lf)
    ro.insert(END, "readonly entry")
    ro.configure(state="readonly")
    ro.pack(fill=X, pady=2)
    de = ttk.Entry(lf, state=DISABLED)
    de.pack(fill=X, pady=2)
    sb = ttk.Spinbox(lf, from_=0, to=100)
    sb.set(42)
    sb.pack(fill=X, pady=2)
    cbo = ttk.Combobox(lf, values=["alpha", "bravo", "charlie"])
    cbo.current(0)
    cbo.pack(fill=X, pady=2)
    ttk.DateEntry(lf).pack(fill=X, pady=2)


def build_indicators(parent):
    lf = _labeled(parent, "Scale / progress / scrollbar / meter / floodgauge")
    ttk.Scale(lf, from_=0, to=100, value=60).pack(fill=X, pady=3)
    ttk.Progressbar(lf, value=55, bootstyle="success").pack(fill=X, pady=3)
    ttk.Progressbar(lf, value=70, bootstyle="info-striped").pack(fill=X, pady=3)
    ttk.Progressbar(lf, value=40, bootstyle="thin").pack(fill=X, pady=3)
    sbar = ttk.Scrollbar(lf, orient=HORIZONTAL)
    sbar.set(0.2, 0.6)
    sbar.pack(fill=X, pady=3)
    row = ttk.Frame(lf)
    row.pack(fill=X, pady=4)
    ttk.Meter(row, amount_used=45, subtext="meter", bootstyle="info",
              meter_size=140, interactive=True).pack(side=LEFT, padx=8)
    fg = ttk.Floodgauge(row, value=66, text="floodgauge", bootstyle="warning")
    fg.pack(side=LEFT, fill=X, expand=YES, padx=8)


def build_data(parent):
    lf = _labeled(parent, "Treeview / Tableview / ScrolledText / Notebook")
    nb = ttk.Notebook(lf)
    nb.pack(fill=BOTH, expand=YES)

    tv = ttk.Treeview(nb, columns=[0, 1], show=HEADINGS, height=4)
    tv.heading(0, text="City")
    tv.heading(1, text="Rank")
    for r in [("Auckland", 1), ("Paris", 2), ("Maui", 3), ("Tahiti", 4)]:
        tv.insert("", END, values=r)
    nb.add(tv, text="Treeview")

    tbl = ttk.Tableview(
        nb,
        coldata=["Name", "Score"],
        rowdata=[("Ada", 95), ("Linus", 88), ("Grace", 99), ("Alan", 77)],
        paginated=True,
        searchable=True,
        pagesize=3,
    )
    nb.add(tbl, text="Tableview")

    st = ttk.ScrolledText(nb, height=5, auto_hide=True)
    st.insert(END, "ScrolledText — auto-hiding scrollbar.\n" * 12)
    nb.add(st, text="ScrolledText")


def build_dialog_launcher(parent, app):
    lf = _labeled(parent, "Dialogs (open each; check light + dark)")
    row1 = ttk.Frame(lf)
    row1.pack(fill=X, pady=2)
    row2 = ttk.Frame(lf)
    row2.pack(fill=X, pady=2)

    def toast():
        ToastNotification(title="Toast", message="A toast notification.",
                          duration=3000, bootstyle="info").show_toast()

    buttons = [
        ("Info box", lambda: Messagebox.show_info("An info message.", "Info")),
        ("Question", lambda: Messagebox.yesno("Proceed?", "Question")),
        ("OK/Cancel", lambda: Messagebox.okcancel("Confirm action.", "Confirm")),
        ("Get string", lambda: Querybox.get_string(prompt="Your name?")),
        ("Get date", lambda: Querybox.get_date(parent=app)),
        ("Font dialog", lambda: FontDialog(parent=app).show()),
        ("Color chooser", lambda: ColorChooserDialog(parent=app).show()),
        ("Message dialog",
         lambda: MessageDialog("A custom MessageDialog.", title="Dialog",
                               buttons=["Cancel", "OK:primary"]).show()),
        ("Toast", toast),
    ]
    for i, (label, cmd) in enumerate(buttons):
        parent_row = row1 if i < 5 else row2
        ttk.Button(parent_row, text=label, command=cmd,
                   bootstyle="secondary-outline").pack(
            side=LEFT, padx=2, fill=X, expand=YES)


def build_controls(parent, app):
    bar = ttk.Frame(parent, padding=(8, 6))
    bar.pack(fill=X)
    style = app.style
    themes = style.theme_names()

    ttk.Label(bar, text="Theme:").pack(side=LEFT)
    picker = ttk.Combobox(bar, values=themes, width=22)
    picker.set(style.theme.name)
    picker.pack(side=LEFT, padx=6)
    picker.bind("<<ComboboxSelected>>",
                lambda e: style.theme_use(picker.get()))

    def on_toggle():
        app.toggle_theme()  # switches the current family's -light/-dark sibling
        picker.set(style.theme.name)

    ttk.Button(bar, text="Toggle light/dark", command=on_toggle,
               bootstyle="primary").pack(side=LEFT, padx=4)
    ttk.Button(bar, text="Recenter window", bootstyle="secondary-outline",
               command=app.place_window_center).pack(side=LEFT, padx=4)
    ttk.Label(bar, text="  (matrix: light/dark × 100/125/150/200% DPI × "
                        "win32/aqua/x11)").pack(side=LEFT, padx=8)


def main():
    app = ttk.Window("ttkbootstrap 2.0 — pre-release visual review",
                     themename="bootstrap-light", minsize=(1180, 720))
    build_controls(app, app)
    ttk.Separator(app).pack(fill=X)

    body = ttk.Frame(app, padding=6)
    body.pack(fill=BOTH, expand=YES)
    left = ttk.Frame(body)
    left.pack(side=LEFT, fill=BOTH, expand=YES)
    right = ttk.Frame(body)
    right.pack(side=LEFT, fill=BOTH, expand=YES)

    build_button_family(left)
    build_toggles(left)
    build_inputs(left)
    build_dialog_launcher(left, app)

    build_indicators(right)
    build_data(right)

    app.place_window_center()
    app.mainloop()


if __name__ == "__main__":
    main()
