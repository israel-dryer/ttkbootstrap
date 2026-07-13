Notebook
========

``Notebook`` is the native ttk tabbed container that shows one child pane at
a time (``ttk.Notebook``), themed by ttkbootstrap. For usage and examples, see
the :doc:`Notebook catalog page </widgets/notebook>`; this page is the
complete reference for its options, methods, and styling.

.. note::

   Python's standard library documents ``ttk.Notebook`` only briefly. The
   canonical upstream source is the
   `Tk ttk::notebook manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_notebook.htm>`__
   (Tcl 8.6).

Options
-------

Each option can be set in the constructor and changed later with ``configure()``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - **Constructor keyword.** An accent color, optionally with a variant. See
       :ref:`Styling options <notebook-styling>` for the available styles.
   * - ``padding``
     - ``int | tuple``
     - Extra space around the pane area, in pixels (a single value, or per-side).
   * - ``width``
     - ``int``
     - The requested width of the pane area, in pixels.
   * - ``height``
     - ``int``
     - The requested height of the pane area, in pixels.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the notebook (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the notebook accepts keyboard focus during traversal.

Methods
-------

.. py:method:: add(child, **kw)
   :noindex:

   Add a pane for ``child`` as a new tab. ``kw`` include ``text``, ``image``,
   ``compound``, ``underline``, ``sticky``, and ``padding``.

   :returns: ``None``.

.. py:method:: insert(pos, child, **kw)
   :noindex:

   Insert a pane at position ``pos``.

   :returns: ``None``.

.. py:method:: hide(tab_id)
   :noindex:

   Hide a tab (it is kept in the widget and can be restored).

   :returns: ``None``.

.. py:method:: select(tab_id=None)
   :noindex:

   Select ``tab_id``, or return the currently selected tab's widget name.

   :rtype: str

.. py:method:: index(tab_id)
   :noindex:

   Return the numeric index of a tab.

   :rtype: int

.. py:method:: tab(tab_id, option=None, **kw)
   :noindex:

   Query or set a tab's options.

.. py:method:: tabs()
   :noindex:

   Return the widget names of all tabs.

   :rtype: tuple

.. py:method:: enable_traversal()
   :noindex:

   Enable Ctrl-Tab / mnemonic keyboard traversal between tabs.

   :returns: ``None``.

.. _notebook-styling:

Styling options
---------------

This section is for changing how the notebook *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Notebook(style=...)``.

.. include:: /reference/api/_style/notebook.rst

Shared capabilities
-------------------

``Notebook`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Notebook catalog page </widgets/notebook>` — usage, screenshots, and
  examples.
- `Tk ttk::notebook manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_notebook.htm>`__
  — the canonical upstream reference (Tcl 8.6).
