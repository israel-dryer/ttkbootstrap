import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ScrolledText(ttk.Frame):

    """A text widget with a vertical scrollbar."""

    def __init__(self, master=None, padding=2, bootstyle=DEFAULT, **kwargs):
        """
        Parameters:

            master (Widget):
                The parent widget.

            padding (int):
                The amount of empty space to create on the outside of the 
                widget.

            bootstyle (str):
                A style keyword used to set the color and style of the vertical 
                scrollbar. Available options include -> primary, secondary, 
                success, info, warning, danger, dark, light.

            **kwargs (Dict[str, Any]):
                Other keyword arguments passed to the `Text` widget.
        """
        super().__init__(master, padding=padding)

        # setup text widget
        kwargs['master'] = self
        self._text = ttk.Text(**kwargs)
        self._text.pack(side=LEFT, fill=BOTH, expand=YES)

        # delegate text methods to frame widget
        for method in vars(ttk.Text).keys():
            if any(['pack' in method, 'grid' in method, 'place' in method]):
                pass
            else:
                setattr(self, method, getattr(self._text, method))

        # setup scrollbar
        self._scrollbar = ttk.Scrollbar(
            master=self, 
            bootstyle=bootstyle,
            command=self._text.yview
        )
        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._text.configure(yscrollcommand=self._scrollbar.set)


if __name__ == '__main__':

    app = ttk.Window()

    nb = ttk.Notebook(app)
    t = ScrolledText(nb, padding=20, bootstyle='info-round')
    t.insert(END, 'What is this?')
    nb.add(t, text="My Text")
    nb.pack()
    app.mainloop()


    