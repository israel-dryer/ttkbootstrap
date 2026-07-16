Mark a window busy
==================

For a slow operation you want to both **show a wait cursor** and **stop the user
clicking** meanwhile. ``busy()`` does both: it covers the widget with a
transparent overlay that swallows mouse-pointer events and shows a busy cursor,
until you release it with ``busy_forget()``:

.. code-block:: python

   app.busy(cursor="watch")
   app.update()                  # paint the overlay + cursor before blocking
   do_slow_work()
   app.busy_forget()

The ``update`` call matters. The overlay is only mapped when the event loop next
runs, so without it the user sees nothing before the blocking work starts —
and Tk's own docs recommend a full ``update`` here, to guarantee the hold takes
effect before any queued clicks are dispatched.

Always release it
-----------------

Pair the calls with ``try``/``finally`` so an exception can't strand the app
looking busy forever:

.. code-block:: python

   app.busy(cursor="watch")
   app.update()
   try:
       do_slow_work()
   finally:
       app.busy_forget()

``busy_status()`` reports whether a widget is currently held busy — useful to
keep a slow action from being started twice:

.. code-block:: python

   if not app.busy_status():
       start_work()

.. warning::

   **The busy overlay is not supported on macOS.** The calls succeed and
   ``busy_status()`` still reports ``True``, but nothing is drawn and nothing is
   blocked — so it fails quietly rather than raising.

   On macOS, get the same effect by disabling the controls that start the work
   and setting the cursor yourself:

   .. code-block:: python

      def busy(is_busy):
          app.configure(cursor="watch" if is_busy else "")
          run.configure(state="disabled" if is_busy else "normal")

   A cursor set on the window covers everything inside it — a child with no
   cursor of its own inherits its parent's. This works on every platform.

.. note::

   The busy overlay itself is a Tk 8.6 feature, so it is there on every Python
   we support — but tkinter only grew the ``busy()`` / ``tk_busy_*`` methods in
   **3.13**. To use it on Python 3.10–3.12, call Tk directly; it is the same
   command underneath:

   .. code-block:: python

      app.tk.call("tk", "busy", "hold", app, "-cursor", "watch")
      app.update()
      try:
          do_slow_work()
      finally:
          app.tk.call("tk", "busy", "forget", app)

.. note::

   ``busy()`` differs from simply setting ``cursor="watch"``: besides the cursor,
   it blocks **pointer events** to the widget and everything inside it. It does
   not block the keyboard — a widget that already had focus keeps receiving
   keystrokes, so move focus off the busy area if that matters. Set ``cursor=``
   alone (see :doc:`Cursors </reference/cursors>`) when you only want to change
   the pointer.

.. note::

   The methods are also spelled ``tk_busy_hold`` / ``tk_busy_forget`` /
   ``tk_busy_status`` / ``tk_busy_configure``. Those are the same calls under
   their longer names, added in the same version.

Long work still needs a thread
------------------------------

The busy state only helps for work short enough to block on briefly — while the
main loop is blocked, the overlay is the *only* thing the window can do, and it
cannot repaint or animate. For genuinely long work, run it on a background thread
and marshal results back with ``after``, so the UI stays responsive while the
busy state is up.

.. seealso::

   - :doc:`Run background work <threads>` — the thread-and-``after`` pattern for
     work too long to block on.
   - :doc:`Ring the system bell <bell>` — the other half of telling the user what
     is going on.
   - :doc:`Windows guide </user-guide/feature-guides/windows>` — window-level
     behavior.

Reference
---------

- :doc:`Cursors </reference/cursors>` — the pointer names you can set.