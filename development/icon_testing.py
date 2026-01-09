from PIL import Image, ImageTk
from ttkbootstrap_icons_bs import BootstrapIcon

import tkinter as tk
from tkinter import ttk

# import ttkbootstrap as ttk
#
#
# app = ttk.Window()
#
# img = Image.new('RGBA', (14, 14), (0, 0, 0, 255))
# pm = ImageTk.PhotoImage(image=img)
#
# icon = BootstrapIcon('bootstrap')
# lbl = ttk.Label(font='caption', text='Icon', image=pm, anchor='center', compound='left', background='red', padding=5).pack(fill='both', expand=True)
# btn = ttk.Button(text='Icon', image=pm, anchor='center', compound='left', style_options={'size': 'xs'}).pack()
#
# app.mainloop()


root = tk.Tk()
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', font='-size 8')

layout = style.layout('TButton')
print(layout)

# img = Image.new('RGBA', (14, 14), (0, 0, 0, 255))
# pm = ImageTk.PhotoImage(image=img)

icon = BootstrapIcon('bootstrap')


btn = ttk.Button(text='Icon', image=icon.image, compound='left', padding=4)
btn.pack()

root.mainloop()