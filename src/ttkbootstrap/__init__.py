"""
    A library for using and creating modern ttk themed applications

    :Author: Israel Dryer

    :Modified: 2021-03-24

    Why does this project exist?
    ============================
    Because... the people need to be able to build modern nice-looking applications. Tkinter is a powerful, and
    fantastic tool that is significantly under-appreciated and overlooked for building modern GUI's. I built this
    project by leveraging the power of ``ttk's`` theme engine to create a large collection of professional and
    asthetically pleasing themes, which are inspired by, and in some cases, whole-sale rip-off's of the themes found
    on https://bootswatch.com/.

    A bootstrap approach to style
    =============================
    Many people are familiar with bootstrap for web developement. It comes pre-packaged with lots of built in css
    classes for styling a webpage. I took the same approach with this project by pre-defining styles for nearly all
    ``ttk`` widgets that allow you to easily use colors from the theme's color palette for your widget. So, if you want
    a button in the secondary theme color, simply apply the ``secondary.TButton`` style to the button. Or, if you want
    a blue outlined button, apply the ``info.Outline.TButton`` style to your button.

    How I built this project
    ========================
    Each ``ttk`` widget is created from a collection of elements. There is an old, but excellent reference to this
    https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-themes.html.

    By using the ``ttk.Style.theme_create`` method, I was able to copy the parts of the built-in themes that I like to
    create completely new and modern looking themes. For example, the ``ttk.Combobox`` widget uses the *field* element
    from the ``ttk.Spinbox``. This allowed me to create the border effect I wanted.  Another example is that I used the
    *clam* theme as the base for my ``ttk.Treeview``, but I used the indicator from the *alt* theme. The reason is that
    I think it just looks nicer.

    All themes are built using the *clam* theme as a base. The *clam* theme provides a lot of flexibilty when it comes
    to borders, so I was able to get some nice focus and hover ring effects (similar to what you see in the Bootstrap
    form widgets) by leveraging this feature.

    I decided to use ``pillow`` to draw the ``ttk.Scale`` widget on the fly for each theme because the look was so much
    better than the old native look. Hopefully this will not be a noticeable performance issue, and it does require you
    to pip install ``pillow``. However, I think the final result is worth this sacrifice. The biggest drawback is that
    I was only able to theme the ``ttk.Scale`` widget with the primary color of the theme. So, it does not have all the
    color options that most of the other widgets have.

    .. note::
        For Windows, I'm using the ``ttk.Checkbutton`` and ``ttk.Radiobutton`` from the *xpnative* theme. For Linux and
        MacOS, these widgets default to the *clam* theme elements.

    What about the old tkinter widgets?
    ===================================
    Some of the ``ttk`` widgets utilize existing ``tkinter`` widgets. For example: the popdown list in the
    ``ttk.Combobox`` or the ``ttk.OptionMenu``. To make sure these widgets didn't stick out like a sore thumb, I created
    a ``StyleTK`` class to apply the same color and style, as much as it was possible, to these legacy widgets. While
    these legacy widgets are not necessarily intended to be used, they are available if needed, and shouldn't look
    complete out-of-place in your ``ttkbootstrap`` themed application.
"""
from .styler import Style, Colors, StylerTTK, ThemeSettings