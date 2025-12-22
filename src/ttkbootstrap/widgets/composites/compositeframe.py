import tkinter as tk
from tkinter import ttk

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.types import Master


class Composite:
    """State coordinator for composite widgets.

    Composite is a pure state management class that synchronizes interaction
    states (hover, pressed, focus, selected, disabled) across multiple widgets.
    It does not inherit from any visual widget, making it suitable as a
    coordination hub for widgets anywhere in the widget tree.

    Attributes:
        HOVER (str): State name constant for hover state ('hover').
        ACTIVE (str): State name constant for active state ('active').
        PRESSED (str): State name constant for pressed state ('pressed').
        SELECTED (str): State name constant for selected state ('selected').
        FOCUS (str): State name constant for focus state ('focus').
        DISABLED (str): State name constant for disabled state ('disabled').
        selected (bool): Read-only property for current selection state.
        disabled (bool): Read-only property for current disabled state.
    """

    # state names
    HOVER = 'hover'
    ACTIVE = 'active'
    PRESSED = 'pressed'
    SELECTED = 'selected'
    FOCUS = 'focus'
    DISABLED = 'disabled'

    def __init__(self, event_target, select_on_click=False):
        """Initialize the Composite coordinator.

        Args:
            event_target: The widget that determines bounds for hover detection
                and where <<CompositeInvoke>> events are generated. This should
                typically be the container widget that visually represents the
                composite group.
            select_on_click: If True, automatically toggles the selected state
                when clicking on non-button registered widgets. Defaults to False.
        """
        self._hovered = False
        self._pressed = False
        self._focused = False

        # semantic
        self._selected = False
        self._disabled = False

        # event target determines bounds and where events are generated
        self._event_target = event_target

        # composites registry
        self._composites = set()

        # auto-toggle selection on click if enabled
        if select_on_click:
            self.on_invoke(lambda e: self.set_selected(not self._selected))

    @property
    def selected(self):
        return self._selected

    @property
    def disabled(self):
        return self._disabled

    def register_composite(self, widget: ttk.Widget):
        """Register a widget to participate in state synchronization.

        The widget will be bound to event handlers and will receive state
        updates whenever any registered widget's state changes. Registered
        widgets can be anywhere in the widget tree; they don't need to be
        children of the event_target.

        Args:
            widget: The ttk widget to register for state synchronization.
                Event bindings are added to this widget using add='+' to
                preserve existing bindings.

        Note:
            Buttons are treated specially - they invoke their command on
            click instead of generating <<CompositeInvoke>> events.
        """
        self._composites.add(widget)

        widget.bind('<Enter>', self._on_enter, add='+')
        widget.bind('<Leave>', self._on_leave, add='+')
        widget.bind('<ButtonPress-1>', self._on_press, add='+')
        widget.bind('<ButtonRelease-1>', self._on_release, add='+')
        widget.bind('<FocusIn>', self._on_focus_in, add='+')
        widget.bind('<FocusOut>', self._on_focus_out, add='+')

    def set_selected(self, selected: bool):
        """Set the selected state and propagate to all registered widgets.

        Args:
            selected: True to mark as selected, False to deselect.
        """
        self._selected = selected
        self._update_states()

    def set_disabled(self, disabled: bool):
        """Set the disabled state and propagate to all registered widgets.

        When disabled, hover, pressed, and focus states are automatically
        cleared and will not update until re-enabled.

        Args:
            disabled: True to mark as disabled, False to enable.
        """
        self._disabled = disabled
        self._update_states()

    def _pointer_inside_bounds(self):
        rx, ry = self._event_target.winfo_rootx(), self._event_target.winfo_rooty()
        rw, rh = self._event_target.winfo_width(), self._event_target.winfo_height()
        px, py = self._event_target.winfo_pointerxy()

        if px < rx or py < ry:
            return False

        return (px - rx - rw) < 0 and (py - ry - rh) < 0

    def _update_states(self):
        states_on = set()
        states_off = set()

        if self._disabled:
            states_on.add(self.DISABLED)
            states_off |= {self.HOVER, self.PRESSED, self.FOCUS}
        else:
            states_off.add(self.DISABLED)
            (states_on if self._hovered else states_off).add(self.HOVER)
            (states_on if self._pressed else states_off).add(self.PRESSED)
            (states_on if self._focused else states_off).add(self.FOCUS)

        (states_on if self._selected else states_off).add(self.SELECTED)

        on = [s for s in states_on]
        off = [f'!{s}' for s in states_off]
        state_map = tuple(on + off)

        for c in self._composites:
            c.state(state_map)

    def _on_enter(self, e):
        self._hovered = True
        self._pressed = False
        self._update_states()

    def _on_leave(self, e):
        in_bounds = self._pointer_inside_bounds()
        if in_bounds:
            self._hovered = True
        else:
            self._hovered = False
        self._pressed = False
        self._update_states()

    def _on_press(self, e):
        self._pressed = True
        self._update_states()

    def _on_release(self, e):
        self._pressed = False
        self._update_states()
        # For buttons, invoke their command; for others, generate event
        if isinstance(e.widget, ttk.Button):
            # Manually invoke the button's command since our binding blocks it
            cmd = e.widget.cget('command')
            if cmd:
                e.widget.tk.call(cmd)
        else:
            # Only non-button widgets trigger selection
            self._event_target.event_generate('<<CompositeInvoke>>', when='tail')

    def _on_focus_in(self, e):
        self._focused = True
        self._update_states()

    def _on_focus_out(self, e):
        self._focused = False
        self._hovered = False
        self._pressed = False
        self._update_states()

    def on_invoke(self, callback) -> str:
        """Bind to ``<<CompositeInvoke>>``. Callback receives ``event.data = None``. Fired when clicking on non-button registered widgets."""
        return self._event_target.bind('<<CompositeInvoke>>', callback, add='+')

    def off_invoke(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<CompositeInvoke>>``."""
        return self._event_target.unbind('<<CompositeInvoke>>', bind_id)


class CompositeFrame(Frame):
    """A ttkbootstrap Frame that uses Composite for state coordination.

    CompositeFrame is a convenience wrapper that combines ttk.Frame with the
    Composite state coordinator. It provides a simple way to create containers
    with synchronized state management across child widgets.

    Attributes:
        selected (bool): Read-only property for current selection state.
        disabled (bool): Read-only property for current disabled state.
    """

    def __init__(self, master: Master = None, select_on_click: bool = False, **kwargs):
        """Initialize the CompositeFrame.

        Args:
            master: The parent widget.
            select_on_click: If True, automatically toggles selection when
                clicking on non-button registered widgets. Defaults to False.
            **kwargs: Additional arguments passed to ttk.Frame constructor.
        """
        super().__init__(master, **kwargs)

        # Create composite coordinator with self as event target
        self._composite = Composite(event_target=self, select_on_click=select_on_click)

        # Register self to receive state updates
        self._composite.register_composite(self)

    def register_composite(self, widget):
        """Register a widget to participate in state synchronization.

        Args:
            widget: The ttk widget to register.

        See Also:
            Composite.register_composite for more details.
        """
        return self._composite.register_composite(widget)

    def set_selected(self, selected: bool):
        """Set the selected state.

        Args:
            selected: True to mark as selected, False to deselect.

        See Also:
            Composite.set_selected for more details.
        """
        return self._composite.set_selected(selected)

    def set_disabled(self, disabled: bool):
        """Set the disabled state.

        Args:
            disabled: True to mark as disabled, False to enable.

        See Also:
            Composite.set_disabled for more details.
        """
        return self._composite.set_disabled(disabled)

    @property
    def selected(self):
        """bool: Current selection state (read-only)."""
        return self._composite.selected

    @property
    def disabled(self):
        """bool: Current disabled state (read-only)."""
        return self._composite.disabled

    def on_invoke(self, callback) -> str:
        """Bind to ``<<CompositeInvoke>>``. Callback receives ``event.data = None``. Fired when clicking on non-button registered widgets."""
        return self._composite.on_invoke(callback)

    def off_invoke(self, bind_id: str | None = None) -> None:
        """Unbind from ``<<CompositeInvoke>>``."""
        return self._composite.off_invoke(bind_id)