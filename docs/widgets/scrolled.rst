Scrolled
========

When content outgrows its window, plain tkinter makes you pair a widget with a
:doc:`Scrollbar <scrollbar>` and wire the two together by hand. ttkbootstrap
ships two widgets that do that wiring for you:

- ``ScrolledFrame`` — a frame with a scrollbar attached; pack or grid any widgets
  into it and it scrolls when they overflow.
- ``ScrolledText`` — a themed multi-line :doc:`Text <text>` with its scrollbar
  attached; its underlying ``Text`` is exposed as ``.text``.

Both take ``auto_hide=True`` to hide the scrollbar until the pointer enters the
region.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Settings", size=(360, 300))

   scroller = ttk.ScrolledFrame(app, auto_hide=True)
   scroller.pack(fill="both", expand=True, padx=10, pady=10)

   for i in range(40):
       ttk.Checkbutton(scroller, text=f"Option {i + 1}", bootstyle="round toggle").pack(anchor="w", pady=2)

   app.mainloop()

The full walkthrough — a scrollable form, a live log, read-only text, and
streaming output — lives in the How-To, which owns the usage:

.. seealso::

   - :doc:`Scroll long content </user-guide/how-to/scrollable>` — the complete
     guide to ``ScrolledFrame`` and ``ScrolledText``.
   - :doc:`Canvas <canvas>` / :doc:`Scrollbar <scrollbar>` — scrolling a drawing or
     a single widget yourself.
