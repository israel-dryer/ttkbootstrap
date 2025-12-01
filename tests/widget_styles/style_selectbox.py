import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_combobox_test(bootstyle, test_name):
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
    cbo = ttk.SelectBox(
        master=frame,
        value='default',
        items=['default', 'other'],
        allow_custom_values=True,
        show_dropdown_button=True,
        bootstyle=bootstyle,
    )
    cbo.pack(padx=5, pady=5, fill=BOTH)

    # color
    for color in ['default', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        cbo = ttk.SelectBox(
            master=frame,
            value=color,
            items=['default', 'primary', 'secondary', 'success', 'info', 'warning', 'danger'],
            bootstyle=color,
        )
        cbo.pack(padx=5, pady=5, fill=BOTH)

    # disabled
    cbo = ttk.SelectBox(
        value='other',
        master=frame,
        items=[bootstyle, 'other'],
        bootstyle=bootstyle,
        state='disabled'
    )
    cbo.pack(padx=5, pady=5, fill='both')
    return frame


def change_style():
    if style.theme_use() == 'light':
        style.theme_use('dark')
    else:
        style.theme_use('light')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_combobox_test(None, 'Combobox')
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
