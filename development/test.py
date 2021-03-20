import tkinter as tk
from tkinter import ttk
from themes.superflat import Style

variations = ['secondary', 'success', 'info', 'warning', 'danger']
style = Style()
style.theme_use('superflat')
# style = ttk.Style()
# style.theme_use('alt')
window = style.master
window.title('Theme Test')

root = ttk.Frame(window, padding=25)
root.pack(side='left', fill='both', expand='yes')

ttk.Scrollbar(window).pack(side='right', fill='y')

# notebook
nb = ttk.Notebook(root)
solid_btn_page = ttk.Frame(nb, padding=10)
nb.add(solid_btn_page, text='Tab 1')

# solid buttons
ttk.Button(solid_btn_page, text='Primary').pack(side='left', fill='x', expand='yes', padx=5)
for v in variations:
    ttk.Button(solid_btn_page, text=v.title(), style=f'{v}.TButton').pack(side='left', fill='x', expand='yes', padx=5)

for x in range(3):
    nb.add(ttk.Frame(nb), text=f'Tab {x+2}')
nb.pack(fill='x', expand='yes', pady=10)

# labels
label_frame = ttk.Frame(root, padding=10)
ttk.Label(label_frame, text='Primary', anchor='center').pack(side='left', fill='x', expand='yes')
for v in variations:
    ttk.Label(label_frame, text=v.title(), anchor='center', style=f'{v}.TLabel').pack(side='left', fill='x', expand='yes')

label_frame.pack(fill='x', expand='yes')

# outline buttons
outline_buttons = ttk.Frame(root)
outline_buttons.pack(fill='x', pady=5)
ttk.Button(outline_buttons, text='Primary', style='Outline.TButton').pack(side='left', expand='yes', fill='x', padx=5)
for v in variations:
    ttk.Button(outline_buttons, text=v.title(), style=f'{v}.Outline.TButton').pack(side='left', padx=5, fill='x', expand='yes')

# progress bar
ttk.Progressbar(root, value=15).pack(fill='x', pady=5)
val = 25
for v in variations:
    ttk.Progressbar(root, value=val, style=f'{v}.Horizontal.TProgressbar').pack(fill='x', pady=5)
    val += 10

entry_frame = ttk.Frame(root, padding=(0, 10))

# combobox
combo = ttk.Combobox(entry_frame, values=['Combo Option 1', 'Combo Option 2'])
combo.current(0)
combo.pack(side='left', padx=5)

# entry
e1 = ttk.Entry(entry_frame)
e1.insert('end', 'Primary focus ring')
e1.pack(side='left', fill='x', expand='yes', padx=(0, 5))
e2 = ttk.Entry(entry_frame, style='success.TEntry')
e2.insert('end', 'Success focus ring')
e2.pack(side='left', fill='x', expand='yes', padx=5)
e3 = ttk.Entry(entry_frame, style='danger.TEntry')
entry_frame.pack(fill='x')

# spinbox
spin = ttk.Spinbox(entry_frame, values=['red', 'yellow', 'orange'])
spin.pack(side='left', fill='x', padx=5)
spin.set('Spinbox option')

# scales
ttk.Scale(root, value=10, from_=1, to=100).pack(fill='x', expand='yes', pady=5)
scale_val = 20
for v in variations:
    ttk.Scale(root, value=scale_val, from_=1, to=100, style=f'{v}.Horizontal.TScale').pack(fill='x', expand='yes', pady=5)
    scale_val += 10

# radio buttons
radio_frame = ttk.LabelFrame(root, text='Radio Buttons')
radio_frame.pack(fill='x', expand='yes')
value = 1
ttk.Radiobutton(radio_frame, text='Primary', value=value).pack(side='left', fill='x', expand='yes')
for v in variations:
    value += 1
    ttk.Radiobutton(radio_frame, text=v.title(), style=f'{v}.TRadiobutton', value=value).pack(side='left', fill='x', expand='yes')

# checkbuttons
check_frame = ttk.LabelFrame(root, text='Check Buttons')
check_frame.pack(fill='x', expand='yes', pady=5)
ttk.Checkbutton(check_frame, text='Primary').pack(side='left', fill='x', expand='yes')
for v in variations:
    ttk.Checkbutton(check_frame, text=v.title(), style=f'{v}.TCheckbutton').pack(side='left', fill='x', expand='yes')

# Menubutton
solid_menu = ttk.Frame(root, padding=10)
solid_menu.pack(fill='x', expand='yes')
mb = ttk.Menubutton(solid_menu, text='Primary')
mb.pack(side='left', fill='x', expand='yes', padx=5)
mb.menu = tk.Menu(mb, tearoff=False)

mb['menu'] = mb.menu
mb.menu.add_checkbutton(label='Summer')
mb.menu.add_checkbutton(label='Fall')
mb.menu.add_checkbutton(label='Winter')
mb.menu.add_checkbutton(label='Spring')

for v in variations:
    m = ttk.Menubutton(solid_menu, text=v.title(), style=f'{v}.TMenubutton')
    m.pack(side='left', fill='x', expand='yes', padx=5)
    m.menu = tk.Menu(m, tearoff=False)
    m['menu'] = m.menu
    m.menu.add_checkbutton(label='Summer')
    m.menu.add_checkbutton(label='Fall')
    m.menu.add_checkbutton(label='Winter')
    m.menu.add_checkbutton(label='Spring')

# Outline Menubutton
outline_menu = ttk.Frame(root, padding=(10, 5))
outline_menu.pack(fill='x', expand='yes')
mb2 = ttk.Menubutton(outline_menu, text='Primary', style='Outline.TMenubutton')
mb2.pack(side='left', fill='x', expand='yes', padx=5)
mb2.menu = tk.Menu(mb2, tearoff=False)

mb2['menu'] = mb2.menu
mb2.menu.add_checkbutton(label='Summer')
mb2.menu.add_checkbutton(label='Fall')
mb2.menu.add_checkbutton(label='Winter')
mb2.menu.add_checkbutton(label='Spring')

for v in variations:
    m = ttk.Menubutton(outline_menu, text=v.title(), style=f'{v}.Outline.TMenubutton')
    m.pack(side='left', fill='x', expand='yes', padx=5)
    m.menu = tk.Menu(m, tearoff=False)
    m['menu'] = m.menu
    m.menu.add_checkbutton(label='Summer')
    m.menu.add_checkbutton(label='Fall')
    m.menu.add_checkbutton(label='Winter')
    m.menu.add_checkbutton(label='Spring')


# treeview
tv = ttk.Treeview(root, columns=[1, 2], height=5)
tv.heading('#0', text='Department')
tv.heading(1, text='Name')
tv.heading(2, text='Job Title')
tv.insert('', 'end', 'finance', text='Finance')
tv.insert('', 'end', 'marketing', text='Marketing')
tv.insert('finance', 'end', values=['Hugo First', 'Senior Manager'])
tv.insert('finance', 'end', values=['Percy Vere', 'Manager'])
tv.insert('finance', 'end', values=['John Quil', 'Associate'])
tv.insert('marketing', 'end', values=['Teri Dactyl', 'Director'])
tv.insert('marketing', 'end', values=['Olive Tree', 'Senior Manager'])
tv.insert('marketing', 'end', values=['Aida Bugg', 'Intern'])
tv.pack(fill='x', pady=10)



window.mainloop()
