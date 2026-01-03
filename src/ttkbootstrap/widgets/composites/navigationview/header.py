"""NavigationViewHeader widget for section labels in navigation menus."""

from typing import Any

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class NavigationViewHeader(Frame):
    """A non-selectable section header for grouping navigation items.

    NavigationViewHeader provides a text label to identify groups of related
    navigation items. Unlike NavigationViewItem, headers are not selectable
    and serve only as visual labels. Uses the 'label' font token for styling.

    Example:
        ```python
        nav.add_item('home', text='Home', icon='house')
        nav.add_header('Favorites')  # Creates NavigationViewHeader
        nav.add_item('photos', text='Photos', icon='image')
        nav.add_item('music', text='Music', icon='music-note')
        ```
    """

    def __init__(
        self,
        master: Master = None,
        text: str = '',
        **kwargs: Any
    ):
        """Initialize a NavigationViewHeader.

        Args:
            master (Master | None): Parent widget.
            text (str): The header text to display.
            **kwargs: Additional arguments passed to Frame.
        """
        self._text = text

        # Default padding: more top margin for visual separation
        kwargs.setdefault('padding', (8, 12, 8, 4))

        super().__init__(master, **kwargs)

        # Create header label with 'label' font (smaller, bold) and secondary accent
        self._text_label = Label(
            self,
            text=text,
            font='label',
            accent='secondary',
            anchor='w',
        )
        self._text_label.pack(fill='x')

    @property
    def text(self) -> str:
        """Get the header text."""
        return self._text

    @configure_delegate('text')
    def _delegate_text(self, value: str = None):
        """Configure the header text."""
        if value is None:
            return self._text
        self._text = value
        self._text_label.configure(text=value)
        return None
