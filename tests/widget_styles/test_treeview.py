import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'dark'
LIGHT = 'light'

def create_treeview_style(_, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text='Treeview', anchor='center')
    title.pack(padx=5, pady=2, fill='both')
    ttk.Separator(frame).pack(padx=5, pady=5, fill='x')

    # default
    ttk.Label(frame, text='default').pack(fill='x')
    tv = ttk.Treeview(frame, columns=[0, 1], height=2)
    tv.heading('#0', text='Column')
    for x in range(2):
        tv.heading(x, text=f'Column {x}')
        tv.insert('', 'end', text=f'Item {x}', 
                  values=[f'Row {x}', f'Row {x+1}'])
    tv.pack(padx=5, pady=5, fill='both')

    # colored 
    for color in style.colors:
        ttk.Label(frame, text=color).pack(fill='x')
        tv = ttk.Treeview(
            master=frame, 
            bootstyle=color, 
            columns=[0, 1],
            height=2
        )
        tv.heading('#0', text='Column')
        for x in range(2):
            tv.heading(x, text=f'Column {x}')
            tv.insert('', 'end', text=f'Item {x}', 
                    values=[f'Row {x}', f'Row {x+1}'])
        tv.pack(padx=5, pady=5, fill='both')

    return frame

def change_style():
    theme = choice(['light', 'dark'])
    print(theme)
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_treeview_style('', style).pack(side='left')

    root.mainloop()