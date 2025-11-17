import ttkbootstrap as ttk

app = ttk.Window()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

def change_theme():
    if app.style.theme_use() == 'dark':
        app.style.theme_use('light')
    else:
        app.style.theme_use('dark')

ttk.Button(app, text="Change Theme", command=change_theme).pack(pady=10)

for color in colors:
    b = ttk.Combobox(app, bootstyle=color, width=20, values=colors)
    b.set(color)
    b.pack(padx=20, pady=20)

app.mainloop()