"""Path entry field widget with file/directory chooser dialog.

Provides an entry field with a button that opens a file or directory chooser
dialog for selecting paths.
"""

from tkinter import filedialog
from typing import Any, Literal

from typing_extensions import Unpack

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.types import Master

FileDialogType = Literal[
    'openfilename', 'openfile', 'directory', 'openfilenames', 'openfiles',
    'saveasfile', 'saveasfilename'
]
"""Type alias for file dialog types.

Available dialog types:
    - 'openfilename': Select a single existing file (returns filename)
    - 'openfile': Select a single existing file (returns file object)
    - 'directory': Select a directory
    - 'openfilenames': Select multiple existing files (returns filenames)
    - 'openfiles': Select multiple existing files (returns file objects)
    - 'saveasfile': Select location to save a file (returns file object)
    - 'saveasfilename': Select location to save a file (returns filename)
"""


class PathEntry(Field):
    """A path entry field widget with file/directory chooser dialog button.

    PathEntry extends the Field widget to provide a specialized input for file
    and directory paths. It includes a button that opens a native file/directory
    chooser dialog, and displays the selected path(s) in the entry field. The
    widget supports various dialog types including single file selection, multiple
    file selection, directory selection, and save file dialogs.

    !!! note "Events"

        ``<<Change>>``: Fired when a path is selected from the dialog.
          Provides ``event.data`` with keys: ``value``, ``prev_value``, ``text``, ``dialog_result``.

        ``<<Input>>``: Fired when user manually types in the entry.

        ``<<Valid>>``: Fired when validation passes.

        ``<<Invalid>>``: Fired when validation fails.

    Attributes:
        entry_widget (TextEntryPart): The underlying text entry widget.
        label_widget (Label): The label widget above the entry (from FieldOptions).
        message_widget (Label): The message label widget below the entry.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
        dialog_result (Any): The raw result from the last file dialog operation.
        dialog_button (Button): The button widget that opens the dialog.
    """

    def __init__(
            self,
            master: Master = None,
            *,
            value: str | None = None,
            dialog: FileDialogType = "openfilename",
            dialog_options: dict[str, Any] | None = None,
            button_text: str = "Browse",
            label: str = None,
            message: str = None,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a PathEntry widget.

        Creates a path entry field with a button that opens a native file or
        directory chooser dialog. The selected path(s) are automatically displayed
        in the entry field. The widget supports various dialog types for different
        use cases (single file, multiple files, directory, save file).

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial path value to display in the entry field. Default is None
                (empty field). This is updated when a path is selected from the dialog.
            dialog: Type of file dialog to open. Default is "openfilename".
                Options:

                - 'openfilename': Single file selection (returns path string)
                - 'openfile': Single file selection (returns file object)
                - 'directory': Directory selection
                - 'openfilenames': Multiple file selection (returns paths)
                - 'openfiles': Multiple file selection (returns file objects)
                - 'saveasfile': Save file dialog (returns file object)
                - 'saveasfilename': Save file dialog (returns path string)

            dialog_options: Dictionary of options to pass to the file dialog.
                Common options: title, initialdir, initialfile, filetypes,
                defaultextension, multiple.
            button_text: Text to display on the browse button. Default is "Browse".
                Can be changed at runtime via ``configure(button_text=...)``.
            label (str): Label text to display above the entry field (from FieldOptions).
            message (str): Message text to display below the field.

        Other Parameters:
            required (bool): If True, field cannot be empty.
            color (str): Color token for the focus ring and active border.
            allow_blank (bool): Allow empty input.
            cursor (str): Cursor style when hovering.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment.
            show_message (bool): If True, displays message area.
            padding (str): Padding around entry widget.
            takefocus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.

        Note:
            When multiple files are selected (using 'openfilenames' or 'openfiles'),
            the paths are joined with ", " (comma-space) and displayed in the entry.
            The raw dialog result (tuple/list) is available via the ``dialog_result``
            property.
        """
        self._dialog = dialog
        self._dialog_options = dialog_options
        self._dialog_result = None
        self._button_text = button_text
        self._prev_value: str | None = value

        super().__init__(master=master, label=label, message=message, value=value, **kwargs)

        self.insert_addon(
            Button,
            position="before",
            name="dialog-button",
            text=self._button_text,
            command=self._show_file_chooser
        )

    @property
    def dialog_button(self):
        """Get the dialog button widget."""
        return self.addons.get('dialog-button')

    @property
    def dialog_result(self):
        """Get the raw result from the last file dialog operation.

        For single file selection, this returns the path string.
        For multiple file selection, this returns a tuple/list of paths.
        """
        return self._dialog_result

    # ------ Configuration Delegates ------

    @configure_delegate('dialog')
    def _delegate_dialog(self, value: FileDialogType = None):
        if value is None:
            return self._dialog
        else:
            self._dialog = value
        return None

    @configure_delegate('button_text')
    def _delegate_button_text(self, value: str = None):
        if value is None:
            return self._button_text
        else:
            self._button_text = value
            if self.dialog_button:
                self.dialog_button['text'] = value
        return None

    @configure_delegate('dialog_options')
    def _delegate_dialog_options(self, value: dict[str, Any] = None):
        if value is None:
            return self._dialog_options
        else:
            self._dialog_options = value
        return None

    def _show_file_chooser(self):
        """Open the file/directory chooser dialog and update the entry."""
        method_name = f"ask{self._dialog}"
        dialog_func = getattr(filedialog, method_name, None)

        if dialog_func is None:
            raise ValueError(f"Invalid dialog type `{self._dialog}`")

        result = dialog_func(**(self._dialog_options or {}))
        self._dialog_result = result

        # Format display text for multiple selections
        if isinstance(result, (tuple, list)):
            display_text = ", ".join(str(p) for p in result)
        else:
            display_text = result

        # Only update if a selection was made (result is truthy)
        if result:
            prev_value = self._prev_value
            self._prev_value = display_text

            # Set the value through the field's standard mechanism
            self.value = display_text

            # Emit <<Change>> on PathEntry (the composite) with full event data
            self.event_generate(
                '<<Change>>',
                data={
                    'value': display_text,
                    'prev_value': prev_value,
                    'text': display_text,
                    'dialog_result': self._dialog_result,
                },
                when="tail"
            )

