Show a splash screen
====================

A splash screen is a borderless window shown while an app gets ready, replaced
by the real window once the work is done. This recipe builds one that reports
its progress and then hands off to the main window.

Hide the main window first
--------------------------

The application root exists from the moment you create ``App``, so the order is:
create the root, hide it, show the splash, then bring the root back when the
work is finished.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="bootstrap-light", size=(600, 400), title="Contact Book")
   app.withdraw()

``withdraw`` takes the window off the screen without destroying it —
``deiconify`` puts it back later. Build the main window's widgets now, while it
is hidden; that is usually the slow part you want the splash to cover.

Build the splash
----------------

The splash is a ``Toplevel``. Two options strip the window chrome, and you want
both — each covers different platforms:

.. code-block:: python

   splash = ttk.Toplevel(
       window_type="splash",
       override_redirect=True,
       topmost=True,
       size=(360, 200),
   )

   panel = ttk.Frame(splash, bootstyle="primary").pack(fill="both", expand=True)
   ttk.Label(panel, text="Contact Book", bootstyle="inverse-primary",
             font="-size 18 -weight bold").pack(pady=(50, 4))
   status = ttk.Label(panel, text="Starting…", bootstyle="inverse-primary")
   status.pack()

   splash.place_window_center()

``topmost`` keeps it above other windows, and ``place_window_center`` puts it in
the middle of the screen. A splash has no titlebar to drag, so centering it is
not a nicety — it's the only placement the user gets.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Option
     - What it does
   * - ``window_type="splash"``
     - Removes the chrome on Linux and macOS. On macOS it also gets the window
       a real system shadow and rounded corners. Ignored on Windows.
   * - ``override_redirect=True``
     - Removes the chrome on Windows and Linux. Ignored on macOS, where it
       breaks click handling.

Show it, then work
------------------

``mainloop`` is not running yet, so nothing you have built has been drawn.
Call ``update`` to pump the event loop once and paint the splash:

.. code-block:: python

   app.update()

   status.configure(text="Loading contacts…")
   app.update()
   load_contacts()

   status.configure(text="Connecting…")
   app.update()
   connect()

Every time you change the status text, ``update`` again — otherwise the label
holds its old text until the next time the event loop runs, which is after all
your work has finished.

Hand off to the main window
---------------------------

Destroy the splash, show the real window, and start the event loop:

.. code-block:: python

   splash.destroy()
   app.deiconify()
   app.mainloop()

.. note::

   Sprinkling ``update`` through a slow startup keeps the splash painted, but the
   app is still frozen between calls — the splash won't redraw if it's dragged
   over, and a spinner won't spin. If your startup is long enough to care, run
   the work on a thread and let the splash animate while it runs; see
   :doc:`Run background work <threads>`.

.. seealso::

   - :doc:`Open a second window <multiple-windows>` — ``Toplevel`` windows,
     modals, and the close button.
   - :doc:`Windows guide </user-guide/feature-guides/windows>` — the window
     geometry and state model in full.
   - :doc:`Animate a GIF <animate-gif>` — a spinner for the splash to show while
     it waits.

Reference
---------

- :doc:`Toplevel </reference/windows/toplevel>` — ``window_type``,
  ``override_redirect``, ``topmost``, and ``place_window_center``.
- :doc:`App </reference/windows/app>` — ``withdraw`` and ``deiconify``.
- :doc:`Lifecycle </reference/capabilities/lifecycle>` — ``update``, and what
  pumping the event loop by hand actually does.