Menus and context menus
=======================

tkinter menus are built from one widget — :class:`~ttkbootstrap.Menu` (the
blessed ``tk.Menu``, re-exported as ``ttk.Menu``). The *same* widget serves as a
menu bar across the top of a window, a drop-down cascade, and a right-click
popup; only how you attach it differs. This recipe covers a menu bar and a
context menu.

.. note::

   ``Menu`` is a classic ``tk`` widget, not a themed ``ttk`` one, so it does not
   take ``bootstyle``. ttkbootstrap still colors it to the active theme through
   the blessed ``ttk.Menu`` subclass — use that (or top-level ``ttk.Menu``), not
   a bare ``tkinter.Menu``.

A menu bar
----------

A menu bar is a ``Menu`` whose items are **cascades** — each cascade opens
another ``Menu`` of commands. Build the bar, build one submenu per top-level
entry, then hand the bar to the window with ``configure(menu=...)``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Editor")

   menubar = ttk.Menu(app)

   file_menu = ttk.Menu(menubar, tearoff=False)
   file_menu.add_command(label="New", command=lambda: print("new"))
   file_menu.add_command(label="Open…", command=lambda: print("open"))
   file_menu.add_separator()
   file_menu.add_command(label="Exit", command=app.destroy)
   menubar.add_cascade(label="File", menu=file_menu)

   edit_menu = ttk.Menu(menubar, tearoff=False)
   edit_menu.add_command(label="Undo", command=lambda: print("undo"))
   menubar.add_cascade(label="Edit", menu=edit_menu)

   app.configure(menu=menubar)     # attach the bar to the window

   app.mainloop()

- Each :meth:`add_command` takes a ``label`` and a ``command=`` callback — the
  same callback contract as a button.
- ``tearoff=False`` removes the dashed "tear this menu off" line at the top,
  which is a dated Tk default you almost always want off.
- :meth:`add_separator` draws a divider between groups.
- ``configure(menu=menubar)`` (equivalently ``app["menu"] = menubar``) installs
  the bar. It attaches to a top-level window — ``App`` or a ``Toplevel``.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The app with a **File** / **Edit** menu bar, the File menu open showing New,
   Open…, a separator, and Exit.

Checkbutton and radiobutton items
---------------------------------

Menus can hold stateful items bound to a variable, exactly like the widgets of
the same name. :meth:`add_checkbutton` toggles a ``BooleanVar``;
:meth:`add_radiobutton` items sharing one variable are mutually exclusive:

.. code-block:: python

   wrap = ttk.BooleanVar(value=True)
   view_menu = ttk.Menu(menubar, tearoff=False)
   view_menu.add_checkbutton(label="Word wrap", variable=wrap)

   theme = ttk.StringVar(value="light")
   for name in ("light", "dark"):
       view_menu.add_radiobutton(label=name.title(), value=name, variable=theme)

Read ``wrap.get()`` / ``theme.get()`` in your callbacks — the menu keeps the
variable in sync as the user toggles items. (See
:doc:`State & variables </user-guide/foundations/state-and-variables>`.)

A right-click context menu
--------------------------

A context menu is the same ``Menu`` widget, popped up at the pointer instead of
attached to a bar. Build it once, then bind the platform's right-click event to
a handler that calls :meth:`tk_popup` with the pointer's screen coordinates:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()
   target = ttk.Label(app, text="Right-click me", padding=40, bootstyle="inverse-secondary")
   target.pack(fill="both", expand=True)

   context = ttk.Menu(app, tearoff=False)
   context.add_command(label="Cut", command=lambda: print("cut"))
   context.add_command(label="Copy", command=lambda: print("copy"))
   context.add_command(label="Paste", command=lambda: print("paste"))

   def show_context(event):
       try:
           context.tk_popup(event.x_root, event.y_root)
       finally:
           context.grab_release()

   target.bind("<Button-3>", show_context)

   app.mainloop()

- ``event.x_root`` / ``event.y_root`` are the pointer's position in **screen**
  coordinates, which is what :meth:`tk_popup` expects.
- The ``try``/``finally`` with :meth:`grab_release` is the standard idiom — it
  makes sure the menu's input grab is released even if the user dismisses the
  popup without choosing anything.

.. admonition:: Right-click across platforms
   :class: note

   The right mouse button is ``<Button-3>`` on Windows and Linux. On macOS the
   right-click event is also ``<Button-2>`` on some setups, and a Control-click
   arrives as ``<Button-1>``; bind the extras when you target macOS::

      target.bind("<Button-3>", show_context)          # Windows / Linux / most macOS
      target.bind("<Button-2>", show_context)          # some macOS mice
      target.bind("<Control-Button-1>", show_context)  # macOS Control-click

.. seealso::

   The :doc:`Events guide </user-guide/feature-guides/events>` for the event
   object (``x_root``/``y_root`` and friends) and binding conventions, and the
   `tkinter menu reference
   <https://docs.python.org/3/library/tkinter.html>`_ for the full option set
   (accelerators, images, ``postcommand``).
