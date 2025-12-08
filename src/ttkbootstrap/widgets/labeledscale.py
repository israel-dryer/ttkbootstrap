import tkinter as tk
from typing import Any, Literal

from ttkbootstrap.core.exceptions import ConfigurationWarning
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.scale import Scale


class LabeledScale(Frame):
    """A horizontal scale widget with a label showing the current value.

    The scale widget can be accessed via `instance.scale` and the label
    widget via `instance.label`. The label automatically updates to display
    the current value and follows the slider position.

    Only horizontal orientation is currently supported.

    Example:
        >>> import ttkbootstrap as ttk
        >>> root = ttk.Window()
        >>> scale = ttk.LabeledScale(root, minvalue=0, maxvalue=100)
        >>> scale.pack(padx=10, pady=10, fill='x')
        >>> print(scale.value)
    """

    def __init__(
            self,
            master=None,
            value: int | float = 0,
            minvalue: int | float = 0,
            maxvalue: int | float = 100,
            variable: tk.Variable = None,
            dtype: type[int] | type[float] = int,
            compound: Literal['before', 'after'] = 'before',
            bootstyle: str = None,
            **kwargs

    ):
        """Create a horizontal labeled scale widget.

        The widget combines a Scale and Label in a Frame, with the label
        positioned either above or below the scale based on the compound
        parameter. The label automatically tracks the slider position and
        displays the current value.

        Args:
            master: The parent widget. If None, uses the default root window.
            value: Initial value for the scale. Defaults to 0.
            minvalue: Minimum value of the scale range. Maps to the scale's
                'from_' parameter. Defaults to 0.
            maxvalue: Maximum value of the scale range. Maps to the scale's
                'to' parameter. Defaults to 100.
            variable: A tkinter variable to associate with the scale. If None,
                creates an IntVar or DoubleVar based on dtype. Defaults to None.
            dtype: Data type for the scale value, either int or float. Determines
                the type of variable created if variable is None. Defaults to int.
            compound: Label position relative to the scale. Use 'before' for
                label above the scale or 'after' for label below the scale.
                Defaults to 'before'.
            bootstyle: Style to apply to both the scale and label. Options
                include primary, secondary, success, info, warning, danger,
                light, dark. Defaults to None.
            **kwargs: Additional keyword arguments passed to the Frame constructor.
                A padding of 2 is forced to provide minimal spacing.
        """
        self._compound = compound
        self._dtype = dtype
        self._variable: tk.Variable = (
            variable or
            tk.IntVar(master, dtype(value)) if dtype is int else
            tk.DoubleVar(master, dtype(value))
        )
        min_value = kwargs.pop('from_', dtype(minvalue))
        max_value = kwargs.pop('to', dtype(maxvalue))

        # force small padding on container
        kwargs['padding'] = 2

        super().__init__(master, **kwargs)

        # state tracking
        self._last_value = dtype(value)

        # layout
        self.label = Label(self, bootstyle=bootstyle, anchor="center")
        self.scale = Scale(
            self,
            variable=self._variable,
            from_=min_value,
            to=max_value,
            bootstyle=bootstyle,
            orient='horizontal',
        )

        # Pack scale and dummy label to reserve space
        scale_side: Any = 'bottom' if compound == 'before' else 'top'
        label_side: Any = 'top' if scale_side == 'bottom' else 'bottom'
        self.scale.pack(side=scale_side, fill='x')

        # Dummy required to make frame correct height
        dummy = Label(self)
        dummy.pack(side=label_side)
        dummy.lower()

        # Position label with place geometry manager
        lbl_anchor: Any = 'n' if compound == 'before' else 's'
        self.label.place(anchor=lbl_anchor)
        self.label.lift()

        # event and value binding
        self._bindings = {
            '<<RangeChanged>>': self.scale.bind('<<RangeChanged>>', self._adjust_value),
            '<Configure>': self.bind('<Configure>', self._adjust_value),
            '<Map>': self.bind('<Map>', self._adjust_value),
            'trace': self._variable.trace_add('write', self._adjust_value)
        }

    def destroy(self):
        """Destroy the widget and clean up the associated variable."""
        try:
            self._variable.trace_remove('write', self._bindings['trace'])
        except AttributeError:
            pass
        else:
            del self._variable
        super().destroy()
        self.label = None
        self.scale = None

    @property
    def value(self) -> int | float:
        """Get the current scale value.

        Returns:
            The current value of the scale as an int or float.
        """
        return self._variable.get()

    @value.setter
    def value(self, value: int | float):
        """Set the scale to a new value.

        Args:
            value: The new value to set.
        """
        self._variable.set(value)

    @configure_delegate('value')
    def _delegate_value(self, value=None):
        if value is not None:
            return self.value
        else:
            self.value = value
            return None

    @configure_delegate('minvalue')
    def _delegate_minvalue(self, value=None):
        if value is not None:
            return self.cget('from_')
        else:
            self.configure(from_=value)
            return None

    @configure_delegate('maxvalue')
    def _delegate_maxvalue(self, value=None):
        if value is not None:
            return self.cget('to')
        else:
            self.configure(to=value)
            return None

    @configure_delegate('dtype')
    def _delegate_dtype(self, value=None):
        if value is None:
            return self._dtype
        else:
            raise ConfigurationWarning('dtype must be configured in the widget constructor')

    def _adjust_value(self, *_):
        """Update label text and position to follow the slider handle."""

        def adjust_label():
            self.update_idletasks()  # "force" scale redraw

            # Get slider position
            x, y = self.scale.coords()

            # ttkbootstrap Scale may have different padding than tkinter
            # Adjust x position to properly center the label
            x = x - (6 if self._compound == 'before' else 7)

            # Calculate y position based on compound setting
            if self._compound == 'before':
                y = self.scale.winfo_y() - self.label.winfo_reqheight() - 3  # add small offset for focus ring
            else:
                y = self.scale.winfo_reqheight() + self.label.winfo_reqheight()

            self.label.place_configure(x=x, y=y)

        # Validate value is within range
        minvalue = self._dtype(self.scale['from'])
        maxvalue = self._dtype(self.scale['to'])
        if maxvalue < minvalue:
            minvalue, maxvalue = maxvalue, minvalue
        new_value = self._variable.get()
        if not minvalue <= new_value <= maxvalue:
            # value outside range, set value back to the last valid one
            self.value = self._last_value
            return

        self._last_value = new_value
        self.label['text'] = new_value
        self.after_idle(adjust_label)
