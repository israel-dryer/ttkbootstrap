from izzythemes import Style, ttk
import tkinter as tk


def checked(btn):
    btn_text = "Unchecked" if btn['text'] == "Checked" else "Checked"
    btn.configure(text=btn_text)


style = Style()
style.theme_use('flatly')
root = style.master
root.title('IzzyThemes - flatly')
root.geometry('500x500')

# Scrollbar
ttk.Scrollbar(root).pack(side='right', fill='y')

# Notebook
nb = ttk.Notebook(root)
nb.pack(fill='both', expand='yes')


def create_themed_tab(color=''):
    """Create a return a frame containing themed widgets"""
    style_color = color + '.' if color else color
    print(style_color)
    tab = ttk.Frame(nb, padding=5)
    colors = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger']

    # Label
    ttk.Label(tab, text='This is an example label', style=f'{style_color}TLabel').pack(side='top', fill='x', pady=5)

    frm2 = ttk.Frame(tab)
    frm2.pack(fill='x', pady=5)

    # Menubutton
    mb = ttk.Menubutton(frm2, text='Menubutton', style=f'{style_color}TMenubutton')
    mb.pack(side='left', fill='x', padx=(0, 5))
    mb.menu = tk.Menu(mb)
    mb['menu'] = mb.menu
    for color in colors:
        mb.menu.add_radiobutton(label=color)

    # Entry
    ttk.Entry(frm2, style=f'{style_color}TEntry').pack(fill='x')

    # Button
    btn_frame = ttk.Frame(tab)
    b1 = ttk.Button(btn_frame, text='Button', style=f'{style_color}TButton')
    b1.pack(side='left', fill='x', expand='yes', padx=(0, 5))
    b2 = ttk.Button(btn_frame, text='Button', style=f'{style_color}Outline.TButton')
    b2.pack(side='left', fill='x', expand='yes')
    btn_frame.pack(fill='x', pady=5)

    # Labelframe
    lf = ttk.Labelframe(tab, text='Labelframe', style=f'{style_color}TLabelframe')
    lf.pack(fill='x', pady=5)

    # Radio
    radio_frame = ttk.Frame(lf)
    radio_frame.pack(side='top', fill='x')
    r1 = ttk.Radiobutton(radio_frame, value=1, text='Radio one', width=15, style=f'{style_color}TRadiobutton')
    r1.pack(side='left', fill='x')
    r1.invoke()
    ttk.Radiobutton(radio_frame, value=2, text='Radio two', style=f'{style_color}TRadiobutton').pack(side='left',
                                                                                                     fill='x')

    # Checkbutton
    check_frame = ttk.Frame(lf)
    check_frame.pack(side='top', fill='x')
    cb1 = ttk.Checkbutton(check_frame, text='Unchecked', width=15, style=f'{style_color}TCheckbutton')
    cb1.configure(command=lambda: checked(cb1))
    cb1.pack(side='left')
    cb1.invoke()

    cb2 = ttk.Checkbutton(check_frame, text='Unchecked', style=f'{style_color}TCheckbutton')
    cb2.configure(command=lambda: checked(cb2))
    cb2.pack(side='left')

    # Treeview
    tv = ttk.Treeview(tab, height=3, style=f'{style_color}Treeview')
    tv.pack(fill='x', pady=5)
    tv.heading('#0', text='Example heading')
    tv.insert('', 'end', 'example1', text='Example 1')
    tv.insert('', 'end', 'example2', text='Example 2')
    tv.insert('example2', 'end', text='Example 2 Child 1')
    tv.insert('example2', 'end', text='Example 2 Child 2')

    # Scale
    scale_frame = ttk.Frame(tab)
    scale_var = tk.IntVar(value=25)
    scale = ttk.Scale(scale_frame, variable=scale_var, from_=1, to=100, style=f'{style_color}Horizontal.TScale')
    scale.pack(side='left', fill='x', expand='yes', padx=(0, 2))
    scale_frame.pack(side='top', fill='x', pady=5)
    ttk.Entry(scale_frame, textvariable=scale_var, width=4, style=f'{style_color}TEntry').pack(side='right')

    # Combobox

    cbo = ttk.Combobox(tab, values=colors, style=f'{style_color}TCombobox')
    cbo.current(0)
    cbo.pack(fill='x', pady=5)

    # Progressbar
    ttk.Progressbar(tab, value=30, style=f'{style_color}Horizontal.TProgressbar').pack(fill='x', pady=5)

    return tab


nb.add(create_themed_tab(''), text='Primary')
nb.add(create_themed_tab('secondary'), text='Secondary')
nb.add(create_themed_tab('info'), text='Info')
nb.add(create_themed_tab('success'), text='Success')
nb.add(create_themed_tab('warning'), text='Warning')
nb.add(create_themed_tab('danger'), text='Danger')

root.mainloop()
