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

    Features:
        - Native file/directory chooser dialog
        - Multiple dialog types (open, save, directory, multiple files)
        - Configurable dialog options (file types, initial directory, etc.)
        - Button with customizable label
        - Automatic path display in entry field
        - Support for multiple file selection (displayed as comma-separated)
        - All Field features (label, validation, messages, etc.)

    Events (inherited from Field):
        <<Changed>>: Fired when a path is selected from the dialog
        <<Input>>: Fired when user manually types in the entry
        <<Valid>>: Fired when validation passes
        <<Invalid>>: Fired when validation fails

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.composites.pathentry import PathEntry

        root = ttk.Window()

        # Single file selection
        file_entry = PathEntry(
            root,
            label="Select File",
            dialog="openfilename",
            dialog_options={
                'title': 'Choose a file',
                'filetypes': [('Text files', '*.txt'), ('All files', '*.*')]
            }
        )
        file_entry.pack(padx=20, pady=10, fill='x')

        # Directory selection
        dir_entry = PathEntry(
            root,
            label="Select Directory",
            dialog="directory",
            dialog_options={'title': 'Choose a folder'}
        )
        dir_entry.pack(padx=20, pady=10, fill='x')

        # Multiple file selection
        multi_entry = PathEntry(
            root,
            label="Select Files",
            dialog="openfilenames",
            dialog_options={
                'title': 'Choose multiple files',
                'filetypes': [('Images', '*.png *.jpg'), ('All files', '*.*')]
            }
        )
        multi_entry.pack(padx=20, pady=10, fill='x')

        # Save file dialog
        save_entry = PathEntry(
            root,
            label="Save As",
            value="untitled.txt",
            dialog="saveasfilename",
            dialog_options={
                'defaultextension': '.txt',
                'filetypes': [('Text files', '*.txt')]
            }
        )
        save_entry.pack(padx=20, pady=10, fill='x')

        # Get selected path
        def on_select():
            path = file_entry.value()
            print(f"Selected: {path}")
            # Access raw dialog result
            print(f"Dialog result: {file_entry.dialog_result}")

        ttk.Button(root, text="Get Path", command=on_select).pack(pady=10)

        root.mainloop()
        ```

    Inherited Properties:
        entry_widget: Access to the underlying TextEntryPart widget
        label_widget: Access to the label widget
        message_widget: Access to the message label widget
        addons: Dictionary of inserted addon widgets
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates
    """

    def __init__(
            self,
            master=None,
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
                Common options include:
                - title: Dialog window title
                - initialdir: Initial directory to show
                - initialfile: Initial filename (for save dialogs)
                - filetypes: List of (label, pattern) tuples for file filters
                  Example: [('Text files', '*.txt'), ('All files', '*.*')]
                - defaultextension: Default file extension (e.g., '.txt')
                - multiple: Allow multiple selection (for compatible dialog types)
            **kwargs: Additional keyword arguments from FieldOptions:
                required: If True, field cannot be empty
                bootstyle: The accent color of the focus ring and active border
                allow_blank: Allow empty input
                cursor: Cursor style when hovering
                value_format: Format pattern for parsing/formatting
                exportselection: Export selection to clipboard
                font: Font for text display
                foreground: Text color
                initial_focus: If True, widget receives focus on creation
                justify: Text alignment
                show_message: If True, displays message area
                message: Message text to display below the field
                padding: Padding around entry widget
                take_focus: If True, widget accepts Tab focus
                textvariable: Tkinter Variable to link with text
                textsignal: Signal object for reactive updates
                width: Width in characters
                xscrollcommand: Callback for horizontal scrolling

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
                '<<Changed>>', data={
                    'value': result, 'prev_value': self.entry_widget._prev_changed_value
                }, when="tail")
            self.entry_widget.commit()

