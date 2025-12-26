import ttkbootstrap as ttk



app = ttk.App(theme="docs-light")

# solid buttons
solid = ttk.Frame(app, padding=(16, 8))
solid.pack(side='top')

ttk.Label(solid, font="label", text='Solid', width=10).pack(side='left')
ttk.Button(solid, text='default').pack(side='left', padx=8)
solid_active = ttk.Button(solid, text='active', state='active')
solid_active.pack(side='left', padx=8)
solid_active.state(['hover'])

solid_focus = ttk.Button(solid, text='focus', state='focus')
solid_focus.pack(side='left', padx=8)
solid_focus.state(['focus'])

ttk.Button(solid, text='disabled', state='disabled').pack(side='left', padx=8)

# outline buttons
outline = ttk.Frame(app, padding=(16, 8))
outline.pack(side='top')

ttk.Label(outline, font="label", text='Outline', width=10).pack(side='left')
ttk.Button(outline, text='default', bootstyle="outline").pack(side='left', padx=8)
outline_active = ttk.Button(outline, text='active', state='active', bootstyle="outline")
outline_active.pack(side='left', padx=8)
outline_active.state(['hover'])

outline_focus = ttk.Button(outline, text='focus', state='focus', bootstyle="outline")
outline_focus.pack(side='left', padx=8)
outline_focus.state(['focus'])

ttk.Button(outline, text='disabled', state='disabled', bootstyle="outline").pack(side='left', padx=8)

# ghost buttons
ghost = ttk.Frame(app, padding=(16, 8))
ghost.pack(side='top')

ttk.Label(ghost, font="label", text='Ghost', width=10).pack(side='left')
ttk.Button(ghost, text='default', bootstyle="ghost").pack(side='left', padx=8)
ghost_active = ttk.Button(ghost, text='active', state='active', bootstyle="ghost")
ghost_active.pack(side='left', padx=8)
ghost_active.state(['hover'])

ghost_focus = ttk.Button(ghost, text='focus', state='focus', bootstyle="ghost")
ghost_focus.pack(side='left', padx=8)
ghost_focus.state(['focus'])

ttk.Button(ghost, text='disabled', state='disabled', bootstyle="ghost").pack(side='left', padx=8)

# link buttons
link = ttk.Frame(app, padding=(16, 8))
link.pack(side='top')

ttk.Label(link, font="label", text='Link', width=10).pack(side='left')
ttk.Button(link, text='default', bootstyle="link").pack(side='left', padx=8)
link_active = ttk.Button(link, text='active', state='active', bootstyle="link")
link_active.pack(side='left', padx=8)
link_active.state(['hover'])

link_focus = ttk.Button(link, text='focus', state='focus', bootstyle="link")
link_focus.pack(side='left', padx=8)
link_focus.state(['focus'])

ttk.Button(link, text='disabled', state='disabled', bootstyle="link").pack(side='left', padx=8)

# text buttons
text = ttk.Frame(app, padding=(16, 8))
text.pack(side='top')

ttk.Label(text, font="label", text='Text', width=10).pack(side='left')
ttk.Button(text, text='default', bootstyle="text").pack(side='left', padx=8)
text_active = ttk.Button(text, text='active', state='active', bootstyle="text")
text_active.pack(side='left', padx=8)
text_active.state(['hover'])

text_focus = ttk.Button(text, text='focus', state='focus', bootstyle="text")
text_focus.pack(side='left', padx=8)
text_focus.state(['focus'])

ttk.Button(text, text='disabled', state='disabled', bootstyle="text").pack(side='left', padx=8)

icons = ttk.Frame(app, padding=(16, 8))
icons.pack(side='top')

ttk.Button(icons, text='Settings', icon='gear').pack(side='left', padx=8)
ttk.Button(icons, icon='gear', icon_only=True).pack(side='left', padx=8)

colors = ttk.Frame(app, padding=(16, 8))
colors.pack(side='top')
for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']:
    ttk.Button(colors, text=color.title(), bootstyle=color).pack(side='left', padx=8)

app.mainloop()