"""Integration helpers for using Signal with tkinter/ttk widgets.

Call ``enable_widget_integration()`` once early (after creating your Tk/Window)
to allow passing ``Signal`` objects directly to widget constructors and
``configure(...)`` for options like ``textvariable`` and ``variable``.

Without this, some environments/widgets may not coerce custom objects to the
required Tcl variable name automatically.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable, Tuple

import tkinter as tk
import tkinter.ttk as ttk


def _is_signal(obj: Any) -> bool:
    try:
        # Cheap duck-typing to avoid hard import dependency
        m = type(obj).__module__
        return (
            (m.startswith("ttkbootstrap.signals") or m.startswith("ttkbootstrap.core.signals"))
            and hasattr(obj, "name")
            and hasattr(obj, "var")
        )
    except Exception:
        return False


def _coerce_kwargs(kwargs: dict[str, Any]) -> None:
    for key in ("textvariable", "variable"):
        if key in kwargs:
            val = kwargs[key]
            if _is_signal(val):
                kwargs[key] = str(val)


def _wrap_init(cls: type) -> None:
    orig_init = cls.__init__  # type: ignore[attr-defined]

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        _coerce_kwargs(kwargs)
        orig_init(self, *args, **kwargs)  # type: ignore[misc]

    cls.__init__ = __init__  # type: ignore[assignment]


def _wrap_configure(cls: type) -> None:
    orig_config = cls.configure  # type: ignore[attr-defined]

    def configure(self, cnf: Any = None, **kwargs: Any):  # type: ignore[override]
        if isinstance(cnf, dict):
            _coerce_kwargs(cnf)
        _coerce_kwargs(kwargs)
        return orig_config(self, cnf, **kwargs)  # type: ignore[misc]

    cls.configure = configure  # type: ignore[assignment]
    cls.config = configure  # type: ignore[assignment]


def _patch(classes: Iterable[type]) -> None:
    for cls in classes:
        _wrap_init(cls)
        _wrap_configure(cls)


def enable_widget_integration() -> None:
    """Enable passing ``Signal`` directly to widget options.

    Patches common tk/ttk widget classes so that when you pass a ``Signal``
    instance to ``textvariable`` or ``variable`` in the constructor or in
    ``configure(...)``, it is automatically converted to its Tcl name.
    """

    ttk_classes: Tuple[type, ...] = (
        ttk.Entry,
        ttk.Label,
        ttk.Button,
        ttk.Checkbutton,
        ttk.Radiobutton,
        ttk.Combobox,
        ttk.Spinbox,
        ttk.Progressbar,
        ttk.Scale,
        ttk.OptionMenu,
    )

    tk_classes: Tuple[type, ...] = (
        tk.Entry,
        tk.Label,
        tk.Button,
        tk.Checkbutton,
        tk.Radiobutton,
    )

    _patch(ttk_classes)
    _patch(tk_classes)

