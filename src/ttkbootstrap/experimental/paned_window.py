import tkinter as tk
from tkinter import ttk

settings = {}
sashcolor = 'green'

root = tk.Tk()
style = ttk.Style()
style.theme_use("clam")

settings.update(
    {
        'Sash': {
            "configure": {
                "sashthickness": 3,
                "gripcount": 0,
            },
        },
        'green.TPanedwindow': {
            "configure": {
                "background": sashcolor
            }
        },
    }
)

style.theme_settings("clam", settings)

pw = ttk.PanedWindow(root, style="green.TPanedwindow")
pw.add(ttk.Frame(pw, width=200, height=200))
pw.add(ttk.Frame(pw, width=200, height=200))
pw.pack(padx=10, pady=10)

root.mainloop()
