from tkinter import Widget


class BaseMixin:
    """A mixin class for common functionality between all widgets."""
    _widget: Widget

    def __str__(self):
        return str(self.widget)

    @property
    def tk(self):
        return self.widget.tk

    @property
    def _last_child_ids(self):
        return self.widget._last_child_ids

    @_last_child_ids.setter
    def _last_child_ids(self, value):
        self.widget._last_child_ids = value

    @property
    def children(self):
        return self.widget.children

    @property
    def widget(self):
        return self._widget

    @property
    def cursor(self):
        """Specifies the mouse cursor to be used for the widget."""
        return self.widget.cget("cursor")

    @cursor.setter
    def cursor(self, value):
        self.widget.configure(cursor=value)

    @property
    def state(self):
        """May be set to normal or disabled to control the disabled state bit."""

        return self.widget.cget("state")

    @state.setter
    def state(self, value):
        self.widget.configure(state=value)

    @property
    def take_focus(self) -> bool:
        """Get or set whether the button can take focus via keyboard navigation."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)

    @property
    def _w(self):
        return self._widget._w

    def pack(self, **kwargs):
        return self.widget.pack(**kwargs)

    def grid(self, **kwargs):
        return self.widget.grid(**kwargs)

    def place(self, **kwargs):
        return self.widget.place(**kwargs)

    def destroy(self):
        return self.widget.destroy()
