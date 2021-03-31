Reference
=========
Style
-----
Sets the theme of the ``tkinter.Tk`` instance and supports all ttkbootstrap and ttk themes provided. This class is meant
to be a drop-in replacement for ``ttk.Style`` and inherits all of it's methods and properties. Creating a ``Style``
object will instantiate the ``tkinter.Tk`` instance in the ``Style.master`` property, and so it is not
necessary to explicitly create an instance of ``tkinter.Tk``. For more details on the ``ttk.Style`` class, see the
python documentation_.

.. code-block:: python

    # instantiate the style and apply a theme
    style = Style()
    style.theme_use('lumen')

    # available themes
    for theme in style.theme_names():
        print(theme)

.. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style

.. autoclass:: ttkbootstrap.Style
    :show-inheritance:
    :special-members:
    :members:

.. _colors:

Colors
------
A class that contains the theme colors as well as several helper methods for manipulating colors. This class is attached
to the ``Style`` object at run-time for the selected theme, and so is available to use with ``Style.colors``. The colors
can be accessed via dot notation or get method:

.. code-block:: python

    # dot-notation
    Colors.primary

    # get method
    Colors.get('primary')

This class is an iterator, so you can iterate over the main style color labels (primary, secondary, success, info, warning,
danger):

.. code-block:: python

    for color_label in Colors:
        color = Colors.get(color_label)
        print(color_label, color)

If, for some reason, you need to iterate over all theme color labels, then you can use the ``Colors.label_iter`` method.
This will include all theme colors, including border, fg, bg, etc...

.. code-block:: python

    for color_label in Colors.label_iter():
        color = Colors.get(color_label)
        print(color_label, color)

.. autoclass:: ttkbootstrap.Colors
    :show-inheritance:
    :special-members:
    :members:
