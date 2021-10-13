import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_menubutton_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default button
    btn = ttk.Menubutton(frame, text=widget_style, style=widget_style)
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored buttons
    for color in style.colors:
        button_style = f'{color}.{widget_style}'
        btn = ttk.Menubutton(frame, text=button_style, style=button_style)
        btn.pack(padx=5, pady=5, fill=tk.BOTH)

    # disabled button
    disabled_style = f'{widget_style} (disabled)'
    btn = ttk.Menubutton(frame, text=disabled_style, state=tk.DISABLED, 
                    style=widget_style)
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_menubutton_frame('TMenubutton', style).pack(side=tk.LEFT)
    create_menubutton_frame('Outline.TMenubutton', style).pack(side=tk.LEFT)

    root.mainloop()