from tkinter import Widget


class BaseMixin:
    """A mixin class for common functionality between all widgets."""
    _widget: Widget

    def __str__(self):
        return str(self.widget)

    @property
    def widget(self):
        return self._widget

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
