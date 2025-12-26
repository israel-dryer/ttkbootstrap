from __future__ import annotations

from typing import Any, Callable


class AfterMixin:
    """Scheduling helpers (after).

    Tk’s `after` family lets you schedule callbacks to run later on the Tk event loop.

    Common uses:
        - Debounce user input (schedule a callback and cancel previous ones).
        - Run periodic UI updates (schedule, then reschedule from inside the callback).
        - Defer work until the UI is idle (`after_idle`) so layout/paint can complete.

    Notes:
        - Callbacks run on the Tk thread/event loop. If you have long-running work,
          run it off-thread/process and schedule UI updates back onto Tk using `after`.
        - `after` returns an identifier that can be canceled with `after_cancel`.
    """

    def after(self, ms: int, func: Callable[..., Any] | None = None, *args: Any) -> str:
        """Schedule a callback to run after a delay.

        Args:
            ms: Delay in milliseconds.
            func: Callback to run. If omitted/None, Tk blocks for `ms` milliseconds
                while still processing events (use sparingly).
            *args: Arguments to pass to `func` when it is called.

        Returns:
            An identifier that can be used with `after_cancel`.
        """
        return super().after(ms, func, *args)  # type: ignore[misc]

    def after_idle(self, func: Callable[..., Any], *args: Any) -> str:
        """Schedule a callback to run when the event loop is idle.

        Idle callbacks run after Tk has finished processing the current batch of
        events and pending UI work.

        Args:
            func: Callback to run.
            *args: Arguments to pass to `func` when it is called.

        Returns:
            An identifier that can be used with `after_cancel`.
        """
        return super().after_idle(func, *args)  # type: ignore[misc]

    def after_cancel(self, id: str) -> None:
        """Cancel a scheduled callback.

        Args:
            id: The identifier returned by `after` or `after_idle`.
        """
        return super().after_cancel(id)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Convenience helpers (optional)
    # -------------------------------------------------------------------------

    def after_repeat(self, ms: int, func: Callable[..., Any], *args: Any) -> Callable[[], None]:
        """Call `func` repeatedly every `ms` milliseconds.

        This helper schedules `func` and then automatically reschedules it after
        each run. It returns a `cancel()` function you can call to stop repetition.

        Args:
            ms: Interval in milliseconds.
            func: Callback to run each interval.
            *args: Arguments to pass to `func`.

        Returns:
            A `cancel()` callable. Call it to stop the repeating schedule.

        Examples:
            >>> cancel = widget.after_repeat(250, tick)
            >>> cancel()
        """
        cancelled = False
        token: str | None = None

        def _run():
            nonlocal token
            if cancelled:
                return
            func(*args)
            token = self.after(ms, _run)

        token = self.after(ms, _run)

        def cancel() -> None:
            nonlocal cancelled, token
            cancelled = True
            if token is not None:
                try:
                    self.after_cancel(token)
                except Exception:
                    pass
                token = None

        return cancel
