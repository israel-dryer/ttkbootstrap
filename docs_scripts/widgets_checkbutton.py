import ttkbootstrap as ttk



app = ttk.App(theme="docs-light")

r1 = ttk.Frame(app, padding=10)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=10)
r2.pack(side='top')

r3 = ttk.Frame(app, padding=10)
r3.pack(side='top')

r4 = ttk.Frame(app, padding=10)
r4.pack(side='top')


# unchecked
b1 = ttk.CheckButton(r1)
b1.pack(side='left', padx=10)
b1.invoke()
b1.invoke()

# checked
b2 = ttk.CheckButton(r1)
b2.pack(side='left', padx=10)
b2.invoke()

# unchecked disabled
b1 = ttk.CheckButton(r1)
b1.pack(side='left', padx=10)
b1.invoke()
b1.invoke()
b1['state'] = 'disabled'

# checked
b2 = ttk.CheckButton(r1)
b2.pack(side='left', padx=10)
b2.invoke()
b2['state'] = 'disabled'

# indeterminate
b3 = ttk.CheckButton(r2)
b3.pack(side='left', padx=10)

# indeterminate disable
b3 = ttk.CheckButton(r2)
b3.pack(side='left', padx=10)
b3['state'] = 'disabled'


# toggles

b4 = ttk.CheckButton(r3, bootstyle='toggle')
b4.pack(side='left', padx=10)
b4.state(['!selected'])

b4 = ttk.CheckButton(r3, bootstyle='toggle')
b4.pack(side='left', padx=10)
b4.state(['selected'])

# with labels

b4 = ttk.CheckButton(r4, text="checkbutton")
b4.pack(side='left', padx=10)
b4.state(['!selected'])

b4 = ttk.CheckButton(r4, text="toggle", bootstyle='toggle')
b4.pack(side='left', padx=10)
b4.state(['selected'])


# colors
colors = ttk.Frame(app, padding=(16, 8))
colors.pack(side='top')
for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']:
    b = ttk.CheckButton(colors, bootstyle=color)
    b.pack(side='left', padx=8)
    b.invoke()

colors = ttk.Frame(app, padding=(16, 8))
colors.pack(side='top')
for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']:
    b = ttk.CheckButton(colors, bootstyle=color + '-toggle')
    b.pack(side='left')
    b.invoke()

icons = ttk.Frame(app, padding=(16, 8))
icons.pack(side='top')

ttk.CheckButton(icons, value=None, icon='mic-fill', text='Volume').pack()

app.mainloop()