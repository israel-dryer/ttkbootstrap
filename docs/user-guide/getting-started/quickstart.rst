Quickstart
==========

Your first themed window takes about a minute.

Hello ttkbootstrap
------------------

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.Window(title="Hello", themename="bootstrap-light")

   ttk.Label(app, text="Hello from ttkbootstrap!").pack(padx=16, pady=(16, 8))
   ttk.Button(app, text="Primary", bootstyle="primary").pack(padx=16, pady=4)
   ttk.Button(app, text="Success", bootstyle="success").pack(padx=16, pady=4)
   ttk.Button(app, text="Danger Outline", bootstyle="danger-outline").pack(padx=16, pady=(4, 16))

   app.mainloop()

A few things to notice:

- ``ttk.Window`` creates the root window and installs a theme in one step. Pass
  ``themename=`` to choose one; it defaults to ``bootstrap-light``.
- Every ttkbootstrap widget accepts ``bootstyle=``. The value describes intent
  — a color (``"primary"``), a variant (``"outline"``), or both
  (``"danger-outline"``) — not a literal color.
- ``app.mainloop()`` starts the event loop, exactly as in stock tkinter.

Window vs Tk
------------

``ttk.Window`` is a drop-in replacement for ``tkinter.Tk`` that also owns the
theme. If you already have a ``Tk`` root, create a :class:`~ttkbootstrap.style.Style`
instead — the styling engine attaches to whichever root exists. Prefer
``ttk.Window`` for new code.

Choosing a theme
----------------

ttkbootstrap ships 30 themes as light/dark pairs. Switch at runtime through the
style engine:

.. code-block:: python

   from ttkbootstrap import Style

   style = Style.get_instance()
   style.theme_use("bootstrap-dark")

.. seealso::

   :doc:`The bootstyle grammar </user-guide/concepts/bootstyle-grammar>` for the
   full styling vocabulary, and :doc:`Theming </user-guide/concepts/theming>`
   for the color model behind the themes.
