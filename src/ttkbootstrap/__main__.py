"""
    ttkbootstrap demo (modernized)

    This version uses the updated ttkbootstrap.widgets API
    and avoids legacy tk widget usage where possible.
"""

from ttkbootstrap.widgets import (
    Frame, Labelframe, Button, Checkbutton, Radiobutton, Entry,
    Spinbox, Combobox, DateEntry, Menubutton, Separator, Progressbar,
    Scrollbar, Scale, Treeview, Notebook, Meter, ScrolledText
)
from ttkbootstrap.window import Window
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from tkinter import CENTER, END, LEFT, RIGHT, TOP, BOTTOM, BOTH, X, Y, NSEW
from tkinter import Label
from tkinter.font import Font


def setup_demo(master):
    ZEN = """Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

    style = master.style
    theme_names = style.theme_names()

    root = Frame(master, padding=10)

    # Theme Selector
    theme_selection = Frame(root, padding=(10, 10, 10, 0))
    theme_selection.pack(fill=X, expand=YES)

    header_font = Font(size=24, weight="bold")
    theme_selected = Label(theme_selection, text="litera", font=header_font)
    theme_selected.pack(side=LEFT)

    lbl = Button(theme_selection, text="Select a theme:")
    lbl.pack(side=RIGHT)

    theme_cbo = Combobox(theme_selection, text=style.theme.name, values=theme_names)
    theme_cbo.pack(padx=10, side=RIGHT)
    theme_cbo.current(theme_names.index(style.theme.name))

    Separator(root).pack(fill=X, pady=10, padx=10)

    def change_theme(e):
        t = theme_cbo.get()
        style.theme_use(t)
        theme_selected.configure(text=t)
        theme_cbo.selection_clear()
        default.focus_set()

    theme_cbo.bind("<<ComboboxSelected>>", change_theme)

    # Left and Right Panels
    lframe = Frame(root, padding=5)
    lframe.pack(side=LEFT, fill=BOTH, expand=YES)

    rframe = Frame(root, padding=5)
    rframe.pack(side=RIGHT, fill=BOTH, expand=YES)

    # Theme colors
    color_group = Labelframe(lframe, text="Theme color options", padding=10)
    color_group.pack(fill=X, side=TOP)

    for color in style.colors:
        Button(color_group, text=color, color=color).pack(side=LEFT, expand=YES, padx=5, fill=X)

    # Check & Radio
    rb_group = Labelframe(lframe, text="Checkbuttons & radiobuttons", padding=10)
    rb_group.pack(fill=X, pady=10, side=TOP)

    check1 = Checkbutton(rb_group, text="selected")
    check1.pack(side=LEFT, expand=YES, padx=5)
    check1.invoke()

    check2 = Checkbutton(rb_group, text="alternate")
    check2.pack(side=LEFT, expand=YES, padx=5)

    check4 = Checkbutton(rb_group, text="deselected")
    check4.pack(side=LEFT, expand=YES, padx=5)
    check4.invoke()
    check4.invoke()

    Checkbutton(rb_group, text="disabled", state=DISABLED).pack(side=LEFT, expand=YES, padx=5)

    radio1 = Radiobutton(rb_group, text="selected", value=1)
    radio1.pack(side=LEFT, expand=YES, padx=5)
    radio1.invoke()

    Radiobutton(rb_group, text="deselected", value=2).pack(side=LEFT, expand=YES, padx=5)
    Radiobutton(rb_group, text="disabled", value=3, state=DISABLED).pack(side=LEFT, expand=YES, padx=5)

    # Table + Notebook
    ttframe = Frame(lframe)
    ttframe.pack(pady=5, fill=X, side=TOP)

    table_data = [
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
    ]

    tv = Treeview(ttframe, columns=[0, 1], show=HEADINGS, height=5)
    for row in table_data:
        tv.insert("", END, values=row)
    tv.selection_set("I001")
    tv.heading(0, text="City")
    tv.heading(1, text="Rank")
    tv.column(0, width=300)
    tv.column(1, width=70, anchor=CENTER)
    tv.pack(side=LEFT, anchor="ne", fill=X)

    nb = Notebook(ttframe)
    nb.pack(side=LEFT, padx=(10, 0), expand=YES, fill=BOTH)
    nb.add(Button(nb, text="This is a notebook tab.\nYou can put any widget you want here."), text="Tab 1")
    nb.add(Button(nb, text="A notebook tab."), text="Tab 2")
    for i in range(3, 6):
        nb.add(Frame(nb), text=f"Tab {i}")

    # Text + Meter + Scale + Progressbar
    txt = ScrolledText(lframe, height=5, width=50, autohide=True)
    txt.insert(END, ZEN)
    txt.pack(side=LEFT, anchor="nw", pady=5, fill=BOTH, expand=YES)

    lframe_inner = Frame(lframe)
    lframe_inner.pack(fill=BOTH, expand=YES, padx=10)

    Scale(lframe_inner, orient=HORIZONTAL, value=75, from_=100, to=0).pack(fill=X, pady=5, expand=YES)

    Progressbar(lframe_inner, orient=HORIZONTAL, value=50).pack(fill=X, pady=5, expand=YES)
    Progressbar(lframe_inner, orient=HORIZONTAL, value=75, variant="striped", color="success").pack(fill=X, pady=5, expand=YES)

    Meter(lframe_inner, metersize=150, amountused=45, subtext="meter widget", color="info", interactive=True).pack(pady=10)

    Scrollbar(lframe_inner, orient=HORIZONTAL).pack(fill=X, pady=5, expand=YES)
    Scrollbar(lframe_inner, orient=HORIZONTAL, color="danger", variant="round").pack(fill=X, pady=5, expand=YES)

    # Buttons
    btn_group = Labelframe(rframe, text="Buttons", padding=(10, 5))
    btn_group.pack(fill=X)

    default = Button(btn_group, text="solid button")
    default.pack(fill=X, pady=5)
    default.focus_set()

    menu = master.create_menu()
    for i, t in enumerate(style.theme_names()):
        menu.add_radiobutton(label=t, value=i)

    Menubutton(btn_group, text="solid menubutton", color="secondary", menu=menu).pack(fill=X, pady=5)
    Checkbutton(btn_group, text="solid toolbutton", color="success", variant="toolbutton").pack(fill=X, pady=5)

    Button(btn_group, text="outline button", color="info", variant="outline", command=lambda: Messagebox.ok("You pushed an outline button")).pack(fill=X, pady=5)
    Menubutton(btn_group, text="outline menubutton", color="warning", variant="outline", menu=menu).pack(fill=X, pady=5)
    Checkbutton(btn_group, text="outline toolbutton", color="success", variant="outline toolbutton").pack(fill=X, pady=5)

    Button(btn_group, text="link button", variant="link").pack(fill=X, pady=5)
    Checkbutton(btn_group, text="rounded toggle", color="success", variant="round toggle").pack(fill=X, pady=5)
    Checkbutton(btn_group, text="squared toggle", variant="square toggle").pack(fill=X, pady=5)

    # Input widgets
    input_group = Labelframe(rframe, text="Other input widgets", padding=10)
    input_group.pack(fill=BOTH, pady=(10, 5), expand=YES)

    e = Entry(input_group)
    e.pack(fill=X)
    e.insert(END, "entry widget")

    pw = Entry(input_group, show="•")
    pw.pack(fill=X, pady=5)
    pw.insert(END, "password")

    sp = Spinbox(input_group, from_=0, to=100)
    sp.pack(fill=X)
    sp.set(45)

    cbo = Combobox(input_group, text=style.theme.name, values=theme_names, exportselection=False)
    cbo.pack(fill=X, pady=5)
    cbo.current(theme_names.index(style.theme.name))

    DateEntry(input_group).pack(fill=X)

    return root


if __name__ == "__main__":
    app = Window(title="ttkbootstrap widget demo")
    demo = setup_demo(app)
    demo.pack(fill=BOTH, expand=YES)
    app.mainloop()
