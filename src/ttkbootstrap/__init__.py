"""ttkbootstrap - A supercharged theme extension for tkinter.

A modern flat style theme engine for tkinter that enables on-demand styling
of ttk widgets with over a dozen built-in themes inspired by Bootstrap.

This package provides:
    - A comprehensive collection of modern, flat-style themes
    - Custom widgets extending tkinter/ttk functionality
    - Easy-to-use styling API with color keywords
    - Window and Toplevel classes with enhanced functionality
    - Cross-platform compatibility

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    # Create a themed window
    root = ttk.Window(themename="darkly")

    # Create styled widgets
    btn = ttk.Button(root, text="Click Me", bootstyle="success")
    btn.pack(padx=10, pady=10)

    root.mainloop()
    ```

For more information, see: https://ttkbootstrap.readthedocs.io/
"""
from tkinter import (
    Menu as _tkMenu, Text as _tkText, Canvas as _tkCanvas, Tk as _tkTk,
    Frame as _tkFrame, LabelFrame,
    Variable, StringVar, IntVar, BooleanVar, DoubleVar, PhotoImage
)
from tkinter.ttk import (Button, Checkbutton, Combobox, Entry, Frame, Label, Labelframe, Menubutton, Notebook,
                         OptionMenu, Panedwindow, Progressbar, Radiobutton, Scale, Scrollbar, Separator, Sizegrip,
                         Spinbox, Treeview)

# Re-export tk widgets with original names BEFORE importing submodules
# This prevents circular import issues when submodules try to import these
Tk = _tkTk
Menu = _tkMenu
Text = _tkText
Canvas = _tkCanvas
TkFrame = _tkFrame  # Exported as TkFrame to avoid conflict with ttk.Frame

from ttkbootstrap import widgets as _widgets
from ttkbootstrap.style import Bootstyle, Style
from ttkbootstrap.widgets import DateEntry, Floodgauge, FloodgaugeLegacy, LabeledScale, M, Meter
from ttkbootstrap.window import Toplevel, Window

Bootstyle.setup_ttkbootstrap_api()

# Typing-time augmentation so local type checkers see `bootstyle`
# in constructors and `configure(...)` for ttk widgets imported from
# `ttkbootstrap` during development within this repo.
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

if TYPE_CHECKING:
    from tkinter import ttk as _ttk

    BootstyleArg = Union[str, Tuple[str, ...]]

    # TTK widgets with bootstyle parameter
    class Button(Button):
        """TTK Button widget with ttkbootstrap theming support.

        A button widget that can display text and images and invoke a command when pressed.

        Args:
            master: Parent widget.
            class_: Widget class name for styling.
            command: Function or method to call when button is pressed.
            compound: How to display text and image together (text, image, top, bottom, left, right, center, none).
            cursor: Cursor to display when mouse is over the widget.
            default: Whether button is the default button (normal, active, disabled).
            image: Image to display on the button.
            name: Widget name.
            padding: Extra space around the button contents.
            state: Widget state (normal, active, disabled, readonly).
            style: Custom ttk style name.
            takefocus: Whether widget accepts focus during keyboard traversal.
            text: Text to display on the button.
            textvariable: Variable linked to the button text.
            underline: Index of character to underline in text.
            width: Width of the button in characters.
            bootstyle: ttkbootstrap style keywords for theming (e.g., 'primary', 'success.outline').
                       Can be a string or tuple of keywords. Use this instead of 'style' for
                       ttkbootstrap theming.
        """
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            command: Any = ...,
            compound: Any = ...,
            cursor: str = ...,
            default: Any = ...,
            image: Any = ...,
            name: str = ...,
            padding: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            textvariable: Any = ...,
            underline: int = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Checkbutton(Checkbutton):
        """TTK Checkbutton widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            command: Any = ...,
            compound: Any = ...,
            cursor: str = ...,
            image: Any = ...,
            name: str = ...,
            offvalue: Any = ...,
            onvalue: Any = ...,
            padding: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            textvariable: Any = ...,
            underline: int = ...,
            variable: Any = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Combobox(Combobox):
        """TTK Combobox widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            background: str = ...,
            class_: str = ...,
            cursor: str = ...,
            exportselection: bool = ...,
            font: Any = ...,
            foreground: str = ...,
            height: int = ...,
            invalidcommand: Any = ...,
            justify: Any = ...,
            name: str = ...,
            postcommand: Any = ...,
            show: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            textvariable: Any = ...,
            validate: Any = ...,
            validatecommand: Any = ...,
            values: Any = ...,
            width: int = ...,
            xscrollcommand: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Entry(Entry):
        """TTK Entry widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            widget: Any = ...,
            *,
            background: str = ...,
            class_: str = ...,
            cursor: str = ...,
            exportselection: bool = ...,
            font: Any = ...,
            foreground: str = ...,
            invalidcommand: Any = ...,
            justify: Any = ...,
            name: str = ...,
            show: str = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            textvariable: Any = ...,
            validate: Any = ...,
            validatecommand: Any = ...,
            width: int = ...,
            xscrollcommand: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Frame(Frame):
        """TTK Frame widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            border: Any = ...,
            borderwidth: Any = ...,
            class_: str = ...,
            cursor: str = ...,
            height: Any = ...,
            name: str = ...,
            padding: Any = ...,
            relief: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Labelframe(Labelframe):
        """TTK Labelframe widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            border: Any = ...,
            borderwidth: Any = ...,
            class_: str = ...,
            cursor: str = ...,
            height: Any = ...,
            labelanchor: Any = ...,
            labelwidget: Any = ...,
            name: str = ...,
            padding: Any = ...,
            relief: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            underline: int = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Label(Label):
        """TTK Label widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            anchor: Any = ...,
            background: str = ...,
            border: Any = ...,
            borderwidth: Any = ...,
            class_: str = ...,
            compound: Any = ...,
            cursor: str = ...,
            font: Any = ...,
            foreground: str = ...,
            image: Any = ...,
            justify: Any = ...,
            name: str = ...,
            padding: Any = ...,
            relief: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            textvariable: Any = ...,
            underline: int = ...,
            width: Any = ...,
            wraplength: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Menubutton(Menubutton):
        """TTK Menubutton widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            compound: Any = ...,
            cursor: str = ...,
            direction: Any = ...,
            image: Any = ...,
            menu: Any = ...,
            name: str = ...,
            padding: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            textvariable: Any = ...,
            underline: int = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Notebook(Notebook):
        """TTK Notebook widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            cursor: str = ...,
            height: int = ...,
            name: str = ...,
            padding: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            width: int = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Panedwindow(Panedwindow):
        """TTK Panedwindow widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            cursor: str = ...,
            height: int = ...,
            name: str = ...,
            orient: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            width: int = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Progressbar(Progressbar):
        """TTK Progressbar widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            cursor: str = ...,
            length: Any = ...,
            maximum: float = ...,
            mode: Any = ...,
            name: str = ...,
            orient: Any = ...,
            phase: int = ...,
            style: str = ...,
            takefocus: Any = ...,
            value: float = ...,
            variable: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Radiobutton(Radiobutton):
        """TTK Radiobutton widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            command: Any = ...,
            compound: Any = ...,
            cursor: str = ...,
            image: Any = ...,
            name: str = ...,
            padding: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            text: Any = ...,
            textvariable: Any = ...,
            underline: int = ...,
            value: Any = ...,
            variable: Any = ...,
            width: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Scale(Scale):
        """TTK Scale widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            command: Any = ...,
            cursor: str = ...,
            from_: float = ...,
            length: Any = ...,
            name: str = ...,
            orient: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            to: float = ...,
            value: float = ...,
            variable: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Scrollbar(Scrollbar):
        """TTK Scrollbar widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            command: Any = ...,
            cursor: str = ...,
            name: str = ...,
            orient: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Separator(Separator):
        """TTK Separator widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            cursor: str = ...,
            name: str = ...,
            orient: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Sizegrip(Sizegrip):
        """TTK Sizegrip widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            cursor: str = ...,
            name: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Spinbox(Spinbox):
        """TTK Spinbox widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            background: str = ...,
            class_: str = ...,
            command: Any = ...,
            cursor: str = ...,
            exportselection: bool = ...,
            font: Any = ...,
            foreground: str = ...,
            format: str = ...,
            from_: float = ...,
            increment: float = ...,
            invalidcommand: Any = ...,
            justify: Any = ...,
            name: str = ...,
            show: Any = ...,
            state: str = ...,
            style: str = ...,
            takefocus: Any = ...,
            textvariable: Any = ...,
            to: float = ...,
            validate: Any = ...,
            validatecommand: Any = ...,
            values: Any = ...,
            width: int = ...,
            wrap: bool = ...,
            xscrollcommand: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class Treeview(Treeview):
        """TTK Treeview widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            *,
            class_: str = ...,
            columns: Any = ...,
            cursor: str = ...,
            displaycolumns: Any = ...,
            height: int = ...,
            name: str = ...,
            padding: Any = ...,
            selectmode: Any = ...,
            show: Any = ...,
            style: str = ...,
            takefocus: Any = ...,
            xscrollcommand: Any = ...,
            yscrollcommand: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    class OptionMenu(OptionMenu):
        """TTK OptionMenu widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any,
            variable: Any,
            default: Any = ...,
            *values: Any,
            style: str = ...,
            direction: Any = ...,
            command: Any = ...,
            bootstyle: Optional[BootstyleArg] = ...,
        ) -> None: ...
        def configure(self, cnf: Any = ..., *, bootstyle: Optional[BootstyleArg] = ..., **kwargs: Any) -> Any: ...
        config = configure

    # TK widgets with autostyle parameter
    class TkFrame(_tkFrame):
        """Tkinter Frame widget with ttkbootstrap theming support.

        A container widget that groups other tk widgets. Unlike ttk.Frame,
        this is the legacy tk.Frame widget with ttkbootstrap theming.

        Args:
            master: Parent widget.
            background: Background color of the frame.
            bd: Border width (alias for borderwidth).
            bg: Background color (alias for background).
            border: Border width (alias for borderwidth).
            borderwidth: Width of the border around the frame.
            class_: Widget class name.
            colormap: Colormap to use for the frame.
            container: Whether frame is a container for embedding.
            cursor: Cursor to display when mouse is over the widget.
            height: Height of the frame.
            highlightbackground: Color of focus highlight when widget does not have focus.
            highlightcolor: Color of focus highlight when widget has focus.
            highlightthickness: Width of focus highlight border.
            name: Widget name.
            padx: Horizontal padding inside the frame.
            pady: Vertical padding inside the frame.
            relief: 3D effect for the border (flat, raised, sunken, groove, ridge).
            takefocus: Whether widget accepts focus during keyboard traversal.
            visual: Visual information.
            width: Width of the frame.
            autostyle: If True (default), applies ttkbootstrap theme styling automatically.
                       Set to False to disable automatic theming and use custom styling.
        """
        def __init__(
            self,
            master: Any = ...,
            cnf: Optional[dict[str, Any]] = ...,
            *,
            background: str = ...,
            bd: Any = ...,
            bg: str = ...,
            border: Any = ...,
            borderwidth: Any = ...,
            class_: str = ...,
            colormap: Any = ...,
            container: bool = ...,
            cursor: str = ...,
            height: Any = ...,
            highlightbackground: str = ...,
            highlightcolor: str = ...,
            highlightthickness: Any = ...,
            name: str = ...,
            padx: Any = ...,
            pady: Any = ...,
            relief: str = ...,
            takefocus: Any = ...,
            visual: Any = ...,
            width: Any = ...,
            autostyle: bool = ...,
        ) -> None: ...

    class Tk(_tkTk):
        """Main tkinter root window with ttkbootstrap theming support."""
        def __init__(
            self,
            screenName: Optional[str] = ...,
            baseName: Optional[str] = ...,
            className: str = ...,
            useTk: bool = ...,
            sync: bool = ...,
            use: Optional[str] = ...,
            *,
            autostyle: bool = ...,
        ) -> None: ...

    class Menu(_tkMenu):
        """Tkinter Menu widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            cnf: Optional[dict[str, Any]] = ...,
            *,
            activebackground: str = ...,
            activeborderwidth: Any = ...,
            activeforeground: str = ...,
            background: str = ...,
            bd: Any = ...,
            bg: str = ...,
            border: Any = ...,
            borderwidth: Any = ...,
            cursor: str = ...,
            disabledforeground: str = ...,
            fg: str = ...,
            font: Any = ...,
            foreground: str = ...,
            name: str = ...,
            postcommand: Any = ...,
            relief: str = ...,
            selectcolor: str = ...,
            takefocus: Any = ...,
            tearoff: Any = ...,
            tearoffcommand: Any = ...,
            title: str = ...,
            type: str = ...,
            autostyle: bool = ...,
        ) -> None: ...

    class Text(_tkText):
        """Tkinter Text widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            cnf: Optional[dict[str, Any]] = ...,
            *,
            autoseparators: bool = ...,
            background: str = ...,
            bd: Any = ...,
            bg: str = ...,
            blockcursor: bool = ...,
            borderwidth: Any = ...,
            cursor: str = ...,
            endline: Any = ...,
            exportselection: bool = ...,
            fg: str = ...,
            font: Any = ...,
            foreground: str = ...,
            height: Any = ...,
            highlightbackground: str = ...,
            highlightcolor: str = ...,
            highlightthickness: Any = ...,
            inactiveselectbackground: str = ...,
            insertbackground: str = ...,
            insertborderwidth: Any = ...,
            insertofftime: int = ...,
            insertontime: int = ...,
            insertwidth: Any = ...,
            maxundo: int = ...,
            name: str = ...,
            padx: Any = ...,
            pady: Any = ...,
            relief: str = ...,
            selectbackground: str = ...,
            selectborderwidth: Any = ...,
            selectforeground: str = ...,
            setgrid: bool = ...,
            spacing1: Any = ...,
            spacing2: Any = ...,
            spacing3: Any = ...,
            startline: Any = ...,
            state: str = ...,
            tabs: Any = ...,
            tabstyle: str = ...,
            takefocus: Any = ...,
            undo: bool = ...,
            width: Any = ...,
            wrap: str = ...,
            xscrollcommand: Any = ...,
            yscrollcommand: Any = ...,
            autostyle: bool = ...,
        ) -> None: ...

    class Canvas(_tkCanvas):
        """Tkinter Canvas widget with ttkbootstrap theming support."""
        def __init__(
            self,
            master: Any = ...,
            cnf: Optional[dict[str, Any]] = ...,
            *,
            background: str = ...,
            bd: Any = ...,
            bg: str = ...,
            border: Any = ...,
            borderwidth: Any = ...,
            closeenough: float = ...,
            confine: bool = ...,
            cursor: str = ...,
            height: Any = ...,
            highlightbackground: str = ...,
            highlightcolor: str = ...,
            highlightthickness: Any = ...,
            insertbackground: str = ...,
            insertborderwidth: Any = ...,
            insertofftime: int = ...,
            insertontime: int = ...,
            insertwidth: Any = ...,
            name: str = ...,
            offset: Any = ...,
            relief: str = ...,
            scrollregion: Any = ...,
            selectbackground: str = ...,
            selectborderwidth: Any = ...,
            selectforeground: str = ...,
            state: str = ...,
            takefocus: Any = ...,
            width: Any = ...,
            xscrollcommand: Any = ...,
            xscrollincrement: Any = ...,
            yscrollcommand: Any = ...,
            yscrollincrement: Any = ...,
            autostyle: bool = ...,
        ) -> None: ...

__all__ = [
    # Tk exports
    Tk, Menu, Text, Canvas, TkFrame, Variable, StringVar, IntVar, BooleanVar, DoubleVar,
    PhotoImage, LabelFrame,

    # TTk exports
    Button, Checkbutton, Combobox, Entry, Frame, Labelframe,
    Label, Menubutton, Notebook, Panedwindow, Progressbar, Radiobutton,
    Scale, Scrollbar, Separator, Sizegrip, Spinbox,
    Treeview, OptionMenu,

    # TTkBootstrap exports
    Bootstyle,
    Style,
    Toplevel,
    Window,
    DateEntry,
    Floodgauge,
    FloodgaugeLegacy,
    LabeledScale,
    Meter,
    M
]
