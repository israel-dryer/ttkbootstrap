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

Tab labels and keyboard traversal
---------------------------------

``add`` (and ``tab``) take more than ``text``. ``image=`` with ``compound=`` puts
an icon on the tab, ``underline=`` marks a mnemonic character, and ``sticky=``
controls how the page fills its tab area. Call ``enable_traversal()`` once to turn
on keyboard navigation — Control-Tab and Control-Shift-Tab cycle the tabs, and
Alt+mnemonic jumps straight to one:

.. code-block:: python

   notebook.add(advanced, text="Advanced", underline=0)   # Alt+A jumps here
   notebook.enable_traversal()

Traversal only reaches pages that are **direct children** of the notebook. To show
an icon, pass a ``PhotoImage`` as ``image=`` (see
:doc:`Show images and icons </user-guide/how-to/working-with-images>`).

Switching tabs
--------------

The user clicks a tab to switch; ``select`` switches programmatically, and
``index("current")`` (or ``select()`` with no argument) reports the current tab:

.. code-block:: python

   notebook.select(advanced)               # show a page by its widget
   notebook.select(0)                       # or by index
   current = notebook.index(notebook.select())   # -> the selected tab's index

Methods that address a tab — ``select``, ``tab``, ``hide``, ``forget``, ``index``
— accept the same tab-id forms: the page widget, an integer index, ``"current"``,
or ``"@x,y"`` (the tab at a point). ``tabs()`` returns every page widget in tab
order, handy for iterating.

Reacting to a tab change
------------------------

To run code when the page changes — lazy-load its contents, say — bind the
``<<NotebookTabChanged>>`` virtual event:

.. code-block:: python

   notebook.bind("<<NotebookTabChanged>>", lambda event: print("now on", notebook.index("current")))

This also fires once when the notebook first appears and selects its initial tab —
so a handler that lazy-loads a page's contents runs for the starting tab too,
which is usually what you want.

Disabling and removing tabs
---------------------------

Disable a tab to grey it out and block selection while leaving it in place; set it
back to ``"normal"`` to re-enable:

.. code-block:: python

   notebook.tab(advanced, state="disabled")   # visible but not selectable
   notebook.tab(advanced, state="normal")     # re-enable

To take a tab off the bar, ``hide`` it — the page is kept, and ``add``-ing it again
restores it — or ``forget`` it to remove it for good:

.. code-block:: python

   notebook.hide(advanced)                     # remove from the bar; add() restores it
   notebook.forget(advanced)                   # remove permanently

Color
-----

``bootstyle`` colors the selected tab and the notebook's accents from the semantic
palette:

.. code-block:: python

   ttk.Notebook(app, bootstyle="primary")

API & reference
---------------

``Notebook`` is the native ``ttk.Notebook`` — ttkbootstrap adds ``bootstyle=`` but
no other Python API. Its own methods manage tabs: ``add`` / ``insert(pos, …)`` to
append or insert a page, ``select`` / ``tab`` / ``index`` / ``tabs`` to query and
switch, ``hide`` / ``forget`` to remove, ``enable_traversal`` for keyboard
navigation, and ``identify(x, y)`` to hit-test the tab bar. For the full signatures
see the
`tkinter.ttk.Notebook <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Notebook>`__
reference.

.. seealso::

   :doc:`Frame <frame>` for the page containers, and
   :doc:`Panedwindow <panedwindow>` for a split rather than tabbed layout. Want to
   restyle the notebook yourself? The
   :ref:`Notebook's styling options <notebook-styling>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
