import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style(theme=DARK)

    menu = tk.Menu(root)
    for x in range(5):
        menu.insert_checkbutton('end', label=f'Option {x+1}')
    menu.post(100, 100)

    root.mainloop()