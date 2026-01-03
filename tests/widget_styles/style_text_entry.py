import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import get_style


def create_entry_test():
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Entry', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    entry = ttk.TextEntry(frame)
    entry.pack(padx=5, pady=5, fill=BOTH)
    entry.insert(END, 'default')

    # color
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        entry = ttk.TextEntry(frame, accent=color)
        entry.pack(padx=5, pady=5, fill=BOTH)
        entry.insert(END, color)

    # readonly
    entry = ttk.TextEntry(frame)
    entry.insert(END, 'readonly')
    entry.configure(state=READONLY)

    entry.pack(padx=5, pady=5, fill=BOTH)

    # disabled
    entry = ttk.TextEntry(frame)
    entry.insert(END, 'disabled')
    entry.configure(state=DISABLED)
    entry.pack(padx=5, pady=5, fill=BOTH)

    return frame


if __name__ == '__main__':
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    test1 = create_entry_test()
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
