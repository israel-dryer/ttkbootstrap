"""Window and Toplevel classes for ttkbootstrap applications.

This module provides enhanced Window and Toplevel classes that wrap tkinter.Tk
and tkinter.Toplevel with integrated ttkbootstrap Style support, providing a
consolidated API for application initialization and window creation.

Classes:
    Window: Main application window (wraps tk.Tk with Style)
    Toplevel: Top-level popup window (wraps tk.Toplevel with Style)

Features:
    - Integrated ttkbootstrap theme support
    - Simplified window configuration (size, position, title, etc.)
    - High-DPI awareness configuration
    - Window positioning utilities (center, place)
    - Alpha transparency support
    - Icon management (PhotoImage or file path)
    - Resizable window control
    - Theme-aware styling

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    # Create main window with theme
    root = ttk.Window(
        title="My Application",
        themename="darkly",
        size=(800, 600),
        position=(100, 100),
        resizable=(True, True)
    )

    # Add widgets
    ttk.Label(root, text="Hello, World!").pack(padx=20, pady=20)
    ttk.Button(root, text="Click Me", bootstyle="success").pack()

    # Create toplevel popup
    popup = ttk.Toplevel(title="Popup Window")
    popup.geometry("400x300")

    root.mainloop()
    ```
"""
import tkinter
from typing import Any, Optional, Tuple, Union

from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Icon
from ttkbootstrap.publisher import Publisher
from ttkbootstrap.style import Style


def get_default_root(what: Optional[str] = None) -> tkinter.Tk:
    """Returns the default root if it has been created, otherwise
    returns a new instance."""
    if not tkinter._support_default_root:
        raise RuntimeError(
            "No master specified and tkinter is "
            "configured to not support default root")
    if not tkinter._default_root:
        if what:
            raise RuntimeError(f"Too early to {what}: no default root window")
        root = tkinter.Tk()
        assert tkinter._default_root is root
    return tkinter._default_root


def apply_class_bindings(window: tkinter.Widget) -> None:
    """Add class level event bindings in application"""
    for className in ["TEntry", "TSpinbox", "TCombobox", "Text"]:
        window.bind_class(
            className=className,
            sequence="<Configure>",
            func=on_disabled_readonly_state,
            add="+")

        for sequence in ["<Control-a>", "<Control-A>"]:
            window.bind_class(
                className=className,
                sequence=sequence,
                func=on_select_all)

    window.unbind_class("TButton", "<Key-space>")

    def button_default_binding(event: tkinter.Event) -> None:
        """The default keybind on a button when the return or enter key
        is pressed and the button has focus or is the default button."""
        try:
            widget = window.nametowidget(event.widget)
            widget.invoke()
        except KeyError:
            window.tk.call(event.widget, 'invoke')

    window.bind_class(
        "TButton", "<Key-Return>", button_default_binding,
        add="+")
    window.bind_class("TButton", "<KP_Enter>", button_default_binding, add="+")


def apply_all_bindings(window: tkinter.Widget) -> None:
    """Add bindings to all widgets in the application"""
    window.bind_all('<Map>', on_map_child, '+')
    window.bind_all('<Destroy>', lambda e: Publisher.unsubscribe(e.widget))


def on_visibility(event: tkinter.Event) -> None:
    """Set Window or Toplevel alpha value on Visibility (X11)"""
    widget = event.widget
    if isinstance(widget, (Window, Toplevel)) and widget.alpha_bind:
        widget.unbind(widget.alpha_bind)
        widget.attributes("-alpha", widget.alpha)


def on_disabled_readonly_state(event: tkinter.Event) -> None:
    """Change the cursor of entry type widgets to 'arrow' if in a
    disabled or readonly state."""
    try:
        widget = event.widget
        state = str(widget.cget('state'))
        cursor = str(widget.cget('cursor'))
        if state in (DISABLED, READONLY):
            if cursor == 'arrow':
                return
            else:
                widget['cursor'] = 'arrow'
        else:
            if cursor in ('ibeam', ''):
                return
            else:
                widget['cursor'] = None
    except:
        pass


def on_map_child(event: tkinter.Event) -> None:
    """Callback for <Map> event which generates a <<MapChild>> virtual
    event on the parent"""
    widget: tkinter.Widget = event.widget
    try:
        if widget.master is None:  # root widget
            return
        else:
            widget.master.event_generate('<<MapChild>>')
    except:
        # not a tkinter widget that I'm handling (ex. Combobox.popdown)
        return


def on_select_all(event: tkinter.Event) -> None:
    """Callback to select all text in Entry or Text widget when Ctrl+A is pressed."""
    widget = event.widget

    if isinstance(widget, tkinter.Text):
        widget.tag_add(SEL, "1.0", END)
        widget.mark_set(INSERT, END)
        widget.see(INSERT)
    elif isinstance(widget, tkinter.Entry):
        widget.selection_range(0, END)
        widget.icursor(END)


class Window(tkinter.Tk):
    """A class that wraps the tkinter.Tk class in order to provide a
    more convenient api with additional bells and whistles. For more
    information on how to use the inherited `Tk` methods, see the
    [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Tk).

    ![](../../assets/window/window-toplevel.png)

    Examples:

        ```python
        app = Window(title="My Application", themename="superhero")
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            themename: str = "litera",
            iconphoto: Optional[str] = '',
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            hdpi: bool = True,
            scaling: Optional[float] = None,
            transient: Optional[tkinter.Misc] = None,
            overrideredirect: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            themename (str):
                The name of the ttkbootstrap theme to apply to the
                application.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method
                and the image will be the default icon for all windows.
                A ttkbootstrap image is used by default. To disable
                this default behavior, set the value to `None` and use
                the `Tk.iconphoto` or `Tk.iconbitmap` methods directly.

            size (tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Window.geometry`
                method.

            minsize (tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Window.resizable` method.

            hdpi (bool):
                Enable high-dpi support for Windows OS. This option is
                enabled by default.

            scaling (float):
                Sets the current scaling factor used by Tk to convert
                between physical units (for example, points, inches, or
                millimeters) and pixels. The number argument is a
                floating point number that specifies the number of pixels
                per point on window's display.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Window.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is passed to the
                `Window.overrideredirect(1)` method.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs:
                Any other keyword arguments that are passed through to tkinter.Tk() constructor
                List of available keywords available at: https://docs.python.org/3/library/tkinter.html#tkinter.Tk
        """
        if hdpi:
            utility.enable_high_dpi_awareness()

        super().__init__(**kwargs)
        self.winsys: str = self.tk.call('tk', 'windowingsystem')

        if scaling is not None:
            utility.enable_high_dpi_awareness(self, scaling)

        if iconphoto is not None:
            if iconphoto == '':
                # the default ttkbootstrap icon
                self._icon = tkinter.PhotoImage(master=self, data=Icon.icon)
                self.iconphoto(True, self._icon)
            else:
                try:
                    # the user provided an image path
                    self._icon = tkinter.PhotoImage(file=iconphoto, master=self)
                    self.iconphoto(True, self._icon)
                except tkinter.TclError:
                    # The fallback icon if the user icon fails.
                    print('iconphoto path is bad; using default image.')
                    self._icon = tkinter.PhotoImage(data=Icon.icon, master=self)
                    self.iconphoto(True, self._icon)

        self.title(title)

        if size is not None:
            width, height = size
            self.geometry(f"{width}x{height}")

        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")

        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)

        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)

        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)

        if transient is not None:
            self.transient(transient)

        if overrideredirect:
            self.overrideredirect(1)

        if alpha is not None:
            if self.winsys == 'x11':
                self.alpha = alpha
                self.alpha_bind = self.bind("<Visibility>", on_visibility, '+')
            else:
                self.attributes("-alpha", alpha)

        apply_class_bindings(self)
        apply_all_bindings(self)
        self._style = Style(themename)

    @property
    def style(self) -> Style:
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return self._style

    def destroy(self) -> None:
        """Destroy the window and all its children."""
        self._style.instance = None
        super().destroy()

    def place_window_center(self) -> None:
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    position_center = place_window_center  # alias


class Toplevel(tkinter.Toplevel):
    """A class that wraps the tkinter.Toplevel class in order to
    provide a more convenient api with additional bells and whistles.
    For more information on how to use the inherited `Toplevel`
    methods, see the [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/toplevel.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel).

    ![](../../assets/window/window-toplevel.png)

    Examples:

        ```python
        app = Toplevel(title="My Toplevel")
        app.mainloop()
        ```
    """

    def __init__(
            self,
            title: str = "ttkbootstrap",
            iconphoto: str = '',
            size: Optional[Tuple[int, int]] = None,
            position: Optional[Tuple[int, int]] = None,
            minsize: Optional[Tuple[int, int]] = None,
            maxsize: Optional[Tuple[int, int]] = None,
            resizable: Optional[Tuple[bool, bool]] = None,
            transient: Optional[tkinter.Misc] = None,
            overrideredirect: bool = False,
            windowtype: Optional[str] = None,
            topmost: bool = False,
            toolwindow: bool = False,
            alpha: float = 1.0,
            **kwargs: Any,
    ) -> None:
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method.
                By default the application icon is used.

            size (tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry`
                method.

            minsize (tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.

            maxsize (tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.

            resizable (tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Toplevel.resizable` method.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Toplevel.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`.

            windowtype (str):
                On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', windowtype)`.

                See the [-type option](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                for a list of available options.

            topmost (bool):
                Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.

            toolwindow (bool):
                On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if 'iconify' in kwargs:
            iconify = kwargs.pop('iconify')
        else:
            iconify = None

        super().__init__(**kwargs)
        self.winsys: str = self.tk.call('tk', 'windowingsystem')

        if iconphoto != '':
            try:
                # the user provided an image path
                self._icon = tkinter.PhotoImage(file=iconphoto, master=self)
                self.iconphoto(True, self._icon)
            except tkinter.TclError:
                # The fallback icon if the user icon fails.
                print('iconphoto path is bad; using default image.')
                pass

        self.title(title)

        if size is not None:
            width, height = size
            self.geometry(f'{width}x{height}')

        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")

        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)

        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)

        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)

        if iconify:
            self.iconify()

        if transient is not None:
            self.transient(transient)

        if overrideredirect:
            self.overrideredirect(1)

        if windowtype is not None:
            if self.winsys == 'x11':
                self.attributes("-type", windowtype)

        if topmost:
            self.attributes("-topmost", 1)

        if toolwindow:
            if self.winsys == 'win32':
                self.attributes("-toolwindow", 1)

        if alpha is not None:
            if self.winsys == 'x11':
                self.alpha = alpha
                self.alpha_bind = self.bind("<Visibility>", on_visibility, '+')
            else:
                self.attributes("-alpha", alpha)

    @property
    def style(self) -> Style:
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return Style()

    def place_window_center(self) -> None:
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    position_center = place_window_center  # alias


if __name__ == "__main__":
    root = Window(themename="superhero", alpha=0.5, size=(1000, 1000))
    # root.withdraw()
    root.place_window_center()
    # root.deiconify()

    top = Toplevel(title="My Toplevel", alpha=0.4, size=(1000, 1000))
    top.place_window_center()

    root.mainloop()
