"""FormDialog - A dialog that embeds a Form widget for data entry.

This module provides FormDialog, which combines the Dialog and Form widgets
to create modal or non-modal dialogs for structured data entry.

Basic Usage
-----------
Create a form dialog with auto-inferred fields:

    >>> from ttkbootstrap.dialogs import FormDialog
    >>>
    >>> initial_data = {
    ...     "first_name": "Jane",
    ...     "last_name": "Doe",
    ...     "age": 30,
    ...     "active": True,
    ... }
    >>> dialog = FormDialog(
    ...     title="Edit User",
    ...     data=initial_data,
    ...     col_count=2,
    ... )
    >>> dialog.show()
    >>> if dialog.result:
    ...     print("Updated data:", dialog.result)

Explicit Form Layout
--------------------
Use FieldItem, GroupItem, and TabsItem for complex layouts:

    >>> from ttkbootstrap.dialogs import FormDialog
    >>> from ttkbootstrap.widgets.form import FieldItem, GroupItem
    >>>
    >>> items = [
    ...     GroupItem(
    ...         label="Personal Info",
    ...         col_count=2,
    ...         items=[
    ...             FieldItem(key="first_name", label="First Name"),
    ...             FieldItem(key="last_name", label="Last Name"),
    ...             FieldItem(key="email", label="Email"),
    ...         ]
    ...     ),
    ...     FieldItem(key="bio", label="Bio", editor="text"),
    ... ]
    >>> dialog = FormDialog(
    ...     title="User Profile",
    ...     items=items,
    ...     data={"first_name": "", "last_name": "", "email": "", "bio": ""},
    ...     buttons=["Cancel", "Save"],
    ... )
    >>> dialog.show()

Custom Validation
-----------------
Add validation before accepting the form data:

    >>> def validate_form(form_dialog):
    ...     data = form_dialog.form.data
    ...     if not data.get("email"):
    ...         messagebox.showwarning("Validation Error", "Email is required!")
    ...         return False
    ...     return True
    >>>
    >>> from ttkbootstrap.dialogs import DialogButton
    >>> dialog = FormDialog(
    ...     title="Registration",
    ...     data={"email": "", "password": ""},
    ...     buttons=[
    ...         DialogButton(text="Cancel", role="cancel", result=None),
    ...         DialogButton(
    ...             text="Register",
    ...             role="primary",
    ...             result="submitted",
    ...             command=lambda dlg: validate_form(dlg)
    ...         )
    ...     ]
    ... )
"""

from __future__ import annotations

from typing import Any, Callable, Iterable, Literal, Mapping, Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.widgets.form import FormItem

from ttkbootstrap.dialogs.dialog import Dialog, DialogButton, ButtonSpec
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.constants import DEFAULT_MIN_COL_WIDTH as FORM_MIN_COL_WIDTH


class FormDialog:
    """A dialog window that embeds a Form widget for structured data entry.

    FormDialog combines the Dialog and Form widgets to create modal or non-modal
    dialogs for data entry with automatic field generation or explicit layouts.

    Attributes:
        result: The form data returned after closing (dict), or None if cancelled.
        form: The embedded Form widget instance, accessible for advanced usage.

    Args:
        master: Parent widget. If None, uses the default root window.
        title: Dialog window title. Defaults to "Form".
        data: Initial data backing the form. Keys become field names.
        items: Optional explicit form definition using FieldItem/GroupItem/TabsItem.
            If not provided, fields are inferred from data keys and types.
        col_count: Number of columns for form layout. Defaults to 1.
        min_col_width: Minimum width for each column in pixels. Defaults to the
            shared form default.
        on_data_changed: Optional callback invoked when any field value changes.
            Receives the updated data dict as parameter.
        width: Requested width for the form. Defaults to None (auto-size).
        height: Requested height for the form. Defaults to None (auto-size).
          scrollable: Deprecated; FormDialog manages scrolling internally.
          scrollview_options: Additional options passed to ScrollView when scrollable is True.
        buttons: Footer buttons. Can be DialogButton instances, dicts, or strings.
            If not provided, defaults to Cancel and OK buttons.
            First button appears rightmost (Bootstrap convention).
        minsize: Minimum dialog window size as (width, height).
            If None, automatically calculated based on col_count * min_col_width + padding.
            If provided, ensures width is at least the calculated minimum to prevent
            horizontal scrolling. Defaults to None (auto-calculate).
        maxsize: Maximum dialog window size as (width, height). Defaults to None.
        resizable: Allow window resizing as (width, height) bools. Defaults to (True, True).
        alert: If True, plays system alert sound on show. Defaults to False.
        mode: Dialog interaction mode ("modal" or "popover"). Defaults to "modal".

    Example:
        Simple form dialog:

        >>> dialog = FormDialog(
        ...     title="Settings",
        ...     data={"username": "admin", "port": 8080, "debug": False},
        ...     col_count=1
        ... )
        >>> dialog.show()
        >>> if dialog.result:
        ...     print("Settings saved:", dialog.result)

        With custom buttons and validation:

        >>> def save_settings(dlg):
        ...     if dlg.form.data["port"] < 1024:
        ...         print("Port must be >= 1024")
        ...         return  # Don't close dialog
        ...     dlg.result = dlg.form.data
        >>>
        >>> dialog = FormDialog(
        ...     title="Advanced Settings",
        ...     data={"port": 8080},
        ...     buttons=[
        ...         DialogButton(text="Cancel", role="cancel"),
        ...         DialogButton(
        ...             text="Apply",
        ...             role="primary",
        ...             closes=False,  # Keep dialog open
        ...             command=save_settings
        ...         ),
        ...         DialogButton(text="OK", role="primary", result="ok")
        ...     ]
        ... )
    """

    def __init__(
        self,
        master=None,
        *,
        title: str = "Form",
        data: dict[str, Any] | None = None,
        items: Sequence[FormItem | Mapping[str, Any]] | None = None,
        col_count: int = 1,
        min_col_width: int | None = None,
        on_data_changed: Callable[[dict[str, Any]], Any] | None = None,
        width: int | None = None,
        height: int | None = None,
        scrollable: bool = True,
        scrollview_options: dict[str, Any] | None = None,
        buttons: Iterable[ButtonSpec | str] | None = None,
        minsize: tuple[int, int] | None = None,
        maxsize: tuple[int, int] | None = None,
        resizable: tuple[bool, bool] | bool | None = False,
        alert: bool = False,
        mode: Literal['modal', 'popover'] = "modal",
    ):
        """Initialize a FormDialog that wraps a Form inside a Dialog.

        Args:
            master: Parent widget. Defaults to the default root window.
            title: Dialog window title.
            data: Initial data backing the form; keys become field names.
            items: Optional explicit form layout (FieldItem/GroupItem/TabsItem or mappings).
            col_count: Number of columns for the form layout.
            min_col_width: Minimum width per column; defaults to the shared form default.
            on_data_changed: Callback invoked when any field value changes.
            width: Explicit form width; if None, size naturally.
            height: Explicit form height; if None, size naturally.
            scrollable: Whether the form content should be scrollable.
            scrollview_options: Extra options passed to the ScrollView when scrollable.
            buttons: Dialog footer buttons (DialogButton, mapping, or string).
            minsize: Minimum dialog window size (width, height).
            maxsize: Maximum dialog window size (width, height).
            resizable: Bool or (width, height) tuple to allow window resizing.
            alert: Whether to play the system alert sound when shown.
            mode: Dialog interaction mode, "modal" or "popover".
        """
        self._data = data or {}
        self._items = items
        self._col_count = col_count
        # Use the shared form default when not provided to keep layouts consistent
        self._min_col_width = min_col_width if min_col_width is not None else FORM_MIN_COL_WIDTH
        self._on_data_changed = on_data_changed
        self._width = width
        self._height = height
        self._scrollable = scrollable  # deprecated; kept for compatibility with callers

        # Use better default scrollview options - auto-hide when content fits
        default_scrollview_options = {
            # Keep the scrollbar visible to avoid width jumps when it appears/disappears
            'show_scrollbar': 'always',
            'autohide_delay': 1000,
        }
        if scrollview_options:
            default_scrollview_options.update(scrollview_options)
        self._scrollview_options = default_scrollview_options

        # Normalize buttons and wrap command callbacks
        self._buttons = self._normalize_buttons(buttons)
        self._wrap_button_commands()

        # Store minsize for later adjustment
        self._user_minsize = minsize
        self._user_maxsize = maxsize

        # Normalize resizable flag: bool applies to both axes
        if isinstance(resizable, bool):
            resizable = (resizable, resizable)

        # Create the dialog with form as content
        # We'll set the proper minsize after measuring the actual form
        self._dialog = Dialog(
            master=master,
            title=title,
            content_builder=self._build_form_content,
            buttons=self._buttons,
            minsize=minsize,  # Use user-provided or None initially
            maxsize=maxsize,
            resizable=resizable,
            alert=alert,
            mode=mode,
        )

        self.form: Any = None  # Form widget, imported lazily to avoid circular import
        self.result: Any = None
        self._initial_layout_done = False
        self._scrollview = None
        self._window_id = None

    def show(self, position: Optional[tuple[int, int]] = None, modal: Optional[bool] = None):
        """Show the form dialog and populate `result` when closed."""
        # Allow initial layout priming each time the dialog is shown
        self._initial_layout_done = False

        self._dialog.show(position=position, modal=modal)

        # Transfer the result from dialog to FormDialog
        if self._dialog.result is not None:
            self.result = self.form.data if self.form else None
        else:
            self.result = None

    def show_centered(self, modal: Optional[bool] = None):
        """Convenience helper to center on the parent window."""
        # Allow initial layout priming each time the dialog is shown
        self._initial_layout_done = False

        self._dialog.show_centered(modal=modal)

        # Transfer the result from dialog to FormDialog
        if self._dialog.result is not None:
            self.result = self.form.data if self.form else None
        else:
            self.result = None


    def _build_form_content(self, parent):
        """Builder callback that creates the Form widget inside the dialog."""
        # Import Form here to avoid circular import
        from ttkbootstrap.widgets.form import Form
        from ttkbootstrap.widgets.scrollview import ScrollView

        # Configure parent to allow stretching
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        container = parent
        if self._scrollable:
            self._scrollview = ScrollView(parent, direction='vertical', **self._scrollview_options)
            self._scrollview.grid(row=0, column=0, sticky="nsew")
            self._scrollview.enable_scrolling()
            # add a padding frame inside the scrollview so the form has margins
            padding_frame = Frame(self._scrollview, padding=10)
            padding_frame.columnconfigure(0, weight=1)
            padding_frame.rowconfigure(0, weight=1)
            self._scrollview.add(padding_frame, anchor='nw')
            self._window_id = self._scrollview._window_id
            self._scrollview.bind('<Configure>', self._on_scrollview_configure, add="+")
            # Keep canvas window width in sync with viewport on every resize
            self._scrollview.canvas.bind("<Configure>", self._on_canvas_configure, add="+")
            container = padding_frame
        else:
            self._scrollview = None

        # Create the form without its own scrolling; scrolling is managed by the dialog
        self.form = Form(
            container,
            data=self._data,
            items=self._items,
            col_count=self._col_count,
            min_col_width=self._min_col_width,
            on_data_changed=self._on_data_changed,
            width=None,  # Let form size naturally
            height=self._height,
            buttons=None,
        )

        # Add the form to the scrollview container or grid directly
        if self._scrollview:
            self.form.grid(row=0, column=0, sticky="nsew")
        else:
            self.form.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Ensure initial layout runs right after build (for scrollable dialogs)
        self._schedule_initial_layout()

        # Measure the actual content width after rendering
        measured_width = self._col_count * self._min_col_width
        if self._items:
            nested_width = self._calculate_required_width()
            measured_width = max(measured_width, nested_width)

        if self._width:
            measured_width = self._width

        # Calculate dialog size: content + padding (10x2) + dialog chrome (~40)
        dialog_width = measured_width + 60
        dialog_height = 500  # Default height, will adjust after geometry update

        # Apply user minsize if provided
        if self._user_minsize:
            user_width, user_height = self._user_minsize
            dialog_width = max(user_width, dialog_width)
            dialog_height = max(user_height, dialog_height)

        if self._height:
            dialog_height = self._height + 100

        dialog_height = min(dialog_height, 800)
        # Store the intended content width for pre-show sizing of the scrollview
        self._desired_canvas_width = measured_width

        # Set minsize and geometry BEFORE forcing layout
        if self._dialog.toplevel:
            self._dialog.toplevel.minsize(dialog_width, dialog_height)
            self._dialog.toplevel.geometry(f"{dialog_width}x{dialog_height}")

            # Force complete geometry calculation while window is still withdrawn
            self._dialog.toplevel.update_idletasks()

    def _schedule_initial_layout(self):
        """Run layout fixups immediately before showing the window."""
        if not self._scrollable:
            return
        if self._dialog and self._dialog.toplevel:
            # Make sure all pending geometry work is processed while withdrawn
            self._dialog.toplevel.update_idletasks()
            self._dialog.toplevel.update()
        # Run once synchronously so sizing is applied before deiconify
        self._fire_initial_configure(blocking=True)

    def _fire_initial_configure(self, _event=None, attempts: int = 5, blocking: bool = False):
        """Trigger scrollview/layout config once after geometry stabilizes."""
        if self._initial_layout_done:
            return
        if not (self._scrollable and self._scrollview and self.form):
            return

        canvas = self._scrollview.canvas
        canvas_width = 0

        # When blocking, loop a few times to give Tk a chance to size the canvas
        loops = attempts if blocking else 1
        for _ in range(max(1, loops)):
            if self._dialog and self._dialog.toplevel:
                self._dialog.toplevel.update_idletasks()
            self._scrollview.update_idletasks()
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                break

        fallback_width = max(
            getattr(self, "_desired_canvas_width", 0),
            self.form.winfo_reqwidth() if self.form else 0,
            self._col_count * self._min_col_width,
        )
        if canvas_width <= 1:
            canvas_width = fallback_width

        # Apply width and manually call handlers
        if self._window_id:
            canvas.itemconfigure(self._window_id, width=canvas_width)
        self._on_scrollview_configure(None)
        try:
            self._scrollview._on_frame_configure(None)
        except Exception:
            pass

        # Ensure scrolling bindings are active after layout adjustments
        try:
            if getattr(self._scrollview, "_scrolling_enabled", False):
                self._scrollview.refresh_bindings()
            else:
                self._scrollview.enable_scrolling()
        except Exception:
            pass

        # Generate configure to mirror user-driven resize
        try:
            canvas.event_generate("<Configure>")
        except Exception:
            pass

    def _on_scrollview_configure(self, _event=None):
        """Keep scrollview content width in sync with the viewport."""
        if self._scrollview and self._window_id:
            canvas_width = self._scrollview.canvas.winfo_width()
            if canvas_width > 1:
                self._scrollview.canvas.itemconfigure(self._window_id, width=canvas_width)

    def _on_canvas_configure(self, event=None):
        """Keep the embedded form window width aligned to the canvas viewport."""
        if not (self._scrollview and self._window_id):
            return
        width = event.width if event and hasattr(event, "width") else self._scrollview.canvas.winfo_width()
        if width <= 1:
            return
        self._scrollview.canvas.itemconfigure(self._window_id, width=width)
        try:
            self._scrollview._on_frame_configure(None)
        except Exception:
            pass

    def _calculate_required_width(self) -> int:
        """Calculate the required minimum width for the dialog based on form structure."""
        try:
            from ttkbootstrap.widgets.form import GroupItem, TabsItem

            # Start by finding the maximum width requirement
            max_content_width = self._find_max_content_width(self._items, self._col_count, self._min_col_width)

            # Add all the padding layers:
            # 1. Form widget padding (grid padx=10 on each side) = 20px
            # 2. Dialog content frame borders = 10px
            # 3. Window chrome and safety margin = 30px
            total_width = max_content_width + 60

            return total_width
        except:
            # Fallback to basic calculation
            return (self._col_count * self._min_col_width) + 60

    def _find_max_content_width(self, items, parent_col_count: int, parent_min_col_width: int) -> int:
        """Find the maximum content width needed, accounting for nested structures."""
        if not items:
            # No items, use parent layout
            # Each column needs: min_col_width + padx (6 on each side = 12)
            return (parent_col_count * (parent_min_col_width + 12))

        max_width = 0

        # Calculate width for current level
        current_width = parent_col_count * (parent_min_col_width + 12)
        max_width = max(max_width, current_width)

        # Check all items for nested layouts
        try:
            from ttkbootstrap.widgets.form import GroupItem, TabsItem

            for item in items:
                if isinstance(item, dict):
                    item_type = item.get('type', 'field')
                    if item_type == 'group':
                        nested_col_count = item.get('col_count', parent_col_count)
                        nested_min_col_width = item.get('min_col_width', self._min_col_width)
                        nested_items = item.get('items', [])

                        # GroupItem content width
                        group_content = self._find_max_content_width(nested_items, nested_col_count, nested_min_col_width)
                        # Add LabelFrame padding (8px each side) and borders (~4px) = 24px total
                        group_total = group_content + 24
                        max_width = max(max_width, group_total)

                    elif item_type == 'tabs':
                        tabs = item.get('tabs', [])
                        for tab in tabs:
                            if isinstance(tab, dict):
                                tab_items = tab.get('items', [])
                                tab_width = self._find_max_content_width(tab_items, parent_col_count, parent_min_col_width)
                                # Add Notebook borders = 20px
                                max_width = max(max_width, tab_width + 20)

                elif isinstance(item, GroupItem):
                    nested_col_count = item.col_count if item.col_count else parent_col_count
                    nested_min_col_width = item.min_col_width if item.min_col_width else self._min_col_width

                    # GroupItem content width
                    group_content = self._find_max_content_width(item.items, nested_col_count, nested_min_col_width)
                    # Add LabelFrame padding
                    group_total = group_content + 24
                    max_width = max(max_width, group_total)

                elif isinstance(item, TabsItem):
                    for tab in item.tabs:
                        tab_items = tab.items if hasattr(tab, 'items') else []
                        tab_width = self._find_max_content_width(tab_items, parent_col_count, parent_min_col_width)
                        # Add Notebook borders
                        max_width = max(max_width, tab_width + 20)
        except:
            pass

        return max_width

    def _wrap_button_commands(self):
        """Wrap button command callbacks to pass FormDialog instead of Dialog."""
        for button in self._buttons:
            # For non-cancel buttons, handle validation and closing manually
            if button.role != "cancel":
                button.closes = False
            if button.command:
                original_command = button.command
                def wrapped_command(dlg, cmd=original_command, btn=button):
                    # Validate form before running custom command
                    if self.form and btn.role != "cancel":
                        if not self.form.validate():
                            return
                    result = cmd(self)  # Pass FormDialog, not Dialog
                    if result is False:
                        return
                    # Set result and close manually when not cancelled
                    if self._dialog:
                        self._dialog.result = btn.result if btn.result is not None else (self.form.data if self.form else None)
                        if btn.closes is False and self._dialog.toplevel:
                            self._dialog.toplevel.destroy()
                    return result
                button.command = wrapped_command
            else:
                # No custom command: inject validation and close behavior for non-cancel buttons
                def auto_command(dlg=None, btn=button):
                    if self.form and btn.role != "cancel":
                        if not self.form.validate():
                            return
                    if self._dialog:
                        self._dialog.result = btn.result if btn.result is not None else (self.form.data if self.form else None)
                        if btn.closes is False and self._dialog.toplevel:
                            self._dialog.toplevel.destroy()
                button.command = auto_command

    def _normalize_buttons(self, buttons: Iterable[ButtonSpec | str] | None) -> list[DialogButton]:
        """Normalize button specifications, providing defaults if none given."""
        if buttons is None:
            # Default buttons: Cancel and OK
            return [
                DialogButton(text="Cancel", role="cancel", result=None),
                DialogButton(text="OK", role="primary", result="ok", default=True),
            ]

        normalized: list[DialogButton] = []
        for btn in buttons:
            if isinstance(btn, DialogButton):
                normalized.append(btn)
            elif isinstance(btn, str):
                # Simple string becomes a button
                role = "primary" if not normalized else "secondary"
                result = btn.lower() if btn.lower() in ("ok", "submit", "save") else None
                normalized.append(DialogButton(text=btn, role=role, result=result))
            elif isinstance(btn, Mapping):
                normalized.append(DialogButton(**btn))
            else:
                raise TypeError(f"Invalid button type: {type(btn)}")

        return normalized

    @property
    def toplevel(self):
        """Read-only access to the underlying toplevel window."""
        return self._dialog.toplevel if self._dialog else None


__all__ = ["FormDialog"]
