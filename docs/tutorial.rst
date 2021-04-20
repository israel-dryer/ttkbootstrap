Tutorial
########
**ttkbootstrap** works by generating pre-defined themes at runtime which you can then apply and use as you would any
built-in ``ttk`` theme such as **clam**, **alt**, **classic**, etc... You also have the ability to
`create a new theme`_ using the **ttkcreator** application.

Simple usage
============
.. code-block:: python

    from ttkbootstrap import Style
    from tkinter import ttk

    style = Style()

    window = style.master
    ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)
    ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)
    window.mainloop()


This results in the window below:

.. image:: images/submit.png

If you do not create an instance of ``Tk()``, the ``Style`` object automatically creates one. You can access this root
window through the **master** property.

By default, the **flatly** theme will be applied to the application if you do not explicitly select one.

If you want to use a different theme, you can pass the style name as a keyword argument when you create the ``style``
object:

.. code-block:: python

    style = Style(theme='darkly')


.. note:: Check out the :ref:`visual style guide <widgets-section>` for each widget. Here you will find an image
    for each available widget style, as well as information on how to apply and modify styles as needed for each widget.

Choose a theme
==============
**ttkbootstrap** *light* and *dark* themes are generated at run-time. Generally, the ``ttkbootstrap.Style`` api is
identical to the ``ttk.Style`` api. See the `Python documentation on styling`_ to learn more about this class.

.. _`Python documentation on styling`: https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling

To use a **ttkbootstrap** theme, create a ``ttkbootstrap.Style`` and pass in the name of the theme you want to use.

.. code-block:: python

    style = Style(theme='superhero')

If you want to load a theme from a specific file (for example, to release an application with a custom theme), you can
use the ``user_themes`` argument:

.. code-block:: python

    style = Style(theme='custom_name', themes_file='C:/example/my_themes.json')

If for some reason you need to change the theme *after* the window has already been created, you will need to use the
``Style.theme_use`` method, which is what ``ttkbootstrap.Style`` does internally when instantiated.

To get a list of all available themes:

.. code-block:: python

    style.theme_names()

Currently, the available pre-defined themes include:

:light: cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
:dark: cyborg - darkly - solar - superhero


Use themed widgets
==================
**ttkbootstrap** includes many *pre-defined widget styles* that you can apply with the ``style`` option on ttk widgets.
The style pattern  is ``Color.WidgetClass`` where the color is a prefix to the ttk widget class. Most widgets include a
style pattern for each main theme color (primary, secondary, success, info, warning, danger).

For example, the ``ttk.Button`` has a widget class of *TButton*. The style patterns available on the button include:

    * primary.TButton
    * secondary.TButton
    * success.TButton
    * info.TButton
    * warning.TButton
    * danger.TButton

These style patterns produce the following buttons:

.. image:: images/color-options.png

Consider the following example, which also shows the *Outline* style that is available on buttons:

.. code-block:: python

    # solid button
    ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)

    # outline button
    ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)

.. image:: images/submit.png

.. note::

    While all widgets are themed, not all have themed color styles available, such as ``ttk.PanedWindow`` or the
    ``ttk.Scrollbar``. Instead, these widgets are styled with a default theme color.

Modify a style
==============
In a large application, you may need to customize widget styles. I've done this in several of :ref:`gallery applications
<gallery-applications>`. To customize a style, you need to create a ``Style`` object first and then use the ``configure``
method using the pattern ``newName.oldName``. In the :ref:`File Backup Utility <file-backup-utility>`, I created a
custom style for a frame that used the background color of the theme border.

For this example, let's say that color is *gray*.

.. code-block:: python

    style = Style()
    style.configure('custom.TFrame', background='gray')

This would create a frame style with the background color of gray. To apply this new style, I would create a frame and
then use the *style* option to set the new style.

.. code-block:: python

    myframe = ttk.Frame(style='custom.TFrame')

There is a widget style class whose name is '.' By configuring this widget style class, you will change some features'
default appearance for every widget that is not already configured by another style.

.. code-block:: python

    style.configure('.', font=('Helvetica', 10))


Use themed colors
=================
**ttkbootstrap** has a :ref:`Colors <reference:colors>` class that contains the theme colors as well as several helper
methods for manipulating colors. This class is attached to the ``Style`` object at run-time for the selected theme, and
so is available to use with ``Style.colors``. The colors can be accessed via dot notation or get method:

.. code-block:: python

    # dot-notation
    Colors.primary

    # get method
    Colors.get('primary')

This class is an iterator, so you can iterate over the main style color labels (primary, secondary, success, info,
warning, danger):

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



Create a new theme
==================

**TTK Creator** is a program that makes it really easy to create and use your own defined themes.

.. image:: images/ttkcreator.png

Starting the application
------------------------
From the console, type:

.. code-block:: python

    python -m ttkcreator

Select a base theme
-------------------
When you start **TTK Creator**, you'll be prompted to select a *light* or *dark* theme base. The reason you need to
choose a base is that there are some nuanced differences in how the elements are constructed in a light vs a dark theme.

.. image:: images/ttkcreator-splash.png

The first time you start **TTK Creator**, or if you happen to upgrade the package, you'll be prompted to select the
destination for your user-defined themes file. It is recommended to store these themes in a location that is safe and
writable. It is not recommended to store themes in the package directory as they may get overwritten if the package is
updated, re-installed, etc...

.. image:: images/ttkcreator-alert.png

.. image:: images/ttkcreator-filedialog.png


Create and save your theme
--------------------------
You should now see the **TTK Creator** design window

.. image:: images/ttkcreator.png

- Name your theme
- Click the color palette to select a color, or input a hex color directly
- Click **Save** to save your theme
- Click **Reset** to apply the defaults and start from scratch

Theme names must be unique. If you choose a theme name that already exists, you will be prompted to choose another.

You can check your new theme by starting up the **ttkbootstrap** demo application, which will load all available themes.
Then, select your new theme from the option menu.

.. code-block:: python

    python -m ttkbootstrap

.. warning:: If you are using **Linux** or **MacOS** and the program crashes without starting, you may not have a font
    with emoji support. To fix this ``sudo apt-get install fonts-symbola``
