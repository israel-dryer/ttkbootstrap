"""TabView widget - a tabbed container combining Tabs with PageStack."""
from __future__ import annotations

__all__ = ['TabView']

import tkinter as tk
from typing import Callable, Literal, Union

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.composites.tabs.tabs import Tabs
from ttkbootstrap.widgets.composites.tabs.tabitem import TabItem
from ttkbootstrap.widgets.composites.pagestack import PageStack
from ttkbootstrap.widgets.types import Master


class TabView(Frame):
    """A tabbed container that combines Tabs with a PageStack.

    TabView provides a complete tabbed interface where each tab corresponds
    to a page in the page stack. Selecting a tab navigates to the associated
    page.

    !!! note "Events"
        - ``<<TabSelect>>``: Fired when a tab is selected.
        - ``<<TabClose>>``: Fired when a tab's close button is clicked.
        - ``<<TabAdd>>``: Fired when the add button is clicked (if enable_adding=True).
        - ``<<PageChange>>``: Fired when the page changes (from PageStack).
    """

    def __init__(
        self,
        master: Master = None,
        orient: Literal['horizontal', 'vertical'] = 'horizontal',
        variant: Literal['pill', 'bar'] = 'bar',
        show_divider: bool = None,
        compound: Literal['left', 'right', 'top', 'bottom', 'center', 'none'] = 'left',
        tab_width: Union[None, int, Literal['stretch']] = None,
        tab_padding: tuple = (12, 8),
        tab_anchor: str = None,
        enable_closing: Union[bool, Literal['hover']] = False,
        enable_adding: bool = False,
        color: str = None,
        **kwargs
    ):
        """Create a TabView widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            orient: Orientation of the tab bar. 'horizontal' places tabs above
                the content, 'vertical' places tabs to the left. Default is 'horizontal'.
            variant: Visual style variant ('pill' or 'bar').
            show_divider: Whether to show a divider between tabs and content.
            compound: How to position icon relative to text in tabs.
            tab_width: Width of tabs (None, integer, or 'stretch').
            tab_padding: Padding for all tabs as (horizontal, vertical).
            tab_anchor: Anchor for tab text/icon alignment. If None, defaults
                to 'w' for vertical orientation, 'center' for horizontal.
            enable_closing: Default close button visibility for all tabs.
                True=always visible, False=hidden, 'hover'=visible on hover.
                Can be overridden per-tab via `closable` in add().
            enable_adding: If True, shows an "add" button that fires `<<TabAdd>>`.
            color: Color token for styling.
            **kwargs: Additional arguments passed to Frame.
        """
        super().__init__(master, **kwargs)

        self._orient = orient
        self._variant = variant
        self._color = color

        # Create internal variable for tab selection
        self._tab_variable = tk.StringVar()

        # Create tabs container
        self._tabs = Tabs(
            self,
            orient=orient,
            variant=variant,
            show_divider=show_divider,
            compound=compound,
            tab_width=tab_width,
            tab_padding=tab_padding,
            tab_anchor=tab_anchor,
            enable_closing=enable_closing,
            enable_adding=enable_adding,
            variable=self._tab_variable,
            color=color,
        )

        # Create page stack
        self._page_stack = PageStack(self)

        # Layout based on orientation
        if orient == 'horizontal':
            self._tabs.pack(side='top', fill='x')
            self._page_stack.pack(side='top', fill='both', expand=True)
        else:
            self._tabs.pack(side='left', fill='y')
            self._page_stack.pack(side='left', fill='both', expand=True)

        # Bind variable trace to navigate pages
        self._trace_id = self._tab_variable.trace_add('write', self._on_tab_selected)

        # Track tabs by key for removal
        self._tab_map: dict[str, TabItem] = {}

        # Clean up trace on destroy
        self.bind('<Destroy>', self._on_destroy, add='+')

    def _on_destroy(self, event=None):
        """Clean up variable trace when widget is destroyed."""
        if event.widget is not self:
            return
        if self._trace_id is not None:
            try:
                self._tab_variable.trace_remove('write', self._trace_id)
            except Exception:
                pass
            self._trace_id = None

    def _on_tab_selected(self, *args):
        """Handle tab selection to navigate page stack."""
        key = self._tab_variable.get()
        if key and key in self._tab_map:
            # Only navigate if not already on this page
            current = self._page_stack.current()
            if current is None or current[0] != key:
                self._page_stack.navigate(key)

    def add(
        self,
        key: str,
        text: str = "",
        icon: str | dict = None,
        page: tk.Widget = None,
        closable: Union[bool, Literal['hover'], None] = None,
        close_command: Callable = None,
        command: Callable = None,
        sticky: str = 'nsew',
        **kwargs
    ) -> tk.Widget:
        """Add a tab and its associated page.

        Args:
            key: Unique identifier for the tab/page.
            text: Text to display on the tab.
            icon: Icon to display on the tab.
            page: The page widget. If None, creates a Frame.
            closable: Close button visibility (True, False, 'hover', or None).
                If None, uses the widget's `enable_closing` setting.
            close_command: Callback when close button is clicked.
                If not provided and closable is enabled, removes the tab/page.
            command: Callback when tab is selected.
            sticky: Grid sticky parameter for the page layout.
            **kwargs: Additional arguments passed to page Frame (if created).

        Returns:
            The page widget.
        """
        # Determine effective closable value
        effective_closable = closable if closable is not None else self._tabs._enable_closing

        # Create close command wrapper if closable but no command provided
        if effective_closable and close_command is None:
            close_command = lambda k=key: self.remove(k)

        # Add tab
        tab = self._tabs.add_tab(
            text=text,
            icon=icon,
            value=key,
            closable=closable,
            close_command=close_command,
            command=command,
        )
        self._tab_map[key] = tab

        # Add page
        page_widget = self._page_stack.add(key, page, sticky=sticky, **kwargs)

        # If this is the first tab, select it
        if len(self._tab_map) == 1:
            self._tab_variable.set(key)

        return page_widget

    def remove(self, key: str) -> None:
        """Remove a tab and its associated page.

        Args:
            key: The identifier of the tab/page to remove.
        """
        # Remove tab
        if key in self._tab_map:
            tab = self._tab_map.pop(key)
            self._tabs.remove(tab)
            tab.destroy()

        # Remove page
        self._page_stack.remove(key)

        # If the removed tab was selected, select another
        if self._tab_variable.get() == key:
            if self._tab_map:
                # Select the first available tab
                first_key = next(iter(self._tab_map))
                self._tab_variable.set(first_key)
            else:
                self._tab_variable.set('')

    def select(self, key: str) -> None:
        """Select a tab by its key.

        Args:
            key: The identifier of the tab to select.
        """
        if key in self._tab_map:
            self._tab_variable.set(key)

    def navigate(self, key: str, data: dict = None) -> None:
        """Navigate to a tab/page with optional data.

        Args:
            key: The identifier of the tab/page to navigate to.
            data: Optional data to pass to the page.
        """
        if key in self._tab_map:
            self._tab_variable.set(key)
            if data:
                self._page_stack.navigate(key, data=data)

    @property
    def tabs_widget(self) -> Tabs:
        """Get the internal Tabs widget."""
        return self._tabs

    @property
    def page_stack_widget(self) -> PageStack:
        """Get the internal PageStack widget."""
        return self._page_stack

    @property
    def current(self) -> str | None:
        """Get the currently selected tab key."""
        key = self._tab_variable.get()
        return key if key else None

    def page(self, key: str) -> tk.Widget:
        """Get a page widget by its key.

        Args:
            key: The identifier of the page.

        Returns:
            The page widget.

        Raises:
            KeyError: If no page with the given key exists.
        """
        return self._page_stack.item(key)

    def pages(self) -> tuple[tk.Widget, ...]:
        """Get all page widgets.

        Returns:
            A tuple of all page widgets.
        """
        return self._page_stack.items()

    def page_keys(self) -> tuple[str, ...]:
        """Get all page keys.

        Returns:
            A tuple of all page keys.
        """
        return self._page_stack.keys()

    def tab(self, key: str) -> TabItem:
        """Get a tab widget by its key.

        Args:
            key: The identifier of the tab.

        Returns:
            The TabItem widget.

        Raises:
            KeyError: If no tab with the given key exists.
        """
        if key not in self._tab_map:
            raise KeyError(f"No tab with key '{key}'")
        return self._tab_map[key]

    def tabs(self) -> tuple[TabItem, ...]:
        """Get all tab widgets.

        Returns:
            A tuple of all TabItem widgets.
        """
        return tuple(self._tab_map.values())

    def tab_keys(self) -> tuple[str, ...]:
        """Get all tab keys.

        Returns:
            A tuple of all tab keys.
        """
        return tuple(self._tab_map.keys())

    def configure_tab(self, key: str, option: str = None, **kwargs):
        """Configure a specific tab by its key.

        Args:
            key: The key of the tab to configure.
            option: If provided, return the value of this option.
            **kwargs: Configuration options to apply to the tab.

        Returns:
            If option is provided, returns the value of that option.
        """
        tab = self.tab(key)
        if option is not None:
            return tab.cget(option)
        tab.configure(**kwargs)

    def on_page_changed(self, callback: Callable) -> str:
        """Bind to ``<<PageChange>>`` event.

        Args:
            callback: Function to call when page changes.

        Returns:
            Binding identifier.
        """
        return self._page_stack.on_page_changed(callback)

    def off_page_changed(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<PageChange>>`` event."""
        self._page_stack.off_page_changed(bind_id)

    def on_tab_added(self, callback: Callable) -> str:
        """Bind to ``<<TabAdd>>`` event (when add button is clicked).

        Args:
            callback: Function to call when add button is clicked.

        Returns:
            Binding identifier for use with off_tab_added().
        """
        return self._tabs.on_tab_added(callback)

    def off_tab_added(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<TabAdd>>`` event."""
        self._tabs.off_tab_added(bind_id)
