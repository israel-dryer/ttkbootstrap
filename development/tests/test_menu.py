import tkinter as tk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    menu = tk.Menu(root)
    for x in range(5):
        menu.insert_checkbutton('end', label=f'Option {x+1}')
    menu.post(100, 100)

    root.mainloop()