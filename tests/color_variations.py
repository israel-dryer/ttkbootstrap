from ttkbootstrap import Style
import tkinter
from tkinter import ttk

root = tkinter.Tk()
style = Style()
style.theme_use('superhero')

f1 = ttk.Frame(root, padding=5)
f1.pack(fill='x', padx=25, pady=25)
for color in style.theme.colors:
    ttk.Button(f1, text=color.title(), style=f'{color}.TButton').pack(side='left', fill='x', expand='yes', padx=2)

f2 = ttk.Frame(root, padding=5)
f2.pack(fill='x')
for color in style.theme.colors:
    ttk.Button(f2, text=color.title(), style=f'{color}.Outline.TButton').pack(side='left', fill='x', expand='yes', padx=2)

f3 = ttk.Frame(root, padding=5)
f3.pack(fill='x')
om_var = tkinter.StringVar()
for color in style.theme.colors:
    ttk.OptionMenu(f3, om_var, 'Option Menu', *style.theme_names(), style=f'{color}.TMenubutton').pack(side='left', fill='x', expand='yes', padx=2)

f4 = ttk.Frame(root, padding=5)
f4.pack(fill='x')
for color in style.theme.colors:
    ttk.Scale(f4, from_=1, to=100, value=25, style=f'{color}.Horizontal.TScale').pack(side='left', fill='x', expand='yes', padx=2)

f5 = ttk.Frame(root, padding=5)
f5.pack(fill='x')
for color in style.theme.colors:
    tv = ttk.Treeview(f5, height=1, style=f'{color}.Treeview')
    tv.pack(side='left', fill='x', expand='yes', padx=2)
    tv.heading('#0', text='Example heading')

f6 = ttk.Frame(root, padding=5)
f6.pack(fill='x')
for color in style.theme.colors:
    spinner_options = ['Spinner option 1', 'Spinner option 2', 'Spinner option 3']
    spinner = ttk.Spinbox(f6, from_=1, to=100, style=f'{color}.TSpinbox')
    spinner.set(1)
    spinner.pack(side='left', fill='x', expand='yes', padx=2)

f7 = ttk.Frame(root, padding=5)
f7.pack(fill='x')
for color in style.theme.colors:
    entry = ttk.Entry(f7, style=f'{color}.TEntry')
    entry.insert('end', color.title())
    entry.pack(side='left', fill='x', expand='yes', padx=2)

f8 = ttk.Frame(root, padding=5)
f8.pack(fill='x')
for color in style.theme.colors:
    ttk.Label(f8, text=color.title(), style=f'{color}.TLabel').pack(side='left', fill='x', expand='yes', padx=2)

f9 = ttk.Frame(root, padding=5)
f9.pack(fill='x')
for i, color in enumerate(style.theme.colors):
    ttk.Radiobutton(f9, value=i, text=color.title(), style=f'{color}.TRadiobutton').pack(side='left', fill='x', expand='yes', padx=2)

f10 = ttk.Frame(root, padding=5)
f10.pack(fill='x')
for color in style.theme.colors:
    ttk.Checkbutton(f10, text=color.title(), style=f'{color}.TCheckbutton').pack(side='left', fill='x', expand='yes', padx=2)

f11 = ttk.Frame(root, padding=5)
f11.pack(fill='x')
for color in style.theme.colors:
    ttk.Progressbar(f11, value=30, style=f'{color}.Horizontal.TProgressbar').pack(side='left', fill='x', expand='yes', pady=2)

root.mainloop()
