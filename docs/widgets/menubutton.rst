Menubutton
==========

A **menubutton** is a button that opens a dropdown menu when clicked.
``Menubutton`` is the native ``ttk.Menubutton``, styled with ``bootstyle=``. This
page covers attaching its menu, choosing where the menu opens, then the
``bootstyle`` colors, variants, and states.

.. image:: /_static/examples/menubutton-open-light.png
   :class: tb-screenshot-light tb-window-screenshot
   :width: 218px
   :alt: A primary menubutton with its dropdown menu open — light theme

.. image:: /_static/examples/menubutton-open-dark.png
   :class: tb-screenshot-dark tb-window-screenshot
   :width: 218px
   :alt: A primary menubutton with its dropdown menu open — dark theme

Usage
-----

A menubutton owns a :doc:`Menu </user-guide/feature-guides/menus>`. Build the menu
with the menubutton as its parent, add items, then attach it — either with
``menu=`` at construction or by assigning ``menubutton["menu"]``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   menubutton = ttk.Menubutton(app, text="Actions", bootstyle="primary")
   menubutton.pack(padx=10, pady=10)

   menu = ttk.Menu(menubutton)
   menu.add_command(label="New", command=lambda: print("new"))
   menu.add_command(label="Open", command=lambda: print("open"))
   menu.add_separator()
   menu.add_command(label="Quit", command=app.destroy)

   menubutton["menu"] = menu

   app.mainloop()

The menu is a full ``Menu`` — it takes commands, separators, checkbuttons, and
radiobuttons. Building menus (including stateful items and submenus) is covered in
the :doc:`Menus guide </user-guide/feature-guides/menus>`.

Where the menu opens
--------------------

``direction=`` sets which way the menu drops relative to the button — ``below``
(the default), ``above``, ``left``, ``right``, or ``flush`` (over the button):

.. code-block:: python

   ttk.Menubutton(app, text="More", menu=menu, direction="right")

.. admonition:: Across platforms
   :class: note

   The button itself is themed consistently on every platform. Its dropdown,
   though, is a native :doc:`Menu </user-guide/feature-guides/menus>`, and menus
   are where the platform shows through. On **macOS** the menu opens as a native
   pop-up anchored over the button, so ``direction`` has little effect there; on
   **Windows and Linux** it drops in the requested direction. The
   :doc:`Menus guide </user-guide/feature-guides/menus>` covers the cross-platform
   menu behavior in full.

Colors and variants
-------------------

``bootstyle`` sets the button's color from the semantic palette, and a variant
changes how much the button fills, from boldest to quietest: solid fills with the
color, ``outline`` gives a bordered button instead, and ``ghost`` is transparent
until you hover it — a low-emphasis dropdown trigger for a toolbar or menu bar:

.. code-block:: python

   ttk.Menubutton(app, text="Solid",   bootstyle="primary")
   ttk.Menubutton(app, text="Outline", bootstyle="primary outline")
   ttk.Menubutton(app, text="Ghost",   bootstyle="primary ghost")

States
------

Toggle the ``disabled`` state to grey the button out and block it from opening its
menu:

.. code-block:: python

   menubutton.state(["disabled"])      # greyed out, won't open
   menubutton.state(["!disabled"])     # re-enable

Reference
---------

``Menubutton`` is the native ``ttk.Menubutton``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Menubutton API reference </reference/api/menubutton>` — every option and
  method.
- :ref:`Menubutton styling options <menubutton-styling>` — restyle it yourself,
  with the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`OptionMenu <optionmenu>` — when the menu is just a list of values.
   - :doc:`Menus guide </user-guide/feature-guides/menus>` — building the menu itself.
