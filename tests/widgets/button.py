import ttkbootstrap as ttk

app = ttk.App(theme="dark")

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    b = ttk.Button(app, text=color.title(), bootstyle=color, width=25, icon="bootstrap-fill", compound="left")
    b.pack(padx=20, pady=20)

from tkinter import font
print('font-height', font.nametofont('body').metrics()['linespace'])

ttk.Button(app, text="Dark", icon="moon", command=lambda: ttk.set_active_theme("dark")).pack()
ttk.Button(app, text="Light", icon="sun", command=lambda: ttk.set_active_theme("light")).pack()

print(ttk.get_theme_color("background[+1]"))

app.mainloop()