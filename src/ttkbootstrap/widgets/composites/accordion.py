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
    one can be expanded at a time. When ``allow_multiple=False``, expanding one
    section automatically collapses the others. When ``allow_collapse_all=False``,
    at least one section must remain open.

    Attributes:
        expanders (list[Expander]): List of managed Expander widgets.
        expanded (list[Expander]): Currently expanded Expander(s).

    !!! note "Events"
        - ``<<AccordionChange>>``: Fired when the expanded section(s) change.
          ``event.data = {'expanded': list[Expander]}``
    """

    def __init__(
        self,
        master: Master = None,
        *,
        allow_multiple: bool = False,
        allow_collapse_all: bool = True,
        show_separators: bool = False,
        accent: str = None,
        variant: str = None,
        **kwargs
    ):
        """Create an Accordion widget.

        Args:
            master (Master): Parent widget. If None, uses the default root window.
            allow_multiple (bool): If True, multiple sections can be open at once.
                If False (default), only one section can be open at a time.
            allow_collapse_all (bool): If True (default), all sections can be collapsed.
                If False, at least one section must remain open.
            show_separators (bool): If True, show separators between expanders.
            accent (str): Accent token for the expanders (e.g., 'success', 'primary').
            variant (str): Variant for the expanders (e.g., 'solid', 'default').
            **kwargs: Additional arguments passed to Frame.
        """

        if 'show_border' in kwargs:
            kwargs.setdefault('padding', 3)  # required to avoid clipping corners

        super().__init__(master, **kwargs)

        self._allow_multiple = allow_multiple
        self._allow_collapse_all = allow_collapse_all
        self._show_separators = show_separators
        self._accent = accent
        self._variant = variant
        self._expanders: dict[str, Expander] = {}
        self._expander_order: list[str] = []
        self._separator_widgets: list[Separator] = []
        self._updating = False  # Prevent recursive updates
        self._counter = 0  # For auto-generating keys

    def add(
        self,
        expander: Expander = None,
        *,
        key: str = None,
        title: str = "",
        icon: str | dict = None,
        expanded: bool = None,
        **kwargs
    ) -> Expander:
        """Add an expander to the accordion.

        Args:
            expander (Expander | None): Existing Expander to add. If None, creates one.
            key (str | None): Unique identifier for the expander. Auto-generated if not provided.
            title (str): Title for the expander header (when creating new).
            icon (str | dict): Icon for the expander header (when creating new).
            expanded (bool | None): Initial expansion state. If None, first expander
                is expanded when allow_collapse_all=False, otherwise collapsed.
            **kwargs: When expander is None, passed to Expander constructor.

        Returns:
            Expander: The added or created Expander widget.

        Raises:
            ValueError: If an expander with the same key already exists.
        """
        # Auto-generate key if not provided
        if key is None:
            key = f"expander_{self._counter}"
            self._counter += 1

        if key in self._expanders:
            raise ValueError(f"An expander with the key '{key}' already exists.")

        # Add separator before this expander (if not the first)
        if self._show_separators and len(self._expanders) > 0:
            sep = Separator(self, orient='horizontal')
            sep.pack(fill='x')
            self._separator_widgets.append(sep)

        # Create expander if not provided
        if expander is None:
            # Determine initial expanded state
            if expanded is None:
                # If not collapsible and this is the first, expand it
                if not self._allow_collapse_all and len(self._expanders) == 0:
                    expanded = True
                else:
                    expanded = False

            # Get accent/variant from kwargs or use accordion defaults
            accent = self._accent or kwargs.pop('accent', None)
            variant = self._variant or kwargs.pop('variant', None)

            expander = Expander(
                self,
                title=title,
                icon=icon,
                expanded=expanded,
                highlight=True,
                accent=accent,
                variant=variant,
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
        self._expanders[key] = expander
        self._expander_order.append(key)

        # Bind to toggle events
        expander.on_toggled(lambda e, exp=expander: self._on_expander_toggle(exp, e))

        return expander

    def remove(self, key: str) -> None:
        """Remove an expander from the accordion.

        Args:
            key: The key of the expander to remove.

        Raises:
            KeyError: If no expander with the given key exists.

        Note:
            The expander widget is destroyed. If allow_collapse_all=False and
            removing would leave no expanders, or would remove the only
            open expander, another expander will be expanded automatically.
        """
        if key not in self._expanders:
            raise KeyError(f"No expander with key '{key}'")

        expander = self._expanders[key]
        index = self._expander_order.index(key)
        was_expanded = expander['expanded']

        # Remove associated separator
        if self._show_separators and self._separator_widgets:
            if index > 0:
                # Remove the separator before this expander
                sep_index = index - 1
            elif len(self._expanders) > 1:
                # Removing first expander - remove the separator after it
                sep_index = 0
            else:
                sep_index = None

            if sep_index is not None and sep_index < len(self._separator_widgets):
                sep = self._separator_widgets.pop(sep_index)
                sep.destroy()

        # Remove expander from dict/list and destroy
        del self._expanders[key]
        self._expander_order.remove(key)
        expander.destroy()

        # Handle allow_collapse_all=False constraint
        if not self._allow_collapse_all and was_expanded and self._expanders:
            # The removed expander was open - need to open another
            expander_list = [self._expanders[k] for k in self._expander_order]
            any_open = any(exp['expanded'] for exp in expander_list)
            if not any_open:
                expander_list[0].expand()

        # Fire change event
        if self._expanders:
            expander_list = [self._expanders[k] for k in self._expander_order]
            self.event_generate('<<AccordionChange>>', data={
                'expanded': [exp for exp in expander_list if exp['expanded']]
            })

    def _on_expander_toggle(self, expander: Expander, event):
        """Handle expander toggle events."""
        if self._updating:
            return

        self._updating = True
        try:
            is_expanded = event.data.get('expanded', False)
            expander_list = [self._expanders[k] for k in self._expander_order]

            if is_expanded:
                # Expander was just opened
                if not self._allow_multiple:
                    # Collapse all others
                    for exp in expander_list:
                        if exp is not expander and exp['expanded']:
                            exp.collapse()
            else:
                # Expander was just closed
                if not self._allow_collapse_all:
                    # Check if any are still open
                    any_open = any(exp['expanded'] for exp in expander_list)
                    if not any_open:
                        # Re-open this one - can't collapse all
                        expander.expand()
                        return

            # Fire change event
            self.event_generate('<<AccordionChange>>', data={
                'expanded': [exp for exp in expander_list if exp['expanded']]
            })
        finally:
            self._updating = False

    def item(self, key: str) -> Expander:
        """Get an expander by its key.

        Args:
            key: The key of the expander to retrieve.

        Returns:
            The Expander instance.

        Raises:
            KeyError: If no expander with the given key exists.
        """
        if key not in self._expanders:
            raise KeyError(f"No expander with key '{key}'")
        return self._expanders[key]

    def items(self) -> tuple[Expander, ...]:
        """Get all expander widgets in order.

        Returns:
            A tuple of all Expander instances in the order they were added.
        """
        return tuple(self._expanders[key] for key in self._expander_order)

    def keys(self) -> tuple[str, ...]:
        """Get all expander keys in order.

        Returns:
            A tuple of all expander keys in the order they were added.
        """
        return tuple(self._expander_order)

    def configure_item(self, key: str, option: str = None, **kwargs: Any):
        """Configure a specific expander by its key.

        Args:
            key: The key of the expander to configure.
            option: If provided, return the value of this option.
            **kwargs: Configuration options to apply to the expander.

        Returns:
            If option is provided, returns the value of that option.
        """
        expander = self.item(key)
        if option is not None:
            return expander.cget(option)
        expander.configure(**kwargs)

    def expand(self, key: str):
        """Expand the expander with the given key.

        Args:
            key (str): Key of the expander to expand.
        """
        if key in self._expanders:
            self._expanders[key].expand()

    def collapse(self, key: str):
        """Collapse the expander with the given key.

        Args:
            key (str): Key of the expander to collapse.

        Note:
            If allow_collapse_all=False and this is the only open expander,
            this call will be ignored.
        """
        if key in self._expanders:
            exp = self._expanders[key]
            if not self._allow_collapse_all:
                # Check if this is the only open one
                expander_list = [self._expanders[k] for k in self._expander_order]
                open_count = sum(1 for e in expander_list if e['expanded'])
                if open_count <= 1 and exp['expanded']:
                    return  # Can't collapse the last one
            exp.collapse()

    def expand_all(self):
        """Expand all expanders (only effective when allow_multiple=True)."""
        if not self._allow_multiple:
            return
        for exp in self._expanders.values():
            exp.expand()

    def collapse_all(self):
        """Collapse all expanders (only effective when allow_collapse_all=True)."""
        if not self._allow_collapse_all:
            return
        for exp in self._expanders.values():
            exp.collapse()

    @property
    def expanded(self) -> list[Expander]:
        """Get the list of currently expanded Expanders."""
        return [self._expanders[k] for k in self._expander_order if self._expanders[k]['expanded']]

    @configure_delegate('allow_multiple')
    def _delegate_allow_multiple(self, value=None):
        """Get or set whether multiple sections can be open at once."""
        if value is None:
            return self._allow_multiple
        self._allow_multiple = value
        return None

    @configure_delegate('allow_collapse_all')
    def _delegate_allow_collapse_all(self, value=None):
        """Get or set whether all sections can be collapsed."""
        if value is None:
            return self._allow_collapse_all
        self._allow_collapse_all = value
        return None

    @configure_delegate('show_separators')
    def _delegate_show_separators(self, value=None):
        """Get or set whether separators are shown between sections."""
        if value is None:
            return self._show_separators
        self._show_separators = value
        return None

    def on_accordion_changed(self, callback: Callable) -> str:
        """Bind callback to ``<<AccordionChange>>`` events.

        Args:
            callback: Function to call when expanded sections change.
                Receives event with ``event.data = {'expanded': list[Expander]}``.

        Returns:
            Bind ID that can be passed to ``off_accordion_changed`` to remove this callback.
        """
        return self.bind('<<AccordionChange>>', callback, add='+')

    def off_accordion_changed(self, bind_id: str = None):
        """Unbind ``<<AccordionChange>>`` callback(s).

        Args:
            bind_id (str | None): Bind ID returned by ``on_accordion_changed``. If None, unbinds all.
        """
        self.unbind('<<AccordionChange>>', bind_id)