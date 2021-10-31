import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_radiobutton_test(bootstyle, style, testname):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=testname, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default style
    cb = ttk.Radiobutton(frame, text='default', bootstyle=bootstyle)
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    # color styles
    for color in style.theme.colors:
        cb = ttk.Radiobutton(frame, text=color, bootstyle=(color, bootstyle))
        cb.pack(padx=5, pady=5, fill=tk.BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.Radiobutton(
        master=frame, 
        text=bootstyle, 
        bootstyle=bootstyle,
        state=tk.DISABLED
    )
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_radiobutton_test('', style, 'Radiobutton')
    test1.pack(side=tk.LEFT, fill=tk.BOTH)
    test2 = create_radiobutton_test('round', style, 'Roundtoggle')
    test2.pack(side=tk.LEFT, fill=tk.BOTH)
    test3 = create_radiobutton_test('square', style, 'Squaretoggle')
    test3.pack(side=tk.LEFT, fill=tk.BOTH)
    test4 = create_radiobutton_test('toolbutton', style, 'Toolbutton')
    test4.pack(side=tk.LEFT, fill=tk.BOTH)
    test5 = create_radiobutton_test('outline-toolbutton', style, 'Outline Toolbutton')
    test5.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()