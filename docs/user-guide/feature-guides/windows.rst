Windows
=======

``App`` (also exported as ``ttk.Window``) and ``ttk.Toplevel`` are enhanced
replacements for ``tk.Tk`` / ``tk.Toplevel`` that fold window setup — size,
position, icon, constraints — into the constructor, so a window is configured in
one call instead of a scatter of ``geometry`` / ``minsize`` / ``wm_*`` calls
afterward. Keep **one** ``App`` per program (the single-root rule — see
:doc:`Structuring an app </user-guide/getting-started/app-structures>`); every
other window is a ``Toplevel``.

Creating the main window
------------------------

The one thing ``App`` needs is nothing — ``ttk.App()`` gives you a themed window.
Everything else is a keyword you set once, up front:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(
       title="Invoices",
       theme="nord-light",
       size=(800, 600),
       position=(200, 120),
       minsize=(480, 360),
   )

   app.mainloop()

- ``size=(width, height)`` and ``position=(x, y)`` are pixel tuples; set
  either or both. ``position`` is signed and **edge-relative** — a negative
  coordinate measures from the opposite screen edge, so ``position=(-20, -20)``
  pins the window near the bottom-right corner.
- ``minsize`` / ``maxsize=(width, height)`` clamp how far the user can resize;
  ``resizable=(horizontal, vertical)`` takes two booleans to lock an axis
  entirely (``resizable=(True, False)`` allows width but fixes height).
- ``alpha`` sets window transparency from ``0.0`` to ``1.0`` (opaque).
- ``iconphoto`` sets the titlebar icon from an image path; the default is
  ttkbootstrap's brand icon, and ``iconphoto=None`` leaves the platform default.

.. note::

   ``theme=`` is the canonical name; ``themename=`` is a permanent alias (the
   pre-2.0 spelling). ``Window`` is likewise a permanent alias for ``App`` — use
   whichever reads better. For choosing and switching themes, see
   :doc:`Theming & Colors </user-guide/feature-guides/theming>`.

Second windows — ``Toplevel``
-----------------------------

Every window after the first is a ``ttk.Toplevel``. It shares ``App``'s
constructor conveniences (``size``, ``position``, ``iconphoto``, …) and inherits
the app's theme and icon automatically.

.. warning::

   ``Toplevel``'s **first positional argument is the title**, not the parent —
   ``ttk.Toplevel(app)`` sets the *title* to the app object. Pass the parent as
   ``master=``:

   .. code-block:: python

      win = ttk.Toplevel(master=app, title="Details", size=(400, 300))

``Toplevel`` adds a few window-manager options ``App`` doesn't need:

- ``topmost=True`` keeps the window above all others.
- ``tool_window=True`` gives it a thin tool-window frame and keeps it off the
  taskbar (Windows).
- ``window_type=...`` requests a window kind from the OS — ``"splash"``,
  ``"utility"``, ``"tooltip"`` — used for borderless/auxiliary windows (mapped to
  native styles on macOS, an X11 hint on Linux).
- ``iconify=True`` starts the window minimized.
- ``transient=parent`` marks it a satellite of ``parent`` (next section).

Focus, modality & lifecycle
---------------------------

Beyond its size and position, a window has three behaviors you control in code:
which window has the **keyboard focus**, whether it is **modal** (blocks the rest
of the app), and its **lifecycle** — mapping, closing, and cleanup. These apply
to any window.

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
puts these together into a reusable modal dialog, and the
:doc:`Dialogs guide </user-guide/feature-guides/dialogs>` covers the shipped
modal dialogs built on the same mechanism.

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

Positioning
-----------

``place_window_center()`` centers a window on screen — on the monitor under the
mouse cursor when the optional ``screeninfo`` package is installed, and clamped so
the window stays fully visible either way. Call it *after* the window's size is
known (the constructor ``size`` counts):

.. code-block:: python

   win = ttk.Toplevel(master=app, title="About", size=(360, 200))
   win.place_window_center()

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A small Toplevel centered over its parent window with ``place_window_center``.

Light & dark
------------

A window follows the active theme, and its light/dark mode is switched through the
same ``App``: ``app.theme_mode`` reads ``"light"`` / ``"dark"``,
``app.toggle_theme()`` flips between the family's pair, and
``App(light_theme=..., dark_theme=...)`` designates which two to toggle. The
:doc:`Theming & Colors </user-guide/feature-guides/theming>` guide covers this in
full.

High-DPI displays
-----------------

On a high-resolution display, an unaware app renders tiny and blurry. ``App``
turns on high-DPI awareness by **default** (``high_dpi=True``) on Windows, so most
apps need nothing. Two utilities cover the rest:

- ``enable_high_dpi_awareness(root=None, scaling=None)`` — the manual control.
  On Windows it must run *before* the root exists (``App`` already does this); on
  Linux, pass the root and a ``scaling`` factor (``1.6``–``2.0`` is typical) after
  creating it to scale the whole UI.
- ``scale_size(widget, size)`` — convert a logical size to physical pixels for
  the current display, for code that sets pixel geometry or builds image assets:

  .. code-block:: python

     ttk.scale_size(app, 24)          # 24 logical px -> physical px for this display
     ttk.scale_size(app, [24, 24])    # a (width, height) pair -> scaled ints

.. admonition:: Sidebar — the deferred-config seam
   :class: note

   A few settings need to apply before any widget is built but read most naturally
   at the top of the file, before ``App()`` exists. ``set_locale``,
   ``set_global_family``, and ``set_default_button`` **queue** when called
   pre-root and flush the moment the root comes up (they apply live if a root
   already exists), so this works as written:

   .. code-block:: python

      import ttkbootstrap as ttk

      ttk.set_global_family("Segoe UI")     # queued...
      ttk.set_default_button("primary")

      app = ttk.App()                        # ...applied here

.. seealso::

   :doc:`Structuring an app </user-guide/getting-started/app-structures>` for the
   single-root rule, :doc:`Theming & Colors </user-guide/feature-guides/theming>`
   for themes and light/dark, and the :doc:`Multiple windows how-to
   </user-guide/how-to/multiple-windows>` for second-window recipes.
