"""MenuBar composite widget."""
from __future__ import annotations

from typing import Any, Callable, Dict, Literal, Optional, Tuple, TypedDict, Union

from typing_extensions import Unpack

from ttkbootstrap.widgets.composites.contextmenu import ContextMenuItem
from ttkbootstrap.widgets.composites.dropdownbutton import DropdownButton
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.gridframe import GridFrame
from ttkbootstrap.widgets.primitives.packframe import PackFrame
from ttkbootstrap.widgets.types import Master

Region = Literal["before", "center", "after"]


class MenuBarButtonKwargs(TypedDict, total=False):
    """Keyword arguments for MenuBar.add_button()."""
    command: Optional[Callable[[], Any]]
    image: Any
    icon: Any
    icon_only: bool
    compound: str
    padding: Any
    width: int
    state: str
    accent: str
    variant: str


class MenuBarMenuKwargs(TypedDict, total=False):
    """Keyword arguments for MenuBar.add_menu()."""
    image: Any
    icon: Any
    icon_only: bool
    compound: str
    padding: Any
    width: int
    state: str
    accent: str
    variant: str
    popdown_options: dict[str, Any]
    show_dropdown_button: bool
    dropdown_button_icon: str | dict


class MenuBar(GridFrame):
    """A horizontal menu bar with three regions: before (left), center, and after (right).

    MenuBar provides a 5-column grid layout where the center region stays visually
    centered. All three regions support adding buttons, labels, and menus.

    Example:
        ```python
        menubar = MenuBar(app, gap=6)

        # Add menus to the left (before) region
        menubar.add_menu("File", items=[
            {"type": "command", "text": "Open", "command": open_file},
            {"type": "command", "text": "Save", "command": save_file},
            {"type": "separator"},
            {"type": "command", "text": "Exit", "command": app.destroy},
        ])

        # Add label to center region
        menubar.add_label("My App", region="center")

        # Add buttons to the right (after) region
        menubar.add_button("Help", region="after", command=show_help)
        menubar.add_menu("Account", region="after", items=[...])
        ```

    Args:
        master: Parent widget. If None, uses the default root window.
        gap: Default gap between items in all region PackFrames. Defaults to 0.
        region_gap: Override gap per region. Can be a dict with keys 'before',
            'center', 'after', or a tuple of 3 ints (before, center, after).
        chevron: Show dropdown chevron on menu buttons. Defaults to False.
        popdown_options: Default popdown options for all menus.
        **kwargs: Additional GridFrame options (accent, variant, etc.).
    """

    # Column indices for the 5-column layout
    _COL_BEFORE = 0
    _COL_SPACER_LEFT = 1
    _COL_CENTER = 2
    _COL_SPACER_RIGHT = 3
    _COL_AFTER = 4

    def __init__(
        self,
        master: Master = None,
        *,
        gap: int = 0,
        region_gap: Optional[Union[Dict[str, int], Tuple[int, int, int]]] = None,
        chevron: bool = None,
        popdown_options: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        # Initialize GridFrame with 5-column centered layout
        # columns=[0, 1, 0, 1, 0] means:
        #   col 0 (before): weight=0 (shrink to content)
        #   col 1 (spacer_left): weight=1 (expand)
        #   col 2 (center): weight=0 (shrink to content)
        #   col 3 (spacer_right): weight=1 (expand)
        #   col 4 (after): weight=0 (shrink to content)

        self._chevron = chevron if chevron else False

        # Remove options controlled by MenuBar
        for key in ("rows", "columns", "gap", "auto_flow", "sticky_items", "padding"):
            kwargs.pop(key, None)

        kwargs.setdefault('surface', 'chrome')  # suggested 'titlebar' if used as the titlebar.

        super().__init__(
            master,
            rows=[1],
            columns=[0, 1, 0, 1, 0],
            auto_flow="none",
            sticky_items="ns",
            padding=(4, 0),
            **kwargs,
        )

        # Parse region gaps
        gap_before, gap_center, gap_after = self._parse_region_gap(gap, region_gap)

        # Create PackFrames directly in the grid (no intermediate cell frames needed)
        # Column weights [0, 1, 0, 1, 0] handle spacing - cols 1 and 3 expand to center col 2

        # Before: horizontal (left to right), children fill vertically
        self._before = PackFrame(self, direction="horizontal", gap=gap_before, fill_items="y")
        self._before.grid(row=0, column=self._COL_BEFORE, sticky="nsw")

        # Center: horizontal (for centered content), children fill vertically
        self._center = PackFrame(self, direction="horizontal", gap=gap_center, fill_items="y")
        self._center.grid(row=0, column=self._COL_CENTER, sticky="ns")

        # After: row-reverse (items align to right), children fill vertically
        self._after = PackFrame(self, direction="row-reverse", gap=gap_after, fill_items="y")
        self._after.grid(row=0, column=self._COL_AFTER, sticky="nse")

        # Default popdown options for all menus. Offset matches the focus-ring
        # affordance baked into the menu trigger image so popdowns align with
        # the visible button border.
        from ttkbootstrap.style.bootstyle_builder_base import BootstyleBuilderBase
        self._popdown_options = {"offset": (BootstyleBuilderBase.scale_from_source(10), 0), "density": "compact"}
        if popdown_options:
            self._popdown_options.update(popdown_options)

    @staticmethod
    def _parse_region_gap(
        gap: int,
        region_gap: Optional[Union[Dict[str, int], Tuple[int, int, int]]],
    ) -> Tuple[int, int, int]:
        """Parse region_gap into (before, center, after) tuple."""
        if region_gap is None:
            return gap, gap, gap

        if isinstance(region_gap, tuple) and len(region_gap) == 3:
            return region_gap

        if isinstance(region_gap, dict):
            return (
                region_gap.get("before", gap),
                region_gap.get("center", gap),
                region_gap.get("after", gap),
            )

        return gap, gap, gap

    @property
    def before(self) -> PackFrame:
        """The PackFrame used for the 'before' (left) region.

        Advanced users can access this to customize layout behavior.
        """
        return self._before

    @property
    def after(self) -> PackFrame:
        """The PackFrame used for the 'after' (right) region.

        Advanced users can access this to customize layout behavior.
        """
        return self._after

    @property
    def center(self) -> PackFrame:
        """The PackFrame used for the 'center' region."""
        return self._center

    def _get_region_frame(self, region: Region) -> PackFrame:
        """Get the PackFrame for the specified region."""
        if region == "before":
            return self._before
        elif region == "center":
            return self._center
        else:
            return self._after

    def add_button(
        self,
        text: str,
        *,
        region: Region = "before",
        **kwargs: Unpack[MenuBarButtonKwargs],
    ) -> Button:
        """Add a regular button to the specified region.

        Args:
            text: Label text for the button.
            region: Which region to add to ('before', 'center', 'after').
                Defaults to 'before'.
            **kwargs: Additional Button options (command, icon, accent, etc.).

        Returns:
            The created Button widget.
        """
        frame = self._get_region_frame(region)
        kwargs.pop("variant", None)
        if 'icon' in kwargs and 'text':
            kwargs['compound'] = 'left' if 'compound' not in kwargs else kwargs['compound']
        else:
            kwargs['compound'] = 'center'
        button = Button(frame, text=text, variant="menubar-item", **kwargs)
        button.pack()
        return button

    def add_label(
        self,
        text: str,
        *,
        region: Region = "before",
        **kwargs: Any,
    ) -> Label:
        """Add a text label to the specified region.

        Args:
            text: The text to display.
            region: Which region to add to ('before', 'center', 'after').
                Defaults to 'before'.
            **kwargs: Additional Label options (accent, padding, etc.).

        Returns:
            The created Label widget.
        """
        frame = self._get_region_frame(region)
        kwargs.setdefault("font", "caption")
        label = Label(frame, text=text, **kwargs)
        label.pack()
        return label

    def add_menu(
        self,
        text: str,
        items: Optional[list[ContextMenuItem]] = None,
        *,
        region: Region = "before",
        popdown_options: Optional[dict[str, Any]] = None,
        **kwargs: Unpack[MenuBarMenuKwargs],
    ) -> DropdownButton:
        """Add a dropdown menu button to the specified region.

        Args:
            text: Label text for the menu button.
            items: List of ContextMenuItem entries for the dropdown menu.
            region: Which region to add to ('before', 'center', 'after').
                Defaults to 'before'.
            popdown_options: Options forwarded to ContextMenu (anchor, attach, offset).
            **kwargs: Additional DropdownButton options (icon, accent, etc.).

        Returns:
            The created DropdownButton widget.
        """
        frame = self._get_region_frame(region)

        # Remove options that are controlled by MenuBar
        kwargs.pop("popdown_options", None)
        kwargs.pop("variant", None)
        if 'icon' in kwargs and 'text':
            kwargs['compound'] = 'left' if 'compound' not in kwargs else kwargs['compound']
        else:
            kwargs['compound'] = 'center'
        # Merge menubar defaults with per-menu options
        merged_popdown = dict(self._popdown_options)
        if popdown_options:
            merged_popdown.update(popdown_options)

        dropdown = DropdownButton(
            frame,
            text=text,
            items=items,
            variant="menubar-item",
            show_dropdown_button=self._chevron,
            popdown_options=merged_popdown,
            **kwargs,
        )
        dropdown.pack()
        return dropdown