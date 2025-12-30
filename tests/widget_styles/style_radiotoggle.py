import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_radio_toggle_test(bootstyle, name):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    sig = ttk.Signal('primary')

    # default style
    cb = ttk.RadioToggle(frame, text='default', variant=bootstyle)
    cb.pack(padx=5, pady=5, fill=BOTH)
    cb.invoke()

    # color styles
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        cb = ttk.RadioToggle(
            master=frame,
            text=color,
            signal=sig,
            value=color,
            color=color,
            variant=bootstyle,
            width=15
        )
        cb.pack(padx=5, pady=5, fill=BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.RadioToggle(
        master=frame,
        text='disabled',
        value='disabled',
        variant=bootstyle,
        state=DISABLED
    )
    cb.pack(padx=5, pady=5, fill=BOTH)
    cb.invoke()

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.App(title="RadioToggle Test")

    test4 = create_radio_toggle_test('default','Default')
    test4.pack(side='left', fill=BOTH)
    test5 = create_radio_toggle_test('outline','Outline')
    test5.pack(side='left', fill=BOTH)
    test6 = create_radio_toggle_test('ghost','Ghost')
    test6.pack(side='left', fill=BOTH)

    btn = ttk.Button(text="Change Theme", command=ttk.toggle_theme)
    btn.pack(padx=10, pady=10)

    root.mainloop()
