Theming
=======
``ttkbootstrap`` includes several built-in **light** and **dark** themes that are generated at run-time using the
``ttk.Style`` class. Generally, the ttkbootstrap api is identical to the ``ttk.Style`` api.

Choosing a theme
----------------
Using a pre-defined ``ttkbootstrap`` theme is identical to using any other ``ttk`` theme, by using the
``ttk.Style.theme_use``.

.. code-block:: python

    style = Style()
    style.theme_use('superhero')


To get a list of all available themes:

.. code-block:: python

    style.theme_names()

As of this latest update, the currently available themes include:

    :light: cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
    :dark: cyborg - darkly - solar - superhero


Using themed widgets
--------------------
``ttkboostrap`` includes many *pre-defined widget styles* that you can easily apply with the ``style`` property
available to every ``ttk`` widget.

Color patterns
..........................
``ttkbootstrap`` includes a set of pre-defined themed colors based on a pattern common to many bootstrap styles.
All ``ttkbootstrap`` themes include style colors associated with the following labels:

    * primary
    * secondary
    * success *(green hue)*
    * info *(blue hue)*
    * warning *(orange hue)*
    * danger *(red hue)*

Styles
..................
Every widget has an associated ``ttk`` class_. All pre-defined styles include a **color prefix**, followed by the ``ttk``
**widget class**.

.. _class: link_here

As an example, the ``ttk.Button`` has the following styles available:

    * primary.TButton
    * secondary.TButton
    * success.TButton
    * info.TButton
    * warning.TButton
    * danger.TButton

Applying a themed style
-----------------------
Use the ``style`` property of the widget to apply any ``ttkbootstrap`` pre-defined style.

.. code-block:: python

    # solid button
    ttk.Button(master, text="Quit", style='warning.TButton').pack()

    # outline button
    ttk.Button(master, text="Quit", style='warning.Outline.TButton').pack()

.. note::

    While all widgets are themed, not all have themed color styles available, such as ``ttk.PanedWindow`` or
    ``ttk.Scale``. Instead, these widgets are styled with the primary theme color.






