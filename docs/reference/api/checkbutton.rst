Checkbutton
===========

``Checkbutton`` is the native ttk labeled on/off toggle (``ttk.Checkbutton``),
themed by ttkbootstrap. For usage and examples, see the
:doc:`Checkbutton catalog page </widgets/checkbutton>`; this page is the
complete reference for its options, methods, and styling.

.. note::

   Python's standard library documents ``ttk.Checkbutton`` only briefly. The
   canonical upstream source is the
   `Tk ttk::checkbutton manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_checkbutton.htm>`__
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
       :ref:`Styling options <checkbutton-styling>` for the available styles.
   * - ``text``
     - ``str``
     - The label shown beside the check.
   * - ``textvariable``
     - ``Variable``
     - A ``StringVar`` whose value is shown as the label and tracked live.
   * - ``variable``
     - ``Variable``
     - The variable that holds the check state.
   * - ``onvalue``
     - ``any``
     - The value written to ``variable`` when checked.
   * - ``offvalue``
     - ``any``
     - The value written to ``variable`` when unchecked.
   * - ``command``
     - ``callable``
     - The function called when the check state is toggled.
   * - ``image``
     - ``PhotoImage``
     - An image to display in place of, or beside, the text.
   * - ``compound``
     - ``str``
     - How text and image are combined: ``"none"``, ``"left"``, ``"right"``,
       ``"top"``, ``"bottom"``, or ``"center"``.
   * - ``underline``
     - ``int``
     - The character index to underline (for a keyboard mnemonic), or ``-1``.
   * - ``width``
     - ``int``
     - The requested width in characters (negative sets a minimum).
   * - ``padding``
     - ``int | tuple``
     - Extra space around the label, in pixels (a single value, or per-side).
   * - ``state``
     - ``str``
     - ``"normal"`` or ``"disabled"``. For finer control use the ``state`` method
       (see :doc:`Capabilities </reference/capabilities/index>`).

Methods
-------

.. py:method:: invoke()
   :noindex:

   Toggle the check state and run its ``command``.

   :returns: the command's return value.

.. _checkbutton-styling:

Styling options
---------------

This section is for changing how the checkbutton *looks*. Define a style with
``style.configure(...)`` (and ``style.map(...)`` for per-state colors), then
apply it with ``Checkbutton(style=...)``.

.. include:: /reference/api/_style/checkbutton.rst

Shared capabilities
-------------------

``Checkbutton`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection — plus the ttk
state methods ``state`` / ``instate`` / ``identify``. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Checkbutton catalog page </widgets/checkbutton>` — usage, screenshots,
  and examples.
- `Tk ttk::checkbutton manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/ttk_checkbutton.htm>`__
  — the canonical upstream reference (Tcl 8.6).
