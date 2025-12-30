"""Accordion widget - a container of mutually exclusive expanders."""
from __future__ import annotations

from typing import Any, Callable, Literal, TYPE_CHECKING

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.composites.expander import Expander
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    pass


class Accordion(Frame):
    """A container of Expander widgets with optional mutual exclusion.

    The Accordion manages a group of Expanders, optionally enforcing that only
    one can be expanded at a time. When ``multiple=False``, expanding one
    section automatically collapses the others. When ``collapsible=False``,
    at least one section must remain open.

    Attributes:
        expanders (list[Expander]): List of managed Expander widgets.
        expanded (list[Expander]): Currently expanded Expander(s).

    Events:
        ``<<AccordionChange>>``: Fired when the expanded section(s) change.
            ``event.data = {'expanded': list[Expander]}``
    """

    def __init__(
        self,
        master: Master = None,
        multiple: bool = False,
        collapsible: bool = True,
        separators: bool = False,
        bootstyle: str = '',
        color: str = None,
        variant: str = None,
        **kwargs
    ):
        """Create an Accordion widget.

        Args:
            master (Master): Parent widget. If None, uses the default root window.
            multiple (bool): If True, multiple sections can be open at once.
                If False (default), only one section can be open at a time.
            collapsible (bool): If True (default), all sections can be collapsed.
                If False, at least one section must remain open.
            separators (bool): If True, show separators between expanders.
            bootstyle (str): DEPRECATED - Bootstyle for the expanders.
            color (str): Color token for the expanders (e.g., 'success', 'primary').
            variant (str): Variant for the expanders (e.g., 'solid', 'default').
            **kwargs: Additional arguments passed to Frame.
        """

        if 'show_border' in kwargs:
            kwargs.setdefault('padding', 3)  # required to avoid clipping corners

        super().__init__(master, **kwargs)

        self._multiple = multiple
        self._collapsible = collapsible
        self._separators = separators
        self._bootstyle = bootstyle
        self._color = color
        self._variant = variant
        self._expanders: list[Expander] = []
        self._separator_widgets: list[Separator] = []
        self._updating = False  # Prevent recursive updates

    def add(
        self,
        expander: Expander = None,
        *,
        title: str = "",
        icon: str | dict = None,
        expanded: bool = None,
        **kwargs
    ) -> Expander:
        """Add an expander to the accordion.

        Args:
            expander (Expander | None): Existing Expander to add. If None, creates one.
            title (str): Title for the expander header (when creating new).
            icon (str | dict): Icon for the expander header (when creating new).
            expanded (bool | None): Initial expansion state. If None, first expander
                is expanded when collapsible=False, otherwise collapsed.
            **kwargs: When expander is None, passed to Expander constructor.

        Returns:
            Expander: The added or created Expander widget.
        """
        # Add separator before this expander (if not the first)
        if self._separators and len(self._expanders) > 0:
            sep = Separator(self, orient='horizontal')
            sep.pack(fill='x')
            self._separator_widgets.append(sep)

        # Create expander if not provided
        if expander is None:
            # Determine initial expanded state
            if expanded is None:
                # If not collapsible and this is the first, expand it
                if not self._collapsible and len(self._expanders) == 0:
                    expanded = True
                else:
                    expanded = False

            expander = Expander(
                self,
                title=title,
                icon=icon,
                expanded=expanded,
                highlight=True,
                color=self._color or self._bootstyle or kwargs.pop('color', kwargs.pop('bootstyle', None)),
                variant=self._variant or kwargs.pop('variant', None),
                **kwargs
            )
        else:
            # Configure existing expander
            expander.configure(highlight=True)
            if expanded is not None:
                if expanded:
                    expander.expand()
                else:
                    expander.collapse()

        expander.pack(fill='x')
        self._expanders.append(expander)

        # Bind to toggle events
        expander.on_toggle(lambda e, exp=expander: self._on_expander_toggle(exp, e))

        return expander

    def _on_expander_toggle(self, expander: Expander, event):
        """Handle expander toggle events."""
        if self._updating:
            return

        self._updating = True
        try:
            is_expanded = event.data.get('expanded', False)

            if is_expanded:
                # Expander was just opened
                if not self._multiple:
                    # Collapse all others
                    for exp in self._expanders:
                        if exp is not expander and exp['expanded']:
                            exp.collapse()
            else:
                # Expander was just closed
                if not self._collapsible:
                    # Check if any are still open
                    any_open = any(exp['expanded'] for exp in self._expanders)
                    if not any_open:
                        # Re-open this one - can't collapse all
                        expander.expand()
                        return

            # Fire change event
            self.event_generate('<<AccordionChange>>', data={
                'expanded': [exp for exp in self._expanders if exp['expanded']]
            })
        finally:
            self._updating = False

    def expand(self, index: int):
        """Expand the expander at the given index.

        Args:
            index (int): Index of the expander to expand.
        """
        if 0 <= index < len(self._expanders):
            self._expanders[index].expand()

    def collapse(self, index: int):
        """Collapse the expander at the given index.

        Args:
            index (int): Index of the expander to collapse.

        Note:
            If collapsible=False and this is the only open expander,
            this call will be ignored.
        """
        if 0 <= index < len(self._expanders):
            exp = self._expanders[index]
            if not self._collapsible:
                # Check if this is the only open one
                open_count = sum(1 for e in self._expanders if e['expanded'])
                if open_count <= 1 and exp['expanded']:
                    return  # Can't collapse the last one
            exp.collapse()

    def expand_all(self):
        """Expand all expanders (only effective when multiple=True)."""
        if not self._multiple:
            return
        for exp in self._expanders:
            exp.expand()

    def collapse_all(self):
        """Collapse all expanders (only effective when collapsible=True)."""
        if not self._collapsible:
            return
        for exp in self._expanders:
            exp.collapse()

    @property
    def expanders(self) -> list[Expander]:
        """Get the list of managed Expander widgets."""
        return list(self._expanders)

    @property
    def expanded(self) -> list[Expander]:
        """Get the list of currently expanded Expanders."""
        return [exp for exp in self._expanders if exp['expanded']]

    @configure_delegate('multiple')
    def _delegate_multiple(self, value=None):
        """Get or set whether multiple sections can be open at once."""
        if value is None:
            return self._multiple
        self._multiple = value
        return None

    @configure_delegate('collapsible')
    def _delegate_collapsible(self, value=None):
        """Get or set whether all sections can be collapsed."""
        if value is None:
            return self._collapsible
        self._collapsible = value
        return None

    @configure_delegate('separators')
    def _delegate_separators(self, value=None):
        """Get or set whether separators are shown between sections."""
        if value is None:
            return self._separators
        self._separators = value
        return None

    def on_change(self, callback: Callable) -> str:
        """Bind callback to ``<<AccordionChange>>`` events.

        Args:
            callback: Function to call when expanded sections change.
                Receives event with ``event.data = {'expanded': list[Expander]}``.

        Returns:
            Bind ID that can be passed to ``off_change`` to remove this callback.
        """
        return self.bind('<<AccordionChange>>', callback, add='+')

    def off_change(self, bind_id: str = None):
        """Unbind ``<<AccordionChange>>`` callback(s).

        Args:
            bind_id (str | None): Bind ID returned by ``on_change``. If None, unbinds all.
        """
        self.unbind('<<AccordionChange>>', bind_id)