import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_treeview_style(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text=widget_style).pack(fill=tk.X)
    tv = ttk.Treeview(frame, style=widget_style, columns=[0, 1],
                      height=2)
    tv.heading('#0', text='Column')
    for x in range(2):
        tv.heading(x, text=f'Column {x}')
        tv.insert('', 'end', text=f'Item {x}', 
                  values=[f'Row {x}', f'Row {x+1}'])
    tv.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored 
    for color in style.colors:
        sg_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=sg_style).pack(fill=tk.X)
        tv = ttk.Treeview(frame, style=sg_style, columns=[0, 1],
                          height=2)
        tv.heading('#0', text='Column')
        for x in range(2):
            tv.heading(x, text=f'Column {x}')
            tv.insert('', 'end', text=f'Item {x}', 
                    values=[f'Row {x}', f'Row {x+1}'])
        tv.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_treeview_style('Treeview', style).pack(side=tk.LEFT)

    root.mainloop()