import ttkbootstrap as ttk

app = ttk.Window()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    b = ttk.Button(app, text=color.title(), bootstyle=color, icon="plus-square", compound="left")
    b.pack(padx=20, pady=20)

from tkinter import font
print('font-height', font.nametofont('body').metrics()['linespace'])

app.mainloop()