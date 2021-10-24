import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets.calendar import DateEntry, ask_date

DARK = 'superhero'
LIGHT = 'flatly'


def calendar_style_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default button
    btn = ttk.Button(frame, text=widget_style)
    btn.pack(padx=5, pady=5, fill=tk.BOTH, expand=tk.YES)
    btn.configure(command=lambda: ask_date(btn, style=widget_style))

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    calendar_style_frame(
        widget_style='TCalendar',
        style=style
    ).pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    for color in style.colors:
        DateEntry(root, style=f'{color}.TCalendar').pack(padx=10, pady=10)

    root.mainloop()
