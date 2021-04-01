.. _stylingwidgets:

How to style widgets
====================
ttkbootstrap **light** and **dark** themes are generated at run-time. Generally, the ``ttkbootstrap.Style`` api is
identical to the ``ttk.Style`` api.

Choosing a theme
----------------
To use a ttkbootstrap theme, you first create a ``ttkbootstrap.Style`` object. You can pass in the name of the theme
you want to use as an argument. Otherwise, by default, the *flatly* style will be applied.

.. code-block:: python

    # flatly style is applied by default
    style = Style()

    # if you want to set a specific theme at runtime, pass it's name as a keyword argument
    style = Style(theme='superhero')

If for some reason you need to change the theme *after* the window has already been created, you will need to use the
``Style.theme_use`` method, which is actually what the ``ttkbootstrap.Style`` class does internally when instantiated.

To get a list of all available themes:

.. code-block:: python

    style.theme_names()

Currently, the available pre-defined themes include:

:light: cosmo - flatly - journal - literal - lumen - minty - pulse - sandstone - united - yeti
:dark: cyborg - darkly - solar - superhero


Using themed widgets
--------------------
ttkbootstrap includes many *pre-defined widget styles* that you can apply with the ``style`` property available to every
ttk widget. The ttkbootstrap style pattern  is ``Color.WidgetClass`` where the color is a prefix to the ttk widget
class. Most widgets include a style pattern for each main theme color (primary, secondary, success, info, warning,
danger).

For example, the ``ttk.Button`` has a widget class of *TButton*. The style patterns available on the button include:

    * primary.TButton
    * secondary.TButton
    * success.TButton
    * info.TButton
    * warning.TButton
    * danger.TButton

These style patterns would produce the following buttons:

.. image:: images/color-options.png

Consider the following example, which also shows the *Outline* style that is available on buttons:

.. code-block:: python

    # solid button
    ttk.Button(window, text="Submit", style='success.TButton').pack(side='left', padx=5, pady=10)

    # outline button
    ttk.Button(window, text="Submit", style='success.Outline.TButton').pack(side='left', padx=5, pady=10)

.. image:: images/submit.png

.. note::

    While all widgets are themed, not all have themed color styles available, such as ``ttk.PanedWindow`` or
    ``ttk.Scale``. Instead, these widgets are styled with the primary theme color.


Style patterns
--------------
The following table includes the styles available for all ttkbootstrap widgets:

+-------------+----------------+------------------------+------------------------------------+
|Widget       | Colors         | Class                  | Example                            |
+=============+================+========================+====================================+
| Button      | all            | TButton                | ``info.TButton``                   |
+             +                +------------------------+------------------------------------+
|             |                | Outline.TButton        | ``info.Outline.TButton``           |
+-------------+----------------+------------------------+------------------------------------+
| Checkbutton | [1]_ all       | TCheckbutton           | ``info.TCheckbutton``              |
+-------------+----------------+------------------------+------------------------------------+
| Combobox    | all            | TCombobox              | ``info.TCombobox``                 |
+-------------+----------------+------------------------+------------------------------------+
| Entry       | all            | TEntry                 | ``info.TEntry``                    |
+-------------+----------------+------------------------+------------------------------------+
| Frame       | all            | TFrame                 | ``info.TFrame``                    |
+-------------+----------------+------------------------+------------------------------------+
| Label       | all            | TLabel                 | ``info.TLabel``                    |
+-------------+----------------+------------------------+------------------------------------+
| LabelFrame  | all            | TLabelframe            | ``info.TLabelframe``               |
+-------------+----------------+------------------------+------------------------------------+
| Menubutton  | all            | TMenubutton            | ``info.TMenubutton``               |
+             +                +------------------------+------------------------------------+
|             |                | Outline.TMenubutton    | ``info.Outline.TMenubutton``       |
+-------------+----------------+------------------------+------------------------------------+
| Notebook    | all            | TNotebook              | ``info.TNotebook``                 |
+-------------+----------------+------------------------+------------------------------------+
| PanedWindow | primary        | TPanedWindow           | applied by default                 |
+-------------+----------------+------------------------+------------------------------------+
| Progressbar | all            | Horizontal.TProgressbar| ``info.Horizontal.TProgressbar``   |
+             +                +------------------------+------------------------------------+
|             |                | Vertical.TProgressbar  | ``info.Vertical.TProgressbar``     |
+-------------+----------------+------------------------+------------------------------------+
| Radiobutton | [#]_ all       | TRadiobutton           | ``info.TRadiobutton``              |
+-------------+----------------+------------------------+------------------------------------+
| Scale       | primary        | TScale                 | applied by default                 |
+-------------+----------------+------------------------+------------------------------------+
| Scrollbar   | primary        | TScrollbar             | applied by default                 |
+-------------+----------------+------------------------+------------------------------------+
| Separator   | all            | Horizontal.TSeparator  | ``info.Horizontal.TSeparator``     |
+             +                +------------------------+------------------------------------+
|             |                | Vertical.TSeparator    | ``info.Vertical.TSeparator``       |
+-------------+----------------+------------------------+------------------------------------+
| Sizegrip    | primary        | TSizegrip              | applied by default                 |
+-------------+----------------+------------------------+------------------------------------+
| Spinbox     | all            | TSpinbox               | ``info.TSpinbox``                  |
+-------------+----------------+------------------------+------------------------------------+
| Treeview    | all            | Treeview               | ``info.Treeview``                  |
+-------------+----------------+------------------------+------------------------------------+

.. [#] can only be styled on Linux and MacOS. Windows defaults to the *xpnative* style buttons

