Notebook
========

A **notebook** is a tabbed container — one page per tab, with only the selected
page visible. ``Notebook`` is the native ``ttk.Notebook``, styled with
``bootstyle=``. This page covers adding tabs, switching between them, reacting to a
tab change, disabling or hiding a tab, then the ``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A three-tab notebook with the middle tab selected, in light and dark themes.

Usage
-----

Each page is a widget — usually a :doc:`Frame <frame>` — added with ``add`` and a
tab ``text``. Build a frame per page, fill it, and add it:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *

   app = ttk.App()

   notebook = ttk.Notebook(app)
   notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

   general = ttk.Frame(notebook, padding=16)
   ttk.Label(general, text="General settings").pack()
   notebook.add(general, text="General")

   advanced = ttk.Frame(notebook, padding=16)
   ttk.Label(advanced, text="Advanced settings").pack()
   notebook.add(advanced, text="Advanced")

   app.mainloop()

Switching tabs
--------------

The user clicks a tab to switch; ``select`` switches programmatically, and
``index("current")`` (or ``select()`` with no argument) reports the current tab:

.. code-block:: python

   notebook.select(advanced)               # show a page by its widget
   notebook.select(0)                       # or by index
   current = notebook.index(notebook.select())   # -> the selected tab's index

To run code when the page changes — lazy-load its contents, say — bind the
``<<NotebookTabChanged>>`` virtual event:

.. code-block:: python

   notebook.bind("<<NotebookTabChanged>>", lambda event: print("now on", notebook.index("current")))

Disabling and hiding tabs
-------------------------

``tab(page, state=...)`` sets a tab's state — ``"disabled"`` greys it out and
blocks selection, ``"hidden"`` removes it from the bar (``add`` it again to
restore). ``hide`` / ``forget`` also remove a page (``forget`` permanently):

.. code-block:: python

   notebook.tab(advanced, state="disabled")   # visible but not selectable
   notebook.tab(advanced, state="normal")     # re-enable
   notebook.hide(advanced)                     # remove from the bar (add() to restore)

Color
-----

``bootstyle`` colors the selected tab and the notebook's accents from the semantic
palette:

.. code-block:: python

   ttk.Notebook(app, bootstyle="primary")

API & reference
---------------

``Notebook`` is the native ``ttk.Notebook`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. For its constructor and the tab-management methods
(``add``, ``insert``, ``select``, ``tab``, ``hide``, ``forget``, ``index``,
``tabs``) see the
`tkinter.ttk.Notebook <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Notebook>`__
reference.

.. seealso::

   :doc:`Frame <frame>` for the page containers, and
   :doc:`Panedwindow <panedwindow>` for a split rather than tabbed layout. Want to
   restyle the notebook yourself? The
   :doc:`Style Reference › Notebook </reference/style-reference/notebook>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
