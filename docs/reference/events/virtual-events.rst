Built-in virtual events
=======================

A **virtual event** is a named notification in double brackets — ``<<Copy>>``,
``<<ThemeChanged>>`` — decoupled from any one physical event. Bind them exactly
like physical events. This page catalogs the ones Tk, ttk, and ttkbootstrap
define; to define or fire your *own*, see
:doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>`.

Editing & clipboard
-------------------

Defined by default with the key sequences shown; emitted by ``Text`` and
``Entry`` widgets and safe to bind or generate yourself.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Virtual event
     - Default sequence
     - Meaning
   * - ``<<Cut>>``
     - ``Control-x``, ``Shift-Delete``
     - Cut the selection.
   * - ``<<Copy>>``
     - ``Control-c``, ``Control-Insert``
     - Copy the selection.
   * - ``<<Paste>>``
     - ``Control-v``, ``Shift-Insert``
     - Paste the clipboard.
   * - ``<<PasteSelection>>``
     - ``ButtonRelease-2``
     - Paste the X selection (middle-click).
   * - ``<<Undo>>``
     - ``Control-z``
     - Undo.
   * - ``<<Redo>>``
     - ``Control-y``
     - Redo.
   * - ``<<SelectAll>>``
     - ``Control-a``, ``Control-/``
     - Select everything.
   * - ``<<SelectNone>>``
     - ``Control-\``
     - Clear the selection.
   * - ``<<ToggleSelection>>``
     - ``Control-Button-1``
     - Toggle selection of the item under the pointer.
   * - ``<<ContextMenu>>``
     - ``Button-3``
     - Request a context menu (right-click).

Caret navigation
----------------

Text-editing motion events, each mapped to an arrow/navigation key. Every one
below has a ``<<Select…>>`` counterpart (e.g. ``<<SelectNextWord>>``) that the
``Shift``-modified key fires to *extend* the selection.

.. list-table::
   :header-rows: 1
   :widths: 34 30 36

   * - Virtual event
     - Default key
     - Moves the caret
   * - | ``<<PrevChar>>``
       | ``<<NextChar>>``
     - ``Left`` / ``Right``
     - one character
   * - | ``<<PrevWord>>``
       | ``<<NextWord>>``
     - ``Control-Left`` / ``Control-Right``
     - one word
   * - | ``<<PrevLine>>``
       | ``<<NextLine>>``
     - ``Up`` / ``Down``
     - one line
   * - | ``<<PrevPara>>``
       | ``<<NextPara>>``
     - ``Control-Up`` / ``Control-Down``
     - one paragraph
   * - | ``<<LineStart>>``
       | ``<<LineEnd>>``
     - ``Home`` / ``End``
     - to the line edge

Focus traversal
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Virtual event
     - Default key
     - Meaning
   * - ``<<NextWindow>>``
     - ``Tab``
     - Move focus to the next widget.
   * - ``<<PrevWindow>>``
     - ``Shift-Tab``
     - Move focus to the previous widget.

Widget notifications
--------------------

Emitted by specific widgets when their selection or state changes — no default
key sequence; you bind them to react to the widget. Read the current value from
the widget in the handler.

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Virtual event
     - Emitted by
   * - ``<<ComboboxSelected>>``
     - ``Combobox`` — a value was chosen.
   * - ``<<NotebookTabChanged>>``
     - ``Notebook`` — the active tab changed.
   * - ``<<TreeviewSelect>>``
     - ``Treeview`` — the selection changed.
   * - | ``<<TreeviewOpen>>``
       | ``<<TreeviewClose>>``
     - ``Treeview`` — a node was expanded / collapsed.
   * - ``<<ListboxSelect>>``
     - ``Listbox`` — the selection changed.
   * - ``<<MenuSelect>>``
     - ``Menu`` — the highlighted item changed.
   * - ``<<Modified>>``
     - ``Text`` — the contents changed.

Theme & locale (ttkbootstrap)
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Virtual event
     - Fires when
   * - ``<<ThemeChanged>>``
     - The theme is switched (delivered to every widget). Bind it to recolor
       anything you drew yourself; for rebuilding a custom *style* prefer
       :func:`~ttkbootstrap.on_theme_change`.
   * - ``<<LocaleChanged>>``
     - The locale is switched via ``set_locale`` — what drives
       :class:`~ttkbootstrap.LocaleVar`.
