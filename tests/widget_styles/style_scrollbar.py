import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_scrollbar_frame(orient, bootstyle=''):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=bootstyle.title() + ' Scrollbar', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    ttk.Label(frame, text='default').pack(fill=X)
    sb = ttk.Scrollbar(frame, orient=orient, bootstyle=bootstyle)
    sb.set(0.1, 0.9)
    if orient == HORIZONTAL:
        sb.pack(padx=5, pady=5, fill=X)
    else:
        sb.pack(padx=5, pady=5, fill=Y, side=LEFT)

    # colored
    for _, color in enumerate(['primary', 'secondary', 'success', 'info', 'warning', 'danger']):
        ttk.Label(frame, text=color).pack(fill=X)
        sb = ttk.Scrollbar(frame, bootstyle=f"{color}-{bootstyle}", orient=orient)
        sb.set(0.1, 0.3)
        if orient == HORIZONTAL:
            sb.pack(padx=5, pady=5, fill=X, expand=YES)
        else:
            sb.pack(padx=5, pady=5, fill=Y, side=LEFT,
                    expand=YES)

    return frame

def change_style():
    if style.theme_use() == 'dark':
        style.theme_use('light')
    else:
        style.theme_use('dark')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    root.geometry('1000x500')
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)
    test1 = create_scrollbar_frame(orient=HORIZONTAL, bootstyle='default')
    test1.pack(side=LEFT, anchor=N, fill=BOTH, expand=YES)
    
    test2 = create_scrollbar_frame(orient=VERTICAL, bootstyle='default')
    test2.pack(side=LEFT, anchor=N, fill=BOTH, expand=YES)

    test3 = create_scrollbar_frame(orient=HORIZONTAL, bootstyle='square')
    test3.pack(side=LEFT, anchor=N, fill=BOTH, expand=YES)
    
    test4 = create_scrollbar_frame(orient=VERTICAL, bootstyle='square')
    test4.pack(side=LEFT, anchor=N, fill=BOTH, expand=YES)

    root.mainloop()