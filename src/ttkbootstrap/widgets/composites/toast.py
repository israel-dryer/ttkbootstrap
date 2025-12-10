from tkinter import Toplevel, Widget, Misc
from typing import Any, Callable, Literal, Optional, Sequence, Tuple, Union

from typing_extensions import TypedDict, Unpack

from ttkbootstrap.runtime.window_utilities import WindowPositioning, AnchorPoint


class IconSpec(TypedDict, total=False):
    """Icon configuration for toast."""
    name: str
    size: Optional[int]
    color: Optional[str]


class ToastConfig(TypedDict, total=False):
    """Configuration options for Toast widget."""
    title: Optional[str]
    icon: Union[str, IconSpec, None]
    message: Optional[str]
    memo: Optional[str]
    duration: Optional[int]
    buttons: Optional[Sequence[dict[str, Any]]]
    show_close_button: bool
    bootstyle: Optional[str]
    position: Optional[str]
    alert: bool
    on_dismissed: Optional[Callable[[Any], Any]]


class Toast:
    """A notification toast widget that displays temporary messages.

    Toast notifications appear in a small window, typically in the corner of the screen,
    and can display a title, message, icon, buttons, and optional metadata. They can be
    configured to auto-dismiss after a duration or remain visible until manually closed.
    """

    def __init__(
            self,
            *,
            title: Optional[str] = None,
            icon: Union[str, IconSpec, None] = None,
            message: Optional[str] = None,
            memo: Optional[str] = None,
            duration: Optional[int] = None,
            buttons: Optional[Sequence[dict[str, Any]]] = None,
            show_close_button: bool = True,
            bootstyle: Optional[str] = None,
            position: Optional[str] = None,
            alert: bool = False,
            on_dismissed: Optional[Callable[[Any], Any]] = None,
    ) -> None:
        """Initialize a Toast notification.

        Args:
            title: The toast title text. If provided without a message, it will be displayed
                with a larger "label" font. If both title and message are provided, the title
                appears in the header and the message appears in a separate section below.
            icon: Icon to display in the header. Can be a string icon name (e.g., "bootstrap-fill")
                or an IconSpec dict with name, size, and color properties.
            message: The main message text. If no title is provided, this message is displayed
                in the header with a "body" font. If a title is provided, this appears in a
                separate section below the header.
            memo: Small metadata text displayed in the header (e.g., "5 mins ago"). Appears
                with muted styling.
            duration: Auto-dismiss duration in milliseconds. If None, the toast remains visible
                until manually closed.
            buttons: Sequence of button configurations. Each dict can contain any ttkbootstrap
                button options (text, bootstyle, command, etc.). Button commands will trigger
                the on_dismissed callback before closing the toast.
            show_close_button: Whether to show the close button in the header. Default is True.
            bootstyle: The color theme for the toast container (e.g., "primary", "success",
                "danger"). If None, uses the default background color.
            position: Tkinter geometry string for toast position (e.g., "-25-75" for bottom-right).
                If None, uses platform-specific defaults.
            alert: If True, plays a system bell sound when the toast is shown.
            on_dismissed: Callback function invoked when the toast is dismissed. Receives the
                button options dict if dismissed via a button, or None if dismissed via close
                button or auto-dismiss.

        Examples:
            Simple toast with just a message::

                toast = Toast(message="Hello, world!")
                toast.show()

            Toast with title, message, and auto-dismiss::

                toast = Toast(
                    title="Success",
                    message="Your changes have been saved.",
                    duration=3000,
                    bootstyle="success"
                )
                toast.show()

            Toast with buttons and callback::

                def on_dismiss(data):
                    if data and data.get('text') == 'Confirm':
                        print("User confirmed!")

                toast = Toast(
                    title="Confirm Action",
                    message="Are you sure you want to continue?",
                    buttons=[
                        {"text": "Confirm", "bootstyle": "primary"},
                        {"text": "Cancel", "bootstyle": "secondary"}
                    ],
                    on_dismissed=on_dismiss
                )
                toast.show()
        """
        self._config_keys = {'title', 'icon', 'message', 'memo', 'duration', 'buttons', 'show_close_button',
                             'bootstyle', 'position', 'alert', 'on_dismissed'}

        # initialized configuration
        self._title = title
        self._icon = icon
        self._message = message
        self._memo = memo
        self._duration = duration
        self._buttons = buttons
        self._show_close_button = show_close_button
        self._bootstyle = bootstyle
        self._position = position
        self._alert = alert
        self._on_dismissed = on_dismissed

        # top level widget
        self._toplevel: Optional[Toplevel] = None

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a configuration option using dictionary syntax."""
        self.configure(**{key: value})

    def __getitem__(self, key: str) -> Any:
        """Get a configuration option using dictionary syntax."""
        return self.cget(key)

    def _handle_on_dismissed(self, data: Any = None) -> None:
        """Invoke the on_dismissed callback if configured."""
        if self._on_dismissed:
            self._on_dismissed(data)

    def configure(
            self,
            option: Optional[str] = None,
            **kwargs: Unpack[ToastConfig]
    ) -> Optional[tuple[str, str, str, None, Any]]:
        """Configure toast options.

        Args:
            option: If provided, returns the configuration for this option.
            **kwargs: Configuration options to set.

        Returns:
            If option is provided, returns a tuple of (option, option, option.capitalize(), None, value).
            Otherwise, returns None.
        """
        if option is not None:
            if option in self._config_keys:
                attr = f"_{option}"
                value = getattr(self, attr)
                # returns in the expected tkinter.configure format
                return option, option, option.capitalize(), None, value
            else:
                raise AttributeError(f"'{option}' is not a valid option")

        if kwargs:
            for key, value in kwargs.items():
                if key in self._config_keys:
                    attr = f"_{key}"
                    setattr(self, attr, value)
                else:
                    raise AttributeError(f"'{key}' is not a valid option")
        return None

    def cget(self, option: str) -> Any:
        """Get the value of a configuration option.

        Args:
            option: The configuration option name.

        Returns:
            The value of the configuration option.
        """
        if option in self._config_keys:
            attr = f"_{option}"
            return getattr(self, attr)
        else:
            raise AttributeError(f"'{option}' is not a valid option")

    def show(self, merge: bool = True, **options: Unpack[ToastConfig]) -> None:
        """Display the toast.

        If options are provided, they are merged with the existing toast configuration. If you do not want this
        behavior, set the merge flag to False, or create a new toast instance.

        Args:
            merge: If True, merge options with existing configuration. If False, clear existing options first.
            **options: Configuration options to set before showing.
        """
        if not merge:
            self._clear_options()

        self.configure(**options)
        self._build_toast()
        if self._toplevel:
            self._toplevel.deiconify()

    def _clear_options(self) -> None:
        """Clear all configuration options to their default values."""
        self._title = None
        self._icon = None
        self._message = None
        self._memo = None
        self._duration = None
        self._buttons = None
        self._show_close_button = True
        self._bootstyle = None
        self._position = None
        self._alert = False
        self._on_dismissed = None

    def hide(self) -> None:
        """Hide the toast and trigger the on_dismissed callback."""
        if self._toplevel:
            self._toplevel.destroy()
        self._handle_on_dismissed(None)

    def destroy(self) -> None:
        """Destroy the toast widget and cleanup resources."""
        if hasattr(self, '_toplevel') and self._toplevel:
            self._toplevel.destroy()
        self._toplevel = None

    def _build_toast(self) -> None:
        import ttkbootstrap as ttk
        # ----- Configuration Options -------

        has_title = self._title is not None
        has_title_and_message = has_title and self._message is not None
        resolved_title_font = "label" if has_title else "body"
        muted_foreground = "background[muted]" if self._bootstyle is None else f"{self._bootstyle}[muted]"

        # ------ Toplevel setup ------

        top = Toplevel()
        top.minsize(400, 30)
        top.attributes('-topmost', True)
        top.attributes('-alpha', 0.97)
        top.overrideredirect(True)
        top.withdraw()

        # ------ Toast Layout ------

        container = ttk.Frame(top, padding=4, bootstyle=self._bootstyle)
        container.pack(fill='both', expand=True)

        header = ttk.Frame(container, padding=(8, 0, 0, 0))
        header.pack(side='top', fill='x')

        # icon
        if self._icon:
            ttk.Label(header, icon=self._icon).pack(side='left', padx=(0, 8))

        # title
        ttk.Label(
            header,
            text=self._title if has_title else self._message,
            font=resolved_title_font,
            wraplength=380,
            justify='left',
        ).pack(side='left', fill='x')

        # close
        if self._show_close_button:
            ttk.Button(
                header,
                icon="x-lg",
                bootstyle=f"{muted_foreground}-text",
                style_options={"icon_only": True},
                command=self.hide
            ).pack(side='right')

        # memo
        if self._memo:
            ttk.Label(
                header,
                text=self._memo,
                font="caption",
                bootstyle=muted_foreground,
            ).pack(side='right', pady=8, padx=(0, 0 if self._show_close_button else 12))

        # message
        if has_title_and_message:
            ttk.Separator(container).pack(side='top', fill='x')
            ttk.Label(
                container,
                text=self._message,
                wraplength=400,
                justify='left'
            ).pack(side='top', fill='x', pady=8, padx=8)

        # buttons
        if self._buttons:
            def execute_command(options: dict[str, Any], fn: Optional[Callable[[], None]] = None) -> Callable[[], None]:
                def inner() -> None:
                    if fn:
                        fn()
                    self._handle_on_dismissed(options)
                    top.destroy()

                return inner

            ttk.Separator(container).pack(side='top', fill='x', pady=4)
            button_frame = ttk.Frame(container)
            button_frame.pack(side='top', fill='x')

            for i, button_options in enumerate(self._buttons):
                func = button_options.get('command', None)
                button_opts = {k: v for k, v in button_options.items() if k != 'command'}
                ttk.Button(
                    button_frame,
                    **button_opts,
                    command=execute_command(button_options, func)
                ).grid(column=i, row=0, sticky="ew")

        # ------ Positioning -------

        # Update layout to get final window size
        top.update_idletasks()

        # Apply positioning using WindowPositioning utilities
        if self._position:
            # Support legacy geometry strings (e.g., "-25-75")
            if self._position.startswith(('+', '-')):
                # Legacy geometry string - use directly
                top.geometry(self._position)
            else:
                # New positioning - assume it's a corner specification
                # (future enhancement: could support more complex positioning)
                top.geometry(self._position)
        else:
            # Default positioning based on platform
            winsys = top.tk.call('tk', 'windowingsystem')
            if winsys in ['win32', 'aqua']:
                # Bottom-right corner
                WindowPositioning.position_anchored(
                    window=top,
                    anchor_to="screen",
                    parent=None,
                    anchor_point="se",
                    window_point="se",
                    offset=(-25, -75),
                    auto_flip=False,
                    ensure_visible=True
                )
            else:
                # Top-right corner for X11
                WindowPositioning.position_anchored(
                    window=top,
                    anchor_to="screen",
                    parent=None,
                    anchor_point="ne",
                    window_point="ne",
                    offset=(-25, 25),
                    auto_flip=False,
                    ensure_visible=True
                )

        # ------ Other setup -------

        if self._duration:
            top.after(self._duration, self.hide)

        if self._alert:
            top.bell()

        self._toplevel = top

