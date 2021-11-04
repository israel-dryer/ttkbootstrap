import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

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


root = tk.Tk()
root.title("ttkbootstrap widget demo")
style = Style()
style.theme_use('superhero')
theme_names = style.theme_names()

sb1 = ttk.Scrollbar(root, orient=tk.HORIZONTAL)
sb1.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES, padx=10, pady=10)
sb1.set(0.2, 0.6)

pb = ttk.Progressbar(root, value=75, bootstyle='striped')
pb.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES, padx=10)
pb.start(100)

lframe = ttk.Frame(root, padding=10)
lframe.pack(side=tk.LEFT, fill=tk.BOTH)

rframe = ttk.Frame(root, padding=10)
rframe.pack(side=tk.RIGHT, fill=tk.BOTH)

theme_frame = ttk.Frame(lframe)
theme_frame.pack(fill=tk.X, pady=15, side=tk.TOP)

ttk.Label(theme_frame, text="Theme").pack(side=tk.LEFT)

cbo = ttk.Combobox(
    master=theme_frame,
    text=style.theme.name,
    values=theme_names,
    bootstyle='info'
)
cbo.pack(side=tk.LEFT, padx=10)
cbo.current(theme_names.index(style.theme.name))


def change_theme(e):
    t = cbo.get()
    style.theme_use(t)
    # root.configure(background=root.theme.colors.background)


cbo.bind('<<ComboboxSelected>>', change_theme)

cb1 = ttk.Checkbutton(
    master=theme_frame,
    text="rounded toggle",
    bootstyle="round",
)
cb1.pack(side=tk.RIGHT)
cb1.invoke()

cb2 = ttk.Checkbutton(
    master=theme_frame,
    text="squared toggle",
    bootstyle="square"
)
cb2.pack(side=tk.RIGHT, padx=10)
cb2.invoke()

cb_group = ttk.Labelframe(
    master=lframe,
    text="Check & Toggle buttons",
    padding=10
)
cb_group.pack(fill=tk.X, side=tk.TOP)

for color in style.colors:
    cb = ttk.Checkbutton(cb_group, text=color, bootstyle=color)
    cb.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    cb.invoke()

cb = ttk.Checkbutton(cb_group, text="disabled", state=tk.DISABLED)
cb.pack(side=tk.LEFT, expand=tk.YES, padx=5)

radio_var = tk.Variable()
rb_group = ttk.Labelframe(lframe, text="Radiobuttons", padding=10)
rb_group.pack(fill=tk.X, pady=10, side=tk.TOP)

for i, color in enumerate(style.colors):
    rb = ttk.Radiobutton(
        master=rb_group,
        value=i,
        text=color,
        variable=radio_var,
        bootstyle=color
    )
    rb.pack(side=tk.LEFT, expand=tk.YES, padx=5)
    rb.invoke()

rb = ttk.Radiobutton(
    master=rb_group,
    value=i+1,
    text="disabled",
    variable=radio_var,
    state=tk.DISABLED
)
rb.pack(side=tk.LEFT, expand=tk.YES, padx=5)

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
tv.column(1, width=50, anchor=tk.CENTER)
tv.pack(side=tk.LEFT, anchor=tk.NE, padx=(0, 2))

# text widget
txt = tk.Text(ttframe, height=5, width=50)
txt.insert(tk.END, ZEN)
txt.pack(side=tk.RIGHT, anchor=tk.NW, padx=(2, 0), fill=tk.Y)

# # notebook with table and text tabs
nb = ttk.Notebook(lframe)
nb.pack(pady=5, fill=tk.BOTH, expand=True)
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

btn_group = ttk.Labelframe(rframe, text="Buttons", padding=10)
btn_group.pack(fill=tk.X)

menu = tk.Menu(root)
for i, t in enumerate(style.theme_names()):
    menu.add_radiobutton(label=t, value=i)

mb = ttk.Menubutton(btn_group, text="Menubutton", menu=menu)
mb.pack(fill=tk.X, pady=5)

default = ttk.Button(btn_group, text="Default button")
default.pack(fill=tk.X)
default.focus_set()

ob = ttk.Button(btn_group, text="Outline button", bootstyle='outline')
ob.pack(fill=tk.X, pady=5)

lb = ttk.Button(btn_group, text="Link button", bootstyle='link')
lb.pack(fill=tk.X, pady=5)

input_group = ttk.Labelframe(rframe, text="Other input widgets", padding=10)
input_group.pack(fill=tk.X, pady=10)

entry = ttk.Entry(input_group)
entry.pack(fill=tk.X)
entry.insert(tk.END, "entry widget")

password = ttk.Entry(input_group, show="•")
password.pack(fill=tk.X, pady=5)
password.insert(tk.END, "password")

spinbox = ttk.Spinbox(input_group, from_=0, to=100)
spinbox.pack(fill=tk.X)
spinbox.set(45)

lb = ttk.Treeview(input_group, columns=[0], height=4, show='', bootstyle='primary')
lb.pack(fill=tk.X, pady=5)
for name in theme_names:
    lb.insert('', tk.END, name, values=(name))
lb.set('superhero')

# # vertical widgets
vframe = ttk.Frame(rframe)
vframe.pack(expand=tk.YES, fill=tk.BOTH)

s1 = ttk.Scale(
    master=vframe,
    orient=tk.VERTICAL,
    value=50,
    from_=100,
    to=0
)
s1.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

s2 = ttk.Scale(
    master=vframe,
    orient=tk.VERTICAL,
    bootstyle='info',
    value=75,
    from_=100,
    to=0
)
s2.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

s3 = ttk.Scale(
    master=vframe,
    orient=tk.VERTICAL,
    bootstyle='warning',
    value=25,
    from_=100,
    to=0
)
s3.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

ttk.Progressbar(
    master=vframe,
    orient=tk.VERTICAL,
    value=50,
).pack(fill=tk.Y, padx=5, side=tk.LEFT)

ttk.Progressbar(
    master=vframe,
    orient=tk.VERTICAL,
    value=75,
    bootstyle='success-striped'
).pack(fill=tk.Y, padx=5, side=tk.LEFT)

ttk.Progressbar(
    master=vframe,
    orient=tk.VERTICAL,
    value=25,
    bootstyle='danger-striped'
).pack(fill=tk.Y, padx=5, side=tk.LEFT)

sb = ttk.Scrollbar(
    master=vframe,
    orient=tk.VERTICAL,
)
sb.set(0.1, 0.9)
sb.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

sb = ttk.Scrollbar(
    master=vframe,
    orient=tk.VERTICAL,
    bootstyle='info'
)
sb.set(0.1, 0.9)
sb.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

sb = ttk.Scrollbar(
    master=vframe,
    orient=tk.VERTICAL,
    bootstyle='primary'
)
sb.set(0.1, 0.9)
sb.pack(fill=tk.Y, padx=5, side=tk.LEFT, expand=tk.YES)

default.configure(command=lambda: lb.delete(1))

if __name__ == '__main__':

    root.mainloop()
