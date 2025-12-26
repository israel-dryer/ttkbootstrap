from __future__ import annotations

from typing import Any, Callable


class SelectionMixin:
    """X selection helpers (selection).

    Tk’s `selection` command provides access to the X selection mechanism (ICCCM),
    most commonly the **PRIMARY** selection, and also supports **CLIPBOARD** and
    other named selections.

    Portability notes:
        - On X11, PRIMARY is a system-wide selection shared across processes.
        - On Windows, PRIMARY is provided by Tk (not the OS) and is shared only
          within related interpreters, not across processes.
        - For clipboard-style usage, Tk also provides the `clipboard_*` methods,
          which are often a better cross-platform fit.

    Intended usage:
        class Widget(SelectionMixin, ttk.Widget): ...
        class App(SelectionMixin, tkinter.Tk): ...
    """

    def selection_clear(self, **kw: Any) -> None:
        """Clear a selection so that no window owns it.

        This corresponds to `selection clear` and clears the specified selection
        on the target display (if it exists).

        Args:
            **kw: Selection options forwarded to Tkinter. Common options include:
                - selection: The selection name (e.g. "PRIMARY", "CLIPBOARD").
                  Defaults to "PRIMARY".
                - displayof: A widget/window whose display should be targeted.
                  Defaults to "." (the application’s main display).
        """
        return super().selection_clear(**kw)  # type: ignore[misc]

    def selection_get(self, **kw: Any) -> str:
        """Return the current contents of a selection.

        This corresponds to `selection get` and retrieves a selection from the
        target display. The default selection is "PRIMARY" and the default type
        is "STRING".

        Args:
            **kw: Selection options forwarded to Tkinter. Common options include:
                - selection: The selection name (e.g. "PRIMARY", "CLIPBOARD").
                  Defaults to "PRIMARY".
                - type: The desired “target” type for conversion (e.g. "STRING",
                  "UTF8_STRING", "TARGETS", "FILE_NAME"). Defaults to "STRING".
                - displayof: A widget/window whose display should be targeted.
                  Defaults to ".".

        Returns:
            The selection contents as a string.

        Notes:
            - If the owner returns a non-string representation (e.g. ATOM or INTEGER),
              Tk converts it to a space-separated string representation.
            - Tk will not retrieve UTF-8 formatted data unless you request
              `type="UTF8_STRING"`.
        """
        return super().selection_get(**kw)  # type: ignore[misc]

    def selection_handle(self, command: str | None, **kw: Any) -> None:
        """Register or remove a handler for selection retrieval requests.

        This corresponds to `selection handle`. When this widget owns a selection,
        Tk will execute *command* when another client attempts to retrieve the
        selection in the requested type.

        Args:
            command: A Tcl command (string) to execute to supply selection data.
                If an empty string or None, removes any existing handler for the
                given selection/type combination.
            **kw: Handler options forwarded to Tkinter. Common options include:
                - selection: Selection name (defaults to "PRIMARY").
                - type: Requested type (defaults to "STRING").
                - format: Representation format used to transmit the selection
                  (defaults to "STRING"). Usually only needed for compatibility
                  with non-Tk requesters.

        Notes:
            - When handling type "STRING", Tk will also handle "UTF8_STRING"
              automatically.
            - The command is invoked with two additional arguments appended:
              `offset` and `maxChars`. The command should return up to `maxChars`
              characters starting at `offset`. Large selections are retrieved
              in multiple chunks.
        """
        # Tkinter expects `command` to be a Tcl script; keep the pass-through shape.
        if command is None:
            command = ""
        return super().selection_handle(command, **kw)  # type: ignore[misc]

    def selection_own(self, **kw: Any) -> str:
        """Query the current selection owner within this application.

        This corresponds to the *query* form of `selection own`, returning the
        pathname of the window in this application that owns the selection on
        the target display, or an empty string if none.

        Args:
            **kw: Query options forwarded to Tkinter. Common options include:
                - selection: Selection name (defaults to "PRIMARY").
                - displayof: A widget/window whose display should be targeted.
                  Defaults to ".".

        Returns:
            The pathname of the owner window in this application, or an empty
            string if no window in this application owns the selection.
        """
        return super().selection_own(**kw)  # type: ignore[misc]

    def selection_own_set(
            self,
            owner: Any,
            command: Callable[[], Any] | None = None,
            *,
            selection: str = "PRIMARY",
    ) -> None:
        """Make *owner* the selection owner (convenience helper).

        Tk’s `selection own` *setter* form is easy to confuse with the query form.
        This helper makes the intent explicit while still using Tk’s semantics.

        Args:
            owner: The widget/window that should own the selection.
            command: Optional callback invoked when this widget loses ownership
                of the selection (i.e., another window claims it).
            selection: The selection name to claim (defaults to "PRIMARY").
        """
        # `selection_own` in Tkinter supports setting with `command` and `selection`.
        return super().selection_own(owner, command=command, selection=selection)  # type: ignore[misc]
