from tkinter import Misc, StringVar
from tkinter.font import Font
from tkinter.ttk import Label as ttkLabel

from ..mixins import BackgroundMixin, BaseMixin, StyleMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower

try:
    from typing import Literal, Optional, Tuple, TypedDict, Union, Unpack
except ImportError:
    from typing_extensions import Unpack


# --- Typing Options ---

class BadgeOptions(TypedDict, total=False):
    anchor: Literal['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']
    cursor: str
    font: Union[str, Font]
    padding: str | tuple
    width: int
    justify: Literal['left', 'right', 'center']
    wrap_length: int


# --- Badge Widget ---

class Badge(StyleMixin, BaseMixin, BackgroundMixin):
    """
    A styled and theme-aware badge widget based on `ttk.Label`.

    Args:
        master (Optional[Misc]): Parent widget.
        text (Optional[str]): The initial text displayed by the label.
        color (StyleColor): The style token for theming the label. Defaults to "default".
        variant (Literal["default", "circle", "pill"]): The style variant. Defaults to "default".
        **kwargs (BadgeOptions): Additional style and layout options.
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        color: StyleColor = "default",
        variant: Literal["default", "circle", "pill"] = "default",
        **kwargs: Unpack[BadgeOptions]
    ):
        kw = dict(kwargs)
        self._master = master
        self._color = color
        self._variant = variant
        self._kwargs = kw
        self._extras = {}
        self._text = text
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = StringVar(master, text)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Label widget."""
        self._widget: "ttkLabel" = ttkLabel(
            self._master,
            textvariable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._initialize_style(
            'badge',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    # --- Core Access ---

    @property
    def widget(self) -> "ttkLabel":
        """Return the internal ttk widget."""
        return self._widget

    @property
    def variable(self) -> StringVar:
        """Return the StringVar linked to the widget text."""
        return self._variable

    # --- Text Properties ---

    @property
    def text(self) -> str:
        """Get or set the label text."""
        return self.variable.get()

    @text.setter
    def text(self, value: str):
        self.variable.set(value)

    @property
    def justify(self):
        """How multiple lines of text are laid out relative to one another."""
        return self.widget.cget('justify')

    @justify.setter
    def justify(self, value: Literal['left', 'center', 'right']):
        self.widget.configure(justify=value)

    @property
    def wrap_length(self) -> int:
        """Maximum line length in pixels before text wraps. 0 disables wrapping."""
        return self.widget.cget('wraplength')

    @wrap_length.setter
    def wrap_length(self, value: int):
        self.widget.configure(wraplength=value)

    # --- Layout and Spacing ---

    @property
    def width(self) -> int:
        """Width of the badge in text units (characters)."""
        return self.widget.cget('width')

    @width.setter
    def width(self, value: int):
        self.widget.configure(width=value)

    @property
    def padding(self):
        """Internal padding for the widget (left, top, right, bottom)."""
        return self.widget.cget('padding')

    @padding.setter
    def padding(self, value: str | tuple):
        self.widget.configure(padding=value)

    @property
    def anchor(self):
        """Positioning of the content inside the badge."""
        return self.widget.cget('anchor')

    @anchor.setter
    def anchor(self, value: Literal['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']):
        self.widget.configure(anchor=value)

    # --- Appearance ---

    @property
    def font(self):
        """Font used to display the text."""
        return self.widget.cget('font')

    @font.setter
    def font(self, value: Union[str, Font]):
        self.widget.configure(font=value)

    @property
    def cursor(self) -> str:
        """Mouse cursor used when hovering over the badge."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)
