import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from this import s as ZEN

app = ttk.Window("Legacy Widgets")


def change_theme():
    themename = app.getvar("themename")
    app.style.theme_use(themename)


frame = tk.Frame(app, padx=10, pady=10)
frame.pack(fill=BOTH, expand=YES)

themes = app.style.theme_names()

headerframe = tk.Frame(frame)
headerframe.pack(fill=X)

themename = tk.Variable(name="themename", value="litera")
header = tk.Label(headerframe, textvariable=themename, font="-size 24")
header.pack(side=LEFT, fill=X)

lf = tk.LabelFrame(frame, text="tkinter widgets", padx=10, pady=10)
lf.pack(fill=BOTH)

# label
tk.Label(lf, text="This is a label", anchor=W).pack(fill=X)

# input widgets
inputframe = tk.Frame(lf)
inputframe.pack(fill=X, pady=10)
ent = tk.Entry(inputframe)
ent.insert(END, "An entry field")
ent.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
spn = tk.Spinbox(inputframe, values=["Option 1", "Option 2"])
spn.pack(side=LEFT, fill=X, expand=YES)

# button
btnframe = tk.Frame(lf)
btnframe.pack(fill=X)
tk.Button(btnframe, text="Solid Button").pack(side=LEFT, fill=X, expand=YES)
theme_options = tk.Menubutton(btnframe, text="Select a theme")
menu = tk.Menu(theme_options)
for t in themes:
    menu.add_radiobutton(label=t, variable="themename", command=change_theme)

theme_options["menu"] = menu
theme_options.pack(side=LEFT, padx=(5, 0), fill=X)

# radio & checkbuttons
rcframe = tk.Frame(lf, pady=10)
rcframe.pack(fill=X)
app.setvar("radio", 1)
r1 = tk.Radiobutton(rcframe, text="Radio one", value=1, variable="radio")
r1.pack(side=LEFT)
r2 = tk.Radiobutton(rcframe, text="Radio two", value=2, variable="radio")
r2.pack(side=LEFT)
c1 = tk.Checkbutton(rcframe, text="Check One")
c1.invoke()
c1.pack(side=LEFT)
c2 = tk.Checkbutton(rcframe, text="Check two")
c2.pack(side=LEFT)

# scale widget
app.setvar("scale", 25)
scaleframe = tk.Frame(lf, pady=5)
scaleframe.pack(fill=X, expand=YES)
scale = tk.Scale(scaleframe, orient=HORIZONTAL, variable="scale")
scale.pack(side=LEFT, fill=X, expand=YES, pady=5)
tk.Label(scaleframe, textvariable="scale").pack(side=RIGHT, padx=(5, 0))

# text list frame
textframe = tk.Frame(lf, pady=10)
textframe.pack(fill=X, expand=YES)
txt = tk.Text(textframe, width=30, height=8)
txt.pack(side=LEFT, fill=X)
txt.insert(END, ZEN)
lb = tk.Listbox(textframe, height=8)
lb.pack(side=LEFT, fill=X, padx=(5, 0))
[lb.insert(END, c) for c in app.style.colors]

# scrollbar
sb = ttk.Scrollbar(lf, orient=HORIZONTAL)
sb.pack(fill=X, expand=YES)
sb.set(0.05, 0.95)

app.mainloop()
