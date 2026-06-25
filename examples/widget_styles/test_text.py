import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

def change_style(window):
    theme = choice(window.style.theme_names())
    window.style.theme_use(theme)


if __name__ == '__main__':
    # create visual widget style tests
    window = ttk.Window(themename='darkly')

    ttk.Button(text="Change Theme", command=lambda x=window: change_style(x)).pack(padx=10, pady=10)
    text = ttk.Text(window, font='helvetica 24 bold')
    text.pack(padx=10, pady=10)
    text.insert('end', 'Hello, this is my text.')

    window.mainloop()