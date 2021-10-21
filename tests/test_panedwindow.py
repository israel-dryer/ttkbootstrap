import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_panedwindow_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    pw = ttk.PanedWindow(frame, orient=tk.HORIZONTAL, style=widget_style)
    pw.pack(padx=5, pady=5, fill=tk.BOTH)
    pw.add(ttk.Frame(pw, width=200, height=200, style='info.TFrame'))
    pw.add(ttk.Frame(pw, width=200, height=200, style='success.TFrame'))

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_panedwindow_frame('TPanedwindow', style).pack(side=tk.LEFT)

    root.mainloop()
