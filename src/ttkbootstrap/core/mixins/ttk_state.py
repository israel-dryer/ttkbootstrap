from __future__ import annotations

from typing import Iterable, Any


class TtkStateMixin:
    """ttk-only widget helpers.

    This mixin contains methods that exist on ttk widgets but not on classic Tk widgets
    (e.g., `tk.Text`, `tk.Canvas`).
    """

    def state(self, statespec: str | Iterable[str] | None = None) -> Any:
        """Get or modify the ttk state of the widget.

        Args:
            statespec: State specification (e.g. ("disabled",) or ("!disabled",)).
                If None, returns the current state.

        Returns:
            The current state (getter) or an implementation-dependent result.
        """
        return super().state(statespec)  # type: ignore[misc]

    def instate(self, statespec: str | Iterable[str], callback: Any = None) -> bool:
        """Test the ttk state of the widget.

        Args:
            statespec: State specification to test.
            callback: Optional callable invoked if the test succeeds.

        Returns:
            True if the widget matches the state spec; otherwise False.
        """
        return super().instate(statespec, callback)  # type: ignore[misc]
