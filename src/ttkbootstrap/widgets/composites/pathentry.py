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

        - ``<<Change>>``: Fired when a path is selected from the dialog.
        - ``<<Input>>``: Fired when user manually types in the entry.
        - ``<<Valid>>``: Fired when validation passes.
        - ``<<Invalid>>``: Fired when validation fails.

    Attributes:
        entry_widget (TextEntryPart): The underlying text entry widget.
        label_widget (Label): The label widget above the entry.
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
            value: str = "No file chosen",
            label: str = "Choose File",
            dialog: FileDialogType = "openfilename",
            dialog_options: dict[str, Any] = None,
            **kwargs: Unpack[FieldOptions]
    ):
        """Initialize a PathEntry widget.

        Creates a path entry field with a button that opens a native file or
        directory chooser dialog. The selected path(s) are automatically displayed
        in the entry field. The widget supports various dialog types for different
        use cases (single file, multiple files, directory, save file).

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display in the entry field. Default is
                "No file chosen". This is updated when a path is selected from
                the dialog.
            label: Text to display on the dialog button. Default is "Choose File".
                Can be updated later via configure(label=...).
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

        Other Parameters:
            required (bool): If True, field cannot be empty.
            color (str): Color token for the focus ring and active border.
            bootstyle (str): DEPRECATED - Use `color` instead.
            allow_blank (bool): Allow empty input.
            cursor (str): Cursor style when hovering.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment.
            show_message (bool): If True, displays message area.
            message (str): Message text to display below the field.
            padding (str): Padding around entry widget.
            take_focus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.

        Note:
            When multiple files are selected (using 'openfilenames' or 'openfiles'),
            the paths are joined with ", " (comma-space) and displayed in the entry.
            The raw dialog result (tuple/list) is available via the dialog_result
            property.
        """
        self._dialog = dialog
        self._dialog_options = dialog_options
        self._dialog_result = None
        self._label = label

        super().__init__(master=master, value=value, **kwargs)

        self.insert_addon(
            Button,
            position="before",
            name="dialog-button",
            text=self._label,
            command=self._show_file_chooser
        )

    @property
    def dialog_button(self):
        """Get the dialog button widget."""
        return self.addons.get('dialog-button')

    @property
    def dialog_result(self):
        """Get the raw result from the last file dialog operation."""
        return self._dialog_result

    @configure_delegate('dialog')
    def _delegate_dialog(self, value: FileDialogType = None):
        """Get or set the file dialog type."""
        if value is None:
            return self._dialog
        else:
            self._dialog = value
        return None

    @configure_delegate('label')
    def _delegate_label(self, value: str = None):
        """Get or set the dialog button label text."""
        if value is None:
            return self._label
        else:
            self._label = value
            self.dialog_button['text'] = value
        return None

    def _show_file_chooser(self):
        """Open the file/directory chooser dialog and update the entry."""
        method_name = f"ask{self._dialog}"
        dialog_func = getattr(filedialog, method_name, None)

        if dialog_func is None:
            raise ValueError(f"Invalid dialog type `{self._dialog}`")

        result = dialog_func(**self._dialog_options or dict())
        self._dialog_result = result

        if isinstance(result, (tuple, list)):
            result = ", ".join(result)

        if result:
            self.variable.set(result)
            self.entry_widget.event_generate(
                '<<Change>>', data={
                    'value': result, 'prev_value': self.entry_widget._prev_changed_value
                }, when="tail")
            self.entry_widget.commit()

