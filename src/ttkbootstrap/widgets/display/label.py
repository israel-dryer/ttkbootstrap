from tkinter import Misc, PhotoImage, StringVar
from tkinter.font import Font
from tkinter.ttk import Label as ttkLabel

from ..mixins import BackgroundMixin, BaseMixin, IconMixin, StyleMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower

try:
    from typing import Literal, Optional, Tuple, TypedDict, Union, Unpack
except ImportError:
    from typing_extensions import Unpack


# --- Typing Options ---

class LabelOptions(TypedDict, total=False):
    anchor: Literal['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']
    compound: Literal['left', 'right', 'top', 'bottom', 'center']
    cursor: str
    font: Union[str, Font]
    foreground: str
    background: str
    image: PhotoImage
    padding: str | tuple
    width: int
    justify: Literal['left', 'right', 'center']
    wrap_length: int


# --- Label Widget ---

class Label(StyleMixin, BaseMixin, IconMixin, BackgroundMixin):
    """
    A styled and theme-aware label widget based on `ttk.Label`.

    Args:
        master (Optional[Misc]): Parent widget.
        text (Optional[str]): The initial text displayed by the label.
        icon (Optional[str | Tuple[str, int]]): Optional icon name or (name, size) tuple.
        color (StyleColor): The style token for theming the label. Defaults to "default".
        variant (Literal["default", "inverse"]): The style variant. Defaults to "default".
        **kwargs (LabelOptions): Additional style and layout options.
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            text: Optional[str] = None,
            icon: Optional[str | Tuple[str, int]] = None,
            color: StyleColor = "default",
            variant: Literal["default", "inverse"] = "default",
            **kwargs: Unpack[LabelOptions]
    ):
        kw = dict(kwargs)
        self._master = master
        self._icon = icon
        self._color = color
        self._variant = variant
        self._kwargs = kw
        self._extras = {}
        self._text = text
        self._image: Optional[PhotoImage] = None
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
        self._bind_icon_events()
        self._prepare_icon_kwargs(default_compound="left")
        self._initialize_style(
            'label',
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

    # --- Icon/Image ---

    @property
    def image(self) -> Optional[PhotoImage]:
        """Return the associated image if set via icon mixin."""
        return self._image

    @property
    def compound(self):
        """How to display the image and text (left, right, top, bottom, center)."""
        return self.widget.cget('compound')

    @compound.setter
    def compound(self, value: Literal['left', 'right', 'top', 'bottom', 'center']):
        self.widget.configure(compound=value)

    # --- Layout and Spacing ---

    @property
    def width(self) -> int:
        """Width of the label in text units (characters)."""
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
        """Positioning of the content inside the label."""
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
    def foreground(self):
        """Text (foreground) color."""
        return self.widget.cget('foreground')

    @foreground.setter
    def foreground(self, value):
        self.widget.configure(foreground=value)

    @property
    def background(self):
        """Background color of the widget."""
        return self.widget.cget('background')

    @background.setter
    def background(self, value):
        self.widget.configure(background=value)

    @property
    def cursor(self) -> str:
        """Mouse cursor used when hovering over the label."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)
