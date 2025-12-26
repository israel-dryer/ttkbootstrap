from __future__ import annotations

from typing import Any


class BusyMixin:
    """Busy (input-blocking) helpers (busy).

    Tk’s *busy* facility blocks pointer events from reaching a widget/window by
    placing an input-only window above it. This is typically used to prevent
    user interaction during a long-running operation (e.g., loading, saving).

    Notes:
        - Busy blocks pointer events; it does not guarantee keyboard events are blocked.
        - Always release busy state in a `finally:` block (or use a context manager).
    """

    def busy_hold(self, **kw: Any) -> None:
        """Activate busy mode for this widget/window.

        While busy is active, pointer events are intercepted so the user cannot
        interact with the target window (and typically its children).

        Args:
            **kw: Busy options forwarded to Tk. Common options include `cursor`.
        """
        return super().busy_hold(**kw)  # type: ignore[misc]

    def busy_forget(self) -> None:
        """Deactivate busy mode for this widget/window."""
        return super().busy_forget()  # type: ignore[misc]

    def busy_status(self) -> bool:
        """Return True if this widget/window is currently in busy mode."""
        return bool(super().busy_status())  # type: ignore[misc]

    def busy_configure(self, **kw: Any) -> Any:
        """Query or configure busy options for this widget/window.

        With no options, returns configuration information (format depends on Tk).
        With options provided, updates the busy configuration.

        Args:
            **kw: Busy options forwarded to Tk.

        Returns:
            The raw Tk result for the configure query/set.
        """
        return super().busy_configure(**kw)  # type: ignore[misc]

    def busy_cget(self, option: str) -> Any:
        """Return the current value of a single busy option.

        Args:
            option: Option name (e.g. "-cursor" or "cursor").

        Returns:
            The option value.
        """
        opt = option if option.startswith("-") else f"-{option}"
        return super().busy_cget(opt)  # type: ignore[misc]
