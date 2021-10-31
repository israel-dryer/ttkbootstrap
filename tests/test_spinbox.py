import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_spinbox_test(bootstyle, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Spinbox', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    spinbox = ttk.Spinbox(frame)
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)
    spinbox.insert(tk.END, bootstyle)

    # color
    for color in style.theme.colors:
        spinbox = ttk.Spinbox(frame, bootstyle=color)
        spinbox.pack(padx=5, pady=5, fill=tk.BOTH)
        spinbox.insert(tk.END, color)

    # disabled
    spinbox = ttk.Spinbox(frame)
    spinbox.insert(tk.END, bootstyle)
    spinbox.configure(state=tk.DISABLED)
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_spinbox_test('', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()
