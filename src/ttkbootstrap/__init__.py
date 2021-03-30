"""
    Izzy-Themes
        A package for creating modern ttk (tkinter) by customizing built-in ttk themes.

    Author
        Israel Dryer

    Modified
        2021-03-24


    PURPOSE:
        The purpose of this package is to provide a simple and easy to use api for creating modern ttk themes using
        the themes that are already built into Tkinter and Python.

    APPROACH:
        I've created several new widget layouts using the parts of existing themes. For example, the Combobox widget
        uses the field element from the Spinbox so that I could create the border effect I wanted.  Another example is
        the Treeview, which uses the indicator from the `alt` theme, because I just think it looks nicer.

        For Windows, I'm using the checkbutton and radiobutton from the `xpnative` theme. For Linux and MacOS, it defaults
        the the clam theme elements.

        I decided to use PILLOW to draw the scale widget on the fly for each theme because the look was so much better than
        the native looks. Hopefully this will not be a noticeable performance issue, and it does require you to pip install
        pillow (PIL).

        I decided to use the clam theme as the base for much of this project because it provides a lot of flexibility when
        it comes to borders. Because the clam theme has an outer border and an inner border (light & dark), I am able to use
        the states to create a focus ring effect that is similar to what you would find with a CSS Boostrap theme. There
        are many cool tricks and hacks that you can tease out of the existing set of themes,  so I hope you enjoy this
        library as well as using the bones to create something of your own.

    USING STANDARD TK WIDGETS (WARNING):
        There are some widgets in TTK that borrow from standard TK widgets, such as the popdown list in the TTK
        combobox, or the dropdown menu. To make sure the style for these legacy widgets is consistent, I've created
        a StyleTK class that takes care of styling these widgets. However, because with TK the styling is
        tightly-coupled with the widget creation, you cannot easily change the style of a widget that is built with
        standard TK options --- unlike with TTK, which separates the style and structure of the elements. So, if you
        plan to do anything fancy, like support light and dark changeable themes, you'll need to make sure you
        create a mechanism for manually configuring the style of the standard TK widget. You can also destroy and then
        re-create the window as I have done in the example (actually I'm building the entire inside frame and then
        rebuilding when the style changes).
"""
from .styler import Style, Colors, StylerTTK, ThemeSettings