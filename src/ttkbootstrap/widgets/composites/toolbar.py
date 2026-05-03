"""Toolbar widget with customizable content and optional window controls."""

from __future__ import annotations

from tkinter import Widget
from typing import Any, Callable, Literal

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master


class ToolbarKwargs(TypedDict, total=False):
    """Keyword arguments for Toolbar."""

    show_window_controls: bool
    draggable: bool
    button_variant: str
    density: Literal['default', 'compact']
    padding: Any
    # Frame options
    width: int
    height: int
    surface: str
    show_border: bool


class Toolbar(Frame):
    """A horizontal toolbar with customizable content and optional window controls.

    Toolbar provides a container for icon buttons, labels, and other widgets
    arranged horizontally. It optionally supports window control buttons
    (minimize, maximize, close) and window dragging for custom titlebars.

    Items are added from left to right. Use `add_spacer()` to push
    subsequent items to the right side.

    Example:
        ```python
        # Basic toolbar with buttons
        toolbar = Toolbar(root)
        toolbar.add_button(icon='list', command=toggle_menu)
        toolbar.add_separator()
        toolbar.add_label(text='My App')
        toolbar.add_spacer()
        toolbar.add_button(icon='gear', command=settings)

        # Custom titlebar with window controls
        toolbar = Toolbar(
            root,
            show_window_controls=True,
            draggable=True,
        )
        toolbar.add_label(text='My App', font='heading-md')
        ```

    """

    def __init__(
        self,
        master: Master = None,
        show_window_controls: bool = False,
        draggable: bool = False,
        button_variant: str = 'ghost',
        density: Literal['default', 'compact'] = 'default',
        padding: int | tuple = None,
        **kwargs: Unpack[ToolbarKwargs]
    ):
        """Initialize a Toolbar.

        Args:
            master (Master | None): Parent widget.
            show_window_controls (bool): Show minimize/maximize/close buttons.
                Default False.
            draggable (bool): Enable window dragging by clicking and dragging
                the toolbar. Default False.
            button_variant (str): Default variant for toolbar buttons.
                Default 'ghost'.
            density (str): Button density for toolbar items. 'compact' for
                smaller buttons, 'default' for standard size. Default 'default'.
            padding (int | tuple): Toolbar padding. If None, uses density-based
                default ((3, 1) for compact, 3 for default).
            **kwargs: Additional arguments passed to Frame.

        """
        if padding is None:
            padding = (3, 1) if density == 'compact' else 3
        super().__init__(master, padding=padding, **kwargs)

        self._show_window_controls = show_window_controls
        self._draggable = draggable or show_window_controls  # Auto-enable drag with window controls
        self._button_variant = button_variant
        self._density = density

        # Content container (left side)
        self._content_frame = Frame(self)
        self._content_frame.pack(side='left', fill='both', expand=True)

        # Window controls container (right side)
        self._controls_frame: Frame | None = None
        if show_window_controls:
            self._build_window_controls()

        # Drag state
        self._drag_start_x = 0
        self._drag_start_y = 0

        if self._draggable:
            self._setup_drag()

    def _build_window_controls(self):
        """Build window control buttons (minimize, maximize, close)."""
        self._controls_frame = Frame(self)
        self._controls_frame.pack(side='right', fill='y')

        # Minimize button
        self._minimize_btn = Button(
            self._controls_frame,
            icon='dash-lg',
            icon_only=True,
            variant='ghost',
            density='compact',
            surface=self._surface,
            command=self._on_minimize,
        )
        self._minimize_btn.pack(side='left', padx=2)

        # Maximize/Restore button
        self._maximize_btn = Button(
            self._controls_frame,
            icon='app',
            icon_only=True,
            variant='ghost',
            density='compact',
            surface=self._surface,
            command=self._on_maximize,
        )
        self._maximize_btn.pack(side='left', padx=2)

        # Close button
        self._close_btn = Button(
            self._controls_frame,
            icon='x-lg',
            icon_only=True,
            variant='ghost',
            density='compact',
            surface=self._surface,
            command=self._on_close,
        )
        self._close_btn.pack(side='left', padx=2)

    def _on_minimize(self):
        """Handle minimize button click."""
        window = self.winfo_toplevel()
        window.iconify()

    def _on_maximize(self):
        """Handle maximize/restore button click."""
        window = self.winfo_toplevel()
        # Check current state and toggle
        if window.state() == 'zoomed':
            window.state('normal')
            self._maximize_btn.configure(icon='app')
        else:
            window.state('zoomed')
            self._maximize_btn.configure(icon='copy')

    def _on_close(self):
        """Handle close button click."""
        window = self.winfo_toplevel()
        window.destroy()

    def _setup_drag(self):
        """Set up window dragging bindings."""
        self.bind('<Button-1>', self._on_drag_start, add='+')
        self.bind('<B1-Motion>', self._on_drag_motion, add='+')
        self._content_frame.bind('<Button-1>', self._on_drag_start, add='+')
        self._content_frame.bind('<B1-Motion>', self._on_drag_motion, add='+')

    def _on_drag_start(self, event):
        """Record drag start position."""
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def _on_drag_motion(self, event):
        """Handle drag motion to move window."""
        window = self.winfo_toplevel()

        # Calculate delta
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y

        # Get current position
        x = window.winfo_x() + dx
        y = window.winfo_y() + dy

        # Move window
        window.geometry(f'+{x}+{y}')

        # Update drag start for next motion
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    # --- Public API: Adding Items ---

    def add_button(
        self,
        icon: str | dict = None,
        text: str = None,
        command: Callable = None,
        accent: str = None,
        variant: str = None,
        **kwargs
    ) -> Button:
        """Add a button to the toolbar.

        Args:
            icon (str | dict | None): Icon name or configuration.
            text (str | None): Button text. If None and icon provided,
                creates icon-only button.
            command (Callable | None): Button click callback.
            accent (str | None): Button accent token.
            variant (str | None): Button variant. Uses toolbar default if None.
            **kwargs: Additional arguments passed to Button.

        Returns:
            Button: The created button.

        """
        btn = Button(
            self._content_frame,
            icon=icon,
            text=text,
            icon_only=(icon is not None and text is None),
            command=command,
            accent=accent,
            variant=variant or self._button_variant,
            density=kwargs.pop('density', self._density),
            surface=kwargs.pop('surface', self._surface),
            **kwargs
        )
        btn.pack(side='left')
        return btn

    def add_label(
        self,
        text: str = '',
        icon: str | dict = None,
        font: str = None,
        **kwargs
    ) -> Label:
        """Add a label to the toolbar.

        Args:
            text (str): Label text.
            icon (str | dict | None): Optional icon.
            font (str | None): Font specification.
            **kwargs: Additional arguments passed to Label.

        Returns:
            Label: The created label.

        """
        lbl = Label(
            self._content_frame,
            text=text,
            icon=icon,
            font=font,
            surface=kwargs.pop('surface', self._surface),
            **kwargs
        )
        lbl.pack(side='left', padx=4)

        # Make label draggable too if toolbar is draggable
        if self._draggable:
            lbl.bind('<Button-1>', self._on_drag_start, add='+')
            lbl.bind('<B1-Motion>', self._on_drag_motion, add='+')

        return lbl

    def add_separator(self, length: int = 16, **kwargs) -> Separator:
        """Add a vertical separator to the toolbar.

        Args:
            length (int | None): Fixed length in pixels. If None, stretches
                to fill the toolbar height.
            **kwargs: Additional arguments passed to Separator.

        Returns:
            Separator: The created separator.

        """
        sep = Separator(
            self._content_frame,
            orient='vertical',
            length=length,
            **kwargs
        )
        # Only fill='y' if no fixed length specified
        if length:
            sep.pack(side='left', padx=4)
        else:
            sep.pack(side='left', fill='y', padx=4)
        return sep

    def add_spacer(self) -> Frame:
        """Add a flexible spacer that pushes subsequent items to the right.

        Returns:
            Frame: The spacer frame.

        """
        spacer = Frame(self._content_frame)
        spacer.pack(side='left', fill='both', expand=True)

        # Make spacer draggable too
        if self._draggable:
            spacer.bind('<Button-1>', self._on_drag_start, add='+')
            spacer.bind('<B1-Motion>', self._on_drag_motion, add='+')

        return spacer

    def add_widget(self, widget: Widget, **pack_kwargs) -> Widget:
        """Add a custom widget to the toolbar.

        The widget must already be created with the toolbar's content frame
        as its parent. Use `toolbar.content` to get the parent frame.

        Args:
            widget (Widget): The widget to add.
            **pack_kwargs: Arguments passed to pack(). Defaults to side='left'.

        Returns:
            Widget: The added widget.

        """
        if widget.master is not self._content_frame:
            raise ValueError(
                f"widget must be parented to toolbar.content, not {widget.master!r}. "
                "Create the widget with `toolbar.content` as its parent."
            )
        pack_kwargs.setdefault('side', 'left')
        pack_kwargs.setdefault('padx', 2)
        widget.pack(**pack_kwargs)
        return widget

    # --- Properties ---

    @property
    def content(self) -> Frame:
        """Get the content frame for adding custom widgets."""
        return self._content_frame

    @property
    def show_window_controls(self) -> bool:
        """Check if window controls are shown."""
        return self._show_window_controls

    @property
    def draggable(self) -> bool:
        """Check if toolbar is draggable."""
        return self._draggable

    @property
    def density(self) -> str:
        """Get the toolbar's button density."""
        return self._density

    # --- Window Control Access ---

    @property
    def minimize_button(self) -> Button | None:
        """Get the minimize button (if window controls are shown)."""
        return getattr(self, '_minimize_btn', None)

    @property
    def maximize_button(self) -> Button | None:
        """Get the maximize button (if window controls are shown)."""
        return getattr(self, '_maximize_btn', None)

    @property
    def close_button(self) -> Button | None:
        """Get the close button (if window controls are shown)."""
        return getattr(self, '_close_btn', None)

    # --- Configuration Delegates ---

    @configure_delegate('density')
    def _delegate_density(self, value: str = None):
        """Configure the toolbar's default button density."""
        if value is None:
            return self._density
        self._density = value
        return None

    @configure_delegate('button_variant')
    def _delegate_button_variant(self, value: str = None):
        """Configure the toolbar's default button variant."""
        if value is None:
            return self._button_variant
        self._button_variant = value
        return None