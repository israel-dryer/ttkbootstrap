# Equalizer

This example demonstrates the use of styles to differentiate scale functions. 
Now for some comments on the code; because I wanted the scale value to be 
reflected in a label below the scale, this application is a lot more 
complicated than it really needs to be due to some oddities of the `Scale` 
implementation. The `Scale` widget outputs a double type, which means that 
in order to display a nice rounded integer, that number has to be converted 
when updated. Fortunately, the scale widget has a command parameter for setting 
a callback. The callback will get the scale value, which can then be converted 
into a nice clean format. 

The theme used is **litera**.

![file search image example](../assets/gallery/equalizer.png)

## Style Summary

| Item          | Class     | Bootstyle |
| ---           | ---       | ---       |
| Volume Scale  | `Scale`   | success   |
| Gain Scale    | `Scale`   | success   |
| Other Scales  | `Scale`   | info      |

!!! note
    For a vertical orientation, the `from_` parameter corresponds to the top 
    and `to` corresponds to the bottom of the widget, so you’ll need to take 
    this into account when you set the minimum and maximum numbers for your 
    scale range.

## Example Code

[Run this code live]() on repl.it

```python
import tkinter as tk
import ttkbootstrap as ttk
from random import randint


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Equalizer')
        self.style = ttk.Style()
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
            lbl = ttk.Label(
                master=frame,
                text=c,
                anchor=tk.CENTER,
                font=('Helvetica 10 bold')
            )
            lbl.pack(side=tk.TOP, fill=tk.X, pady=10)

            # slider

            if c in ['VOL', 'GAIN']:
                _bootstyle = 'success'
            else:
                _bootstyle = 'info'

            def _func(val, name=c): return self.setvar(
                name, f'{float(val):.0f}')

            scale = ttk.Scale(
                master=frame,
                orient=tk.VERTICAL,
                from_=99,
                to=1,
                value=value,
                command=_func,
                bootstyle=_bootstyle
            )
            scale.pack(fill=tk.Y)

            # slider value label
            ttk.Label(frame, textvariable=c).pack(pady=10)


if __name__ == '__main__':
    Application().mainloop()
```