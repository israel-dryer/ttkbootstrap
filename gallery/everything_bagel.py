import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility

utility.enable_high_dpi_awareness()

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

    root = ttk.Frame(master, padding=10)
    style = ttk.Style()
    theme_names = style.theme_names()

    theme_selection = ttk.Frame(root, padding=(10, 10, 10, 0))
    theme_selection.pack(fill=tk.X, expand=tk.YES)

    theme_selected = ttk.Label(theme_selection, text="litera", font="-size 24 -weight bold")
    theme_selected.pack(side=tk.LEFT)

    lbl = ttk.Label(theme_selection, text="Select a theme:")
    theme_cbo = ttk.Combobox(
        master=theme_selection,
        text=style.theme.name,
        values=theme_names,
    )
    theme_cbo.pack(padx=10, side=tk.RIGHT)
    theme_cbo.current(theme_names.index(style.theme.name))
    lbl.pack(side=tk.RIGHT)

    ttk.Separator(root).pack(fill=tk.X, pady=10, padx=10)

    def change_theme(e):
        t = cbo.get()
        style.theme_use(t)
        theme_selected.configure(text=t)
        theme_cbo.selection_clear()    
        default.focus_set()

    theme_cbo.bind('<<ComboboxSelected>>', change_theme)

    lframe = ttk.Frame(root, padding=5)
    lframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    rframe = ttk.Frame(root, padding=5)
    rframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)

    color_group = ttk.Labelframe(
        master=lframe,
        text="Theme color options",
        padding=10
    )
    color_group.pack(fill=tk.X, side=tk.TOP)

    for color in style.colors:
        cb = ttk.Button(color_group, text=color, bootstyle=color)
        cb.pack(side=tk.LEFT, expand=tk.YES, padx=5, fill=tk.X)

    rb_group = ttk.Labelframe(
        lframe, text="Checkbuttons & radiobuttons", padding=10)
    rb_group.pack(fill=tk.X, pady=10, side=tk.TOP)

    check1 = ttk.Checkbutton(rb_group, text="selected")
    check1.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    check1.invoke()
    check2 = ttk.Checkbutton(rb_group, text="deselected")
    check2.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    check3 = ttk.Checkbutton(rb_group, text="disabled", state=tk.DISABLED)
    check3.pack(side=tk.LEFT, expand=tk.YES, padx=5)

    radio1 = ttk.Radiobutton(rb_group, text="selected", value=1)
    radio1.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    radio1.invoke()
    radio2 = ttk.Radiobutton(rb_group, text="deselected", value=2)
    radio2.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    radio3 = ttk.Radiobutton(rb_group, text="disabled",
                             value=3, state=tk.DISABLED)
    radio3.pack(side=tk.LEFT, expand=tk.YES, padx=5)

    ttframe = ttk.Frame(lframe)
    ttframe.pack(pady=5, fill=tk.X, side=tk.TOP)

    table_data = [
        ('South Island, New Zealand', 1),
        ('Paris', 2),
        ('Bora Bora', 3),
        ('Maui', 4),
        ('Tahiti', 5)
    ]

    tv = ttk.Treeview(
        master=ttframe,
        columns=[0, 1],
        show='headings',
        height=5
    )
    for row in table_data:
        tv.insert('', tk.END, values=row)

    tv.selection_set('I001')
    tv.heading(0, text='City')
    tv.heading(1, text='Rank')
    tv.column(0, width=300)
    tv.column(1, width=70, anchor=tk.CENTER)
    tv.pack(side=tk.LEFT, anchor=tk.NE, fill=tk.X)

    # # notebook with table and text tabs
    nb = ttk.Notebook(ttframe)
    nb.pack(
        side=tk.LEFT,
        padx=(10, 0),
        expand=tk.YES,
        fill=tk.BOTH
    )
    nb_text = "This is a notebook tab.\nYou can put any widget you want here."
    nb.add(ttk.Label(nb, text=nb_text), text="Tab 1", sticky=tk.NW)
    nb.add(
        child=ttk.Label(nb, text="A notebook tab."),
        text="Tab 2",
        sticky=tk.NW
    )
    nb.add(ttk.Frame(nb), text='Tab 3')
    nb.add(ttk.Frame(nb), text='Tab 4')
    nb.add(ttk.Frame(nb), text='Tab 5')

    # text widget
    txt = tk.Text(
        master=lframe,
        height=5,
        width=50,
        wrap='none'
    )
    txt.insert(tk.END, ZEN)
    txt.pack(
        side=tk.LEFT,
        anchor=tk.NW,
        pady=5,
        fill=tk.BOTH,
        expand=tk.YES
    )
    lframe_inner = ttk.Frame(lframe)
    lframe_inner.pack(
        fill=tk.BOTH,
        expand=tk.YES,
        padx=10
    )
    s1 = ttk.Scale(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=75,
        from_=100,
        to=0
    )
    s1.pack(fill=tk.X, pady=5, expand=tk.YES)

    ttk.Progressbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=50,
    ).pack(fill=tk.X, pady=5, expand=tk.YES)

    ttk.Progressbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        value=75,
        bootstyle='success-striped'
    ).pack(fill=tk.X, pady=5, expand=tk.YES)

    m = ttk.Meter(
        master=lframe_inner,
        metersize=150,
        amountused=45,
        subtext='meter widget',
        bootstyle='info',
        interactive=True
    )
    m.pack(pady=10)

    sb = ttk.Scrollbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
    )
    sb.set(0.1, 0.9)
    sb.pack(fill=tk.X, pady=5, expand=tk.YES)

    sb = ttk.Scrollbar(
        master=lframe_inner,
        orient=tk.HORIZONTAL,
        bootstyle='danger-round'
    )
    sb.set(0.1, 0.9)
    sb.pack(fill=tk.X, pady=5, expand=tk.YES)

    btn_group = ttk.Labelframe(
        master=rframe,
        text="Buttons",
        padding=(10, 5)
    )
    btn_group.pack(fill=tk.X)

    menu = tk.Menu(root)
    for i, t in enumerate(style.theme_names()):
        menu.add_radiobutton(label=t, value=i)

    default = ttk.Button(
        master=btn_group,
        text="solid button"
    )
    default.pack(fill=tk.X, pady=5)
    default.focus_set()

    mb = ttk.Menubutton(
        master=btn_group,
        text="solid menubutton",
        bootstyle="secondary", menu=menu
    )
    mb.pack(fill=tk.X, pady=5)

    cb = ttk.Checkbutton(
        master=btn_group,
        text="solid toolbutton",
        bootstyle="success-toolbutton",
    )
    cb.invoke()
    cb.pack(fill=tk.X, pady=5)

    ob = ttk.Button(
        master=btn_group,
        text="outline button",
        bootstyle='info-outline'
    )
    ob.pack(fill=tk.X, pady=5)

    mb = ttk.Menubutton(
        master=btn_group,
        text="outline menubutton",
        bootstyle="warning-outline",
        menu=menu
    )
    mb.pack(fill=tk.X, pady=5)

    cb = ttk.Checkbutton(
        master=btn_group,
        text="outline toolbutton",
        bootstyle="success-outline-toolbutton"
    )
    cb.pack(fill=tk.X, pady=5)

    lb = ttk.Button(
        master=btn_group,
        text="link button",
        bootstyle='link'
    )
    lb.pack(fill=tk.X, pady=5)

    cb1 = ttk.Checkbutton(
        master=btn_group,
        text="rounded toggle",
        bootstyle="success-round-toggle",
    )
    cb1.invoke()
    cb1.pack(fill=tk.X, pady=5)

    cb2 = ttk.Checkbutton(
        master=btn_group,
        text="squared toggle",
        bootstyle="square-toggle"
    )
    cb2.pack(fill=tk.X, pady=5)
    cb2.invoke()

    input_group = ttk.Labelframe(
        master=rframe,
        text="Other input widgets",
        padding=10
    )
    input_group.pack(
        fill=tk.BOTH,
        pady=(10, 5),
        expand=tk.YES
    )
    entry = ttk.Entry(input_group)
    entry.pack(fill=tk.X)
    entry.insert(tk.END, "entry widget")

    password = ttk.Entry(
        master=input_group,
        show="•"
    )
    password.pack(fill=tk.X, pady=5)
    password.insert(tk.END, "password")

    spinbox = ttk.Spinbox(
        master=input_group,
        from_=0,
        to=100
    )
    spinbox.pack(fill=tk.X)
    spinbox.set(45)

    cbo = ttk.Combobox(
        master=input_group,
        text=style.theme.name,
        values=theme_names,
        exportselection=False
    )
    cbo.pack(fill=tk.X, pady=5)
    cbo.current(theme_names.index(style.theme.name))

    de = ttk.DateEntry(input_group)
    de.pack(fill=tk.X)

    return root

if __name__ == '__main__':

    root = tk.Tk()
    
    bagel = setup_demo(root)
    bagel.pack(fill=tk.BOTH, expand=tk.YES)

    root.mainloop()
