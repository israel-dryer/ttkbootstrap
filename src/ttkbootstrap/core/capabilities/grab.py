from __future__ import annotations

from typing import Any


class GrabMixin:
    """Pointer/keyboard grab helpers (grab).

    A *grab* confines mouse and keyboard events to a particular widget subtree.

    When a grab is active:
      - Pointer events are delivered only to the grab window and its descendants.
      - Keyboard events are also directed to the grab window (effectively focusing input).
      - This is the foundation for *modal* interactions (e.g., modal dialogs).

    Tk supports two kinds of grabs:
      - **Local (application) grab**: confines events within the current Tk application.
      - **Global grab**: confines events at the window system level (more intrusive).

    Notes:
        - Grabs should be released when you are done (typically in a `finally:` block).
        - Global grabs can make the entire desktop feel “stuck” if misused; prefer local grabs
          unless you specifically need global behavior.
        - A grab does not automatically make a window modal; typical modal patterns also:
          `transient(parent)`, `focus_set()`, and `wait_window()` / `wait_visibility()`.
    """

    def grab_set(self) -> None:
        """Set a local (application) grab on this widget.

        With a local grab, events are confined within the current Tk application.
        This is the preferred grab type for modal dialogs inside an application.
        """
        return super().grab_set()  # type: ignore[misc]

    def grab_set_global(self) -> None:
        """Set a global grab on this widget.

        A global grab confines events at the window system level. This is more
        intrusive than a local grab and should be used with care.
        """
        return super().grab_set_global()  # type: ignore[misc]

    def grab_release(self) -> None:
        """Release a grab held by this widget (if any)."""
        return super().grab_release()  # type: ignore[misc]

    def grab_current(self) -> Any:
        """Return the widget in this application that currently holds the grab.

        Returns:
            The widget instance that currently holds the grab, or None if
                no grab is held by this application.
        """
        return super().grab_current()  # type: ignore[misc]

    def grab_status(self) -> str | None:
        """Return the grab status for this widget.

        Returns:
            The grab status: "local" if this widget holds a local grab,
                "global" if this widget holds a global grab, or None if
                this widget does not hold the grab.
        """
        return super().grab_status()  # type: ignore[misc]
