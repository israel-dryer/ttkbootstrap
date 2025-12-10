import ttkbootstrap as ttk

app = ttk.App()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

def change_theme():
    if ttk.get_theme() == 'dark':
        ttk.set_theme('light')
    else:
        ttk.set_theme('dark')

ttk.Button(app, text="Change Theme", command=change_theme).pack(pady=10)

for color in colors:
    b = ttk.Combobox(app, bootstyle=color, width=20, values=colors)
    b.set(color)
    b.pack(padx=20, pady=20)

app.mainloop()