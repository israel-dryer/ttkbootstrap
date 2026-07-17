Button
======

A **button** runs an action when clicked. ``Button`` is the native
``ttk.Button``, styled with ``bootstyle=``. This page covers using one — wiring
the action, adding an icon, laying out a row, the default button, and disabling —
then the ``bootstyle`` colors, variants, and states.

.. image:: /_static/examples/button-hero-light.png
   :class: tb-screenshot-light
   :width: 298px
   :alt: A row of buttons — solid primary, outline, link, and icon-only — light theme

.. image:: /_static/examples/button-hero-dark.png
   :class: tb-screenshot-dark
   :width: 298px
   :alt: A row of buttons — solid primary, outline, link, and icon-only — dark theme

Usage
-----

Wire the action with ``command=`` — the function to call on each click. Pass the
function itself, without parentheses; tkinter calls it for you:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   def greet():
       print("clicked")

   ttk.Button(app, text="Greet", command=greet, bootstyle="primary").pack(padx=10, pady=10)

   app.mainloop()

To pass arguments to the callback, wrap it in a ``lambda`` — but keep real work in
a named function:

.. code-block:: python

   ttk.Button(app, text="Delete", command=lambda: delete(item_id), bootstyle="danger")

Icons
-----

Give a button a themed glyph with ``icon=`` — a `Bootstrap Icons
<https://icons.getbootstrap.com/>`_ name. The glyph is rendered to match the
button's style, so it inverts on outline buttons, mutes when disabled, and
recolors on a theme switch:

.. code-block:: python

   ttk.Button(app, text="Save", icon="save", bootstyle="success")

``compound=`` places the icon relative to the text (``LEFT`` — the default when
there is text — ``RIGHT``, ``TOP``, ``BOTTOM``):

.. code-block:: python

   from ttkbootstrap.constants import *

   ttk.Button(app, text="Next", icon="arrow-right", compound=RIGHT, bootstyle="primary")

For a compact toolbar control, drop the text with ``icon_only=True`` — the button
becomes a square sized to the glyph:

.. code-block:: python

   ttk.Button(app, icon="trash", icon_only=True, bootstyle="danger")

.. image:: /_static/examples/button-icons-light.png
   :class: tb-screenshot-light
   :width: 236px
   :alt: A Save button with a leading icon, a Next button with a trailing icon, and a square icon-only trash button — light theme

.. image:: /_static/examples/button-icons-dark.png
   :class: tb-screenshot-dark
   :width: 236px
   :alt: A Save button with a leading icon, a Next button with a trailing icon, and a square icon-only trash button — dark theme

A row of buttons
----------------

Buttons in a row read best at a uniform width — set ``width=`` (in characters) to
the widest label so they align. Pack them into a frame with consistent spacing:

.. code-block:: python

   from ttkbootstrap.constants import *

   actions = ttk.Frame(app, padding=10)
   actions.pack()

   ok = ttk.Button(actions, text="OK", width=10, command=on_ok, bootstyle="success")
   ok.pack(side=LEFT, padx=4)
   cancel = ttk.Button(actions, text="Cancel", width=10, command=on_cancel, bootstyle="secondary")
   cancel.pack(side=LEFT, padx=4)

For a **toolbar**, pack icon-only buttons side by side in a frame:

.. code-block:: python

   toolbar = ttk.Frame(app, padding=4)
   toolbar.pack(fill=X)

   for name, action in [("save", save), ("printer", print_doc), ("trash", delete)]:
       button = ttk.Button(toolbar, icon=name, icon_only=True, command=action, bootstyle="secondary ghost")
       button.pack(side=LEFT)

The default button
------------------

A dialog usually has a **default** action that fires on :kbd:`Return`. Mark the
button as the default with ``default="active"`` — on platforms that draw a default
ring (macOS, for one) it gets the highlight. That flag only *marks* the button,
though; it does not wire the key, so also bind :kbd:`Return`, calling ``invoke()``
so the button shows its pressed feedback as it fires:

.. code-block:: python

   submit = ttk.Button(app, text="Submit", command=on_submit, bootstyle="primary", default="active")
   submit.pack(pady=10)
   submit.focus_set()                         # start focused
   app.bind("<Return>", lambda event: submit.invoke())

Now :kbd:`Return` triggers the action from anywhere in the window, and the button
already has the focus ring. (The shipped dialogs wire up their default button — the
ring plus the :kbd:`Return` binding — for you; see the
:doc:`Dialogs guide </user-guide/feature-guides/dialogs>`.)

Enabling and disabling
----------------------

A button you cannot use yet — until a form is valid, say — should be **disabled**.
Toggle the standard ttk ``disabled`` state; the theme mutes it and it stops
responding to clicks:

.. code-block:: python

   submit = ttk.Button(app, text="Submit", command=on_submit, bootstyle="primary")

   submit.state(["disabled"])                 # greyed out, not clickable
   submit.state(["!disabled"])                # re-enable

   submit.instate(["disabled"])               # -> True/False, query the state

Colors
------

``bootstyle`` sets **intent**, not a literal color, so a button renders correctly
in every theme. The nine semantic colors:

.. code-block:: python

   for color in ["neutral", "primary", "secondary", "success", "info",
                 "warning", "danger", "light", "dark"]:
       ttk.Button(app, text=color.title(), bootstyle=color).pack(padx=8, pady=2)

.. image:: /_static/examples/button-colors-light.png
   :class: tb-screenshot-light
   :width: 712px
   :alt: A strip of the nine button colors — light theme

.. image:: /_static/examples/button-colors-dark.png
   :class: tb-screenshot-dark
   :width: 712px
   :alt: A strip of the nine button colors — dark theme

The default color
-----------------

A bare ``Button`` with no ``bootstyle`` uses the ``neutral`` color (as does
``Menubutton``). To restore the pre-2.0 accented default, set it **before** the
app is created — the setting is consumed when a button's style is first built:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(default_button="primary")    # or ttk.set_default_button("primary")

Variants
--------

Combine a color with a variant to change visual weight — ``outline``, ``link``, or
``ghost``:

.. code-block:: python

   ttk.Button(app, text="Solid",   bootstyle="primary")
   ttk.Button(app, text="Outline", bootstyle="primary outline")
   ttk.Button(app, text="Link",    bootstyle="primary link")
   ttk.Button(app, text="Ghost",   bootstyle="primary ghost")

- **solid** (the default) — a filled button for the primary action.
- **outline** — a bordered button for a secondary action next to a solid one.
- **link** — text only, for a low-emphasis action inline with other content.
- **ghost** — no border until hovered; for toolbars and dense UIs.

States
------

Buttons respond to ``hover``, ``pressed``, ``focus``, and ``disabled``
automatically — the theme handles the visuals. You set ``disabled`` yourself (see
`Enabling and disabling`_); the rest follow the pointer and keyboard. To style a
state differently, see :ref:`the button's styling options <button-styling>`.

Reference
---------

``Button`` is the native ``ttk.Button``; ttkbootstrap adds the ``bootstyle`` and
``icon=`` keywords.

- :doc:`Button API reference </reference/api/button>` — every option and method.
- :ref:`Button styling options <button-styling>` — restyle it yourself, with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.
