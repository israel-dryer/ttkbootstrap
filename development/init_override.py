from tkinter import ttk

widgets = (
    ttk.Button,
    ttk.Checkbutton,
    ttk.Combobox,
    ttk.Entry,
    ttk.Frame,
    ttk.Label,
    ttk.Labelframe,
    ttk.Menubutton,
    ttk.Notebook,
    ttk.Panedwindow,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.Treeview
)

def wrapper(func):
    def inner(*args, **kwargs):
        print("wrapper called")
        func(*args, **kwargs)
    return inner

for widget in widgets:
    widget.__init__ = wrapper(widget.__init__)

