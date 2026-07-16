Cursors
=======

Every widget takes a ``cursor`` option that sets the mouse pointer shown while it
is over the widget. Pass one of the names below; an empty string resets it so the
widget inherits its parent's cursor.

.. code-block:: python

   entry = ttk.Entry(app, cursor="xterm")     # text I-beam over this entry
   app.configure(cursor="watch")              # busy pointer over the whole window
   app.configure(cursor="")                   # back to the default

.. note::

   The names come from Tk's ``cursor`` command, whose reference lives in a
   C-oriented `Tk manual page
   <https://www.tcl.tk/man/tcl8.6/TkCmd/cursors.htm>`__. A cursor's **appearance
   is platform-dependent** — the same name can look different on Windows, macOS,
   and Linux, and several names map to the same system pointer. For a busy
   pointer over a whole window, prefer the ``busy`` helper — see
   :doc:`Mark a window busy </user-guide/how-to/busy>`.

Common cursors
--------------

The pointers you will actually reach for, and what each conventionally means.

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Name
     - Meaning / typical use
   * - | ``arrow``
       | ``left_ptr``
     - The default pointer.
   * - ``xterm``
     - Text I-beam — over editable text.
   * - ``hand2``
     - Pointing hand — a clickable link or hotspot.
   * - ``hand1``
     - Open hand — a draggable / grabbable area.
   * - ``fleur``
     - Four-way move arrows — drag to reposition.
   * - ``watch``
     - Busy / working (an ``arrow`` + hourglass on Windows).
   * - | ``crosshair``
       | ``tcross``
     - Precise selection or drawing.
   * - ``sizing``
     - Resize from a corner.
   * - ``sb_h_double_arrow``
     - Horizontal resize (↔) — a vertical split or column edge.
   * - ``sb_v_double_arrow``
     - Vertical resize (↕) — a horizontal split or row edge.
   * - ``question_arrow``
     - Context help.
   * - ``plus``
     - Add, or cell selection.
   * - ``pencil``
     - Draw or edit.
   * - ``circle``
     - Action not allowed.
   * - ``pirate``
     - Delete / kill (a skull-and-crossbones).
   * - | ``dotbox``
       | ``target``
       | ``dot``
     - Miscellaneous marking pointers.

Setting a cursor while busy
---------------------------

A common use is showing a wait pointer during a slow operation, then restoring
it. Force the pointer to update before the work starts:

.. code-block:: python

   app.configure(cursor="watch")
   app.update_idletasks()        # show the cursor before blocking
   do_slow_work()
   app.configure(cursor="")      # restore

See :doc:`Mark a window busy </user-guide/how-to/busy>` for the ``busy``
helper, which does this for a whole window (and disables input) in one call.

All portable names
------------------

These names come from the X11 cursor font and are accepted on **all platforms**.
Many are legacy or decorative shapes (``gumby``, ``coffee_mug``, ``spraycan``)
that map to a generic pointer outside X11 — the common set above is what renders
distinctly everywhere.

.. hlist::
   :columns: 4

   * ``X_cursor``
   * ``arrow``
   * ``based_arrow_down``
   * ``based_arrow_up``
   * ``boat``
   * ``bogosity``
   * ``bottom_left_corner``
   * ``bottom_right_corner``
   * ``bottom_side``
   * ``bottom_tee``
   * ``box_spiral``
   * ``center_ptr``
   * ``circle``
   * ``clock``
   * ``coffee_mug``
   * ``cross``
   * ``cross_reverse``
   * ``crosshair``
   * ``diamond_cross``
   * ``dot``
   * ``dotbox``
   * ``double_arrow``
   * ``draft_large``
   * ``draft_small``
   * ``draped_box``
   * ``exchange``
   * ``fleur``
   * ``gobbler``
   * ``gumby``
   * ``hand1``
   * ``hand2``
   * ``heart``
   * ``icon``
   * ``iron_cross``
   * ``left_ptr``
   * ``left_side``
   * ``left_tee``
   * ``leftbutton``
   * ``ll_angle``
   * ``lr_angle``
   * ``man``
   * ``middlebutton``
   * ``mouse``
   * ``pencil``
   * ``pirate``
   * ``plus``
   * ``question_arrow``
   * ``right_ptr``
   * ``right_side``
   * ``right_tee``
   * ``rightbutton``
   * ``rtl_logo``
   * ``sailboat``
   * ``sb_down_arrow``
   * ``sb_h_double_arrow``
   * ``sb_left_arrow``
   * ``sb_right_arrow``
   * ``sb_up_arrow``
   * ``sb_v_double_arrow``
   * ``shuttle``
   * ``sizing``
   * ``spider``
   * ``spraycan``
   * ``star``
   * ``target``
   * ``tcross``
   * ``top_left_arrow``
   * ``top_left_corner``
   * ``top_right_corner``
   * ``top_side``
   * ``top_tee``
   * ``trek``
   * ``ul_angle``
   * ``umbrella``
   * ``ur_angle``
   * ``watch``
   * ``xterm``

Platform-specific names
-----------------------

Windows and macOS add native pointers on top of the portable set. **Windows**
provides:

.. hlist::
   :columns: 4

   * ``no``
   * ``starting``
   * ``size``
   * ``size_ne_sw``
   * ``size_ns``
   * ``size_nw_se``
   * ``size_we``
   * ``uparrow``
   * ``wait``

**macOS** adds its own native cursors (copy, alias, contextual-menu, and resize
variants, among others). Because these are not portable, see the `Tk cursor
manual page <https://www.tcl.tk/man/tcl8.6/TkCmd/cursors.htm>`__ for the exact
platform lists.

.. warning::

   Tk on Windows accepts *any* of these names without error, but a name outside
   what the platform supports falls back to a generic pointer rather than
   raising — so an unsupported cursor fails silently. Stick to the common set for
   a consistent result across platforms.
