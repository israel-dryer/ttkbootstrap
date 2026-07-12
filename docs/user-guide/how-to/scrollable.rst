Scroll long content
===================

When content outgrows its window — a long form, a wall of log text — you need a
scrollable region. Plain tkinter makes you pair a ``Canvas`` (or ``Text``) with
a ``Scrollbar`` and wire the two together by hand. ttkbootstrap ships two widgets
that do that wiring for you: :class:`~ttkbootstrap.ScrolledFrame` for arbitrary
widgets, and :class:`~ttkbootstrap.ScrolledText` for text. Both are re-exported
at the top level.

A scrollable frame
------------------

``ScrolledFrame`` is a frame with a scrollbar already attached. Treat it as the
parent for your content — pack or grid widgets **into it** and it scrolls when
they overflow:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Settings", size=(360, 300))

   scroller = ttk.ScrolledFrame(app, auto_hide=True)
   scroller.pack(fill="both", expand=True, padx=10, pady=10)

   for i in range(40):
       option = ttk.Checkbutton(scroller, text=f"Option {i + 1}", bootstyle="round toggle")
       option.pack(anchor="w", pady=2)

   app.mainloop()

- ``auto_hide=True`` hides the scrollbar until the pointer enters the region, then
  shows it — tidy for dense UIs. Leave it off (the default) to keep the scrollbar
  always visible.
- The frame scrolls vertically by default. Pass ``height=``/``width=`` to fix its
  size; without a fixed size it requests the size of its content.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The settings window showing a scrollable column of toggle options with the
   scrollbar appearing at the right edge.

.. note::

   Add your widgets with the ``ScrolledFrame`` as their ``master`` — not a child
   frame of your own. The widget manages an internal container and reparents
   your content into the scrollable area automatically.

A scrollable text box
---------------------

``ScrolledText`` is a themed multi-line text widget with its scrollbar attached.
The underlying :class:`tkinter.Text` is exposed as ``.text`` — reach through it
for the standard Text API (``insert``, ``get``, ``delete``, tags):

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Log", size=(480, 320))

   log = ttk.ScrolledText(app, auto_hide=True, padding=10)
   log.pack(fill="both", expand=True)

   log.text.insert("end", "Application started\n")
   log.text.insert("end", "Loading data…\n")
   log.text.see("end")            # scroll to the newest line

   app.mainloop()

- ``.text`` is the real ``Text`` widget — anything the `tkinter Text reference
  <https://docs.python.org/3/library/tkinter.html>`_ documents works on it.
- Pass ``hbar=True`` for a horizontal scrollbar too (off by default); ``vbar`` is
  on by default.
- ``see("end")`` keeps the newest content in view — the usual move for a log.

.. admonition:: Making a log read-only
   :class: note

   A ``Text`` is editable by default. To use one purely for output, set its
   ``state`` to ``"disabled"`` and flip it back around each write, since a
   disabled Text rejects ``insert`` too::

      log.text.configure(state="normal")
      log.text.insert("end", line)
      log.text.configure(state="disabled")

.. seealso::

   :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>` for
   packing and gridding content, and :doc:`Run background work <threads>` for
   streaming output into a ``ScrolledText`` without freezing the UI.
