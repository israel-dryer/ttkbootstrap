"""LabeledScale widget for ttkbootstrap."""
import tkinter as tk
from tkinter import ttk

from ttkbootstrap.constants import DEFAULT


class LabeledScale(ttk.Frame):
    """A Ttk Scale widget with a Ttk Label widget indicating its
    current value.

    The Ttk Scale can be accessed through instance.scale, and Ttk Label
    can be accessed through instance.label"""

    def __init__(self, master=None, variable=None, from_=0, to=10, bootstyle=DEFAULT, **kwargs):
        """Construct a horizontal LabeledScale with parent master, a
        variable to be associated with the Ttk Scale widget and its range.
        If variable is not specified, a tkinter.IntVar is created.

        WIDGET-SPECIFIC OPTIONS

            compound: 'top' or 'bottom'
                Specifies how to display the label relative to the scale.
                Defaults to 'top'.
        """
        super().__init__(master=master, **kwargs)
        self._label_top = kwargs.pop('compound', 'top') == 'top'

        ttk.Frame.__init__(self, master, **kwargs)
        self._variable = variable or tk.IntVar(master)
        self._variable.set(from_)
        self._last_valid = from_
        self._bootstyle = bootstyle

        self.label = ttk.Label(self, bootstyle=bootstyle)
        self.scale = ttk.Scale(self, variable=self._variable, from_=from_, to=to, bootstyle=bootstyle)
        self.scale.bind('<<RangeChanged>>', self._adjust)

        # position scale and label according to the compound option
        scale_side = 'bottom' if self._label_top else 'top'
        label_side = 'top' if scale_side == 'bottom' else 'bottom'
        self.scale.pack(side=scale_side, fill='x')
        # Dummy required to make frame correct height
        dummy = ttk.Label(self)
        dummy.pack(side=label_side)
        dummy.lower()
        self.label.place(anchor='n' if label_side == 'top' else 's')

        # update the label as scale or variable changes
        self.__tracecb = self._variable.trace_add('write', self._adjust)
        self.bind('<Configure>', self._adjust)
        self.bind('<Map>', self._adjust)

    def destroy(self):
        """Destroy this widget and possibly its associated variable."""
        try:
            self._variable.trace_remove('write', self.__tracecb)
        except AttributeError:
            pass
        else:
            del self._variable
        super().destroy()
        self.label = None
        self.scale = None

    def _to_number(self, x):
        if isinstance(x, str):
            if '.' in x:
                x = float(x)
            else:
                x = int(x)
        return x

    def _adjust(self, *args):
        """Adjust the label position according to the scale."""

        def adjust_label():
            self.update_idletasks()  # "force" scale redraw

            x, y = self.scale.coords()
            if self._label_top:
                y = self.scale.winfo_y() - self.label.winfo_reqheight()
            else:
                y = self.scale.winfo_reqheight() + self.label.winfo_reqheight()

            self.label.place_configure(x=x, y=y)

        from_ = self._to_number(self.scale['from'])
        to = self._to_number(self.scale['to'])
        if to < from_:
            from_, to = to, from_
        newval = self._variable.get()
        if not from_ <= newval <= to:
            # value outside range, set value back to the last valid one
            self.value = self._last_valid
            return

        self._last_valid = newval
        self.label['text'] = newval
        self.after_idle(adjust_label)

    @property
    def value(self):
        """Return current scale value."""
        return self._variable.get()

    @value.setter
    def value(self, val):
        """Set new scale value."""
        self._variable.set(val)