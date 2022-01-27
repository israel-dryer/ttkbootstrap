import tkinter as tk
from ttkbootstrap import Style
from random import choice

root = tk.Tk()
root.minsize(500, 500)

style = Style('superhero')

def new_theme():
    theme = choice(style.theme_names())
    print(theme)
    style.theme_use(theme)

btn = tk.Button(root, text='Primary')
btn.configure(command=new_theme)
btn.pack(padx=10, pady=10, fill=tk.BOTH, expand=tk.YES)

label = tk.Label(text="Hello world!")
label.pack(padx=10, pady=10)

text = tk.Text()
text.pack(padx=10, pady=10)
text.insert(tk.END, 'This is a demo of themes applied to regular tk widgets.')

frame = tk.Frame()
frame.pack(padx=10, pady=10, fill=tk.X)
cb1 = tk.Checkbutton(frame, text="Check 1")
cb1.pack(padx=10, pady=10, side=tk.LEFT)
cb1.invoke()
cb2 = tk.Checkbutton(frame, text="Check 2")
cb2.pack(padx=10, pady=10, side=tk.LEFT)

rb_var = tk.Variable(value=1)
rb1 = tk.Radiobutton(frame, text='Radio 1', value=1, variable=rb_var)
rb1.pack(padx=10, pady=10, side=tk.LEFT)
rb2 = tk.Radiobutton(frame, text='Radio 2', value=2, variable=rb_var)
rb2.pack(padx=10, pady=10, side=tk.LEFT)

frame2 = tk.LabelFrame(text="Items")
frame2.pack(padx=10, pady=10, fill=tk.X)

entry = tk.Entry(frame2)
entry.pack(padx=10, pady=10, side=tk.LEFT)

scale = tk.Scale(frame2, orient=tk.HORIZONTAL)
scale.set(25)
scale.pack(padx=10, pady=10, side=tk.LEFT)

sb = tk.Spinbox(frame2)
sb.pack(padx=10, pady=10, side=tk.LEFT)

lb = tk.Listbox(height=3)
lb.insert(tk.END, 'one', 'two', 'three')
lb.pack(padx=10, pady=10)

mb = tk.Menubutton(frame2, text="Hello world")
menu = tk.Menu(mb)
menu.add_checkbutton(label="Option 1")
menu.add_checkbutton(label="Option 2")
mb['menu'] = menu
mb.pack(padx=10, pady=10)

root.mainloop()

