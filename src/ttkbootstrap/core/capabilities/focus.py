from __future__ import annotations

from typing import Any


class FocusMixin:
    """Keyboard focus helpers (focus).

    Tk's *input focus* determines which widget receives key press/release events.
    Focus is typically managed by the window manager at the top-level window level,
    and then by the application within the top-level.

    Tk remembers the most recent focused descendant for each top-level. When the
    window manager gives focus to a top-level, Tk redirects it to that remembered
    widget automatically.

    Notes:
        - Prefer `focus_set()` for normal use.
        - `focus_force()` can steal focus and should be used sparingly.
        - Tab/Shift-Tab traversal typically uses `tk_focusNext()` / `tk_focusPrev()`.
    """

    # -------------------------------------------------------------------------
    # Core focus operations
    # -------------------------------------------------------------------------

    def focus_get(self) -> Any:
        """Return the widget in this application that currently has focus.

        This queries the focus window on the display containing the application's
        main window. If no window in this application has focus on that display,
        the return value is None / empty (depending on Tkinter/Tk behavior).

        Returns:
            The focused widget instance, or None if no widget in this application
            currently has focus on the relevant display.
        """
        return super().focus_get()  # type: ignore[misc]

    def focus_set(self, *, visual_focus: bool = False) -> None:
        """Request focus for this widget.

        If this application currently has the focus on the widget's display, this
        resets the focus for that display to this widget. Otherwise, Tk remembers
        this widget as the focus for its top-level and will redirect focus to it
        the next time the top-level receives focus.

        Args:
            visual_focus: If True, show focus ring as if focused via keyboard
                (Tab navigation). Default is False, which shows no focus ring
                for programmatic focus. Useful for validation errors where you
                want to draw attention to a field.
        """
        return super().focus_set(visual_focus=visual_focus)  # type: ignore[misc]

    def focus_force(self, *, visual_focus: bool = False) -> None:
        """Force focus to this widget (use sparingly).

        This attempts to set the focus for the widget's display even if the
        application does not currently have the input focus for that display.
        In normal usage, applications should not claim focus; they should wait
        for the window manager/user to give it focus.

        Args:
            visual_focus: If True, show focus ring as if focused via keyboard
                (Tab navigation). Default is False, which shows no focus ring
                for programmatic focus.
        """
        return super().focus_force(visual_focus=visual_focus)  # type: ignore[misc]

    def focus_displayof(self) -> Any:
        """Return the focused widget for the display containing this widget.

        If the focus window for this widget's display is not in this application,
        the return value is None / empty (depending on Tkinter/Tk behavior).

        Returns:
            The focused widget instance for this display, or None.
        """
        return super().focus_displayof()  # type: ignore[misc]

    def focus_lastfor(self) -> Any:
        """Return the most recent focused widget within this widget's top-level.

        Tk tracks the most recent focus window for each top-level. This returns
        the widget that will receive focus the next time the top-level gets focus
        from the window manager. If none has ever had focus (or it was deleted),
        Tk returns the top-level itself.

        Returns:
            The most recent focused widget in the same top-level, or the top-level.
        """
        return super().focus_lastfor()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Focus traversal (Tab order utilities)
    # -------------------------------------------------------------------------

    def tk_focusNext(self) -> Any:
        """Return the next widget in the focus traversal order.

        This is used by default bindings for Tab traversal in many Tk widgets.

        Returns:
            The next widget in focus order, or this widget if no other is eligible.
        """
        return super().tk_focusNext()  # type: ignore[misc]

    def tk_focusPrev(self) -> Any:
        """Return the previous widget in the focus traversal order.

        This is used by default bindings for Shift-Tab traversal in many Tk widgets.

        Returns:
            The previous widget in focus order, or this widget if no other is eligible.
        """
        return super().tk_focusPrev()  # type: ignore[misc]