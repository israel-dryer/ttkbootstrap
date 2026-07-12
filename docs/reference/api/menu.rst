Menu
====

``Menu`` is tkinter's menu widget (``tk.Menu``), themed by ttkbootstrap and
re-exported as ``ttk.Menu``. It backs menu bars, cascading submenus, and
right-click context menus; ttkbootstrap adds helpers for the native macOS
application menu. Entries are addressed by integer index (0-based) or the special
index ``"end"`` / ``"active"`` / ``"last"``. This page is the complete reference
for its own options and methods; the shared widget methods are under
:doc:`Capabilities </reference/capabilities/index>`.

.. note::

   Python's standard library doesn't document ``tk.Menu`` in full. This reference
   is maintained by ttkbootstrap. The canonical upstream source is the
   `Tk menu manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/menu.htm>`__
   (Tcl 8.6).

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``autostyle``
     - ``bool``
     - **Constructor only.** ``True`` (default) paints the menu with the active
       theme and repaints on a theme switch; ``False`` opts out.
   * - ``font``
     - ``str | Font``
     - The font for entry labels.
   * - ``foreground`` (``fg``)
     - ``str``
     - The text color of entries.
   * - ``background`` (``bg``)
     - ``str``
     - The menu background color.
   * - ``activeforeground``
     - ``str``
     - The text color of the entry under the pointer.
   * - ``activebackground``
     - ``str``
     - The background color of the entry under the pointer.
   * - ``activeborderwidth``
     - ``int``
     - The border width of the entry under the pointer, in pixels.
   * - ``disabledforeground``
     - ``str``
     - The text color of disabled entries.
   * - ``selectcolor``
     - ``str``
     - The indicator color of checkbutton / radiobutton entries.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``tearoff``
     - ``bool``
     - ``True`` adds a dashed line that tears the menu into a floating window.
   * - ``tearoffcommand``
     - ``callable``
     - A callback invoked when the menu is torn off.
   * - ``postcommand``
     - ``callable``
     - A callback invoked just before the menu is posted — use it to update
       entries lazily.
   * - ``title``
     - ``str``
     - The title shown on a torn-off menu.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the menu (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the menu accepts keyboard focus during traversal.

Methods
-------

Adding entries
~~~~~~~~~~~~~~

Every ``add_*`` appends an entry; the parallel ``insert_*`` methods take a
leading ``index`` and insert before it.

.. py:method:: add_command(**options)
   :noindex:

   Append a command entry.

   :param options: ``label``, ``command``, ``accelerator`` (shown shortcut
      text), ``underline``, ``state``, ``image``, ``compound``.
   :returns: ``None``.

.. py:method:: add_cascade(**options)
   :noindex:

   Append a submenu entry.

   :param options: ``label`` and ``menu`` (a child ``Menu``), plus ``underline``,
      ``state``.
   :returns: ``None``.

.. py:method:: add_checkbutton(**options)
   :noindex:

   Append a checkbutton entry that toggles a variable.

   :param options: ``label``, ``variable``, ``onvalue``, ``offvalue``,
      ``command``.
   :returns: ``None``.

.. py:method:: add_radiobutton(**options)
   :noindex:

   Append a radiobutton entry — one choice in a group sharing a ``variable``.

   :param options: ``label``, ``variable``, ``value``, ``command``.
   :returns: ``None``.

.. py:method:: add_separator(**options)
   :noindex:

   Append a horizontal separator line.

   :returns: ``None``.

.. py:method:: insert(index, itemType, **options)
   :noindex:

   Insert an entry of ``itemType`` (``"command"``, ``"cascade"``,
   ``"checkbutton"``, ``"radiobutton"``, ``"separator"``) before ``index``. The
   ``insert_command`` / ``insert_cascade`` / … shortcuts wrap this.

   :returns: ``None``.

Configuring and removing entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: entryconfigure(index, **options)
   :noindex:

   Set (or query) options on an existing entry. Alias: ``entryconfig``.

   :param index: the entry to change.
   :param options: any options valid for that entry type.
   :returns: the option spec when queried with a single option name, else
      ``None``.

.. py:method:: entrycget(index, option)
   :noindex:

   Return one option of an entry.

.. py:method:: delete(index1, index2=None)
   :noindex:

   Delete an entry, or a range of entries.

   :returns: ``None``.

.. py:method:: index(index)
   :noindex:

   Resolve an index expression to an integer entry number.

   :rtype: int

.. py:method:: type(index)
   :noindex:

   Return the type of an entry — ``"command"``, ``"cascade"``, ``"checkbutton"``,
   ``"radiobutton"``, ``"separator"``, or ``"tearoff"``.

   :rtype: str

Posting and invoking
~~~~~~~~~~~~~~~~~~~~

.. py:method:: tk_popup(x, y, entry='')
   :noindex:

   Pop the menu up as a context menu at a screen position — the usual way to show
   a right-click menu.

   :param int x: screen x, in pixels.
   :param int y: screen y, in pixels.
   :param entry: an entry to position under the pointer.
   :returns: ``None``.

.. py:method:: post(x, y)
   :noindex:

   Map the menu at a screen position (lower-level than ``tk_popup``).

   :returns: ``None``.

.. py:method:: unpost()
   :noindex:

   Unmap the menu.

   :returns: ``None``.

.. py:method:: invoke(index)
   :noindex:

   Invoke the action of an entry as if the user chose it.

   :returns: the value returned by the entry's command, if any.

.. py:method:: activate(index)
   :noindex:

   Highlight an entry as the active one.

   :returns: ``None``.

macOS application menu (ttkbootstrap)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These ttkbootstrap additions wire a menu bar into the native macOS menu
conventions. Each is a **no-op** off macOS, so the same code runs everywhere.

.. py:method:: add_application_menu()
   :noindex:

   Add and return the macOS **application menu** — the bold, app-named menu that
   owns *About*, *Preferences…*, and *Quit*.

   :returns: the application menu, or ``None`` off macOS.
   :rtype: Menu | None

.. py:method:: add_window_menu(label='Window')
   :noindex:

   Add and return the macOS standard **Window** menu.

   :returns: the Window menu, or ``None`` off macOS.
   :rtype: Menu | None

.. py:method:: add_help_menu(label='Help', command=None)
   :noindex:

   Add and return a **Help** menu, wired into the macOS Help conventions.

   :param command: a callback for the search/help action.
   :returns: the Help menu, or ``None`` off macOS.
   :rtype: Menu | None

.. py:method:: on_preferences(callback)
   :noindex:

   Enable the macOS **Preferences…** item (``⌘,``) and call ``callback`` when it
   is chosen. Requires :py:meth:`add_application_menu`.

   :returns: ``None``.

.. py:method:: on_quit(callback)
   :noindex:

   Call ``callback`` when the user chooses macOS **Quit** (``⌘Q``). Requires
   :py:meth:`add_application_menu`.

   :returns: ``None``.

Shared capabilities
-------------------

``Menu`` also has the methods every widget inherits — configuration, event
binding, lifecycle, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Menus </user-guide/feature-guides/menus>` — the usage guide.
- `Tk menu manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/menu.htm>`__ —
  the canonical upstream reference (Tcl 8.6).
