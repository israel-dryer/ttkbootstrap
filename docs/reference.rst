Reference
=========
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
    :members:

Style
-----
Sets the theme of the ``tkinter.Tk`` instance and supports all ttkbootstrap and ttk themes provided. This class is meant
to be a drop-in replacement for ``ttk.Style`` and inherits all of it's methods and properties. Creating a ``Style``
object will instantiate the ``tkinter.Tk`` instance in the ``Style.master`` property, and so it is not
necessary to explicitly create an instance of ``tkinter.Tk``. For more details on the ``ttk.Style`` class, see the
python documentation_.

.. code-block:: python

    # instantiate the style with default theme *flatly*
    style = Style()

    # instantiate the style with another theme
    style = Style(theme='superhero')

    # instantiate the style with a theme from a specific themes file
    style = Style(theme='custon_name', themes_file='C:/example/my_themes.json')

    # available themes
    for theme in style.theme_names():
        print(theme)

.. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style

.. autoclass:: ttkbootstrap.Style
    :show-inheritance:
    :members:


StylerTTK
---------
A class to create a new ttk theme by using a combination of built-in themes and some image-based elements using
``pillow``. A theme is generated at runtime and is available to use with the ``Style`` class methods.
The base theme of all ttkbootstrap themes is *clam*. In many cases, widget layouts are re-created using an
assortment of elements from various styles such as *clam*, *alt*, *default*, etc...

.. autoclass:: ttkbootstrap.StylerTTK
    :show-inheritance:
    :members:

StylerTK
--------
A class for styling tkinter widgets (not ttk). Several ttk widgets utilize tkinter widgets in some capacity, such
as the *popdownlist* on the ``ttk.Combobox``. To create a consistent user experience, standard tkinter widgets are
themed as much as possible with the look and feel of the ttkbootstrap theme applied. Tkinter widgets are not the
primary target of this project; however, they can be used without looking entirely out-of-place in most cases.

.. autoclass:: ttkbootstrap.StylerTK
    :show-inheritance:
    :members:

ThemeDefinition
---------------
Contains the basic theme definition for name, colors, and font.

.. autoclass:: ttkbootstrap.ThemeDefinition
    :show-inheritance:
    :members:
