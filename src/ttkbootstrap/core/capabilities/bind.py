from __future__ import annotations

from typing import Any, Callable, Optional, Union


class BindingsMixin:
    """Event binding and virtual event generation.

    This mixin documents the *Tkinter-style* binding API (`bind`, `unbind`,
    `bind_all`, etc.) while reflecting ttkbootstrap v2’s enhanced event system.

    Differences from stock Tkinter:
        - Virtual events generated via `event_generate("<<Name>>", data=...)` may
          carry **arbitrary Python objects** as event payload.
        - Event handlers receive an event object with a consistent `.data` attribute:
            - `.data` is the Python object you passed for virtual events.
            - `.data` is `None` for non-virtual events.

    Notes:
        - Prefer `bind` over `bind_all` unless you truly need a global binding.
        - Return the string `"break"` from a handler to stop further processing.
        - Virtual event data is intended for application-local messaging.
    """

    # ---------------------------------------------------------------------
    # Binding (widget, class, and application/global)
    # ---------------------------------------------------------------------

    def bind(
            self,
            sequence: Optional[str] = None,
            func: Optional[Callable[..., Any]] = None,
            add: Optional[Union[bool, str]] = None,
    ) -> Optional[str]:
        """Bind an event sequence to a handler.

        Args:
            sequence: Event pattern string (e.g. "<Button-1>", "<KeyPress>", "<<MyEvent>>").
                If None, returns a string describing all bindings on this widget.
            func: Handler callable. The handler is called with a single argument:
                the event object. For ttkbootstrap enhanced events, `event.data`
                is always present (None for regular events, payload for virtual events).
            add: If true/"+" then this binding is added in addition to existing bindings.
                If false/None then any existing binding for this sequence is replaced.

        Returns:
            If `func` is provided, returns an internal Tk binding id that can be used
            with `unbind(sequence, funcid)`. If `func` is None, returns a Tcl binding
            script string (Tkinter behavior varies by version) or None.

        Examples:
            Bind a regular event:

                widget.bind("<Button-1>", on_click)

            Bind a virtual event that carries Python data:

                widget.bind("<<Save>>", on_save)
                widget.event_generate("<<Save>>", data={"path": "doc.txt"})
        """
        return super().bind(sequence, func, add)  # type: ignore[misc]

    def unbind(self, sequence: str, funcid: str | None = None) -> None:
        """Remove a binding for an event sequence.

        Args:
            sequence: The event sequence that was previously bound.
            funcid: The binding id returned from `bind`. If omitted, removes all
                handlers for the given sequence on this widget.
        """
        return super().unbind(sequence, funcid)  # type: ignore[misc]

    def bind_all(
            self,
            sequence: Optional[str] = None,
            func: Optional[Callable[..., Any]] = None,
            add: Optional[Union[bool, str]] = None,
    ) -> Optional[str]:
        """Bind an event sequence at the application level (all widgets).

        Use sparingly. This affects *every* widget in the application.

        Args:
            sequence: Event pattern string.
            func: Handler callable.
            add: Whether to add alongside existing bindings.

        Returns:
            A binding id when setting a binding, otherwise a binding script string
            (version-dependent) or None.
        """
        return super().bind_all(sequence, func, add)  # type: ignore[misc]

    def unbind_all(self, sequence: str) -> None:
        """Remove an application-level binding for the given sequence.

        Args:
            sequence: The event sequence to unbind.
        """
        return super().unbind_all(sequence)  # type: ignore[misc]

    def bind_class(
            self,
            className: str,
            sequence: Optional[str] = None,
            func: Optional[Callable[..., Any]] = None,
            add: Optional[Union[bool, str]] = None,
    ) -> Optional[str]:
        """Bind an event sequence to a Tk widget class.

        This attaches a handler to *all widgets of a given Tk class name*
        (e.g. "TButton", "TEntry").

        Args:
            className: Tk class name.
            sequence: Event pattern string.
            func: Handler callable.
            add: Whether to add alongside existing bindings.

        Returns:
            A binding id when setting a binding, otherwise a binding script string
            (version-dependent) or None.
        """
        return super().bind_class(className, sequence, func, add)  # type: ignore[misc]

    def unbind_class(self, className: str, sequence: str) -> None:
        """Remove a class-level binding.

        Args:
            className: Tk class name.
            sequence: Event sequence to unbind for that class.
        """
        return super().unbind_class(className, sequence)  # type: ignore[misc]

    # ---------------------------------------------------------------------
    # Event generation (including virtual-event payloads)
    # ---------------------------------------------------------------------

    def event_generate(self, sequence: str, data: Any | None = None, **kw: Any) -> None:
        """Generate an event.

        This can synthesize both physical events (like "<Button-1>") and virtual
        events (like "<<MyEvent>>"). For virtual events, ttkbootstrap supports
        attaching a Python payload via the `data` parameter.

        Args:
            sequence: Event sequence to generate (commonly "<<Name>>" for virtual events).
            data: Optional Python object payload for **virtual events**. When provided,
                handlers will receive an event object whose `.data` is this value.
                For non-virtual events, `data` is ignored and `.data` will be None.
            **kw: Additional Tk event fields (e.g. x=..., y=..., rootx=..., rooty=...).
        """
        return super().event_generate(sequence, data=data, **kw)  # type: ignore[misc]
