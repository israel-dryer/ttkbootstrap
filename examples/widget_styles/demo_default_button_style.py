"""Visual demo / validation for issue #1062.

The bug: an app that creates only *styled* buttons (e.g. Outline.Toolbutton)
left the base ``TButton`` style unthemed. Native ttk widgets that the app
never builds directly -- like the ``ttk::button`` widgets inside Tk's file
dialog on Linux -- then rendered with the bare clam look ("lost coloring").

Tk's dialog buttons are created as raw ``ttk::button`` widgets, *not* via
ttkbootstrap's overridden constructor, so they never trigger the lazy
style builder. This demo reproduces that exact path with ``tk.call`` so
the effect is visible on every platform, not just Linux.

Run it:  python tests/widget_styles/demo_default_button_style.py

With the fix, the "simulated dialog button" on the right is themed (it
matches the app's primary color). Revert the fix in style.py and it
renders as a plain grey clam button instead.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window("Issue #1062 - base TButton theming", themename="sandstone")
app.geometry("560x260")

frame = ttk.Frame(app, padding=20)
frame.pack(fill=BOTH, expand=YES)

ttk.Label(
    frame,
    text="This app creates ONLY a styled button (Outline.Toolbutton).",
    font="-size 10",
).pack(anchor=W, pady=(0, 12))

# 1. The only ttkbootstrap button the app builds -- a styled one.
left = ttk.Labelframe(frame, text="App button (styled)", padding=15)
left.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))
ttk.Button(left, text="Browse", style="Outline.Toolbutton").pack()

# 2. A raw ttk::button created the way Tk's file dialog does -- this uses
#    the base "TButton" style and never goes through ttkbootstrap.
right = ttk.Labelframe(frame, text="Simulated dialog button (raw ttk::button)", padding=15)
right.pack(side=LEFT, fill=BOTH, expand=YES)
raw_path = str(right) + ".rawbtn"
app.tk.call("ttk::button", raw_path, "-text", "OK")
app.tk.call("pack", raw_path)

bg = app.tk.call("ttk::style", "lookup", "TButton", "-background")
ttk.Label(
    frame,
    text=f"base TButton background = {bg}   (theme primary = {ttk.Style().colors.primary})",
    font="-size 9",
    bootstyle="secondary",
).pack(side=BOTTOM, anchor=W, pady=(12, 0))

app.mainloop()