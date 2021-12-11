"""
    This module contains a class of the same name that wraps the 
    tkinter.Tk and ttkbootstrap.style.Style classes to provide a more
    consolidated api for initial application startup.

    !!! warning
        This module is experimental.
"""
import tkinter
from ttkbootstrap.style import Style
from ttkbootstrap.icons import Icon
from ttkbootstrap import utility


class Window(tkinter.Tk):
    """A class that wraps the tkinter.Tk class in order to provide a
    more convenient api with additional bells and whistles. For more 
    information on how to use the inherited `Tk` methods, see the 
    [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Tk).

    Examples:

        ```python
        app = Window(title="My Application", themename="superhero")
        app.mainloop()
        ```
    """

    def __init__(
        self, 
        title='ttkbootstrap', 
        themename='litera', 
        iconphoto=None,
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None
        ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            themename (str):
                The name of the ttkbootstrap theme to apply to the 
                application.

            iconphoto (PhotoImage):
                The titlebar icon. This image is applied to all future
                toplevels as well.    
           
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
        """
        if hdpi:
            utility.enable_high_dpi_awareness()
        
        super().__init__()
        
        if scaling:
            utility.enable_high_dpi_awareness(self, scaling)

        self._icon = iconphoto or tkinter.PhotoImage(data=Icon.icon)
        self.iconphoto(True, self._icon)
        self.title(title)

        if size:
            width, height = size
            self.geometry(f'{width}x{height}')

        if position:
            xpos, ypos = position
            self.geometry(f'+{xpos}+{ypos}')

        if minsize: 
            width, height = minsize
            self.minsize(width, height)

        if maxsize:
            width, height
            self.maxsize(width, height)

        if resizable:
            width, height = resizable
            self.resizable(width, height)

        self._style = Style(themename)

    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return self._style

    def move_to_center(self):
        """Position the window in the center of the screen. Does not
        account for the titlebar when placing the window.
        """
        self.eval('tk::PlaceWindow . center')


if __name__ == '__main__':

    utility.enable_high_dpi_awareness()
    root = Window(themename='superhero')
    root.update_idletasks()
    root.mainloop()

