"""Core dialog base class for ttkbootstrap dialogs.

This module provides the base `Dialog` class using a builder pattern
for creating flexible, customizable dialogs with composition-based content
and footer builders.
"""

from __future__ import annotations

from dataclasses import dataclass
import tkinter
from tkinter import Widget
from typing import Any, Callable, Iterable, Literal, Mapping, Optional, Tuple, TypedDict, Union

import ttkbootstrap as ttk
from ttkbootstrap.widgets.types import Master
from ttkbootstrap.runtime.toplevel import Toplevel
from ttkbootstrap.runtime.window_utilities import AnchorPoint, WindowPositioning

# --- Types -----------------------------------------------------------------

ContentBuilder = Callable[[Widget], None]
FooterBuilder = Callable[[Widget], None]

ButtonRole = Literal["primary", "secondary", "danger", "cancel", "help"]
DialogMode = Literal["modal", "popover", "sheet"]


@dataclass
class DialogButton:
    """Specification for a dialog button.

    Attributes:
        text (str): Button label text displayed to the user.
        role (ButtonRole): Button role determining styling and behavior.
            - `"primary"`: Main action (blue, triggered by Enter)
            - `"secondary"`: Standard action (gray)
            - `"danger"`: Destructive action (red)
            - `"cancel"`: Cancel action (outline, triggered by Escape)
            - `"help"`: Help/info action (link style)
        result (Any | None): Value assigned to dialog.result when clicked.
        closes (bool): Whether button closes the dialog when clicked.
        default (bool): Whether this is the default button (focused, triggered by Enter).
        command (Callable[[Dialog], None] | None): Callback called when clicked.
        accent (str | None): Accent token for styling (e.g., 'primary', 'danger').
        variant (str | None): Style variant (e.g., 'outline', 'link').
        bootstyle (str | None): DEPRECATED - Use accent and variant instead.
        icon (str | dict | None): Optional icon specification for the button.
    """
    text: str
    role: ButtonRole = "secondary"
    result: Any | None = None  # value assigned to dialog.result
    closes: bool = True  # close dialog after click
    default: bool = False  # default button (Enter)
    command: Callable[[Dialog], None] | None = None
    accent: str | None = None  # accent token (e.g., 'primary', 'danger')
    variant: str | None = None  # style variant (e.g., 'outline', 'link')
    bootstyle: str | None = None  # DEPRECATED: use accent/variant instead
    icon: str | dict[str, Any] | None = None  # passed straight to ttk.Button(icon=...)


ButtonSpec = Union[DialogButton, Mapping[str, Any]]


class ShowOptions(TypedDict, total=False):
    """Options for showing the dialog window.

    Attributes:
        position (tuple[int, int] | None): Optional (x, y) coordinates.
        modal (bool | None): Override the mode's default modality.
        anchor_to (Widget | str | None): Positioning target widget or string.
        anchor_point (AnchorPoint): Point on the anchor target.
        window_point (AnchorPoint): Point on the dialog window.
        offset (tuple[int, int]): Additional (x, y) offset in pixels.
        auto_flip (bool | str): Smart positioning to keep window on screen.
    """
    position: Optional[Tuple[int, int]]
    modal: Optional[bool]
    anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]]
    anchor_point: AnchorPoint
    window_point: AnchorPoint
    offset: Tuple[int, int]
    auto_flip: Union[bool, Literal['vertical', 'horizontal']]


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
            - "sheet": Like "modal" but on macOS applies the Cocoa sheet
              window class for a chromeless, sheet-styled dialog tied to
              its parent (via `transient`). Falls back to plain modal
              behavior on Windows/Linux where there's no equivalent.
            Defaults to "modal".
        frameless: If True, removes window decorations (title bar, borders) and adds
            a solid border frame around the dialog content. Useful for dropdown-style
            menus or popover UIs. Defaults to False.
        window_style: Windows-only pywinstyles effect. Options include
            'mica', 'acrylic', 'aero', 'transparent', 'win7', etc.
            If None (default), uses AppSettings.window_style.
    """

    def __init__(
            self,
            master: Master = None,
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
            window_style: str | None = None,
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
        self._window_style = window_style

        self._toplevel: Toplevel | None = None
        self._content: ttk.Frame | None = None
        self._footer: ttk.Frame | None = None
        self._border_frame: ttk.Frame | None = None

        self.result: Any = None

    # --------------------------------------------------------------- API

    def show(
            self,
            position: Optional[Tuple[int, int]] = None,
            modal: Optional[bool] = None,
            *,
            anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]] = None,
            anchor_point: AnchorPoint = 'center',
            window_point: AnchorPoint = 'center',
            offset: Tuple[int, int] = (0, 0),
            auto_flip: Union[bool, Literal['vertical', 'horizontal']] = False
    ):
        """Create and show the dialog with flexible positioning options.

        Args:
            position: Optional (x, y) coordinates to position the dialog.
                If provided, takes precedence over anchor-based positioning.
            modal: Override the mode's default modality.
                - If None, uses mode:
                    - "modal": grab_set + wait_window
                    - "popover": no grab, but wait_window
            anchor_to: Positioning target. Can be:
                - Widget: Anchor to a specific widget
                - "screen": Anchor to screen edges/corners
                - "cursor": Anchor to mouse cursor location
                - "parent": Anchor to parent window (same as widget)
                - None: Centers on parent (default)
            anchor_point: Point on the anchor target (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            window_point: Point on the dialog window (n, s, e, w, ne, nw, se, sw, center).
                Default 'center'.
            offset: Additional (x, y) offset in pixels from the anchor position.
            auto_flip: Smart positioning to keep window on screen.
                - False: No flipping (default)
                - True: Flip both vertically and horizontally as needed
                - 'vertical': Only flip up/down
                - 'horizontal': Only flip left/right

        Positioning Logic:
            1. If position is provided: Use explicit coordinates
            2. If anchor_to is provided: Use anchor-based positioning
            3. Default: Center on parent window
        """
        if modal is None:
            modal = self._mode in ("modal", "sheet")

        self.result = None
        self._create_toplevel(modal=modal)
        self._build_footer()
        self._build_content()
        self._position_dialog(
            position=position,
            anchor_to=anchor_to,
            anchor_point=anchor_point,
            window_point=window_point,
            offset=offset,
            auto_flip=auto_flip
        )

        if self._alert:
            self._toplevel.bell()

        if self._mode == "popover":
            self._toplevel.bind("<FocusOut>", self._on_focus_out, add="+")

        if modal:
            # Sheets are inherently modal to their parent on Aqua via the
            # sheet window class; calling grab_set on top of that is fine
            # but unnecessary. Plain modal mode still uses grab to block
            # interaction with the parent on platforms without a sheet.
            if self._mode in ("modal", "sheet"):
                self._toplevel.grab_set()
            self._master.wait_window(self._toplevel)

    @property
    def toplevel(self) -> Toplevel | None:
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

    def _create_toplevel(self, modal: bool = True):
        # Pass transient to Toplevel so it's set before window_style is applied
        # (required for mica effect to work on Windows)
        self._toplevel = Toplevel(
            master=self._master,
            window_style=self._window_style,
            transient=self._master if modal else None
        )
        self._toplevel.title(self._title)
        self._toplevel.protocol("WM_DELETE_WINDOW", self._on_close_request)

        try:
            self._toplevel.withdraw()
        except Exception:
            pass

        # Sheet mode: on Aqua, apply the Cocoa 'sheet' window class so the
        # dialog renders chromeless and tied to its parent. Must be set
        # before the window is mapped, hence here while still withdrawn.
        # On non-Aqua, sheet mode is treated as plain modal — there's no
        # cross-platform equivalent of a Cocoa sheet.
        if self._mode == "sheet" and getattr(self._toplevel, 'winsys', None) == 'aqua':
            try:
                self._toplevel.tk.call(
                    '::tk::unsupported::MacWindowStyle', 'style',
                    self._toplevel, 'sheet', 'none',
                )
            except tkinter.TclError:
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
            # Get accent/variant from spec or derive from role
            if spec.accent or spec.variant:
                # Use explicitly provided accent/variant
                accent, variant = spec.accent, spec.variant
            elif spec.bootstyle:
                # Legacy: spec has bootstyle - parse it
                from ttkbootstrap.style.bootstyle import convert_bootstyle_to_accent_variant
                accent, variant = convert_bootstyle_to_accent_variant(spec.bootstyle, 'TButton', warn=False)
            else:
                accent, variant = self._style_for_role(spec.role)

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
                accent=accent,
                variant=variant,
                command=make_command(spec),
                icon=spec.icon,
                compound="left" if spec.icon else "text",
            )
            btn.pack(side="right")

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

    def _position_dialog(
            self,
            position: Optional[Tuple[int, int]] = None,
            anchor_to: Optional[Union[Widget, Literal["screen", "cursor", "parent"]]] = None,
            anchor_point: AnchorPoint = 'center',
            window_point: AnchorPoint = 'center',
            offset: Tuple[int, int] = (0, 0),
            auto_flip: Union[bool, Literal['vertical', 'horizontal']] = False
    ) -> None:
        """Position the dialog window using consolidated positioning logic.

        Positioning logic:
        1. If position is provided: Use explicit coordinates
        2. If anchor_to is provided: Use anchor-based positioning
        3. Default: Center on parent
        """
        if not self._toplevel:
            return

        # Priority 1: Explicit position coordinates
        if position is not None:
            x, y = position
            x, y = WindowPositioning.ensure_on_screen(self._toplevel, int(x), int(y))
            self._toplevel.geometry(f"+{x}+{y}")

        # Priority 2: Anchor-based positioning
        elif anchor_to is not None:
            WindowPositioning.position_anchored(
                window=self._toplevel,
                anchor_to=anchor_to,
                parent=self._master,
                anchor_point=anchor_point,
                window_point=window_point,
                offset=offset,
                auto_flip=auto_flip,
                ensure_visible=True
            )

        # Priority 3: Default - center on parent
        else:
            WindowPositioning.position_window(
                window=self._toplevel,
                position=None,
                parent=self._master,
                center_on_parent=True,
                ensure_visible=True
            )

        # Apply window style while still withdrawn, right before showing.
        # The update() call is here so pywinstyles can attach to a fully
        # realized HWND on Windows; on Aqua (and X11) it serves no purpose
        # and can hang indefinitely flushing children's pending events
        # (e.g. FontDialog's Treeview with hundreds of tag-configure font
        # calls), so gate it on the platform that actually needs it.
        self._toplevel.update_idletasks()
        self._toplevel._apply_window_style()
        if getattr(self._toplevel, 'winsys', None) == 'win32':
            self._toplevel.update()
        self._toplevel.deiconify()

        # Second centering pass for default positioning (handles dynamic sizing)
        if position is None and anchor_to is None:
            try:
                x, y = WindowPositioning.center_on_parent(self._toplevel, self._master)
                x, y = WindowPositioning.ensure_on_screen(self._toplevel, x, y)
                self._toplevel.geometry(f"+{x}+{y}")
            except Exception:
                pass

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

    def _style_for_role(self, role: ButtonRole) -> tuple[str | None, str | None]:
        """Return (accent, variant) tuple for a button role."""
        if role == "primary":
            return ("primary", None)
        if role == "secondary":
            return ("secondary", None)
        if role == "danger":
            return ("danger", None)
        if role == "cancel":
            return ("secondary", "outline")
        if role == "help":
            return ("info", "link")
        return ("secondary", None)
