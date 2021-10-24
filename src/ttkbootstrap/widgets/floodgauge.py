import tkinter as tk
from uuid import uuid4
import tkinter as tk
from tkinter.ttk import Progressbar
from ttkbootstrap import Style


class Floodgauge(Progressbar):
    """A ``Floodgauge`` widget shows the status of a long-running 
    operation with an optional text indicator. 

    Similar to the ``ttk.Progressbar``, this widget can operate in two 
    modes: **determinate** mode shows the amount completed relative to 
    the total amount of work to be done, and **indeterminate** mode 
    provides an animated display to let the user know that something is 
    happening.

    Variable are generated automatically for this widget and can be 
    linked to other widgets by referencing them via the 
    ``textvariable`` and ``variable`` attributes.

    The ``text`` and ``value`` properties allow you to easily get and 
    set the value of these variables without the need to call the 
    ``get`` and ``set`` methods of the related tkinter variables. For 
    example: ``Floodgauge.value`` or ``Floodgauge.value = 55`` will 
    get or set the amount used on the widget.
    """

    def __init__(
        self,
        master=None,
        cursor=None,
        font=None,
        length=None,
        maximum=100,
        mode='determinate',
        orient=tk.HORIZONTAL,
        style='TFloodgauge',
        takefocus=False,
        text=None,
        value=0,
        **kw
    ):
        """
        Parameters
        ----------
        master : Widget
            Parent widget

        cursor : str
            The cursor that will appear when the mouse is over the 
            progress bar.

        font Union[Font, str]
            The font to use for the progress bar label.

        length : int
            Specifies the length of the long axis of the progress bar 
            (width if horizontal, height if vertical); Default=300.

        maximum : float
            A floating point number specifying the maximum ``value``. 
            Default=100.

        mode : { determinate, indeterminate }
            Use `indeterminate` if you cannot accurately measure the 
            relative progress of the underlying process. In this mode, 
            a rectangle bounces back and forth between the ends of the 
            widget once you use the ``.start()`` method.  Otherwise, 
            use `determinate` if the relative progress can be 
            calculated in advance. This is the default mode. 

        orient : { horizontal, vertical }
            Specifies the orientation of the widget.

        style : str
            The style used to render the widget.

        takefocus : bool
            This widget is not included in focus traversal by default. 
            To add the widget to focus traversal, use 
            ``takefocus=True``.

        text : str
            A string of text to be displayed in the progress bar. This 
            is assigned to the ``StringVar`` which is automatically 
            generated on instantiation. This value can be get and set 
            using the ``Floodgauge.text`` property without having to 
            directly call the ``textvariable``. 

        value : float
            The current value of the progressbar. In `determinate`
            mode, this represents the amount of work completed. In 
            `indeterminate` mode, it is interpreted modulo ``maximum``; 
            that is, the progress bar completes one "cycle" when the 
            ``value`` increases by ``maximum``.

        **kw : Dict[str, Any]
            Other configuration options from the option database.
        """
        # create a custom style in order to adjust the text inside the progress bar layout
        if any(['Horizontal' in style, 'Vertical' in style]):
            self._widgetstyle = f'{uuid4()}.{style}'
        elif orient == 'vertical':
            self._widgetstyle = f'{uuid4()}.Vertical.TFloodgauge'
        else:
            self._widgetstyle = f'{uuid4()}.Horizontal.TFloodgauge'

        # progress bar value variable
        self.variable = tk.IntVar(value=value)

        super().__init__(
            master=master,
            class_='Floodgauge',
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            style=self._widgetstyle,
            takefocus=takefocus,
            variable=self.variable,
            **kw
        )
        # set the label font
        if font:
            self.tk.call("ttk::style", "configure",
                         self._widgetstyle, '-%s' % 'font', font, None)

        # progress bar text variable
        self.textvariable = tk.StringVar(value=text or '')
        self.textvariable.trace_add('write', self._textvariable_write)
        self._textvariable_write()

    @property
    def text(self):
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        self.textvariable.set(value)

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, value):
        self.variable.set(value)

    def _textvariable_write(self, *args):
        """Callback to update the label text when there is a `write` 
        action on the textvariable

        Parameters
        ----------
        *args
            If triggered by a trace, will be `variable`, `index`, 
            `mode`.
        """
        self.tk.call("ttk::style", "configure", self._widgetstyle,
                     '-%s' % 'text', self.textvariable.get(), None)


if __name__ == '__main__':
    # TESTING
    root = tk.Tk()
    root.geometry('500x500')
    root.title('ttkbootstrap')
    s = Style()

    p1 = Floodgauge(
        orient=tk.VERTICAL,
        style='danger.Vertical.TFloodgauge'
    )
    p2 = Floodgauge(
        orient=tk.HORIZONTAL,
        style='danger.Horizontal.TFloodgauge'
    )

    def auto():
        p1.text = f'Memory\n{p1.value}%'
        p1.step(1)

        p2.text = f'Memory\n{p2.value}%'
        p2.step(1)
        p2.after(50, auto)

    p1.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
    p2.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
    auto()
    root.mainloop()
