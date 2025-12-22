from __future__ import annotations

import tkinter
from tkinter import ttk
from typing import Any, Callable, Literal, Optional, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.core import NavigationError
from ttkbootstrap.core.localization import MessageCatalog
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
    fmtargs: tuple[Any, ...] | list[Any]


class Notebook(TTKWrapperBase, ttk.Notebook):
    """A themed tabbed container widget with enhanced navigation and event tracking.

    The Notebook widget provides a tabbed interface where only one tab's content
    is visible at a time. Tabs can be referenced by key (str), index (int), or
    widget instance.

    Events:
        ``<<NotebookTabChange>>``: Triggered when the selected tab changes.
        ``<<NotebookTabActivate>>``: Triggered when a tab becomes active.
        ``<<NotebookTabDeactivate>>``: Triggered when a tab becomes inactive.

        All events include ``event.data`` with: ``current`` (TabRef), ``previous``
        (TabRef), ``reason`` ('user', 'api', 'hide', 'forget', 'reorder'), and
        ``via`` ('click', 'key', 'programmatic').
    """

    _ttk_base = ttk.Notebook

    def __init__(self, master=None, **kwargs: Unpack[NotebookKwargs]) -> None:
        """Create a themed ttkbootstrap Notebook with optional bootstyle extensions.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters:
            padding (int | tuple): Extra space around the tab header and pane area.
            height (int): Requested widget height in pixels.
            width (int): Requested widget width in pixels.
            style (str): Explicit ttk style name that overrides any bootstyle token.
            bootstyle (str): Bootstyle tokens (e.g., 'primary', 'secondary').
            surface_color (str): Optional surface color token; inherits from the current theme if omitted.
            style_options (dict): Additional options forwarded to the style builder.
        """
        super().__init__(master, **kwargs)
        self._key_registry: dict[str, tkinter.Misc] = {}  # key -> widget
        self._tk_to_key: dict[str, str] = {}  # tk id -> key
        self._auto_counter = 0  # for auto keys: tab1, tab2, ...
        self._tab_locale_tokens: dict[str, tuple[str, tuple[Any, ...]]] = {}
        self.bind("<<LocaleChanged>>", self._refresh_tab_labels, add="+")

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

    def _register_tab_token(self, tabid: str, token: str | None, fmtargs: tuple[Any, ...]) -> None:
        """Track the semantic key used for a tab so it can be retranslated."""
        if not token:
            self._tab_locale_tokens.pop(tabid, None)
            return
        self._tab_locale_tokens[tabid] = (token, fmtargs)

    def _refresh_tab_labels(self, event: Any = None) -> None:
        """Refresh all tab labels when the locale changes."""
        for tabid, (token, fmtargs) in list(self._tab_locale_tokens.items()):
            text = MessageCatalog.translate(token, *fmtargs)
            ttk.Notebook.tab(self, tabid, text=text)


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
            label (str): The text used on the tab label.
            key (str): A unique human-friendly identifier for referencing the tab.
            frame_options (dict): Configuration options passed to Frame.

        Other Parameters:
            state (str): One of 'normal', 'disabled', 'hidden'.
            sticky (str): How the content is positioned in the pane area.
            padding (int | tuple): Extra space between notebook and pane.
            text (str): The text of the tab label.
            compound (str): Image placement relative to text.
            image (PhotoImage): The image to display in the tab.
            underline (int): Index of character to underline in the label.

        Returns:
            Frame: The newly created frame.
        """
        return self.insert_frame('end', label=label, frame_options=frame_options, key=key, **kwargs)

    def insert_frame(
            self, index: str | int = 'end', label: str | None = None, key: str | None = None, frame_options: dict | None = None, **kwargs: Unpack[TabOptions]) -> Frame:
        """Create a new frame and insert to Notebook at position ``index``.

        Args:
            index (str | int): Position to insert the widget. Defaults to 'end'.
            label (str): The text used on the tab label.
            key (str): A unique human-friendly identifier for referencing the tab.
            frame_options (dict): Configuration options passed to Frame.

        Other Parameters:
            state (str): One of 'normal', 'disabled', 'hidden'.
            sticky (str): How the content is positioned in the pane area.
            padding (int | tuple): Extra space between notebook and pane.
            text (str): The text of the tab label.
            compound (str): Image placement relative to text.
            image (PhotoImage): The image to display in the tab.
            underline (int): Index of character to underline in the label.

        Returns:
            Frame: The newly created frame.
        """
        frame = Frame(self, **(frame_options or {}))
        self.insert(index, frame, key=key, text=label, **kwargs)
        return frame

    def add(self, child: tkinter.Widget, *, key: str | None = None, **kwargs) -> None:
        """Add a new tab to the notebook.

        If the widget is currently managed by the notebook but hidden, it is
        restored to its previous position.

        Args:
            child (Widget): The widget to add as a tab.
            key (str): A unique human-friendly identifier for referencing the tab.

        Other Parameters:
            state (str): One of 'normal', 'disabled', 'hidden'.
            sticky (str): How the content is positioned in the pane area.
            padding (int | tuple): Extra space between notebook and pane.
            text (str): The text of the tab label.
            compound (str): Image placement relative to text.
            image (PhotoImage): The image to display in the tab.
            underline (int): Index of character to underline in the label.
        """
        self.insert('end', child, key=key, **kwargs)

    def insert(self, index: str | int, child: tkinter.Widget, *, key: str | None = None, **kwargs) -> None:
        """Insert a widget as a tab at position ``index``.

        Args:
            index (str | int): Position to insert the widget. Defaults to 'end'.
            child (Widget): The widget to insert as a tab.
            key (str): A unique human-friendly identifier for referencing the tab.

        Other Parameters:
            state (str): One of 'normal', 'disabled', 'hidden'.
            sticky (str): How the content is positioned in the pane area.
            padding (int | tuple): Extra space between notebook and pane.
            text (str): The text of the tab label.
            compound (str): Image placement relative to text.
            image (PhotoImage): The image to display in the tab.
            underline (int): Index of character to underline in the label.
        """
        self._mark_api_change('reorder')
        fmtargs = tuple(kwargs.pop('fmtargs', ()))
        text_token = kwargs.get('text')
        if text_token is not None:
            kwargs['text'] = MessageCatalog.translate(text_token, *fmtargs)
        super().insert(index, child, **kwargs)
        tab_key = self._make_key(key)
        self._tk_to_key[str(child)] = tab_key
        self._key_registry[tab_key] = child
        self._register_tab_token(str(child), text_token, fmtargs)

    def remove(self, tab: Tab) -> None:
        """Remove a tab and clean registry"""
        self._mark_api_change('forget')
        tabid = self._to_tab_id(tab)
        key = self._tk_to_key.pop(tabid, None)
        if key:
            self._key_registry.pop(key, None)
        self._tab_locale_tokens.pop(tabid, None)
        super().forget(tabid)

    def forget(self, tab: Tab) -> None:
        """Hide or forget a tab while keeping the registry consistent."""
        tabid = self._to_tab_id(tab)
        self._tab_locale_tokens.pop(tabid, None)
        super().forget(tabid)

    def tab(self, tab: Tab, option: str = None, **kwargs) -> Any:
        """Configure or query tab configuration.

        Args:
            tab (Tab): The tab to configure. Can be an index, key, or widget.
            option (str): The option to query.

        Other Parameters:
            state (str): One of 'normal', 'disabled', 'hidden'.
            sticky (str): How the content is positioned in the pane area.
            padding (int | tuple): Extra space between notebook and pane.
            text (str): The text of the tab label.
            compound (str): Image placement relative to text.
            image (PhotoImage): The image to display in the tab.
            underline (int): Index of character to underline in the label.

        Returns:
            Any: The value of option if specified, otherwise None.
        """
        tabid = self._to_tab_id(tab)
        fmtargs = tuple(kwargs.pop('fmtargs', ()))
        text_token = kwargs.get('text')
        if text_token is not None:
            kwargs['text'] = MessageCatalog.translate(text_token, *fmtargs)
        result = super().tab(tabid, option, **kwargs)
        if text_token is not None:
            self._register_tab_token(tabid, text_token, fmtargs)
        return result

    configure_tab = tab  # alias for tab

    def on_tab_activated(self, callback: Callable[[Any], Any]) -> str:
        """Bind a callback to the ``<<NotebookTabActivate>>`` event.

        The ``event.data`` payload includes ``current`` (TabRef), ``previous``
        (TabRef), ``reason`` (ChangeReason), and ``via`` (ChangeMethod).

        Args:
            callback (Callable): Function to call when a tab is activated.

        Returns:
            str: The funcid that can be used with ``off_tab_activated()``.
        """
        return self.bind("<<NotebookTabActivate>>", callback, add=True)

    def off_tab_activated(self, funcid: str) -> None:
        """Remove a ``<<NotebookTabActivate>>`` binding.

        Args:
            funcid (str): The funcid returned by ``on_tab_activated()``.
        """
        self.unbind("<<NotebookTabActivate>>", funcid)

    def on_tab_deactivated(self, callback: Callable[[Any], Any]) -> str:
        """Bind a callback to the ``<<NotebookTabDeactivate>>`` event.

        The ``event.data`` payload includes ``current`` (TabRef), ``previous``
        (TabRef), ``reason`` (ChangeReason), and ``via`` (ChangeMethod).

        Args:
            callback (Callable): Function to call when a tab is deactivated.

        Returns:
            str: The funcid that can be used with ``off_tab_deactivated()``.
        """
        return self.bind("<<NotebookTabDeactivate>>", callback, add=True)

    def off_tab_deactivated(self, funcid: str) -> None:
        """Remove a ``<<NotebookTabDeactivate>>`` binding.

        Args:
            funcid (str): The funcid returned by ``on_tab_deactivated()``.
        """
        self.unbind("<<NotebookTabDeactivate>>", funcid)

    def on_tab_changed(self, callback: Callable[[Any], Any]) -> str:
        """Bind a callback to the ``<<NotebookTabChange>>`` event.

        This also emits ``<<NotebookTabActivate>>`` and ``<<NotebookTabDeactivate>>``
        events for the affected tabs.

        The ``event.data`` payload includes ``current`` (TabRef), ``previous``
        (TabRef), ``reason`` (ChangeReason), and ``via`` (ChangeMethod).

        Args:
            callback (Callable): Function to call when the tab selection changes.

        Returns:
            str: The funcid that can be used with ``off_tab_changed()``.
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
                self.event_generate("<<NotebookTabDeactivate>>", data={"tab": p})
            if c and changed:
                self.event_generate("<<NotebookTabActivate>>", data={"tab": c})

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

        return self.bind("<<NotebookTabChange>>", wrapper, add=True)

    def off_tab_changed(self, funcid: str) -> None:
        """Remove a ``<<NotebookTabChange>>`` binding.

        Args:
            funcid (str): The funcid returned by ``on_tab_changed()``.
        """
        self.unbind("<<NotebookTabChange>>", funcid)
