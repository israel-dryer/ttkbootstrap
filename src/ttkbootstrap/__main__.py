"""
    ttkbootstrap demo (modernized)

    This version uses the updated ttkbootstrap.widgets API
    and avoids legacy tk widget usage where possible.
"""
from ttkbootstrap import Style, Switch, ToolCheckbutton
from ttkbootstrap.widgets import (
    Frame, LabelFrame, Button, Checkbutton, Radiobutton, Entry,
    Spinbox, Combobox, DateEntry, Menubutton, Separator, Progressbar,
    Scrollbar, Scale, Treeview, Notebook, Meter, ScrolledText, Label
)
from ttkbootstrap.window import Window
from ttkbootstrap.dialogs import Messagebox

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

    style = Style.get_instance()
    theme_names = style.theme_names()

    root = Frame(master, padding=10)

    # Theme Selector
    theme_selection = Frame(root, padding=(10, 10, 10, 0))
    theme_selection.pack(fill="x", expand=1)

    header_font = Font(size=24, weight="bold")
    theme_selected = Label(theme_selection, text="litera", font=header_font)
    theme_selected.pack(side="left")

    lbl = Button(theme_selection, text="Select a theme:")
    lbl.pack(side="right")

    theme_cbo = Combobox(theme_selection, text=style.theme.name, values=theme_names)
    theme_cbo.pack(padx=10, side="right")
    theme_cbo.current(theme_names.index(style.theme.name))

    Separator(root).pack(fill="x", pady=10, padx=10)

    def change_theme(e):
        t = theme_cbo.get()
        style.theme_use(t)
        theme_selected.configure(text=t)
        theme_cbo.selection_clear()
        #default.focus_set()

    theme_cbo.bind("<<ComboboxSelected>>", change_theme)

    # Left and Right Panels
    lframe = Frame(root, padding=5)
    lframe.pack(side="left", fill="both", expand=1)

    rframe = Frame(root, padding=5)
    rframe.pack(side="right", fill="both", expand=1)

    # Theme colors
    color_group = LabelFrame(lframe, text="Theme color options", padding=10)
    color_group.pack(fill="x", side="top")

    for color in style.colors:
        Button(color_group, text=color, color=color).pack(side="left", expand=1, padx=5, fill="x")

    # Check & Radio
    rb_group = LabelFrame(lframe, text="Checkbuttons & radiobuttons", padding=10)
    rb_group.pack(fill="x", pady=10, side="top")

    check1 = Checkbutton(rb_group, text="selected")
    check1.pack(side="left", expand=1, padx=5)
    check1.invoke()

    check2 = Checkbutton(rb_group, text="alternate")
    check2.pack(side="left", expand=1, padx=5)

    check4 = Checkbutton(rb_group, text="deselected")
    check4.pack(side="left", expand=1, padx=5)
    check4.invoke()
    check4.invoke()

    Checkbutton(rb_group, color="primary", text="disabled", state="disabled").pack(side="left", expand=1, padx=5)

    radio1 = Radiobutton(rb_group, text="selected", value=1)
    radio1.pack(side="left", expand=1, padx=5)
    radio1.invoke()

    Radiobutton(rb_group, text="deselected", value=2, color="danger").pack(side="left", expand=1, padx=5)
    Radiobutton(rb_group, text="disabled", value=3, state="disabled").pack(side="left", expand=1, padx=5)

    # Table + Notebook
    ttframe = Frame(lframe)
    ttframe.pack(pady=5, fill="x", side="top")

    table_data = [
        ("South Island, New Zealand", 1),
        ("Paris", 2),
        ("Bora Bora", 3),
        ("Maui", 4),
        ("Tahiti", 5),
    ]

    tv = Treeview(ttframe, columns=[0, 1], show="headings", height=5)
    for row in table_data:
        tv.insert("", "end", values=row)
    tv.selection_set("I001")
    tv.heading(0, text="City")
    tv.heading(1, text="Rank")
    tv.column(0, width=300)
    tv.column(1, width=70, anchor="center")
    tv.pack(side="left", anchor="ne", fill="x")

    nb = Notebook(ttframe, color="primary")
    nb.pack(side="left", padx=(10, 0), expand=1, fill="both")
    nb.add(Button(nb, text="This is a notebook tab.\nYou can put any widget you want here."), text="Tab 1")
    nb.add(Button(nb, text="A notebook tab."), text="Tab 2")
    for i in range(3, 6):
        nb.add(Frame(nb), text=f"Tab {i}")

    # Text + Meter + Scale + Progressbar
    txt = ScrolledText(lframe, height=5, width=50, autohide=True)
    txt.insert("end", ZEN)
    txt.pack(side="left", anchor="n", fill="both", expand=1)

    lframe_inner = Frame(lframe)
    lframe_inner.pack(fill="both", expand=1, padx=10)

    Scale(lframe_inner, orient="horizontal", value=75, from_=100, to=0).pack(fill="x", pady=5, expand=1)

    Progressbar(lframe_inner, orient="horizontal", value=50).pack(fill="x", pady=5, expand=1)
    Progressbar(lframe_inner, orient="horizontal", value=75, variant="striped", color="success").pack(fill="x", pady=5, expand=1)

    Meter(lframe_inner, metersize=150, amountused=45, subtext="meter widget", color="info", interactive=True).pack(pady=10)

    Scrollbar(lframe_inner, orient="horizontal").pack(fill="x", pady=5, expand=1)
    Scrollbar(lframe_inner, orient="horizontal", color="danger", variant="round").pack(fill="x", pady=5, expand=1)

    # Buttons
    btn_group = LabelFrame(rframe, text="Buttons", padding=(10, 5))
    btn_group.pack(fill="x")

    default = Button(btn_group, text="solid button")
    default.pack(fill="x", pady=5)
    default.focus_set()

    # menu = master.create_menu()
    # for i, t in enumerate(style.theme_names()):
    #     menu.add_radiobutton(label=t, value=i)

    # Menubutton(btn_group, text="solid menubutton", color="secondary", menu=menu).pack(fill=X, pady=5)
    ToolCheckbutton(btn_group, text="Solid ToolCheckbutton", color="success").pack(fill="x", pady=5)
    Button(btn_group, text="outline button", color="info", variant="outline").pack(fill="x", pady=5)#, command=lambda: Messagebox.ok("You pushed an outline button")).pack(fill="x", pady=5)
    # Menubutton(btn_group, text="outline menubutton", color="warning", variant="outline", menu=menu).pack(fill=X, pady=5)
    ToolCheckbutton(btn_group, text="Outline ToolCheckbutton", color="success", variant="outline").pack(fill="x", pady=5)

    Button(btn_group, text="link button", variant="link").pack(fill="x", pady=5)
    Switch(btn_group, text="Rounded Switch", color="success", variant="round").pack(fill="x", pady=5)
    Switch(btn_group, text="Squared Switch", variant="square").pack(fill="x", pady=5)

    # Input widgets
    input_group = LabelFrame(rframe, text="Other input widgets", padding=10)
    input_group.pack(fill="both", pady=(10, 5), expand=1)

    e = Entry(input_group)
    e.pack(fill="x")
    e.insert("end", "entry widget")

    pw = Entry(input_group, show="•")
    pw.pack(fill="x", pady=5)
    pw.insert("end", "password")

    sp = Spinbox(input_group, from_=0, to=100)
    sp.pack(fill="x")
    sp.set(45)

    cbo = Combobox(input_group, text=style.theme.name, values=theme_names, exportselection=False)
    cbo.pack(fill="x", pady=5)
    cbo.current(theme_names.index(style.theme.name))

    DateEntry(input_group).pack(fill="x")

    return root


if __name__ == "__main__":
    app = Window(title="ttkbootstrap widget demo")
    demo = setup_demo(app)
    demo.pack(fill="both", expand=1)
    app.mainloop()
