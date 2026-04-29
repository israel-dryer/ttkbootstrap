"""AppShell - a top-level application window with built-in navigation.

Provides a convenient way to scaffold the standard desktop app layout:
toolbar at top, sidebar navigation on the left, and page content on the right.
"""

from __future__ import annotations

from typing import Any, Callable, Literal

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.composites.toolbar import Toolbar
from ttkbootstrap.widgets.composites.sidenav import SideNav
from ttkbootstrap.widgets.composites.pagestack import PageStack
from ttkbootstrap.widgets.composites.scrollview import ScrollView
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.runtime.app import App


class AppShellKwargs(TypedDict, total=False):
    title: str
    theme: str
    size: tuple[int, int]
    position: tuple[int, int]
    minsize: tuple[int, int]
    maxsize: tuple[int, int]
    resizable: tuple[bool, bool]
    frameless: bool
    show_toolbar: bool
    show_window_controls: bool
    draggable: bool
    toolbar_density: Literal['default', 'compact']
    show_nav: bool
    nav_display_mode: Literal['expanded', 'compact', 'minimal']
    nav_accent: str


class AppShell(App):
    """A top-level application window with built-in navigation.

    AppShell extends `App` and wires together a `Toolbar`, `SideNav`, and
    `PageStack` into the common toolbar + sidebar + content layout. Each
    component is optional and exposed as a property for customization.
    Pages are registered through `add_page`, which creates the navigation
    item and the page container in one call.
    """

    def __init__(
        self,
        title: str = '',
        theme: str | None = None,
        size: tuple[int, int] | None = None,
        position: tuple[int, int] | None = None,
        minsize: tuple[int, int] | None = None,
        maxsize: tuple[int, int] | None = None,
        resizable: tuple[bool, bool] | None = None,
        frameless: bool = False,
        show_toolbar: bool = True,
        show_window_controls: bool = False,
        draggable: bool = False,
        toolbar_density: Literal['default', 'compact'] = 'default',
        show_nav: bool = True,
        nav_display_mode: Literal['expanded', 'compact', 'minimal'] = 'expanded',
        nav_accent: str = 'primary',
        **kwargs: Unpack[AppShellKwargs],
    ):
        """Initialize an AppShell.

        Args:
            title: Title displayed in the toolbar and window title bar.
            theme: Theme name. If None, uses the default theme.
            size: Initial window size as (width, height).
            position: Initial window position as (x, y).
            minsize: Minimum window size as (width, height).
            maxsize: Maximum window size as (width, height).
            resizable: Whether the window is resizable as (width, height).
            frameless: If True, remove OS window chrome (title bar, borders)
                and rely on the toolbar for window controls and dragging.
                Automatically enables `show_window_controls` and
                `draggable` when True. Default False.
            show_toolbar: Include the toolbar at the top. Default True.
            show_window_controls: Show minimize/maximize/close buttons
                in the toolbar. Default False.
            draggable: Enable window dragging via the toolbar. Default False.
            toolbar_density: Toolbar button density ('default' or 'compact').
            show_nav: Include the sidebar navigation. Default True.
            nav_display_mode: Initial SideNav display mode
                ('expanded', 'compact', or 'minimal'). Default 'expanded'.
            nav_accent: Accent color for navigation selection. Default 'primary'.
            **kwargs: Additional arguments passed to App.
        """
        # Frameless mode: remove OS chrome and enable toolbar controls
        if frameless:
            show_window_controls = True
            draggable = True

        super().__init__(
            title=title,
            theme=theme,
            size=size,
            position=position,
            minsize=minsize,
            maxsize=maxsize,
            resizable=resizable,
            override_redirect=frameless,
            **kwargs,
        )

        self._shell_title = title
        self._show_toolbar = show_toolbar
        self._show_nav = show_nav

        # Track which nav keys have associated pages
        self._page_keys: set[str] = set()
        self._first_page_added = False
        self._navigating = False  # Guard against re-entrant navigation

        # Build components
        self._toolbar: Toolbar | None = None
        self._nav: SideNav | None = None
        self._pages: PageStack | None = None

        self._build_shell(
            show_toolbar=show_toolbar,
            show_window_controls=show_window_controls,
            draggable=draggable,
            toolbar_density=toolbar_density,
            show_nav=show_nav,
            nav_display_mode=nav_display_mode,
            nav_accent=nav_accent,
        )

    def _build_shell(
        self,
        *,
        show_toolbar: bool,
        show_window_controls: bool,
        draggable: bool,
        toolbar_density: str,
        show_nav: bool,
        nav_display_mode: str,
        nav_accent: str,
    ):
        """Build the internal widget structure."""
        # --- Toolbar ---
        if show_toolbar:
            self._toolbar = Toolbar(
                self,
                surface='chrome',
                density=toolbar_density,
                show_window_controls=show_window_controls,
                draggable=draggable,
            )
            self._toolbar.pack(side='top', fill='x')

            # Hamburger button (only when nav is present)
            if show_nav:
                self._toolbar.add_button(
                    icon='list',
                    command=self._toggle_nav,
                )
                self._toolbar.add_separator()

            # Title label
            self._title_label = None
            if self._shell_title:
                self._title_label = self._toolbar.add_label(text=self._shell_title, font='heading-md')

            # Spacer pushes subsequent user-added buttons to the right
            self._toolbar.add_spacer()

        # --- Body (nav + pages) ---
        body = Frame(self)
        body.pack(side='top', fill='both', expand=True)

        # --- SideNav ---
        if show_nav:
            # When toolbar is present, nav hides its own header and hamburger;
            # AppShell puts the hamburger in the toolbar instead.
            # When toolbar is absent, nav manages its own toggle.
            self._nav = SideNav(
                body,
                show_header=False,
                collapsible=not show_toolbar,
                display_mode=nav_display_mode,
                accent=nav_accent,
            )
            self._nav.pack(side='left', fill='y')

            # Wire selection changes to page navigation
            self._nav.on_selection_changed(self._on_nav_selection_changed)

        # --- PageStack ---
        self._pages = PageStack(body)
        self._pages.pack(side='left', fill='both', expand=True)

    # --- Internal Handlers ---

    def _toggle_nav(self):
        """Toggle the SideNav pane."""
        if self._nav is not None:
            self._nav.toggle_pane()

    def _on_nav_selection_changed(self, event):
        """Handle SideNav selection changes."""
        key = event.data.get('key', '')
        if not key or key not in self._page_keys:
            return  # Not a page item (e.g. action-only item)

        if self._navigating:
            return  # Guard against re-entrant calls

        self._navigating = True
        try:
            self._pages.navigate(key)
        finally:
            self._navigating = False

    # --- Public API: Adding Content ---

    def add_page(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        page=None,
        group: str = None,
        is_footer: bool = False,
        scrollable: bool = False,
        **nav_kwargs,
    ):
        """Add a navigation item and its corresponding page in one call.

        Args:
            key: Unique identifier for both the nav item and the page.
            text: Display text for the nav item.
            icon: Icon name or configuration for the nav item.
            page: An existing widget to use as the page. If None, a Frame
                is created automatically.
            group: Key of the nav group to add this item to.
            is_footer: If True, add the nav item to the footer section.
            scrollable: If True, the page is wrapped in a ScrollView with
                vertical scrolling. The returned widget is the ScrollView
                content frame, so widgets can be packed into it as usual.
            **nav_kwargs: Additional arguments passed to the nav item.

        Returns:
            The page widget (passed or auto-created Frame). When
            `scrollable=True`, returns the ScrollView so that children
            are packed into the scrollable area.

        Raises:
            RuntimeError: If `show_nav=False` was set. Use
                `shell.pages.add()` directly instead.
        """
        if self._nav is None:
            raise RuntimeError(
                "Cannot use add_page() when show_nav=False. "
                "Use shell.pages.add() directly instead."
            )

        # Add nav item
        if is_footer:
            self._nav.add_footer_item(key, text=text, icon=icon, **nav_kwargs)
        elif group is not None:
            self._nav.add_item(key, text=text, icon=icon, group=group, **nav_kwargs)
        else:
            self._nav.add_item(key, text=text, icon=icon, **nav_kwargs)

        # Add page
        page_widget = self._pages.add(key, page=page)
        self._page_keys.add(key)

        # Wrap in ScrollView when requested
        if scrollable:
            sv = ScrollView(
                page_widget,
                scroll_direction="vertical",
                scrollbar_visibility="hover",
            )
            sv.pack(fill="both", expand=True)
            page_widget = sv.add()

            # Stretch content frame to canvas width so fill=X works
            def _on_canvas_resize(event, _sv=sv):
                _sv.canvas.itemconfigure(_sv._window_id, width=event.width)
            sv.canvas.bind('<Configure>', _on_canvas_resize, add='+')

        # Auto-navigate to the first page added
        if not self._first_page_added:
            self._first_page_added = True
            self.navigate(key)

        return page_widget

    def add_group(
        self,
        key: str,
        text: str = '',
        icon: str | dict = None,
        is_expanded: bool = False,
        **kwargs,
    ):
        """Add a navigation group.

        Passthrough to `nav.add_group()`.

        Args:
            key: Unique identifier for the group.
            text: Display text.
            icon: Icon name or configuration.
            is_expanded: Initial expansion state.
            **kwargs: Additional arguments passed to SideNavGroup.

        Returns:
            SideNavGroup: The created group.
        """
        if self._nav is None:
            raise RuntimeError("Cannot add groups when show_nav=False.")
        return self._nav.add_group(key, text=text, icon=icon, is_expanded=is_expanded, **kwargs)

    def add_header(self, text: str, **kwargs):
        """Add a section header to the navigation.

        Passthrough to `nav.add_header()`.

        Args:
            text: Header text.
            **kwargs: Additional arguments passed to SideNavHeader.

        Returns:
            SideNavHeader: The created header.
        """
        if self._nav is None:
            raise RuntimeError("Cannot add headers when show_nav=False.")
        return self._nav.add_header(text, **kwargs)

    def add_separator(self, **kwargs):
        """Add a separator to the navigation.

        Passthrough to `nav.add_separator()`.

        Args:
            **kwargs: Additional arguments passed to SideNavSeparator.

        Returns:
            SideNavSeparator: The created separator.
        """
        if self._nav is None:
            raise RuntimeError("Cannot add separators when show_nav=False.")
        return self._nav.add_separator(**kwargs)

    # --- Public API: Navigation ---

    def navigate(self, key: str, data: dict = None):
        """Programmatic navigation: updates nav selection and navigates PageStack.

        Args:
            key: The page key to navigate to.
            data: Optional data to pass to the page.
        """
        if self._navigating:
            return

        self._navigating = True
        try:
            # Update nav selection (which will NOT re-trigger navigation
            # because we set the guard)
            if self._nav is not None and key in self._page_keys:
                self._nav.select(key)

            # Navigate the page stack
            if key in self._page_keys:
                self._pages.navigate(key, data=data)
        finally:
            self._navigating = False

    def select(self, key: str, data: dict = None):
        """Alias for `navigate()`.

        Args:
            key: The page key to navigate to.
            data: Optional data to pass to the page.
        """
        self.navigate(key, data=data)

    # --- Public API: Event Binding ---

    def on_page_changed(self, callback: Callable) -> str:
        """Bind to page change events on the PageStack.

        Args:
            callback: Function to call when the page changes.

        Returns:
            Binding identifier for use with `off_page_changed()`.
        """
        return self._pages.on_page_changed(callback)

    def off_page_changed(self, bind_id: str = None):
        """Unbind from page change events.

        Args:
            bind_id: The binding identifier returned by `on_page_changed()`.
        """
        self._pages.off_page_changed(bind_id)

    # --- Properties ---

    @property
    def toolbar(self) -> Toolbar | None:
        """The Toolbar widget, or None if `show_toolbar=False`."""
        return self._toolbar

    @property
    def nav(self) -> SideNav | None:
        """The SideNav widget, or None if `show_nav=False`."""
        return self._nav

    @property
    def pages(self) -> PageStack:
        """The PageStack widget (always present)."""
        return self._pages

    @property
    def current_page(self) -> str | None:
        """The key of the currently displayed page, or None."""
        result = self._pages.current()
        return result[0] if result else None