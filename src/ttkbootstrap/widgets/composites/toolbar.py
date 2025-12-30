"""Toolbar widget with customizable content and optional window controls."""

from __future__ import annotations

from tkinter import Widget
from typing import Any, Callable, Literal

from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.separator import Separator
from ttkbootstrap.widgets.types import Master


class Toolbar(Frame):
    """A horizontal toolbar with customizable content and optional window controls.

    Toolbar provides a container for icon buttons, labels, and other widgets
    arranged horizontally. It optionally supports window control buttons
    (minimize, maximize, close) and window dragging for custom titlebars.

    Items are added from left to right. Use ``add_spacer()`` to push
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
        padding: int | tuple = 4,
        **kwargs: Any
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
            padding (int | tuple): Toolbar padding. Default 4.
            **kwargs: Additional arguments passed to Frame.
        """
        super().__init__(master, padding=padding, **kwargs)

        self._show_window_controls = show_window_controls
        self._draggable = draggable
        self._button_variant = button_variant

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

        if draggable:
            self._setup_drag()

    def _build_window_controls(self):
        """Build window control buttons (minimize, maximize, close)."""
        self._controls_frame = Frame(self)
        self._controls_frame.pack(side='right', fill='y')

        # Minimize button
        self._minimize_btn = Button(
            self._controls_frame,
            icon={'name': 'dash', 'size': 14},
            icon_only=True,
            variant='ghost',
            command=self._on_minimize,
        )
        self._minimize_btn.pack(side='left', padx=2)

        # Maximize/Restore button
        self._maximize_btn = Button(
            self._controls_frame,
            icon={'name': 'square', 'size': 12},
            icon_only=True,
            variant='ghost',
            command=self._on_maximize,
        )
        self._maximize_btn.pack(side='left', padx=2)

        # Close button
        self._close_btn = Button(
            self._controls_frame,
            icon={'name': 'x-lg', 'size': 14},
            icon_only=True,
            color='danger',
            variant='ghost',
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
            self._maximize_btn.configure(icon={'name': 'square', 'size': 12})
        else:
            window.state('zoomed')
            self._maximize_btn.configure(icon={'name': 'copy', 'size': 12})

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
        color: str = None,
        variant: str = None,
        **kwargs
    ) -> Button:
        """Add a button to the toolbar.

        Args:
            icon (str | dict | None): Icon name or configuration.
            text (str | None): Button text. If None and icon provided,
                creates icon-only button.
            command (Callable | None): Button click callback.
            color (str | None): Button color token.
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
            color=color,
            variant=variant or self._button_variant,
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
            **kwargs
        )
        lbl.pack(side='left', padx=4)

        # Make label draggable too if toolbar is draggable
        if self._draggable:
            lbl.bind('<Button-1>', self._on_drag_start, add='+')
            lbl.bind('<B1-Motion>', self._on_drag_motion, add='+')

        return lbl

    def add_separator(self, **kwargs) -> Separator:
        """Add a vertical separator to the toolbar.

        Args:
            **kwargs: Additional arguments passed to Separator.

        Returns:
            Separator: The created separator.
        """
        sep = Separator(
            self._content_frame,
            orient='vertical',
            **kwargs
        )
        sep.pack(side='left', fill='y', padx=8, pady=4)
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
        as its parent. Use ``toolbar.content`` to get the parent frame.

        Args:
            widget (Widget): The widget to add.
            **pack_kwargs: Arguments passed to pack(). Defaults to side='left'.

        Returns:
            Widget: The added widget.
        """
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