How-To
======

Short, task-focused recipes for common jobs — the everyday tkinter tasks a
newcomer arrives needing, written the ttkbootstrap way (ttkbootstrap widgets and
idioms throughout, with links to the :doc:`Reference </reference/index>` for the
full API).

Building interfaces
-------------------

- **Lay out widgets** — for ``pack``, ``grid``, and ``place``, and when to reach
  for each, see :doc:`Arranging widgets
  </user-guide/foundations/arranging-widgets>`.
- **Wire events and variables** — for ``bind``, ``command=``, and the variable
  classes, see :doc:`Events and callbacks
  </user-guide/foundations/events-and-callbacks>` and the
  :doc:`Variables guide </user-guide/feature-guides/variables>`.
- **Menus** — for a menu bar, submenus, context menus, and the cross-platform
  macOS application menu, see the :doc:`Menus guide </user-guide/feature-guides/menus>`.
- :doc:`Show images and icons <working-with-images>` — ``PhotoImage`` and Pillow,
  the keep-a-reference gotcha, and themed glyphs with ``apply_icon``.
- :doc:`Scroll long content <scrollable>` — ``ScrolledFrame``/``ScrolledText`` for
  content that outgrows the window.

Interaction and data
---------------------

- **Message boxes and dialogs** — for ``Messagebox``/``Querybox`` and the shipped
  pickers, see the :doc:`Dialogs guide </user-guide/feature-guides/dialogs>`.
- **Validate a form** — for attaching validation rules and reading the result,
  see the :doc:`Validation guide </user-guide/feature-guides/validation>`.
- :doc:`Open a second window <multiple-windows>` — a second ``Toplevel``, a modal
  dialog that returns a value, and the close button.
- :doc:`Run background work <threads>` — ``after`` and worker threads, updating
  widgets safely from the main loop.
- :doc:`Copy and paste text <clipboard>` — copy and paste text, and read the
  current selection.
- :doc:`Handle callback errors <error-handling>` — take over
  ``report_callback_exception`` and deal with ``TclError``.
- :doc:`Ring the system bell <bell>` — a system beep to flag a rejected action
  or a finished job.
- :doc:`Mark a window busy <busy>` — a wait cursor and a block on clicks while
  a slow job runs.

Presentation
------------

- :doc:`Animate a GIF <animate-gif>` — frame-by-frame animation with
  ``PhotoImage`` and ``after``.
- :doc:`Show a splash screen <splash-screen>` — a borderless startup window that
  hands off to the main one.
- :doc:`Set the app icon <application-icon>` — the titlebar and taskbar icon.