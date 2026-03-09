"""SideNavSeparator widget for visual grouping in navigation menus."""

from typing import Any

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.types import Master


class SideNavSeparatorKwargs(TypedDict, total=False):
    # Frame options
    padding: Any
    width: int
    height: int


class SideNavSeparator(Frame):
    """A visual separator for grouping items in a SideNav.

    SideNavSeparator provides a horizontal line to visually separate
    groups of navigation items. It is a thin wrapper around the Separator
    primitive with appropriate padding for navigation contexts.

    Example:
        ```python
        nav.add_item('home', text='Home', icon='house')
        nav.add_item('documents', text='Documents', icon='folder')
        nav.add_separator()  # Creates SideNavSeparator
        nav.add_item('settings', text='Settings', icon='gear')
        ```
    """

    DEFAULT_PADDING = (0, 4, 0, 4)

    def __init__(self, master: Master = None, **kwargs: Unpack[SideNavSeparatorKwargs]):
        """Initialize a SideNavSeparator.

        Args:
            master (Master | None): Parent widget.
            **kwargs: Additional arguments passed to Frame.
        """
        # Default padding for visual separation
        kwargs.setdefault('padding', self.DEFAULT_PADDING)

        super().__init__(master, **kwargs)

        # Create horizontal separator
        self._separator = Separator(self, orient='horizontal')
        self._separator.pack(fill='x')
