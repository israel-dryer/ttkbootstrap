import ttkbootstrap as ttk

app = ttk.Window()

colors = ['border', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    ttk.Sizegrip(app, bootstyle=color).pack(padx=20, pady=20)

app.mainloop()