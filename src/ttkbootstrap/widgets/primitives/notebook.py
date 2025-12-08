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
    """Public `ttkbootstrap.api.widgets.Notebook` proxy that adds ttkbootstrap styling.

    Wraps ``ttk.Notebook`` so the widget can be configured with bootstyle tokens,
    surface colors, and enriched tab lifecycle change events that the API exposes.
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
    def _mark_api_change(self, reason: ChangeReason = 'api'):
        """Record a programmatic change reason so the next change can report it"""
        self._last_change_reason = reason
        self._last_change_via = 'programmatic'

    def _make_key(self, key: Optional[str]) -> str:
        """Return a unique, stable key for a tab; auto generated (tabN) if none provided."""
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

    def _to_tab_id(self, tab: Tab):
        """Resolve a tab reference (key/index/widget) to a tk tab id"""
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
                    message=f"Tab index out of range: ${tab}",
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

    def _tab_ref(self, tabid: str | None) -> TabRef:
        """Return a simplified tab reference ({index, key, label}) or None if invalid"""
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

    def hide(self, tab: Tab):
        """Hide a tab without removing it; selection may change implicitly"""
        self._mark_api_change('hide')
        super().hide(self._to_tab_id(tab))

    def index(self, tab: Tab):
        """Return the current position of a tab"""
        return super().index(self._to_tab_id(tab))

    def select(self, tab: Tab = None):
        """Select a tab or return the current tab id"""
        if tab is None:
            return super().select()
        else:
            self._mark_api_change('api')
            return super().select(self._to_tab_id(tab))

    def add_frame(self, label: str = None, key: str = None, frame_options: dict=None, **kwargs: Unpack[TabOptions]) -> Frame:
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
            self, index: str | int = 'end', label=None, key: str = None, frame_options: dict=None, **kwargs: Unpack[TabOptions]) -> Frame:
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

    def add(self, widget: tkinter.Widget, *, key: str = None, **kwargs):
        """Adds a new tab to the notebook.
        If window is currently managed by the notebook but hidden, it is restored to its previous position.

        Args:
            widget: The widget to add as a tab.
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
        super().insert('end', widget, key=key, **kwargs)

    def insert(self, index: str | int, widget: tkinter.Widget, *, key: str = None, **kwargs):
        """Create a new frame and insert to Notebook at position `index`.

        Args:
            index: Indicates where to insert the widget. Defaults to 'end'.
            widget: The widget to insert as a tab.
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
        super().insert(index, widget, **kwargs)
        tab_key = self._make_key(key)
        self._tk_to_key[str(widget)] = tab_key
        self._key_registry[tab_key] = widget

    def remove(self, tab: Tab):
        """Remove a tab and clean registry"""
        self._mark_api_change('forget')
        tabid = self._to_tab_id(tab)
        key = self._tk_to_key.pop(tabid, None)
        if key:
            self._key_registry.pop(key, None)
        self.forget(tabid)

    def tab(self, tab: Tab, option: str = None, **kwargs):
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

    def on_tab_activated(self, callback: Callable[[Any], Any]):
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

    def off_tab_activated(self, funcid: str):
        """Remove the binding associated with funcid for <<NotebookTabActivated>>."""
        self.unbind("<<NotebookTabActivated>>", funcid)

    def on_tab_deactivated(self, callback: Callable[[Any], Any]):
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

    def off_tab_deactivated(self, funcid: str):
        """Remove the binding associated with funcid on <<NotebookTabDeactivated>>"""
        self.unbind("<<NotebookTabDeactivated>>", funcid)

    def on_tab_changed(self, callback: Callable[[Any], Any]):
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

        def build_payload(event: Any):
            """Attach NotebookChanged data payload to the event"""
            payload = dict(
                current=self._tab_ref(self.select()),
                previous=self._tab_ref(self._last_selected),
                reason=self._last_change_reason or 'unknown',
                via=self._last_change_via or 'unknown',
            )
            event.data = payload
            return event

        def fire_lifecycle(event):
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

        def wrapper(event):
            payload = build_payload(event)
            fire_lifecycle(payload)
            commit(payload)
            return callback(event)

        return self.bind("<<NotebookTabChanged>>", wrapper, add=True)

    def off_tab_changed(self, funcid: str):
        """Remove the binding associated with funcid for <<NotebookTabChanged>>."""
        self.unbind("<<NotebookTabChanged>>", funcid)
