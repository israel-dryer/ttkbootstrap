"""
    This module contains a class of the same name that wraps the 
    tkinter.Tk and ttkbootstrap.style.Style classes to provide a more
    consolidated api for initial application startup.
"""
import tkinter
from ttkbootstrap.constants import *
from ttkbootstrap.publisher import Publisher
from ttkbootstrap.style import Style
from ttkbootstrap.icons import Icon
from ttkbootstrap import utility


def get_default_root(what=None):
    """Returns the default root if it has been created, otherwise
    returns a new instance."""
    if not tkinter._support_default_root:
        raise RuntimeError("No master specified and tkinter is "
                           "configured to not support default root")
    if not tkinter._default_root:
        if what:
            raise RuntimeError(f"Too early to {what}: no default root window")
        root = tkinter.Tk()
        assert tkinter._default_root is root
    return tkinter._default_root


def apply_class_bindings(window: tkinter.Widget):
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

    def button_default_binding(event):
        """The default keybind on a button when the return or enter key
        is pressed and the button has focus or is the default button."""
        try:
            widget = window.nametowidget(event.widget)
            widget.invoke()
        except KeyError:
            window.tk.call(event.widget, 'invoke')

    window.bind_class("TButton", "<Key-Return>", button_default_binding,
                      add="+")
    window.bind_class("TButton", "<KP_Enter>", button_default_binding, add="+")


def apply_all_bindings(window: tkinter.Widget):
    """Add bindings to all widgets in the application"""
    window.bind_all('<Map>', on_map_child, '+')
    window.bind_all('<Destroy>', lambda e: Publisher.unsubscribe(e.widget))


def on_disabled_readonly_state(event):
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


def on_map_child(event):
    """Callback for <Map> event which generates a <<MapChild>> virtual
    event on the parent"""
    widget: tkinter.Widget = event.widget
    try:
        if widget.master is None: # root widget
            return
        else:
            widget.master.event_generate('<<MapChild>>')
    except:
        # not a tkinter widget that I'm handling (ex. Combobox.popdown)
        return


def on_select_all(event):
    """Callback to select all text in the input widget when an event is
    executed."""
    widget = event.widget
    if widget.__class__.__name__ == "Text":
        widget.tag_add(SEL, "1.0", END)
        widget.mark_set(INSERT, END)
        widget.see(END)
    else:
        widget.select_range(0, END)
        widget.icursor(END)
    return 'break'    


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
        title="ttkbootstrap",
        themename="litera",
        iconphoto='',
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None,
        transient=None,
        overrideredirect=False,
        alpha=1.0,
    ):
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

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Window.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (Tuple[bool, bool]):
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
        """
        if hdpi:
            utility.enable_high_dpi_awareness()

        super().__init__()
        self.winsys = self.tk.call('tk', 'windowingsystem')

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
                self.wait_visibility(self)
            self.attributes("-alpha", alpha)

        apply_class_bindings(self)
        apply_all_bindings(self)
        self._style = Style(themename)


    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return self._style

    def place_window_center(self):
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

    position_center = place_window_center # alias


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
        title="ttkbootstrap",
        iconphoto='',
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        transient=None,
        overrideredirect=False,
        windowtype=None,
        topmost=False,
        toolwindow=False,
        alpha=1.0,
        **kwargs,
    ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method.
                By default the application icon is used.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.

            resizable (Tuple[bool, bool]):
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
        self.winsys = self.tk.call('tk', 'windowingsystem')
        
        if iconify:
            self.iconify()

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
                self.wait_visibility(self)
            self.attributes("-alpha", alpha)

    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return Style()

    def place_window_center(self):
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

    position_center = place_window_center # alias

if __name__ == "__main__":

    root = Window(themename="superhero", alpha=0.5, size=(1000, 1000))
    #root.withdraw()
    root.place_window_center()
    #root.deiconify()

    top = Toplevel(title="My Toplevel", alpha=0.4, size=(1000, 1000))
    top.place_window_center()

    root.mainloop()
