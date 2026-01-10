from typing import Literal

import ttkbootstrap as ttk


app = ttk.App("ButtonGroup Demo")

orient: Literal['horizontal', 'vertical'] = 'horizontal'

frame = ttk.PackFrame(gap=8, padding=8).pack(fill='both', expand=True)

ttk.Label(frame, text='Default Density').pack()
solid1 = ttk.ButtonGroup(frame, orient=orient).pack()
solid1.add('One')
solid1.add('Two')
solid1.add('Three')

outline1 = ttk.ButtonGroup(frame, variant='outline', orient=orient).pack()
outline1.add('One')
outline1.add('Two')
outline1.add('Three')

ghost1 = ttk.ButtonGroup(frame, variant='ghost', orient=orient).pack()
ghost1.add(icon='justify-left', icon_only=True)
ghost1.add(icon='justify', icon_only=True)
ghost1.add(icon='justify-right', icon_only=True)

ttk.Label(frame, text='Compact Density').pack()
solid2 = ttk.ButtonGroup(frame, orient=orient, density='compact').pack()
solid2.add('One')
solid2.add('Two')
solid2.add('Three')

outline2 = ttk.ButtonGroup(frame, variant='outline', orient=orient, density='compact').pack()
outline2.add('One')
outline2.add('Two')
outline2.add('Three')

ghost2 = ttk.ButtonGroup(frame, variant='ghost', orient=orient, density='compact').pack()
ghost2.add(icon='justify-left', icon_only=True)
ghost2.add(icon='justify', icon_only=True)
ghost2.add(icon='justify-right', icon_only=True)

ttk.Separator(app).pack(fill='x', pady=8)
ttk.Button(app, text='Toggle Theme', command=ttk.toggle_theme).pack(padx=16, pady=8)

def check_sizes():
    print('default', solid1.winfo_height(), solid1.winfo_width())
    print('compact', solid2.winfo_height(), solid2.winfo_width())

    print('default', ghost1.winfo_height(), ghost1.winfo_width())
    print('compact', ghost2.winfo_height(), ghost2.winfo_width())

ttk.Button(app, text='Check Sizes', command=check_sizes).pack(padx=16, pady=8)

app.mainloop()