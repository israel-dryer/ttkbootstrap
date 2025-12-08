import ttkbootstrap as ttk

app = ttk.Window()
app.style.theme_use('dark')

colors = ['default', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']

ttk.LabelFrame(app, width=150, height=50, text='Default').pack(padx=20, pady=20)

for color in colors:
    lf = ttk.LabelFrame(app, width=150, height=50, bootstyle=color, text=color.title())
    lf.pack(padx=20, pady=20)

ttk.Button(app, text='Dark', command=lambda: app.style.theme_use('dark')).pack()
ttk.Button(app, text='Light', command=lambda: app.style.theme_use('light')).pack()

app.mainloop()