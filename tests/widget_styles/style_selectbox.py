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
        value='primary',
        items=['other'],
        allow_custom_values=True,
        show_dropdown_button=True
    )
    cbo.pack(padx=5, pady=5, fill=BOTH)

    # color
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        cbo = ttk.SelectBox(
            master=frame,
            value=color,
            items=['primary', 'secondary', 'success', 'info', 'warning', 'danger'],
            color=color,
        )
        cbo.pack(padx=5, pady=5, fill=BOTH)

    # disabled
    cbo = ttk.SelectBox(
        value='other',
        master=frame,
        items=['other'],
        state='disabled'
    )
    cbo.pack(padx=5, pady=5, fill='both')
    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    test1 = create_combobox_test(None, 'Combobox')
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
