Busy
====

Tk can cover a widget with a transparent window that swallows pointer events and
shows a busy cursor, so a slow operation can't be clicked into. These methods
hold and release that state. For the worked recipe — including the ``update``
call that makes it visible, and the ``try``/``finally`` that always releases it —
see :doc:`Mark a window busy </user-guide/how-to/busy>`.

The canonical upstream reference is the Tcl
`tk busy <https://www.tcl-lang.org/man/tcl8.6/TkCmd/busy.htm>`__ manual page
(Tk 8.6).

.. note::

   **Not supported on macOS.** The calls succeed and ``busy_status()`` reports
   ``True``, but nothing is drawn and nothing is blocked.

   The busy command is Tk 8.6, so it is available on every Python ttkbootstrap
   supports. tkinter itself only grew these methods in **3.13**; on 3.10–3.12
   ttkbootstrap supplies them, issuing the same Tk command underneath.

Each method also has a longer ``tk_busy_*`` spelling — ``busy_hold`` is
``tk_busy_hold``, ``busy_forget`` is ``tk_busy_forget``, and so on. They are the
same calls; the short names are used here.

.. py:method:: busy(**kw)
   :noindex:

   Make this widget appear busy: block pointer events to it and everything inside
   it, and show a busy cursor. Aliases: ``busy_hold``, ``tk_busy``,
   ``tk_busy_hold``.

   Call ``update`` immediately afterward — the overlay is only mapped once the
   event loop runs, so without it nothing appears before your blocking work
   starts.

   Pointer events only: a widget that already had keyboard focus keeps receiving
   keystrokes.

   :param cursor: the cursor to show while busy (e.g. ``"watch"``). The only
      supported option.
   :returns: ``None``.

.. py:method:: busy_forget()
   :noindex:

   Release the busy state; the widget receives user events again. Alias:
   ``tk_busy_forget``.

   :returns: ``None``.

.. py:method:: busy_status()
   :noindex:

   Whether this widget is currently held busy. Alias: ``tk_busy_status``.

   :returns: ``True`` while held, ``False`` otherwise.
   :rtype: bool

.. py:method:: busy_current(pattern=None)
   :noindex:

   The widgets currently held busy. Alias: ``tk_busy_current``.

   :param pattern: an optional glob matched against widget path names.
   :returns: the matching busy widget objects.
   :rtype: list

.. py:method:: busy_cget(option)
   :noindex:

   Read one busy configuration option. The widget must already be held busy.
   Alias: ``tk_busy_cget``.

   :param str option: the option name, e.g. ``"cursor"``.
   :returns: the option's current value.

.. py:method:: busy_configure(cnf=None, **kw)
   :noindex:

   Query or change the busy options while held. Aliases: ``busy_config``,
   ``tk_busy_config``, ``tk_busy_configure``.

   :param cnf: an optional dict of options (merged with ``kw``).
   :param kw: option/value pairs to set.
   :returns: with no arguments, a dict mapping each option to its spec
      ``(name, dbName, dbClass, default, current)``; otherwise ``None``.

.. seealso::

   - :doc:`Mark a window busy </user-guide/how-to/busy>` — the recipe, and what
     to do on macOS instead.
   - :doc:`Cursors </reference/cursors>` — the names ``cursor`` accepts.
