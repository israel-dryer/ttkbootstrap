"""LabeledScale widget for ttkbootstrap.

This module provides the LabeledScale widget, which combines a Scale
widget with a Label that automatically displays the current value.

Example:
    ```python
    import ttkbootstrap as ttk

    root = ttk.Window()

    # Create a labeled scale
    scale = ttk.LabeledScale(root, from_=0, to=100)
    scale.pack(padx=10, pady=10)

    # Access the current value
    print(scale.value)

    root.mainloop()
    ```
"""
from tkinter import Misc
from typing import Any, Optional, Union

from ttkbootstrap import (
    Frame, IntVar, Label, Scale
)
from ttkbootstrap.constants import DEFAULT, Side


class LabeledScale(Frame):
    """A Ttk Scale widget with a Ttk Label widget indicating its current value.

    The label automatically updates to show the current scale value. The
    Ttk Scale can be accessed through instance.scale, and the Ttk Label
    can be accessed through instance.label.

    The label position can be configured to appear above or below the scale
    using the 'compound' parameter.
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            variable: Optional[IntVar] = None,
            from_: Union[int, float] = 0,
            to: Union[int, float] = 10,
            bootstyle: str = DEFAULT,
            **kwargs: Any
    ) -> None:
        """Construct a horizontal LabeledScale.

        Parameters:

            master (Widget, optional):
                The parent widget.

            variable (tk.IntVar, optional):
                A tkinter variable to be associated with the Scale widget.
                If not specified, a tkinter.IntVar is created automatically.

            from_ (int, optional):
                The minimum value of the scale. Defaults to 0.

            to (int, optional):
                The maximum value of the scale. Defaults to 10.

            bootstyle (str, optional):
                The style keyword used to set the color of the scale and label.
                Options include primary, secondary, success, info, warning,
                danger, light, dark. Defaults to DEFAULT.

            compound (str, optional):
                Specifies how to display the label relative to the scale.
                Options are 'top' or 'bottom'. Defaults to 'top'.

            **kwargs (dict[str, Any], optional):
                Other keyword arguments passed to the Frame widget.
        """
        super().__init__(master=master, **kwargs)
        self._label_top = kwargs.pop('compound', 'top') == 'top'

        Frame.__init__(self, master, **kwargs)
        self._variable = variable or IntVar(master)
        self._variable.set(from_)
        self._last_valid = from_
        self._bootstyle = bootstyle

        self.label = Label(self, bootstyle=bootstyle)
        self.scale = Scale(self, variable=self._variable, from_=from_, to=to, bootstyle=bootstyle)
        self.scale.bind('<<RangeChanged>>', self._adjust)

        # position scale and label according to the compound option
        scale_side: Side = 'bottom' if self._label_top else 'top'
        label_side: Side = 'top' if scale_side == 'bottom' else 'bottom'
        self.scale.pack(side=scale_side, fill='x')
        # Dummy required to make frame correct height
        dummy = Label(self)
        dummy.pack(side=label_side)
        dummy.lower()
        self.label.place(anchor='n' if label_side == 'top' else 's')

        # update the label as scale or variable changes
        self.__tracecb = self._variable.trace_add('write', self._adjust)
        self.bind('<Configure>', self._adjust)
        self.bind('<Map>', self._adjust)

    def destroy(self) -> None:
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

    def _to_number(self, x: Union[str, int, float]) -> Union[int, float]:
        """Convert a string to int or float.

        Parameters:
            x: Value to convert (str, int, or float).

        Returns:
            int or float: The converted number.
        """
        if isinstance(x, str):
            if '.' in x:
                x = float(x)
            else:
                x = int(x)
        return x

    def _adjust(self, *_) -> None:
        """Adjust the label position and text according to the scale value."""

        def adjust_label() -> None:
            self.update_idletasks()  # ensure geometry info is current

            x, y = self.scale.coords()

            # Vertical placement above or below the scale
            if self._label_top:
                y = self.scale.winfo_y() - self.label.winfo_reqheight()
            else:
                y = self.scale.winfo_reqheight() + self.label.winfo_reqheight()

            # Prevent horizontal clipping: clamp label center within frame
            frame_w = max(0, self.winfo_width())
            label_w = max(0, self.label.winfo_reqwidth())
            if frame_w > 0 and label_w > 0:
                half = label_w // 2
                # If label wider than frame, center within frame
                if label_w >= frame_w:
                    x = frame_w // 2
                else:
                    x = min(max(x, half), frame_w - half)

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
    def value(self) -> Union[int, float]:
        """Get the current scale value.

        Returns:
            int or float: The current value of the scale.
        """
        return self._variable.get()

    @value.setter
    def value(self, val: Union[int, float]) -> None:
        """Set the scale to a new value.

        Parameters:
            val (int or float): The new value to set.
        """
        self._variable.set(val)
