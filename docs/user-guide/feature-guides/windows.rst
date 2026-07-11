Windows & high-DPI
==================

``App`` (also exported as ``ttk.Window``) and ``ttk.Toplevel`` are enhanced
replacements for ``tk.Tk``/``tk.Toplevel`` that fold window setup into the
constructor and add ttkbootstrap-specific conveniences.

Focus, modality & lifecycle
---------------------------

Beyond its size and position, a window has three behaviors you control in code:
which window has the **keyboard focus**, whether it is **modal** (blocks the rest
of the app), and its **lifecycle** — mapping, closing, and cleanup. These apply
to any window; a second window is always a ``Toplevel``.

.. note::

   ``ttk.Toplevel``'s first positional argument is the **title**, not the parent
   — ``ttk.Toplevel(app)`` would set the title to the app object. Pass the parent
   as ``master=``:

   .. code-block:: python

      win = ttk.Toplevel(master=app, title="Details")

Focus
~~~~~

The focused widget receives keyboard input. Tk moves focus as the user tabs and
clicks; to direct it yourself, call ``focus_set()`` on a widget once its window
is mapped:

.. code-block:: python

   entry.focus_set()          # put the cursor in this entry

``focus_get()`` returns the widget that currently has focus (or ``None``).
``focus_force()`` steals focus even from other applications — it is disruptive,
so avoid it unless you truly must.

Stacking and satellites
~~~~~~~~~~~~~~~~~~~~~~~~~

``lift()`` raises a window above its siblings; ``lower()`` drops it behind them.
Marking a window **transient** to a parent makes it a satellite: it stays above
the parent, minimizes with it, and is kept off the taskbar — the right setting
for dialogs and inspectors. Set it in the constructor or later:

.. code-block:: python

   win = ttk.Toplevel(master=app, title="Inspector", transient=app)
   # or later:  win.transient(app)

Modality
~~~~~~~~

A **modal** window blocks interaction with the rest of the app until it closes.
Two calls make it so:

- ``grab_set()`` routes all input to the window — a **local** grab, confined to
  your application. (Avoid ``grab_set_global()``, which grabs the entire screen.)
  ``grab_release()`` ends it, and ``grab_status()`` reports ``"local"``,
  ``"global"``, or ``None``.
- ``parent.wait_window(win)`` blocks the calling code until ``win`` is destroyed.

Because ``wait_window`` returns only *after* the window closes, the window can
leave a result behind for the caller to read — that is how a dialog "returns a
value." The :doc:`Multiple windows how-to </user-guide/how-to/multiple-windows>`
puts these together into a reusable modal dialog.

Lifecycle
~~~~~~~~~

A window can be hidden and shown without being rebuilt: ``withdraw()`` removes it
from view, ``deiconify()`` restores it, and ``iconify()`` minimizes it. Reuse an
expensive window this way instead of recreating it.

``destroy()`` closes a window for good and tears down its child widgets. Cancel
any ``after`` timers or variable traces first, or they fire against dead widgets.

Clicking the window's close button (**✕**) does not call ``destroy()`` directly —
it fires the ``WM_DELETE_WINDOW`` protocol, which *defaults* to destroying the
window. Register a handler to confirm or veto the close instead:

.. code-block:: python

   def on_close():
       if user_confirms():
           win.destroy()      # closing happens only if you call it
       # returning without destroy() cancels the close

   win.protocol("WM_DELETE_WINDOW", on_close)

Still to come in this guide
---------------------------

.. note::

   The rest of this guide is being written for 2.0. It will also cover:

- **The constructor surface** — ``title``, ``size``, ``position`` (signed and
  edge-relative), ``minsize``/``maxsize``, ``resizable``, ``alpha``,
  ``iconphoto``, plus the renamed ``high_dpi``/``override_redirect``.
- **Positioning** — ``place_window_center()`` (monitor-aware when ``screeninfo``
  is installed, clamped on-screen).
- **Light/dark mode** — the settable ``theme_mode`` property, ``toggle_theme()``,
  and ``set_theme_modes(light=, dark=)``.
- **Toplevels** — ``window_type``, ``topmost``, ``tool_window``, and inherited
  app icons.
- **High-DPI** — ``enable_high_dpi_awareness()`` and ``scale_size()``.
- **Sidebar: the deferred-config seam** — how ``set_locale``,
  ``set_global_family``, and ``set_default_button`` can be called before the root
  exists and flush when it comes up.
