import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

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
    spinbox.insert(tk.END, 'default')

    # color
    for color in style.theme.colors:
        spinbox = ttk.Spinbox(frame, bootstyle=color)
        spinbox.pack(padx=5, pady=5, fill=tk.BOTH)
        spinbox.insert(tk.END, color)

    # disabled
    spinbox = ttk.Spinbox(frame)
    spinbox.insert(tk.END, 'disabled')
    spinbox.configure(state=tk.DISABLED)
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)

    # readonly
    spinbox = ttk.Spinbox(frame)
    spinbox.insert(tk.END, 'readonly')
    spinbox.configure(state='readonly')
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)    

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_spinbox_test('', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()
