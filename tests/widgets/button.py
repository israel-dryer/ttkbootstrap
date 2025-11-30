import ttkbootstrap as ttk

app = ttk.Window()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    b = ttk.Button(app, text=color.title(), bootstyle=color, width=25, icon="bootstrap-fill", compound="left")
    b.pack(padx=20, pady=20)

from tkinter import font
print('font-height', font.nametofont('body').metrics()['linespace'])

ttk.Button(app, icon="bootstrap-fill").pack()
ttk.Button(app, icon="bootstrap-fill", icon_only=True).pack()

app.mainloop()