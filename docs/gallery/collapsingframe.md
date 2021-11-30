# Collapsing Frame
This example demonstrates how to build a collapsing frame widget. Each `Frame` 
added to the widget can be assigned a title and style. Various bootstyles are
applied to each option group. 

The theme used is **litera**.

![file search image example](../assets/gallery/collapsing_frame.png)

## Style Summary

| Item              | Class             | Bootstyle |
| ---               | ---               | --- |
| Option group 1    | `CollapsingFrame` | primary |
| Option group 2    | `CollapsingFrame` | danger |
| Option group 3    | `CollapsingFrame` | success |

## Example Code

[Run this code live]() on repl.it

```python
from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.style import Bootstyle


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Collapsing Frame')
        self.style = ttk.Style()
        self.minsize(300, 1)

        cf = CollapsingFrame(self)
        cf.pack(fill='both')

        # option group 1
        group1 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group1, text=f'Option {x + 1}').pack(fill=tk.X)
        cf.add(child=group1, title='Option Group 1')

        # option group 2
        group2 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group2, text=f'Option {x + 1}').pack(fill=tk.X)
        cf.add(group2, title='Option Group 2', bootstyle='danger')

        # option group 3
        group3 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group3, text=f'Option {x + 1}').pack(fill=tk.X)
        cf.add(group3, title='Option Group 3', bootstyle='success')


class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        _path = Path(__file__).parent / 'assets'
        self.images = [
            tk.PhotoImage(
                name='open',
                file=_path / 'icons8_double_up_24px.png'
            ),
            tk.PhotoImage(
                name='closed',
                file=_path / 'icons8_double_right_24px.png'
            )
        ]

    def add(self, child, title="", bootstyle='primary', **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget

            title (str):
                The title appearing on the collapsible section header

            bootstyle (str):
                The style to apply to the collapsible section header
        """
        if child.winfo_class() != 'TFrame':
            return
        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=tk.EW)

        # header title
        lbl = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, 'inverse')
        )
        if kwargs.get('textvariable'):
            lbl.configure(textvariable=kwargs.get('textvariable'))
        lbl.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(child)
        btn = ttk.Button(
            master=frm,
            image='open',
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=tk.RIGHT)

        # assign toggle button to child so that it's accesible when
        # toggling (need to change image)
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=tk.NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button image 
        accordingly

        Parameters:
        
            child (Frame):
                The child element to add or remove from grid manager
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image='closed')
        else:
            child.grid()
            child.btn.configure(image='open')


if __name__ == '__main__':

    Application().mainloop()
```