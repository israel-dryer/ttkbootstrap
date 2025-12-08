from __future__ import annotations

import tkinter
from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core import NavigationError
from ttkbootstrap.widgets._internal.wrapper_base import TTKWrapperBase
from ttkbootstrap.widgets.primitives import Frame

ChangeReason = Literal['user', 'api', 'hide', 'forget', 'reorder', 'unknown']
ChangeMethod = Literal['click', 'key', 'programmatic', 'unknown']

Tab = tkinter.Widget | int | str


class TabRef(TypedDict):
    index: int | None
    key: str | None
    label: str | None


class NotebookKwargs(TypedDict, total=False):
    # Standard ttk.Notebook options
    padding: Any
    height: int
    width: int
    style: str
    class_: str
    cursor: str
    name: str

    # ttkbootstrap-specific extensions
    bootstyle: str
    surface_color: str
    style_options: dict[str, Any]


class TabOptions(TypedDict, total=False):
    state: Literal['normal', 'disabled', 'hidden']
    sticky: str
    padding: str | float | tuple[str | float] | tuple[str | float, str | float] | tuple[
        str | float, str | float, str | float] | tuple[str | float, str | float, str | float, str | float]
    text: str
    compound: Literal["top", "left", "center", "right", "bottom", "none"]
    image: Any
    underline: int


class Notebook(TTKWrapperBase, ttk.Notebook):
    """A themed tabbed container widget with enhanced navigation and event tracking.

    The Notebook widget provides a tabbed interface where only one tab's content
    is visible at a time. It extends ttk.Notebook with ttkbootstrap styling,
    key-based tab referencing, and enriched lifecycle events for tracking tab changes.

    Features:
        - Add tabs as existing widgets or create new Frame tabs
        - Reference tabs by key, index, or widget instance
        - Automatic key generation for tabs without explicit keys
        - Enriched lifecycle events tracking tab activation/deactivation
        - Hide/show tabs dynamically without removing them
        - Query navigation state and tab metadata
        - Full support for ttkbootstrap styling (bootstyle, surface_color)

    Tab Referencing:
        Tabs can be referenced in three ways:
        - By key (str): Human-readable identifier like 'home', 'settings'
        - By index (int): 0-based position in the tab bar
        - By widget: The actual widget instance

    Lifecycle Events:
        - <<NotebookTabChanged>>: Triggered when the selected tab changes
        - <<NotebookTabActivated>>: Triggered when a tab becomes active
        - <<NotebookTabDeactivated>>: Triggered when a tab becomes inactive

    Event Data:
        All lifecycle events include a data dictionary with:
        - current: TabRef dict with index, key, and label of current tab
        - previous: TabRef dict with index, key, and label of previous tab
        - reason: Change reason ('user', 'api', 'hide', 'forget', 'reorder')
        - via: Change method ('click', 'key', 'programmatic')

    Note:
        This widget wraps ttk.Notebook and adds ttkbootstrap-specific features.
        All standard ttk.Notebook options and methods remain available.
    """

    _ttk_base = ttk.Notebook

    def __init__(self, master=None, **kwargs: Unpack[NotebookKwargs]) -> None:
        """Create a themed ttkbootstrap Notebook with optional bootstyle extensions.

        Args:
            master: Parent widget for this notebook.
            **kwargs: Keyword arguments passed to :class:`ttk.Notebook`.

        Keyword Args:
            padding: Extra space around the tab header and pane area.
            height: Requested widget height in pixels.
            width: Requested widget width in pixels.
            style: Explicit ttk style name that overrides any bootstyle token.
            bootstyle: Bootstyle tokens (for example ``'primary'`` or ``'secondary'``).
            surface_color: Optional surface color token; inherits from the current theme if omitted.
            style_options: Additional options forwarded to the style builder controlling bootstyle rendering.
        """
        super().__init__(master, **kwargs)
        self._key_registry: dict[str, tkinter.Misc] = {}  # key -> widget
        self._tk_to_key: dict[str, str] = {}  # tk id -> key
        self._auto_counter = 0  # for auto keys: tab1, tab2, ...

        # change tracking for enriched events
        self._last_selected: str | None = None
        self._last_change_reason: ChangeReason = 'unknown'
        self._last_change_via: ChangeMethod = 'unknown'

    # ---- Internal helpers ----
    def _mark_api_change(self, reason: ChangeReason = 'api') -> None:
        """Record a programmatic change reason so the next change can report it.

        This method tracks the reason for tab changes initiated through the API
        (as opposed to user interactions), allowing event handlers to provide
        detailed change context.

        Args:
            reason: The reason for the change ('api', 'hide', 'forget', 'reorder').
        """
        self._last_change_reason = reason
        self._last_change_via = 'programmatic'

    def _make_key(self, key: Optional[str]) -> str:
        """Return a unique, stable key for a tab; auto generated (tabN) if none provided.

        Args:
            key: Optional tab key. If None, generates an auto key like 'tab1', 'tab2', etc.

        Returns:
            A unique tab key string.

        Raises:
            NavigationError: If the key already exists in the registry.
            ValueError: If key is an empty string.
        """
        if key is not None and not key:
            raise ValueError("Tab key cannot be an empty string")

        if key in self._key_registry:
            raise NavigationError(
                message=f"Duplicate tab key: {key}",
                hint="Tab keys must be unique per Notebook."
            )
        elif key is not None:
            return key

        # auto-generate
        while True:
            self._auto_counter += 1
            key = f"tab{self._auto_counter}"
            if key not in self._key_registry:
                return key

    def _to_tab_id(self, tab: Tab) -> str:
        """Resolve a tab reference (key/index/widget) to a tkinter tab ID.

        This method provides flexible tab referencing by accepting multiple
        input types and converting them to the tkinter widget ID string format
        that the underlying ttk.Notebook expects.

        Args:
            tab: Tab reference, which can be:
                 - A widget instance (tkinter.Widget)
                 - An integer index (0-based position)
                 - A string key (from _key_registry)
                 - A string widget ID (fallback)

        Returns:
            The tkinter widget ID string for the tab.

        Raises:
            NavigationError: If the tab reference is invalid, out of range,
                           or of an unsupported type.
        """
        # tab is widget
        if isinstance(tab, tkinter.Misc):
            return str(tab)

        # tab is index
        if isinstance(tab, int):
            # index
            tabs = self.tab()
            try:
                return tabs[tab]
            except Exception:
                raise NavigationError(
                    message=f"Tab index out of range: {tab}",
                    hint=f"Valid range is 0..{len(tabs) - 1}."
                ) from None

        # tab is key
        if isinstance(tab, str) and tab in self._key_registry:
            return str(self._key_registry[tab])

        # fallback: assume tab is widget id
        if isinstance(tab, str):
            return tab

        raise NavigationError(
            message=f"Unsupported tab reference: {tab}",
            hint="Use a tab key (str), index (int), or widget"
        )

    def _tab_ref(self, tabid: str | None) -> TabRef | None:
        """Return a simplified tab reference ({index, key, label}) or None if invalid.

        Args:
            tabid: The tkinter widget ID of the tab to reference.

        Returns:
            A TabRef dictionary with index, key, and label fields, or None if the
            tabid is invalid or doesn't exist in the notebook.
        """
        ref: TabRef = {"index": None, "key": None, "label": None}
        if not tabid:
            return None
        try:
            ref['index'] = self.index(tabid)
            ref['label'] = self.tab(tabid, 'text')
        except tkinter.TclError:
            return None
        ref['key'] = self._tk_to_key.get(tabid)
        return ref

    def hide(self, tab: Tab) -> None:
        """Hide a tab without removing it; selection may change implicitly"""
        self._mark_api_change('hide')
        super().hide(self._to_tab_id(tab))

    def index(self, tab: Tab) -> int:
        """Return the current position of a tab"""
        return super().index(self._to_tab_id(tab))

    def select(self, tab: Tab = None) -> str | None:
        """Select a tab or return the current tab id"""
        if tab is None:
            return super().select()
        else:
            self._mark_api_change('api')
            return super().select(self._to_tab_id(tab))

    def add_frame(self, label: str | None = None, key: str | None = None, frame_options: dict | None = None, **kwargs: Unpack[TabOptions]) -> Frame:
        """Create a new frame and add to Notebook.

        Args:
            label: The text used on the tab label.
            key: A unique human-friendly identifier for referencing the tab.
            frame_options: Configuration options passed to Frame.

        Keyword Args:
            state: One of 'normal', 'disabled', 'hidden'. If 'hidden' tab is not shown.
            sticky: How the content is positioned in the pane area.
            padding: The amount of extra space to add between notebook and pane.
            text: The text of the tab Label.
            compound: How to display the image relative to the text when both text and image are present.
            image: The image to display in the tab.
            underline: The integer index (0-based) of a character to underline in the label.

        Returns:
            The newly created frame.
        """
        return self.insert_frame('end', label=label, frame_options=frame_options, key=key, **kwargs)

    def insert_frame(
            self, index: str | int = 'end', label: str | None = None, key: str | None = None, frame_options: dict | None = None, **kwargs: Unpack[TabOptions]) -> Frame:
        """Create a new frame and insert to Notebook at position `index`.

        Args:
            index: Indicates where to insert the widget. Defaults to 'end'.
            label: The text used on the tab label.
            key: A unique human-friendly identifier for referencing the tab.
            frame_options: Configuration options passed to Frame.

        Keyword Args:
            state: One of 'normal', 'disabled', 'hidden'. If 'hidden' tab is not shown.
            sticky: How the content is positioned in the pane area.
            padding: The amount of extra space to add between notebook and pane.
            text: The text of the tab Label.
            compound: How to display the image relative to the text when both text and image are present.
            image: The image to display in the tab.
            underline: The integer index (0-based) of a character to underline in the label.

        Returns:
            The newly created frame.
        """
        frame = Frame(self, **(frame_options or {}))
        self.insert(index, frame, key=key, text=label, **kwargs)
        return frame

    def add(self, child: tkinter.Widget, *, key: str | None = None, **kwargs) -> None:
        """Adds a new tab to the notebook.
        If window is currently managed by the notebook but hidden, it is restored to its previous position.

        Args:
            child: The widget to add as a tab.
            key: A unique human-friendly identifier for referencing the tab.

        Keyword Args:
            state: One of 'normal', 'disabled', 'hidden'. If 'hidden' tab is not shown.
            sticky: How the content is positioned in the pane area.
            padding: The amount of extra space to add between notebook and pane.
            text: The text of the tab Label.
            compound: How to display the image relative to the text when both text and image are present.
            image: The image to display in the tab.
            underline: The integer index (0-based) of a character to underline in the label.
        """
        self.insert('end', child, key=key, **kwargs)

    def insert(self, index: str | int, child: tkinter.Widget, *, key: str | None = None, **kwargs) -> None:
        """Create a new frame and insert to Notebook at position `index`.

        Args:
            index: Indicates where to insert the widget. Defaults to 'end'.
            child: The widget to insert as a tab.
            key: A unique human-friendly identifier for referencing the tab.

        Keyword Args:
            state: One of 'normal', 'disabled', 'hidden'. If 'hidden' tab is not shown.
            sticky: How the content is positioned in the pane area.
            padding: The amount of extra space to add between notebook and pane.
            text: The text of the tab Label.
            compound: How to display the image relative to the text when both text and image are present.
            image: The image to display in the tab.
            underline: The integer index (0-based) of a character to underline in the label.
        """
        self._mark_api_change('reorder')
        super().insert(index, child, **kwargs)
        tab_key = self._make_key(key)
        self._tk_to_key[str(child)] = tab_key
        self._key_registry[tab_key] = child

    def remove(self, tab: Tab) -> None:
        """Remove a tab and clean registry"""
        self._mark_api_change('forget')
        tabid = self._to_tab_id(tab)
        key = self._tk_to_key.pop(tabid, None)
        if key:
            self._key_registry.pop(key, None)
        self.forget(tabid)

    def tab(self, tab: Tab, option: str = None, **kwargs) -> Any:
        """Configure or query tab configuration.

        Args:
            tab: The tab to configure. Can be an index, key, or widget reference.
            option: The option to query.
            **kwargs: Additional keyword arguments used to configure tab.

        Keyword Args:
            state: One of 'normal', 'disabled', 'hidden'. If 'hidden' tab is not shown.
            sticky: How the content is positioned in the pane area.
            padding: The amount of extra space to add between notebook and pane.
            text: The text of the tab Label.
            compound: How to display the image relative to the text when both text and image are present.
            image: The image to display in the tab.
            underline: The integer index (0-based) of a character to underline in the label.

        Returns:
            The value of option if specified, otherwise None.
        """
        tabid = self._to_tab_id(tab)
        return super().tab(tabid, option, **kwargs)

    configure_tab = tab  # alias for tab

    def on_tab_activated(self, callback: Callable[[Any], Any]) -> str:
        """Bind to tab activation. <<NotebookTabActivated>> (public API event).

        The event maps the base event into a NotebookChanged event whose .data payload includes:
            - `current`: TabRef | None
            - `previous`: TabRef | None
            - `reason`: ChangeReason | None
            - `via`: ChangeMethod | None

        Returns
            The funcid associated with this callback.
        """
        return self.bind("<<NotebookTabActivated>>", callback, add=True)

    def off_tab_activated(self, funcid: str) -> None:
        """Remove the binding associated with funcid for <<NotebookTabActivated>>."""
        self.unbind("<<NotebookTabActivated>>", funcid)

    def on_tab_deactivated(self, callback: Callable[[Any], Any]) -> str:
        """Bind to tab deactivation. <<NotebookTabDeactivated>> (public API event).

        The event maps the base event into a NotebookChanged event whose .data payload includes:
            - `current`: TabRef | None
            - `previous`: TabRef | None
            - `reason`: ChangeReason | None
            - `via`: ChangeMethod | None

        Returns
            The funcid associated with this callback.
        """
        return self.bind("<<NotebookTabDeactivated>>", callback, add=True)

    def off_tab_deactivated(self, funcid: str) -> None:
        """Remove the binding associated with funcid on <<NotebookTabDeactivated>>"""
        self.unbind("<<NotebookTabDeactivated>>", funcid)

    def on_tab_changed(self, callback: Callable[[Any], Any]) -> str:
        """Bind to tab changed event (enriched API event surface).

        Emits:
            <<NotebookTabChanged>>
            <<NotebookTabActivated>>
            <<NotebookTabDeactivated>>

        The event maps the base event into a NotebookChanged event whose .data payload includes:
            - `current`: TabRef | None
            - `previous`: TabRef | None
            - `reason`: ChangeReason | None
            - `via`: ChangeMethod | None

        Returns
            The funcid associated with this callback.
        """

        def build_payload(event: Any) -> Any:
            """Attach NotebookChanged data payload to the event"""
            payload = dict(
                current=self._tab_ref(self.select()),
                previous=self._tab_ref(self._last_selected),
                reason=self._last_change_reason or 'unknown',
                via=self._last_change_via or 'unknown',
            )
            event.data = payload
            return event

        def fire_lifecycle(event: Any) -> None:
            """Emit per-tab lifecycle events when selection truly changes."""
            c, p = event.data["current"], event.data["previous"]
            c_key, p_key = (c or {}).get("key"), (p or {}).get("key")
            changed = (c_key != p_key) if (c_key or p_key) else ((c or {}).get("index") != (p or {}).get("index"))
            if p and changed:
                self.event_generate("<<NotebookTabDeactivated>>", data={"tab": p})
            if c and changed:
                self.event_generate("<<NotebookTabActivated>>", data={"tab": c})

        def commit(event: Any) -> None:
            """Reset change-tracking fields after dispatching the change event."""
            self._last_selected = self.select()
            self._last_change_reason = 'unknown'
            self._last_change_via = 'unknown'

        def wrapper(event: Any) -> Any:
            payload = build_payload(event)
            fire_lifecycle(payload)
            commit(payload)
            return callback(event)

        return self.bind("<<NotebookTabChanged>>", wrapper, add=True)

    def off_tab_changed(self, funcid: str) -> None:
        """Remove the binding associated with funcid for <<NotebookTabChanged>>."""
        self.unbind("<<NotebookTabChanged>>", funcid)
