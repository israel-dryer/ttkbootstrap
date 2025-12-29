"""Visual focus management for ttkbootstrap.

This module provides keyboard vs mouse focus distinction by leveraging
the TTK 'background' state as a "keyboard focus" indicator. This enables
style maps to show focus rings only for keyboard navigation (Tab), not
for mouse clicks.

The approach:
    - Tab key press → sets 'background' state on newly focused widget
    - FocusOut → removes 'background' state
    - Mouse clicks never add 'background', so click focus is distinguishable

Style maps can then use:
    ('background focus', ring_color)  # Keyboard focus - show ring
    ('focus', '')                     # Mouse focus - no ring

This matches the CSS :focus-visible behavior that modern browsers implement.

Programmatic focus:
    The focus_set() and focus_force() methods accept a `visual_focus` parameter.
    When True, the focus ring is shown as if the widget was focused via keyboard:

        widget.focus_set(visual_focus=True)  # Shows focus ring

Note:
    The 'background' TTK state is normally used to indicate an inactive
    window. Since this is rarely styled in practice, it's repurposed here
    for keyboard focus tracking.
"""

import tkinter as tk
from tkinter import TclError
from typing import Optional

_installed = False
_root_ref: Optional[tk.Misc] = None

# Store original focus methods
_original_focus_set = tk.Misc.focus_set
_original_focus_force = tk.Misc.focus_force


def _patched_focus_set(self, *, visual_focus: bool = False) -> None:
    """Enhanced focus_set that optionally shows visual focus ring.

    Args:
        visual_focus: If True, show focus as if focused via keyboard. Default is False.

    Examples:
        ```python
        # Normal programmatic focus (no ring)
        entry.focus_set()

        # Focus with visible ring (e.g., after validation error)
        entry.focus_set(visual_focus=True)
        ```
    """
    _original_focus_set(self)
    if visual_focus:
        try:
            self.state(['background'])
        except (TclError, AttributeError):
            pass


def _patched_focus_force(self, *, visual_focus: bool = False) -> None:
    """Enhanced focus_force that optionally shows visual focus ring.

    Args:
        visual_focus: If True, show focus as if focused via keyboard. Default is False.

    Examples:
        ```python
        # Normal forced focus (no ring)
        entry.focus_force()

        # Forced focus with visible ring
        entry.focus_force(visual_focus=True)
        ```
    """
    _original_focus_force(self)
    if visual_focus:
        try:
            self.state(['background'])
        except (TclError, AttributeError):
            pass


def _on_tab_focus(event: tk.Event) -> None:
    """Handle Tab key press by marking the newly focused widget.

    Uses after_idle to wait for focus to actually move before
    querying focus_get() and setting the background state.
    """
    root = event.widget.winfo_toplevel()

    def set_keyboard_focus_state():
        widget = root.focus_get()
        if widget is None:
            return
        try:
            widget.state(['background'])
        except (TclError, AttributeError):
            pass  # Widget doesn't support state (non-TTK)

    root.after_idle(set_keyboard_focus_state)


def _on_focus_out(event: tk.Event) -> None:
    """Clear the keyboard focus indicator when widget loses focus."""
    try:
        event.widget.state(['!background'])
    except (TclError, AttributeError):
        pass  # Widget doesn't support state (non-TTK)


def install_visual_focus(root: tk.Misc = None) -> None:
    """Install keyboard focus tracking for the application.

    This function sets up global event bindings that track whether
    focus was acquired via keyboard (Tab) or mouse click, enabling
    style maps to show focus rings only for keyboard navigation.

    Args:
        root: Optional root widget. If not provided, bindings are
              set up to work with any root via bind_class on Tk.

    Note:
        This is called automatically when ttkbootstrap is imported.
        You typically don't need to call this manually.

    Examples:
        Style builders can use the 'background' state to distinguish:

        ```python
        b.map_style(ttk_style,
            focuscolor=[
                ('background focus', ring_color),  # Keyboard focus
                ('focus', ''),                     # Mouse focus
                ('', ''),
            ]
        )
        ```
    """
    global _installed, _root_ref

    if _installed:
        return

    # Patch focus_set and focus_force to support visual_focus parameter
    tk.Misc.focus_set = _patched_focus_set
    tk.Misc.focus_force = _patched_focus_force

    # Bind Tab key globally - works even before any root exists
    # by using bind_class on the base Tk class
    tk.Tk.bind_all = _bind_all_with_focus

    _installed = True


def _bind_all_with_focus(self, sequence=None, func=None, add=None):
    """Wrapper for bind_all that installs focus tracking on first call."""
    global _root_ref

    # Install our bindings on first bind_all call (when root exists)
    if _root_ref is None:
        _root_ref = self
        # Bind Tab on root window - the after_idle callback will set state
        # on whatever widget receives focus (forward or backward)
        self.bind('<Tab>', _on_tab_focus, '+')
        # Clear background state on focus out (needs bind_all for all widgets)
        self.bind_all('<FocusOut>', _on_focus_out, '+')

    # Call original bind_all
    return tk.Misc.bind_all(self, sequence, func, add)


def uninstall_visual_focus() -> None:
    """Remove keyboard focus tracking bindings.

    This restores the original behavior where focus state doesn't
    distinguish between keyboard and mouse focus.

    Note:
        After calling this, style maps using 'background focus' will
        no longer show focus rings for keyboard navigation.
    """
    global _installed, _root_ref

    if not _installed:
        return

    # Restore original focus methods
    tk.Misc.focus_set = _original_focus_set
    tk.Misc.focus_force = _original_focus_force

    if _root_ref is not None:
        try:
            _root_ref.unbind('<Tab>')
            _root_ref.unbind_all('<FocusOut>')
        except TclError:
            pass  # Root may have been destroyed

    _root_ref = None
    _installed = False


def is_keyboard_focus(widget: tk.Misc) -> bool:
    """Check if a widget currently has keyboard-initiated focus.

    Args:
        widget: The widget to check.

    Returns:
        True if the widget has focus AND was focused via keyboard.
    """
    try:
        state = widget.state()
        return 'focus' in state and 'background' in state
    except (TclError, AttributeError):
        return False


__all__ = [
    'install_visual_focus',
    'uninstall_visual_focus',
    'is_keyboard_focus',
]