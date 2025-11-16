import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
from ttkbootstrap.style.style import use_style

utility.enable_high_dpi_awareness()

DARK = 'dark'
LIGHT = 'light'


def button_style_frame(bootstyle, widget_name):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_name,
        anchor='center'
    )
    title.pack(padx=5, pady=2, fill='both')

    ttk.Separator(frame).pack(padx=5, pady=5, fill='x')

    ttk.Button(
        master=frame,
        text='default',
        bootstyle=bootstyle,
        compound="left",
        icon="bootstrap",
    ).pack(padx=5, pady=5, fill='both')

    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'dark', 'light']:
        ttk.Button(
            master=frame,
            text=color,
            bootstyle=f'{color}-{bootstyle}',
            compound="left",
            icon="bootstrap",
        ).pack(padx=5, pady=5, fill='both')

    ttk.Button(
        master=frame,
        text='disabled',
        state='disabled',
        bootstyle=bootstyle
    ).pack(padx=5, pady=5, fill='both')

    return frame

def change_style():
    theme = choice(['light', 'dark'])
    style.theme_use(theme)
    print(theme)



if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = use_style("light")

    button_style_frame('default', 'Solid Button').pack(side='left')
    button_style_frame('outline', 'Outline Button').pack(side='left')
    button_style_frame('ghost', 'Ghost Button').pack(side='left')
    button_style_frame('text', 'Text Button').pack(side='left')
    ttk.Button(text="Light", command=lambda: style.theme_use('light')).pack(padx=10, pady=10)
    ttk.Button(text="Dark", command=lambda: style.theme_use('dark')).pack(padx=10, pady=10)
    root.mainloop()
