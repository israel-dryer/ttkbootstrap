import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_combobox_test(test_name):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(
        master=frame,
        text=test_name,
        anchor=CENTER
    )
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    cbo = ttk.Combobox(
        master=frame,
        values=['default', 'other']
    )
    cbo.pack(padx=5, pady=5, fill=BOTH)
    cbo.current(0)

    # color
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        cbo = ttk.Combobox(
            master=frame,
            values=[color, 'other'],
            accent=color,
        )
        cbo.pack(padx=5, pady=5, fill=BOTH)
        cbo.current(0)

    # disabled
    cbo = ttk.Combobox(
        master=frame,
        values=['None', 'other'],
        state=DISABLED
    )
    cbo.pack(padx=5, pady=5, fill=BOTH)
    cbo.current(0)

    return frame


def change_style():
    if ttk.get_theme() == 'light':
        ttk.set_theme('dark')
    else:
        ttk.set_theme('light')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App("ComboBox Demo")

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_combobox_test('Combobox')
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
