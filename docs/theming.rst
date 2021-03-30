Theming
=======
Built-in **light** and **dark** themes are generated at run-time. Generally, the ``ttkbootstrap`` api is identical to
the ``ttk.Style`` api.

Choosing a theme
----------------
Using a pre-defined ``ttkbootstrap`` theme is identical to using standard ``ttk`` theme, except that you will use the
``ttkbootstrap.Style`` class instead of the ``ttk.Style`` class.

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

.. image:: https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/images/color-options.png

Styles
..................
Every widget has an associated ``ttk`` class_. All pre-defined styles include a **color prefix**, followed by the ``ttk``
**widget class**.

.. _class: link_here

.. note::

    While all widgets are themed, not all have themed color styles available, such as ``ttk.PanedWindow`` or
    ``ttk.Scale``. Instead, these widgets are styled with the primary theme color.


To demonstrate, the ``ttk.Button`` has the following styles available:

    * primary.TButton
    * secondary.TButton
    * success.TButton
    * info.TButton
    * warning.TButton
    * danger.TButton

Use the ``style`` property of the widget to apply any ``ttkbootstrap`` pre-defined style.

.. code-block:: python

    # solid button
    ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)

    # outline button
    ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)

.. image:: https://raw.githubusercontent.com/israel-dryer/ttkbootstrap/master/docs/images/submit.png








