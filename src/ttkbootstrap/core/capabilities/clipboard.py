from __future__ import annotations

from typing import Any


class ClipboardMixin:
    """Clipboard helpers (clipboard).

    Tk’s `clipboard` command provides access to the system (or Tk-managed) clipboard.
    Tkinter exposes this via the `clipboard_*` methods.

    Notes:
        - Clipboard behavior can vary by platform and window system.
        - Most apps only need text clipboard operations (clear/append/get).
        - For advanced cases (multiple clipboard types, non-text formats), Tk supports
          additional options passed via keyword arguments.
    """

    def clipboard_clear(self, **kw: Any) -> None:
        """Clear the clipboard on the target display.

        This removes all data from the clipboard for the specified display.

        Args:
            **kw: Clipboard options forwarded to Tk. Common options include:
                - displayof: A widget/window whose display should be targeted.
                  (Rarely needed in typical single-display apps.)
        """
        return super().clipboard_clear(**kw)  # type: ignore[misc]

    def clipboard_append(self, string: str, **kw: Any) -> None:
        """Append text to the clipboard.

        Appends *string* to the clipboard. If you want to replace clipboard contents,
        call `clipboard_clear()` first and then `clipboard_append()`.

        Args:
            string: Text to append to the clipboard.
            **kw: Clipboard options forwarded to Tk. Common options include:
                - displayof: Target display for the clipboard.
                - type: Clipboard type name (platform/window-system dependent).
                - format: Data format name (platform/window-system dependent).

        Example:
            self.clipboard_clear()
            self.clipboard_append("Hello, world!")
        """
        return super().clipboard_append(string, **kw)  # type: ignore[misc]

    def clipboard_get(self, **kw: Any) -> str:
        """Return clipboard contents as text.

        Args:
            **kw: Clipboard options forwarded to Tk. Common options include:
                - displayof: Target display for the clipboard.
                - type: Clipboard type name (platform/window-system dependent).

        Returns:
            The clipboard contents as a string.

        Raises:
            tkinter.TclError: If the clipboard is empty or does not contain
                data that can be converted to the requested type.
        """
        return super().clipboard_get(**kw)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Convenience helpers (optional): common "text clipboard" patterns
    # -------------------------------------------------------------------------

    def clipboard_set(self, text: str, **kw: Any) -> None:
        """Replace clipboard contents with *text*.

        This is a convenience wrapper for:

            clipboard_clear(...)
            clipboard_append(text, ...)

        Args:
            text: Text to set on the clipboard.
            **kw: Clipboard options forwarded to `clipboard_clear` / `clipboard_append`.
        """
        self.clipboard_clear(**kw)
        self.clipboard_append(text, **kw)

    def clipboard_get_text(self, **kw: Any) -> str:
        """Return clipboard contents as text (alias for `clipboard_get`)."""
        return self.clipboard_get(**kw)
