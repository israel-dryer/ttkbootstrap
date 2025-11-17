import ttkbootstrap as ttk

app = ttk.Window()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    b = ttk.Spinbox(app, bootstyle=color, width=20, values=colors)
    b.set(color)
    b.pack(padx=20, pady=20)

app.mainloop()