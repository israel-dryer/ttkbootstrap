from tkinter import Tk
from tkinter import ttk


class Button(ttk.Button):

    def __init__(self, parent=None, **kwargs):
        """Ttk button widget, displays as a textual label and/or image, and evaluates a command when pressed.

        Args:
            parent (Widget): The parent widget.

        Keyword Args:
            class (str): Specifies the window class. The class is used when querying the option database for the
                window's other options, to determine the default bindtags for the window, and to select the widget's
                default layout and style. This is a read-only option; it may only be specified when the window is
                created, and may not be changed with the configure widget command.
            compound (str): Specifies if the widget should display text and bitmaps/images at the same time, and if so,
                where the bitmap/image should be placed relative to the text. Must be one of the values **none**,
                **bottom**, **top**, **left**, **right**, or **center**. For example, the (default) value **none**
                specifies that the bitmap or image should (if defined) be displayed `instead` of the text, the value
                **left** specifies that the bitmap or image should be displayed to the `left` of the text, and the value
                **center** specifies that the bitmap or image should be displayed `underneath` the text.
            cursor (str): Specifies the mouse cursor to be used for the widget. Names and values will vary according to
                your operating system. Examples can be found here:
                https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
            image (PhotoImage or str): Specifies an image to display in the widget, which must have been created
                with ``tk.PhotoImage`` or `TkPhotoImage`` if using **pillow**. Can also be a string representing the
                name of the photo if the photo has been given a name using the ``name`` parameter.  Typically, if the
                ``image`` option is specified then it overrides other options that specify a bitmap or textual value to
                display in the widget, though this is controlled by the ``compound`` option; the ``image`` option may be
                reset to an empty string to re-enable a bitmap or text display.
            state (str): May be set to **normal** or **disabled** to control the `disabled` state bit. This is a
                write-only option; setting it changes the widget state, but the state widget command does not affect the
                ``state`` option.
            style (str): May be used to specify a custom widget style.
            takefocus (bool): Determines whether the window accepts the focus during keyboard traversal (e.g., Tab and
                Shift-Tab). To remove the widget from focus traversal, use ``takefocus=False``.
            text (str): Specifies a string to be displayed inside the widget.
            textvariable (StringVar or str): Specifies the name of a variable. Use the ``StringVar`` or the string
                representation if the variable has been named. The value of the variable is a text string to be
                displayed inside the widget; if the variable value changes then the widget will automatically update
                itself to reflect the new value.
            underline (int): Specifies the integer index of a character to underline in the widget. This option is used
                by the default bindings to implement keyboard traversal for menu buttons and menu entries. 0 corresponds
                to the first character of the text displayed in the widget, 1 to the next character, and so on.
            width (int): If the label is text, this option specifies the absolute width of the text area on the button,
                as a number of characters; the actual width is that number multiplied by the average width of a
                character in the current font. For image labels, this option is ignored. The option may also be
                configured in a style.
            command (func): A callback function to evaluate when the widget is invoked.
        """
        super().__init__(parent, **kwargs)
