Quickstart
==========

Your first themed window takes about a minute.

Hello ttkbootstrap
------------------

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Hello", theme="bootstrap-light")

   ttk.Label(app, text="Hello from ttkbootstrap!").pack(padx=16, pady=(16, 8))
   ttk.Button(app, text="Primary", bootstyle="primary").pack(padx=16, pady=4)
   ttk.Button(app, text="Success", bootstyle="success").pack(padx=16, pady=4)
   ttk.Button(app, text="Danger Outline", bootstyle="danger outline").pack(padx=16, pady=(4, 16))

   app.mainloop()

.. image:: /_static/examples/quickstart-hello-light.png
   :class: tb-screenshot-light tb-window-screenshot
   :width: 162px
   :alt: The Hello window — a greeting label above primary, success, and danger-outline buttons — light theme

.. image:: /_static/examples/quickstart-hello-dark.png
   :class: tb-screenshot-dark tb-window-screenshot
   :width: 162px
   :alt: The Hello window — a greeting label above primary, success, and danger-outline buttons — dark theme

A few things to notice:

- ``ttk.App`` creates the root window and installs a theme in one step. Pass
  ``theme=`` to choose one; it defaults to ``bootstrap-light``.
- Every ttkbootstrap widget accepts ``bootstyle=``. The value describes intent
  — a color (``"primary"``), a variant (``"outline"``), or both
  (``"danger outline"``) — not a literal color.
- ``pack`` (and ``grid``/``place``) **return the widget**, so you can construct
  and place in one expression — no separate variable needed unless you keep a
  reference.
- ``app.mainloop()`` starts the event loop, exactly as in stock tkinter.

App vs Tk
---------

``ttk.App`` is a drop-in replacement for ``tkinter.Tk`` that also owns the theme.
(It is also exported under its longtime alias ``ttk.Window`` — both name the same
class.) If you already have a ``Tk`` root, create a
:class:`~ttkbootstrap.style.Style` instead — the styling engine attaches to
whichever root exists. Prefer ``ttk.App`` for new code.

Choosing a theme
----------------

ttkbootstrap ships 30 themes as 15 light/dark pairs. You picked one with ``theme=``
above; you can also switch at runtime straight from the app:

.. code-block:: python

   app.theme_use("bootstrap-dark")   # switch to any theme by name

Because every family comes as a light/dark pair, ``App`` gives you a shortcut for
the common case — flipping between the two:

.. code-block:: python

   app.theme_mode = "dark"   # set the mode directly ("light" or "dark")
   app.toggle_theme()        # or flip to the other mode

Read ``app.theme_names()`` for the full list, and ``app.theme_mode`` to see the
active mode.

.. seealso::

   - :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>` —
     the full styling vocabulary.
   - :doc:`Theming </user-guide/feature-guides/theming>` — the color model behind
     the themes.
