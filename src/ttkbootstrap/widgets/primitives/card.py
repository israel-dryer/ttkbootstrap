"""Card widget — a Frame with elevated card styling."""
from __future__ import annotations

from typing import Any, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.types import Master


class CardKwargs(TypedDict, total=False):
    """Keyword arguments for Card."""

    # Standard ttk.Frame options
    padding: Any
    width: int
    height: int
    style: str
    cursor: str
    name: str
    takefocus: bool
    class_: str

    # ttkbootstrap-specific extensions
    accent: str
    variant: str
    surface: str
    show_border: bool
    style_options: dict[str, Any]
    bootstyle: str  # DEPRECATED: Use accent and variant instead


class Card(Frame):
    """A convenience wrapper for Frame with card styling.

    Card is a Frame with `surface='card'` and `show_border=True` by default,
    providing an elevated container with a visible border for grouping content.

    Example:
        ```python
        card = ttk.Card(app, padding=20)
        ttk.Label(card, text="Card content").pack()
        ```

    """

    def __init__(self, master: Master = None, **kwargs: Unpack[CardKwargs]) -> None:
        """Create a themed Card container.

        Args:
            master: Parent widget. If None, uses the default root window.

        Other Parameters
        ----------------
            padding (int | tuple): Extra padding inside the card. Default 16.
            width (int): Requested width in pixels.
            height (int): Requested height in pixels.
            takefocus (bool): Widget accepts focus during keyboard traversal.
            style (str): Explicit ttk style name (overrides accent/variant).
            accent (str): Accent/color token for the card. Default 'card'.
            variant (str): Style variant (if applicable).
            surface (str): Surface token for the parent background.
            show_border (bool): Draw a border around the card. Default True.
            style_options (dict): Optional dict forwarded to the style builder.

        """
        if 'bootstyle' not in kwargs:
            kwargs.setdefault('accent', 'card')
        kwargs.setdefault('show_border', True)
        kwargs.setdefault('padding', 16)
        super().__init__(master, **kwargs)
