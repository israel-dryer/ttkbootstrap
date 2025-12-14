import ttkbootstrap as ttk



app = ttk.App(theme="docs-light")

r1 = ttk.Frame(app, padding=10)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=10)
r2.pack(side='top')

ttk.Button(r1, text='Solid').pack(side='left', padx=10, pady=20)
ttk.Button(r1, text='Outline', bootstyle='outline').pack(side='left', padx=10)

ghost = ttk.Button(r1, text='Ghost', bootstyle='ghost')
ghost.pack(side='left', padx=10)
ghost.state(['hover'])

link = ttk.Button(r1, text='Link', bootstyle='link')
link.pack(side='left', padx=10)
link.state(['active'])

ttk.Button(r2, text='Text', bootstyle='text').pack(side='left', padx=10)
ttk.Button(r2, text='Disabled', state='disabled').pack(side='left', padx=10)
ttk.Button(r2, text='Icon', icon='bootstrap').pack(side='left', padx=10)
ttk.Button(r2, text='Icon Only', icon='bootstrap', icon_only=True).pack(side='left', padx=10)


app.mainloop()