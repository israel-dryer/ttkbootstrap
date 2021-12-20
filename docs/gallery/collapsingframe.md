# Collapsing Frame
This example demonstrates how to build a collapsing frame widget. Each `Frame` 
added to the widget can be assigned a title and style. Various bootstyles are
applied to each option group. 

![file search image example](../assets/gallery/collapsing_frame.png)
 
## Style Summary
The theme used is **litera**.

| Item              | Class             | Bootstyle |
| ---               | ---               | --- |
| Option group 1    | `CollapsingFrame` | primary |
| Option group 2    | `CollapsingFrame` | danger |
| Option group 3    | `CollapsingFrame` | success |

## Example Code
[Run this code live](https://replit.com/@israel-dryer/collapsing-frame#main.py) on repl.it

```python
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle


IMG_PATH = Path(__file__).parent / 'assets'


class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = [
            ttk.PhotoImage(file=IMG_PATH/'icons8_double_up_24px.png'),
            ttk.PhotoImage(file=IMG_PATH/'icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return
        
        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button 
        image accordingly.

        Parameters:
            
            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])


if __name__ == '__main__':

    app = ttk.Window(minsize=(300, 1))

    cf = CollapsingFrame(app)
    cf.pack(fill=BOTH)

    # option group 1
    group1 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group1, text=f'Option {x + 1}').pack(fill=X)
    cf.add(child=group1, title='Option Group 1')

    # option group 2
    group2 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group2, text=f'Option {x + 1}').pack(fill=X)
    cf.add(group2, title='Option Group 2', bootstyle=DANGER)

    # option group 3
    group3 = ttk.Frame(cf, padding=10)
    for x in range(5):
        ttk.Checkbutton(group3, text=f'Option {x + 1}').pack(fill=X)
    cf.add(group3, title='Option Group 3', bootstyle=SUCCESS)

    app.mainloop()
```