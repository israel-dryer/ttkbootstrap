"""Shot factories for `docs/widgets/actions/button.md`.

Each factory packs a single row of Button variants directly into the
renderer-supplied `parent` Frame. Visual state flags (focus, hover) are
applied via the returned `finalize` callable so they survive WM focus
events that fire while the window is becoming visible.
"""

from __future__ import annotations

import tkinter
from typing import Callable

import ttkbootstrap as ttk


def _label_cell(parent: tkinter.Widget, text: str) -> None:
    ttk.Label(parent, font="label", text=text, width=10).pack(side="left")


def _row(parent: tkinter.Widget, label: str, *, bootstyle: str | None = None) -> Callable[[], None]:
    """Build a 4-button row (default/active/focus/disabled) and return its finalizer."""
    if label:
        _label_cell(parent, label)
    kwargs: dict = {}
    if bootstyle is not None:
        kwargs["bootstyle"] = bootstyle
    ttk.Button(parent, text="default", **kwargs).pack(side="left", padx=8)
    active = ttk.Button(parent, text="active", state="active", **kwargs)
    active.pack(side="left", padx=8)
    focus = ttk.Button(parent, text="focus", state="focus", **kwargs)
    focus.pack(side="left", padx=8)
    ttk.Button(parent, text="disabled", state="disabled", **kwargs).pack(side="left", padx=8)

    def finalize() -> None:
        active.state(["hover"])
        # Use real keyboard focus in addition to the state flag —
        # ttk styles draw the focus ring partly from actual WM focus,
        # and a raw `state(["focus"])` flag is not always honored by
        # the style engine on its own.
        focus.focus_set()
        focus.state(["focus"])

    return finalize


def solid(parent: tkinter.Widget) -> Callable[[], None]:
    return _row(parent, "Solid")


def outline(parent: tkinter.Widget) -> Callable[[], None]:
    return _row(parent, "Outline", bootstyle="outline")


def ghost(parent: tkinter.Widget) -> Callable[[], None]:
    return _row(parent, "Ghost", bootstyle="ghost")


def link(parent: tkinter.Widget) -> Callable[[], None]:
    return _row(parent, "Link", bootstyle="link")


def text(parent: tkinter.Widget) -> Callable[[], None]:
    return _row(parent, "Text", bootstyle="text")


def icons(parent: tkinter.Widget) -> None:
    ttk.Button(parent, text="Settings", icon="gear").pack(side="left", padx=8)
    ttk.Button(parent, icon="gear", icon_only=True).pack(side="left", padx=8)


def colors(parent: tkinter.Widget) -> None:
    for color in ["primary", "secondary", "success", "info", "warning", "danger", "light", "dark"]:
        ttk.Button(parent, text=color.title(), bootstyle=color).pack(side="left", padx=8)
