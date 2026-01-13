import ttkbootstrap as ttk

app = ttk.App(theme="dark")

# colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']
#
# for color in colors:
#     b = ttk.Button(app, text=color.title(), accent=color, icon="bootstrap-fill", compound="left")
#     b.pack(padx=20, pady=20)
#
# from tkinter import font
# print('font-height', font.nametofont('body').metrics()['linespace'])
# print('caption-height', font.nametofont('caption').metrics()['linespace'])
#
# ttk.Button(app, icon='bootstrap', icon_only=True).pack()
#
# ttk.Button(app, text="Dark", icon="moon", icon_only=True, command=lambda: ttk.set_theme("dark")).pack()
# ttk.Button(app, text="Light", icon="sun", command=lambda: ttk.set_theme("light")).pack()
#
# solid = ttk.Button(text='Button', command=lambda: print_size(), size='xs').pack()
# solid_sm = ttk.Button(text='Button', icon="bootstrap", command=lambda: print_size(), size='xs').pack()
# outline = ttk.Button(text='Button', variant='outline').pack()
#
#
# def print_size():
#     print(solid_sm.winfo_height())
#     print(outline.winfo_height())
#
#
# app.update_idletasks()
# app.place_center()

f1 = ttk.PackFrame(direction='horizontal', gap=8).pack()
b1 = ttk.Button(f1, icon='bootstrap', text='Button', command=lambda: check_height()).pack()
b2 = ttk.Button(f1, icon='bootstrap', icon_only=True, command=lambda: check_height()).pack()

f2 = ttk.PackFrame(direction='horizontal', gap=8).pack()
ttk.Button(f2, icon='bootstrap', variant='outline', text='Button').pack()
ttk.Button(f2, icon='bootstrap', icon_only=True, variant='outline').pack()

f2 = ttk.PackFrame(direction='horizontal', gap=8).pack()
ttk.Button(f2, icon='bootstrap', accent='primary', variant='ghost', text='Button').pack()
ttk.Button(f2, icon='bootstrap', accent='primary', icon_only=True, variant='ghost').pack()


f2 = ttk.PackFrame(direction='horizontal', gap=8).pack()
ttk.Button(f2, icon='bootstrap', accent='primary', density='compact', text='Button', command=lambda: check_height()).pack()
ttk.Button(f2, icon='bootstrap', accent='primary', density='compact', icon_only=True, command=lambda: check_height()).pack()

def check_height():
    print(b1.winfo_height())
    print(b2.winfo_height())


app.mainloop()