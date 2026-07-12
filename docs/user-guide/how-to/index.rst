How-To
======

.. note::

   The How-To section is being written for 2.0. Each recipe below will become
   its own page as it is authored; this page lists the planned set.

Short, task-focused recipes for common jobs — the everyday tkinter tasks a
newcomer arrives needing, written the ttkbootstrap way (ttkbootstrap widgets and
idioms throughout, with links out to the `tkinter reference
<https://docs.python.org/3/library/tkinter.html>`_ for the raw API). This band
absorbs the recipes from the old cookbook.

Building interfaces
-------------------

- **Lay out widgets** — ``pack``, ``grid``, and ``place``, and when to reach for
  each (uses the fluent geometry helpers).
- **Wire events and variables** — ``bind``, ``command=``, and the tk variable
  classes (``StringVar``/``IntVar``/…).
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
- **Validate a form** — attach validation rules and read the result.
- :doc:`Open a second window <multiple-windows>` — a second ``Toplevel``, a modal
  dialog that returns a value, and the close button.
- :doc:`Run background work <threads>` — ``after`` and worker threads, updating
  widgets safely from the main loop.
- :doc:`Copy and paste text <clipboard>` — copy and paste text, and read the
  current selection.
- :doc:`Handle callback errors <error-handling>` — take over
  ``report_callback_exception`` and deal with ``TclError``.
- :doc:`Beep and show busy <feedback>` — a system beep and a busy overlay that
  blocks a window while it works.

Presentation
------------

- **Animate a GIF** *(salvaged from the cookbook)* — frame-by-frame animation
  with ``PhotoImage``.
- **Splash screen** — a borderless startup window with ``window_type``.
- **Application icon** — set the window/taskbar icon.
