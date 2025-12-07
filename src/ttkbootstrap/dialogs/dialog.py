"""Core dialog base class for ttkbootstrap dialogs.

This module provides the base `Dialog` class using a builder pattern
for creating flexible, customizable dialogs.

The Dialog class uses a composition-based approach with callback builders
for content and footer, making it easy to create custom dialogs without
requiring inheritance.

Basic Usage
-----------
Create a simple dialog with custom content:

    >>> import ttkbootstrap as ttk
    >>> from ttkbootstrap.dialogs import Dialog, DialogButton
    >>>
    >>> def build_content(parent):
    ...     ttk.Label(parent, text="Hello, World!").pack(pady=20)
    >>>
    >>> dialog = Dialog(
    ...     title="My Dialog",
    ...     content_builder=build_content,
    ...     buttons=[
    ...         DialogButton(text="Cancel", role="cancel", result=None),
    ...         DialogButton(text="OK", role="primary", result="ok", default=True)
    ...     ]
    ... )
    >>> dialog.show()
    >>> print(dialog.result)  # "ok" or None

Custom Positioning
------------------
Control where the dialog appears on screen:

    >>> # Show at specific coordinates
    >>> dialog.show(position=(100, 100))
    >>>
    >>> # Show centered on parent (default)
    >>> dialog.show()

Custom Footer
-------------
Replace standard buttons with custom footer widgets:

    >>> def build_footer(parent):
    ...     ttk.Button(parent, text="Help").pack(side="left")
    ...     ttk.Button(parent, text="OK").pack(side="right")
    >>>
    >>> dialog = Dialog(
    ...     title="Custom Footer",
    ...     content_builder=build_content,
    ...     footer_builder=build_footer  # Replaces standard buttons
    ... )

Dialog Modes
------------
- **modal**: Blocks interaction with parent window (default)
- **popover**: Closes when focus leaves the dialog

    >>> dialog = Dialog(mode="popover", ...)
    >>> dialog.show()  # Closes automatically when clicking outside

Button Roles
------------
Buttons are styled based on their role:
- **primary**: Main action button (blue)
- **secondary**: Standard button (gray)
- **danger**: Destructive action (red)
- **cancel**: Cancel button (outline gray)
- **help**: Help/info button (link style)

Types
-----
ContentBuilder : Callable[[Widget], None]
    Callback function that builds dialog content.
    Receives the content frame as parameter.

FooterBuilder : Callable[[Widget], None]
    Callback function that builds custom footer.
    Receives the footer frame as parameter.

ButtonRole : Literal["primary", "secondary", "danger", "cancel", "help"]
    Role determining button appearance and behavior.

DialogMode : Literal["modal", "popover"]
    Dialog interaction mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Widget
from typing import Any, Callable, Iterable, Literal, Mapping, Optional, Union

import ttkbootstrap as ttk

# --- Types -----------------------------------------------------------------

ContentBuilder = Callable[[Widget], None]
FooterBuilder = Callable[[Widget], None]

ButtonRole = Literal["primary", "secondary", "danger", "cancel", "help"]
DialogMode = Literal["modal", "popover"]


@dataclass
class DialogButton:
    """Specification for a dialog button.

    Attributes:
        text: Button label text displayed to the user.
        role: Button role determining styling and behavior.
            - "primary": Main action (blue, triggered by Enter)
            - "secondary": Standard action (gray)
            - "danger": Destructive action (red)
            - "cancel": Cancel action (outline, triggered by Escape)
            - "help": Help/info action (link style)
        result: Value assigned to dialog.result when button is clicked.
            If None, dialog.result is not set. Defaults to None.
        closes: Whether button closes the dialog when clicked.
            Defaults to True.
        default: Whether this is the default button (focused and triggered by Enter).
            Only one button should be marked as default. Defaults to False.
        command: Optional callback function called when button is clicked.
            Receives the Dialog instance as parameter. Called before setting result
            and before closing the dialog. Defaults to None.
        bootstyle: Optional ttkbootstrap style override.
            If None, style is determined by role. Defaults to None.
        icon: Optional icon specification passed to ttk.Button.
            Can be icon name string or dict with icon parameters.
            Defaults to None.

    Example:
        >>> # Simple button
        >>> btn = DialogButton(text="OK", role="primary", result="ok")
        >>>
        >>> # Button with custom command
        >>> def on_save(dialog):
        ...     print("Saving...")
        >>> btn = DialogButton(
        ...     text="Save",
        ...     role="primary",
        ...     result="saved",
        ...     command=on_save
        ... )
        >>>
        >>> # Button that doesn't close dialog
        >>> btn = DialogButton(
        ...     text="Apply",
        ...     role="secondary",
        ...     closes=False,  # Dialog stays open
        ...     command=lambda dlg: print("Applied!")
        ... )
    """
    text: str
    role: ButtonRole = "secondary"
    result: Any | None = None  # value assigned to dialog.result
    closes: bool = True  # close dialog after click
    default: bool = False  # default button (Enter)
    command: Callable[[Dialog], None] | None = None
    bootstyle: str | None = None  # override style
    icon: str | dict[str, Any] | None = None  # passed straight to ttk.Button(icon=...)


ButtonSpec = Union[DialogButton, Mapping[str, Any]]


# --- Dialog ----------------------------------------------------------------

class Dialog:
    """A flexible dialog window using the builder pattern.

    Dialog provides a composition-based approach to creating modal and non-modal
    dialogs with customizable content, buttons, and behavior. Instead of requiring
    inheritance, you provide callback functions to build the dialog content and
    optionally the footer.

    The dialog manages window creation, positioning, button handling, and keyboard
    shortcuts automatically.

    Attributes:
        result: The value returned by the dialog after closing.
            Set automatically when a button with a result value is clicked.
            Defaults to None.

    Args:
        master: Parent widget for the dialog. If None, uses the default root window.
        title: Dialog window title displayed in the title bar.
            Defaults to "ttkbootstrap".
        content_builder: Optional callback function to build dialog content.
            Receives a Frame widget as parameter. Should pack/grid widgets into it.
            If None, dialog will have no content area. Defaults to None.
        footer_builder: Optional callback function to build custom footer.
            Receives a Frame widget as parameter. If provided, replaces the
            standard button footer. Defaults to None.
        buttons: Optional list of DialogButton or dict specifications for footer buttons.
            Ignored if footer_builder is provided. Button order in list determines
            right-to-left display order (first button appears rightmost).
            Defaults to None (no footer).
        minsize: Optional (width, height) minimum window size in pixels.
            Defaults to None (no minimum).
        maxsize: Optional (width, height) maximum window size in pixels.
            Defaults to None (no maximum).
        resizable: Optional (width, height) tuple of booleans controlling window resize.
            (True, True) allows full resizing, (False, False) prevents all resizing.
            Defaults to (False, False).
        alert: If True, plays system alert sound when dialog is shown.
            Defaults to False.
        mode: Dialog interaction mode.
            - "modal": Blocks parent window interaction, requires user response
            - "popover": Closes automatically when focus leaves dialog
            Defaults to "modal".
        frameless: If True, removes window decorations (title bar, borders) and adds
            a solid border frame around the dialog content. Useful for dropdown-style
            menus or popover UIs. Defaults to False.

    Example:
        Simple confirmation dialog:

        >>> def build_message(parent):
        ...     ttk.Label(parent, text="Are you sure?").pack(pady=20, padx=20)
        >>>
        >>> dialog = Dialog(
        ...     title="Confirm Action",
        ...     content_builder=build_message,
        ...     buttons=[
        ...         DialogButton(text="Cancel", role="cancel", result=False),
        ...         DialogButton(text="Confirm", role="danger", result=True, default=True)
        ...     ],
        ...     alert=True
        ... )
        >>> dialog.show()
        >>> if dialog.result:
        ...     print("User confirmed!")

        Dialog with form input:

        >>> def build_form(parent):
        ...     ttk.Label(parent, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        ...     entry = ttk.Entry(parent)
        ...     entry.grid(row=0, column=1, padx=10, pady=5)
        ...     parent.entry = entry  # Store reference
        >>>
        >>> def on_ok(dialog):
        ...     dialog.result = dialog._content.entry.get()
        >>>
        >>> dialog = Dialog(
        ...     title="Enter Name",
        ...     content_builder=build_form,
        ...     buttons=[
        ...         DialogButton(text="Cancel", role="cancel"),
        ...         DialogButton(text="OK", role="primary", command=on_ok, default=True)
        ...     ]
        ... )
        >>> dialog.show(position=(200, 200))
        >>> print(f"Name entered: {dialog.result}")

        Popover tooltip dialog:

        >>> def build_help(parent):
        ...     ttk.Label(
        ...         parent,
        ...         text="Click outside to close",
        ...         wraplength=200
        ...     ).pack(padx=15, pady=15)
        >>>
        >>> dialog = Dialog(
        ...     title="Help",
        ...     content_builder=build_help,
        ...     mode="popover",  # Closes when clicking outside
        ...     minsize=(250, 100)
        ... )
        >>> dialog.show(position=(100, 100), modal=False)
    """
    def __init__(
            self,
            master=None,
            title: str = "ttkbootstrap",
            content_builder: Optional[ContentBuilder] = None,
            footer_builder: Optional[FooterBuilder] = None,
            *,
            buttons: Iterable[ButtonSpec] | None = None,
            minsize: tuple[int, int] | None = None,
            maxsize: tuple[int, int] | None = None,
            resizable: tuple[bool, bool] | None = (False, False),
            alert: bool = False,
            mode: DialogMode = "modal",
            frameless: bool = False,
    ):
        import tkinter
        self._master = master if master else tkinter._default_root
        self._title = title
        self._content_builder = content_builder
        self._footer_builder = footer_builder
        self._buttons: list[DialogButton] = self._normalize_buttons(buttons)

        self._minsize = minsize
        self._maxsize = maxsize
        self._resizable = resizable
        self._alert = alert
        self._mode = mode
        self._frameless = frameless

        self._toplevel: ttk.Toplevel | None = None
        self._content: ttk.Frame | None = None
        self._footer: ttk.Frame | None = None
        self._border_frame: ttk.Frame | None = None

        self.result: Any = None

    # --------------------------------------------------------------- API

    def show(self, position: Optional[tuple[int, int]] = None, modal: Optional[bool] = None):
        """Create and show the dialog.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
                If None, the dialog will be centered on the parent.
            modal: Override the mode's default modality.
                - If None, uses mode:
                    - "modal": grab_set + wait_window
                    - "popover": no grab, but wait_window
        """
        if modal is None:
            modal = (self._mode == "modal")

        self.result = None
        self._create_toplevel()
        self._build_footer()
        self._build_content()
        self._position_dialog(position)

        if self._alert:
            self._toplevel.bell()

        if self._mode == "popover":
            self._toplevel.bind("<FocusOut>", self._on_focus_out, add="+")

        if modal:
            self._toplevel.transient(self._master)
            if self._mode == "modal":
                self._toplevel.grab_set()
            self._master.wait_window(self._toplevel)

    def show_centered(self, modal: Optional[bool] = None):
        """Show the dialog centered on its parent using default positioning."""
        self.show(position=None, modal=modal)

    @property
    def toplevel(self) -> ttk.Toplevel | None:
        """Read-only access to the underlying toplevel window."""
        return self._toplevel

    # --------------------------------------------------------------- Internals

    def _normalize_buttons(
            self,
            buttons: Iterable[ButtonSpec] | None,
    ) -> list[DialogButton]:
        if not buttons:
            return []

        normalized: list[DialogButton] = []
        for b in buttons:
            if isinstance(b, DialogButton):
                normalized.append(b)
            else:
                # assume mapping/dict
                try:
                    normalized.append(DialogButton(**b))  # type: ignore[arg-type]
                except TypeError as exc:
                    raise ValueError(
                        f"Invalid button mapping {b!r}: {exc}"
                    ) from exc
        return normalized

    def _create_toplevel(self):
        self._toplevel = ttk.Toplevel(self._master)
        self._toplevel.title(self._title)
        self._toplevel.protocol("WM_DELETE_WINDOW", self._on_close_request)

        try:
            self._toplevel.withdraw()
        except Exception:
            pass

        if self._minsize:
            self._toplevel.minsize(*self._minsize)
        if self._maxsize:
            self._toplevel.maxsize(*self._maxsize)
        if self._resizable is not None:
            self._toplevel.resizable(*self._resizable)

        if self._frameless:
            self._toplevel.overrideredirect(True)
            self._border_frame = ttk.Frame(self._toplevel, show_border=True, padding=2)
            self._border_frame.pack(fill='both', expand=True)

    def _build_content(self):
        parent = self._border_frame if self._frameless else self._toplevel
        padding = 2 if self._frameless else 0
        self._content = ttk.Frame(parent, padding=padding)

        if self._frameless:
            self._content.pack(fill="both", side="top", expand=False)
        else:
            self._content.pack(fill="both", side="top", expand=True)

        if self._content_builder:
            self._content_builder(self._content)

    def _build_footer(self):
        parent = self._border_frame if self._frameless else self._toplevel
        footer_padding = 6 if self._frameless else 4

        if self._footer_builder:
            self._footer = ttk.Frame(parent, padding=footer_padding)
            self._footer.pack(side="bottom", fill="x")
            ttk.Separator(parent, orient="horizontal").pack(side="bottom", fill="x")
            self._footer_builder(self._footer)
            return

        if not self._buttons:
            return

        self._footer = ttk.Frame(parent, padding=footer_padding)
        self._footer.pack(side="bottom", fill="x")
        ttk.Separator(parent, orient="horizontal").pack(side="bottom", fill="x")

        self._create_standard_buttons(self._footer)

    def _create_standard_buttons(self, parent: Widget):
        """Create standardized footer buttons from self._buttons.

        Buttons are packed right-to-left so first button appears rightmost.
        """
        default_button: ttk.Button | None = None
        cancel_button: ttk.Button | None = None

        for spec in reversed(self._buttons):
            style = spec.bootstyle or self._style_for_role(spec.role)

            def make_command(s: DialogButton):
                def cmd():
                    if s.command:
                        s.command(self)
                    if s.result is not None:
                        self.result = s.result
                    if s.closes and self._toplevel:
                        self._toplevel.destroy()

                return cmd

            btn = ttk.Button(
                parent,
                text=spec.text,
                bootstyle=style,
                command=make_command(spec),
                icon=spec.icon,
                compound="left" if spec.icon else "text",
            )
            btn.pack(side="right", padx=(4, 0))

            if spec.default and default_button is None:
                default_button = btn
            if spec.role == "cancel" and cancel_button is None:
                cancel_button = btn

        if self._toplevel is None:
            return

        if default_button is not None:
            default_button.focus_set()
            self._toplevel.bind("<Return>", lambda e, b=default_button: b.invoke())

        if cancel_button is not None:
            self._toplevel.bind("<Escape>", lambda e, b=cancel_button: b.invoke())
        else:
            self._toplevel.bind("<Escape>", lambda e: self._toplevel.destroy())

    def _position_dialog(self, position: Optional[tuple[int, int]]) -> None:
        """Position the dialog window.

        Args:
            position: Optional (x, y) coordinates. If None, centers on parent.
        """
        if not self._toplevel:
            return

        self._toplevel.update_idletasks()

        if position is not None:
            try:
                x, y = position
                x, y = self._ensure_on_screen(int(x), int(y))
                self._toplevel.geometry(f"+{x}+{y}")
            except (TypeError, ValueError):
                self._center_on_parent()
        else:
            self._center_on_parent()

        self._toplevel.update_idletasks()

        try:
            self._toplevel.deiconify()
        except Exception:
            pass

        if position is None:
            try:
                self._center_on_parent()
            except Exception:
                pass

    def _ensure_on_screen(self, x: int, y: int) -> tuple[int, int]:
        """Ensure dialog position keeps it fully visible on screen.

        Args:
            x: Desired x coordinate
            y: Desired y coordinate

        Returns:
            Adjusted (x, y) coordinates that keep dialog on screen
        """
        if not self._toplevel:
            return x, y

        dialog_width = self._toplevel.winfo_reqwidth()
        dialog_height = self._toplevel.winfo_reqheight()

        screen_x0 = self._toplevel.winfo_vrootx()
        screen_y0 = self._toplevel.winfo_vrooty()
        screen_width = self._toplevel.winfo_vrootwidth()
        screen_height = self._toplevel.winfo_vrootheight()
        screen_x1 = screen_x0 + screen_width
        screen_y1 = screen_y0 + screen_height

        x = min(x, screen_x1 - dialog_width - 20)
        y = min(y, screen_y1 - dialog_height - 60)
        x = max(screen_x0 + 20, x)
        y = max(screen_y0 + 20, y)

        return int(x), int(y)

    def _center_on_parent(self) -> None:
        """Center the dialog on its parent window."""
        if not self._toplevel or not self._master:
            return

        try:
            self._master.update_idletasks()
            self._toplevel.update_idletasks()
        except Exception:
            pass

        dialog_width = max(self._toplevel.winfo_reqwidth(), self._toplevel.winfo_width())
        dialog_height = max(self._toplevel.winfo_reqheight(), self._toplevel.winfo_height())

        parent_x = self._master.winfo_rootx()
        parent_y = self._master.winfo_rooty()
        parent_width = max(self._master.winfo_width(), self._master.winfo_reqwidth())
        parent_height = max(self._master.winfo_height(), self._master.winfo_reqheight())

        x = parent_x + max(0, (parent_width - dialog_width) // 2)
        y = parent_y + max(0, (parent_height - dialog_height) // 2)

        x, y = self._ensure_on_screen(x, y)

        self._toplevel.geometry(f"+{x}+{y}")

    # --------------------------------------------------------------- Event Handlers

    def _on_focus_out(self, _event):
        """For popover mode: close when focus leaves the dialog."""
        if self._mode != "popover" or not self._toplevel:
            return

        new_focus = self._toplevel.focus_get()

        if new_focus is None:
            self._toplevel.destroy()
            return

        if not str(new_focus).startswith(str(self._toplevel)):
            self._toplevel.destroy()

    def _on_close_request(self):
        if self._toplevel:
            self._toplevel.destroy()

    # --------------------------------------------------------------- Helpers

    def _style_for_role(self, role: ButtonRole) -> str:
        if role == "primary":
            return "primary"
        if role == "secondary":
            return "secondary"
        if role == "danger":
            return "danger"
        if role == "cancel":
            return "secondary-outline"
        if role == "help":
            return "info-link"
        return "secondary"
