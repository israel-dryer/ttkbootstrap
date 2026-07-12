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
   ttk.Button(app, text="Danger Outline", bootstyle="danger-outline").pack(padx=16, pady=(4, 16))

   app.mainloop()

A few things to notice:

- ``ttk.App`` creates the root window and installs a theme in one step. Pass
  ``theme=`` to choose one; it defaults to ``bootstrap-light``.
- Every ttkbootstrap widget accepts ``bootstyle=``. The value describes intent
  — a color (``"primary"``), a variant (``"outline"``), or both
  (``"danger-outline"``) — not a literal color.
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

ttkbootstrap ships 30 themes as light/dark pairs. Switch at runtime through the
style engine:

.. code-block:: python

   from ttkbootstrap import Style

   style = Style.get_instance()
   style.theme_use("bootstrap-dark")

.. seealso::

   :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>` for the
   full styling vocabulary, and :doc:`Theming </user-guide/feature-guides/theming>`
   for the color model behind the themes.
