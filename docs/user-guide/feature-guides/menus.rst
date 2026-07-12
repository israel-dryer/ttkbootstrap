Menus
=====

Menus are built from a single widget — :class:`~ttkbootstrap.Menu`, imported as
``ttk.Menu``. The *same* widget plays three roles depending on how you attach it:
a **menu bar** across the top of a window, a **cascade** that drops down from a
bar entry, and a **popup** at the pointer for a right-click context menu. This
guide builds each in turn, then covers the part that trips people up — how a menu
bar differs across Windows, Linux, and macOS, where the application menu follows
its own rules.

.. note::

   ``Menu`` is a classic ``tk`` widget, not a themed ``ttk`` one, so it takes no
   ``bootstyle`` — but ttkbootstrap colors it to match the active theme
   automatically.

The menu widget
---------------

Every menu is a ``Menu`` you fill with **items**. The item kinds are the same
whatever role the menu plays:

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - Item
     - Adds…
   * - ``add_command(label=, command=)``
     - a clickable entry that runs a callback.
   * - ``add_cascade(label=, menu=)``
     - a submenu — another ``Menu`` opens from this entry.
   * - ``add_checkbutton(label=, variable=)``
     - a toggle bound to a ``BooleanVar``.
   * - ``add_radiobutton(label=, value=, variable=)``
     - one of a mutually exclusive set sharing a variable.
   * - ``add_separator()``
     - a divider line between groups.

A menu bar is just a menu whose items are cascades; a context menu is a menu you
pop up yourself. Build the items once — the structure is identical.

A menu bar
----------

Build the bar, build one submenu per top-level entry, then hand the bar to the
window with ``configure(menu=...)``:

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

- Each submenu takes the bar as its ``master`` (``ttk.Menu(menubar, …)``) and is
  attached with :meth:`add_cascade`.
- ``tearoff=False`` removes the dashed "tear this menu off" line at the top — a
  dated Tk default you almost always want off. (It is a no-op on macOS, which has
  no tearoffs.)
- ``configure(menu=menubar)`` (equivalently ``app["menu"] = menubar``) installs
  the bar on a top-level window — ``App`` or a ``Toplevel``.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The app with a **File** / **Edit** menu bar, the File menu open showing New,
   Open…, a separator, and Exit.

Keyboard shortcuts (accelerators)
---------------------------------

An **accelerator** is the shortcut hint shown at the right of a menu entry. It is
*only a label* — Tk does not bind it for you. Set ``accelerator=`` for the
display and ``bind`` the matching event yourself:

.. code-block:: python

   file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save)
   app.bind_all("<Control-s>", lambda event: save())

Keep the two in step: the accelerator string is cosmetic, the ``bind`` is what
actually fires. Use ``bind_all`` so the shortcut works regardless of which widget
has focus.

.. admonition:: Ctrl on Windows/Linux, Command on macOS
   :class: note

   The conventional modifier is **Ctrl** on Windows/Linux and **Command** on
   macOS. Branch on the windowing system so the label and the binding match the
   platform::

      import ttkbootstrap as ttk

      app = ttk.App()
      is_mac = ttk.windowing_system(app) == "aqua"
      accel = "Cmd+S" if is_mac else "Ctrl+S"
      seq = "<Command-s>" if is_mac else "<Control-s>"

      file_menu.add_command(label="Save", accelerator=accel, command=save)
      app.bind_all(seq, lambda event: save())

Stateful items
--------------

Menus can hold items bound to a variable, exactly like the widgets of the same
name. :meth:`add_checkbutton` toggles a ``BooleanVar``; a group of
:meth:`add_radiobutton` items sharing one variable is mutually exclusive:

.. code-block:: python

   wrap = ttk.BooleanVar(value=True)
   view_menu = ttk.Menu(menubar, tearoff=False)
   view_menu.add_checkbutton(label="Word wrap", variable=wrap)

   theme = ttk.StringVar(value="light")
   for name in ("light", "dark"):
       view_menu.add_radiobutton(label=name.title(), value=name, variable=theme)

The menu keeps the variable in sync as the user toggles items — read
``wrap.get()`` / ``theme.get()`` in your callbacks, or trace the variable to react
immediately (see :doc:`State & variables
</user-guide/foundations/state-and-variables>`).

Enabling, disabling, and rebuilding
-----------------------------------

Refer to an existing item by its label (or index) and change it with
:meth:`entryconfigure` — greying out **Paste** when there is nothing to paste,
say:

.. code-block:: python

   edit_menu.entryconfigure("Paste", state="disabled")
   edit_menu.entryconfigure("Paste", state="normal")     # re-enable

To decide an item's state *at the moment the menu opens*, give the menu a
``postcommand`` — it runs just before the menu is shown, the right hook for
"enable Paste only if the clipboard has text":

.. code-block:: python

   from tkinter import TclError

   def refresh_edit():
       try:
           can_paste = bool(app.clipboard_get())
       except TclError:                        # clipboard empty or not text
           can_paste = False
       edit_menu.entryconfigure("Paste", state="normal" if can_paste else "disabled")

   edit_menu.configure(postcommand=refresh_edit)

A right-click context menu
--------------------------

A context menu is the same ``Menu`` widget, popped up at the pointer instead of
attached to a bar. Build it once, then bind the right-click event to a handler
that calls :meth:`tk_popup` with the pointer's **screen** coordinates:

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

- ``event.x_root`` / ``event.y_root`` are the pointer's position in screen
  coordinates, which is what :meth:`tk_popup` expects.
- The ``try``/``finally`` with :meth:`grab_release` is the standard idiom — it
  releases the menu's input grab even if the user dismisses the popup without
  choosing anything.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The labeled target with a Cut / Copy / Paste context menu popped up at the
   pointer after a right-click.

.. admonition:: Right-click across platforms
   :class: note

   The right mouse button is ``<Button-3>`` on Windows and Linux. On macOS a
   right-click is also ``<Button-2>`` on some mice, and a Control-click arrives as
   ``<Button-1>``; bind the extras when you target macOS::

      target.bind("<Button-3>", show_context)          # Windows / Linux / most macOS
      target.bind("<Button-2>", show_context)          # some macOS mice
      target.bind("<Control-Button-1>", show_context)  # macOS Control-click

The menu bar across platforms
-----------------------------

A menu bar looks the same in code everywhere, but the OS decides where it lives
and how the first menu behaves. This is the one area worth understanding before
you ship cross-platform.

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Platform
     - Where the menu bar lives
   * - Windows / Linux
     - **Per window** — the bar sits at the top of each window it is attached to.
   * - macOS
     - **Global** — one bar at the top of the *screen*, shared by every window in
       the app. The first cascade becomes the bold **application menu** named
       after your app.

macOS: the application menu
~~~~~~~~~~~~~~~~~~~~~~~~~~~

On macOS the leftmost menu is the **application menu** (bold, your app's name),
and users expect *About*, *Preferences…*, and *Quit* to live there — not under
*File*. ``Menu`` builds these native slots for you: :meth:`add_application_menu`,
:meth:`add_window_menu`, and :meth:`add_help_menu` create the standard macOS
menus, and :meth:`on_preferences` / :meth:`on_quit` wire the standard commands.
Every one of them is a **no-op on Windows and Linux** — the ``add_*_menu``
helpers return ``None`` there — so a single code path builds a native-feeling bar
on every platform:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Editor")

   menubar = ttk.Menu(app)

   app_menu = menubar.add_application_menu()     # None off macOS
   if app_menu:
       app_menu.add_command(label="About Editor", command=show_about)
       app_menu.on_preferences(open_preferences)  # enables the Preferences… item (⌘,)
       app_menu.on_quit(save_and_quit)            # runs on Quit / ⌘Q
       menubar.add_window_menu()

   file_menu = ttk.Menu(menubar, tearoff=False)
   file_menu.add_command(label="New", command=new_file)
   menubar.add_cascade(label="File", menu=file_menu)

   menubar.add_help_menu(command=open_help)       # standard Help menu; ⌘? search on macOS

   app.configure(menu=menubar)
   app.mainloop()

The ``if app_menu:`` guard reads as *"if this platform has an application
menu."* On macOS ``app_menu`` is the real menu and its items land in the native
About/Preferences/Quit block; on Windows and Linux it is ``None``, so those items
are simply skipped — put your Exit and Preferences where those platforms expect
them (under *File* and *Edit*, say). ``add_help_menu`` returns an ordinary Help
cascade off macOS, so a Help menu is present everywhere.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The macOS screen-top menu bar with the bold **Editor** application menu open,
   showing About Editor, Preferences… (⌘,), and Quit.

.. seealso::

   :doc:`Windows </user-guide/feature-guides/windows>` for the cross-platform
   windowing model this builds on, the :doc:`Events guide
   </user-guide/feature-guides/events>` for the event object and binding
   conventions, and the `tkinter menu reference
   <https://docs.python.org/3/library/tkinter.html>`_ for the full option set.
