import tkinter
from collections.abc import ValuesView
from typing import Any, Callable

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives import Frame
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.core import NavigationError


class PageOptions(TypedDict, total=False):
    padding: Any
    width: int
    height: int
    style: str
    cursor: str
    show_border: bool
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]
    sticky: str


class PageStackKwargs(TypedDict, total=False):
    takefocus: bool
    width: int
    height: int
    padding: Any


class PageStack(Frame):
    """A navigation container widget for managing multiple pages with history support.

    PageStack provides a stack-based navigation system where only one page is
    visible at a time. It maintains a navigation history, allowing users to move
    backward and forward through pages similar to a web browser.

    !!! note "Events"

        - ``<<PageUnmount>>``: Triggered when the current page is hidden.
        - ``<<PageWillMount>>``: Triggered before a new page is displayed.
        - ``<<PageMount>>``: Triggered after a new page is displayed.
        - ``<<PageChange>>``: Triggered after page navigation completes.

        All events provide ``event.data`` with keys: ``page``, ``prev_page``, ``prev_data``,
        ``nav`` ('push', 'back', 'forward'), ``index``, ``length``, ``can_back``,
        ``can_forward``.
    """

    def __init__(self, master: Master = None, **kwargs: Unpack[PageStackKwargs]):
        """Initialize a new PageStack instance.

        Creates an empty PageStack with no pages and no navigation history.
        The widget inherits from Frame and supports all standard Frame
        configuration options.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            takefocus (bool): If True, the widget can receive keyboard focus.
            width (int): Width of the PageStack in pixels.
            height (int): Height of the PageStack in pixels.
            padding (int | tuple): Padding around the PageStack (can be a single value
                or tuple of (left, top, right, bottom)).

        Note:
            Pages must be added using add() before navigation can occur.
            The PageStack starts with an empty history and no current page.
        """
        super().__init__(master, **kwargs)
        self._pages: dict[str, tkinter.Widget] = {}
        self._current: str | None = None
        self._history: list[tuple[str, dict]] = []
        self._index: int = -1

    def add(self, key: str, page: tkinter.Widget = None, *, sticky: str = '', **kwargs) -> tkinter.Widget:
        """Add a page to the stack, optionally creating a Frame.

        Args:
            key (str): Unique identifier for the page (required for navigation).
            page (Widget | None): The widget to add. If None, creates a Frame.
            sticky (str): Grid sticky parameter for the page layout (e.g., 'nsew').
            **kwargs: When page is None, these are passed to Frame (e.g., padding, bootstyle).

        Returns:
            Widget: The page widget (passed or created Frame).

        Raises:
            NavigationError: If a page with the given key already exists.
            ValueError: If key is an empty string.
        """
        if not key:
            raise ValueError("Page key cannot be an empty string")
        if key in self._pages:
            raise NavigationError(f"Page {key} already exists")

        if page is None:
            page = Frame(self, **kwargs)

        self._pages[key] = page
        page.grid(sticky=sticky)
        page.grid_remove()
        return page

    def remove(self, key: str) -> None:
        """Remove a page from the stack and destroy its widget.

        Args:
            key: The identifier of the page to remove

        Note:
            If the removed page is currently displayed, the current page
            will be set to None without navigating to another page.
        """
        if key in self._pages:
            page = self._pages.pop(key)
            page.destroy()
        if self._current == key:
            self._current = None

    def navigate(
            self,
            key: str,
            data: dict | None = None,
            replace: bool = False,
            _nav: str = 'push',
            _prev: tuple[str, dict] | None = None
    ) -> None:
        """Navigate to the page with the given key.

        This method handles page transitions, manages navigation history,
        and triggers lifecycle events (``<<PageUnmount>>``, ``<<PageWillMount>>``,
        ``<<PageMount>>``, ``<<PageChange>>``).

        Args:
            key: The identifier of the page to navigate to
            data: Optional data to pass to the page and include in event payloads
            replace: If True, replace the current history entry instead of adding a new one
            _nav: Internal parameter indicating navigation type ('push', 'back', 'forward')
            _prev: Internal parameter for preserving previous page state

        Raises:
            NavigationError: If the page with the given key does not exist
            ValueError: If key is an empty string

        Note:
            Event payloads include: page, prev_page, prev_data, nav, index,
            length, can_back, and can_forward.
        """
        if not key:
            raise ValueError("Page key cannot be an empty string")
        if key not in self._pages:
            raise NavigationError(f"Page {key} does not exist")

        # Normalize data to empty dict if None
        if data is None:
            data = {}

        # Snapshot "previous" BEFORE mutating history
        if _prev is None:
            prev_key = self._current
            prev_data = self._history[self._index][1] if self._index >= 0 else {}
        else:
            prev_key, prev_data = _prev

        # Mutate history
        if replace and 0 <= self._index < len(self._history):
            self._history[self._index] = (key, data)
        else:
            if self._index < len(self._history) - 1:
                self._history = self._history[:self._index + 1]
            self._history.append((key, data))
            self._index += 1

        # Unmount previous page
        if self._current is not None:
            self._pages[self._current].event_generate('<<PageUnmount>>', when="tail")
            self._pages[self._current].grid_remove()

        # Normalized payload (self-contained snapshot)
        payload = dict(data)
        payload.update(
            {
                "page": key,
                "prev_page": prev_key,
                "prev_data": prev_data,
                "nav": _nav,
                "index": self._index,
                "length": len(self._history),
                "can_back": self._index > 0,
                "can_forward": self._index < len(self._history) - 1,
            }
        )

        # Mount and notify
        page = self._pages[key]
        page.event_generate('<<PageWillMount>>', data=payload, when="tail")
        page.grid()
        self._current = key
        self.event_generate('<<PageMount>>', data=payload, when="tail")
        self.event_generate('<<PageChange>>', data=payload, when="tail")

    def back(self) -> None:
        """Navigate to the previous page in the navigation history.

        This method moves backward in the history stack if possible.
        Does nothing if already at the first page.
        """
        if self._index > 0:
            # Snapshot BEFORE changing index
            prev = (self._current, self._history[self._index][1] if self._index >= 0 else {})
            self._index -= 1
            key, data = self._history[self._index]
            # use replace=True to avoid pushing a new entry
            # pass _prev to preserve the correct 'previous' snapshot
            self.navigate(key, data=data, replace=True, _nav='back', _prev=prev)

    def forward(self) -> None:
        """Navigate to the next page in the navigation history.

        This method moves forward in the history stack if possible.
        Does nothing if already at the most recent page.
        """
        if self._index < len(self._history) - 1:
            prev = (self._current, self._history[self._index][1] if self._index >= 0 else {})
            self._index += 1
            key, data = self._history[self._index]
            self.navigate(key, data=data, replace=True, _nav='forward', _prev=prev)

    def can_back(self) -> bool:
        """Check if backward navigation is possible.

        Returns:
            True if there is a previous page in the history to navigate back to,
            False otherwise.
        """
        return self._index > 0

    def can_forward(self) -> bool:
        """Check if forward navigation is possible.

        Returns:
            True if there is a next page in the history to navigate forward to,
            False otherwise.
        """
        return self._index < len(self._history) - 1

    def current(self) -> tuple[str, dict] | None:
        """Return the current page key and its navigation data.

        Returns:
            A tuple of (page_key, data_dict) if a page is currently displayed,
            None if no page is currently displayed.
        """
        if self._current is None:
            return None
        return self._current, (self._history[self._index][1] if self._index >= 0 else {})

    def configure_page(self, key: str, option: Any = None, **kwargs: Any) -> Any:
        """Query or configure the page configuration.

        Args:
            key: The identifier of the page to configure
            option: Optional configuration option to query. If 'sticky', returns
                   the grid sticky value. Otherwise queries the widget option.
            **kwargs: Configuration options to set on the page widget

        Returns:
            If option is provided, returns the value of that option.
            Otherwise returns the result of configure() if kwargs are provided.

        Raises:
            NavigationError: If the page with the given key does not exist
            ValueError: If key is an empty string
        """
        if not key:
            raise ValueError("Page key cannot be an empty string")
        if key not in self._pages:
            raise NavigationError(f"Page {key} does not exist")
        if option == 'sticky':
            return self._pages[key].grid_info().get('sticky')
        elif option is not None:
            return self._pages[key].cget(option)
        else:
            return self._pages[key].configure(**kwargs)

    def pages(self) -> ValuesView[tkinter.Widget]:
        """Return all page widgets in the stack.

        Returns:
            A view of all page widgets managed by this PageStack.
        """
        return self._pages.values()

    def on_page_changed(self, callback: Callable) -> str:
        """Bind to ``<<PageChange>>``. Callback receives ``event.data`` with navigation info.

        Returns:
            Binding identifier for use with off_page_changed().
        """
        return self.bind('<<PageChange>>', callback, add="+")

    def off_page_changed(self, funcid: str) -> None:
        """Unbind from ``<<PageChange>>``."""
        self.unbind("<<PageChange>>", funcid)
