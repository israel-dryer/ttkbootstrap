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
- **Menus and context menus** — a menu bar and a right-click popup.
- :doc:`Working with images <working-with-images>` — ``PhotoImage`` and Pillow,
  the keep-a-reference gotcha, and themed glyphs with ``apply_icon``.
- **Scrollable content** — ``ScrolledFrame``/``ScrolledText`` for content that
  outgrows the window.

Interaction and data
---------------------

- **Message boxes and dialogs** — ``Messagebox``/``Querybox`` and the shipped
  dialogs.
- **Validate a form** — attach validation rules and read the result.
- **Multiple windows** — ``Toplevel``, modality, and returning a value.
- **Background work without freezing the UI** — ``after`` and worker threads,
  updating widgets safely from the main loop.

Presentation
------------

- **Animate a GIF** *(salvaged from the cookbook)* — frame-by-frame animation
  with ``PhotoImage``.
- **Splash screen** — a borderless startup window with ``window_type``.
- **Application icon** — set the window/taskbar icon.

.. toctree::
   :hidden:

   working-with-images
