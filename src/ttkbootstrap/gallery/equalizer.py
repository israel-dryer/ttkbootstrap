"""
    Author: Israel Dryer
    Modified: 2021-10-14
"""
import tkinter as tk
from random import randint
from tkinter import ttk
from ttkbootstrap import Style


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Equalizer')
        self.style = Style()
        self.eq = Equalizer(self)
        self.eq.pack(fill=tk.BOTH, expand=tk.YES)


class Equalizer(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=20)
        controls = [
            'VOL', '31.25', '62.5', '125', 
            '250', '500', '1K', '2K', 
            '4K', '8K', '16K', 'GAIN'
            ]

        # create band widgets
        for c in controls:
            # starting random value
            value = randint(1, 99)
            self.setvar(c, value)

            # container
            frame = ttk.Frame(self, padding=5)
            frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

            # header
            lbl = ttk.Label(frame, text=c, anchor=tk.CENTER, 
                            font=('Helvetica 10 bold'))
            lbl.pack(side=tk.TOP, fill=tk.X, pady=10)

            # slider

            if c in ['VOL','GAIN']:
                _style = 'success.Vertical.TScale'
            else:
                _style = 'info.Vertical.TScale'

            _func = lambda val, name=c: self.setvar(name, f'{float(val):.0f}')

            scale = ttk.Scale(frame, orient=tk.VERTICAL, from_=99, to=1, 
                              value=value, command=_func, style=_style)
            scale.pack(fill=tk.Y)

            # slider value label
            ttk.Label(frame, textvariable=c).pack(pady=10)


if __name__ == '__main__':
    Application().mainloop()
