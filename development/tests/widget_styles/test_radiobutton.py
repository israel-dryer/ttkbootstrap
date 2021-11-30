import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

def create_radiobutton_test(bootstyle, style, testname):
    frame = ttk.Frame(padding=10)

    var = tk.Variable()

    # title
    title = ttk.Label(frame, text=testname, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default style
    cb = ttk.Radiobutton(frame, text='default', bootstyle=bootstyle, value=0)
    cb.configure(variable=var)
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    # color styles
    for i, color in enumerate(style.colors):
        cb = ttk.Radiobutton(frame, text=color, bootstyle=f'{color}-{bootstyle}')
        cb.configure(variable=var, value=i+1)
        cb.pack(padx=5, pady=5, fill=tk.BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.Radiobutton(
        master=frame, 
        text=bootstyle, 
        bootstyle=bootstyle,
        state=tk.DISABLED,
        variable=var,
        value=i+1
    )
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_radiobutton_test('', style, 'Radiobutton')
    test1.pack(side=tk.LEFT, fill=tk.BOTH)
    test4 = create_radiobutton_test('toolbutton', style, 'Toolbutton')
    test4.pack(side=tk.LEFT, fill=tk.BOTH)
    test5 = create_radiobutton_test('outline-toolbutton', style, 'Outline Toolbutton')
    test5.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()