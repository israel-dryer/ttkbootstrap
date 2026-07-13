Canvas
======

``Canvas`` is tkinter's drawing surface (``tk.Canvas``) — a 2-D area that holds
**items** (lines, shapes, text, images, embedded widgets) you create, move,
restyle, and delete by id or tag. It is themed by ttkbootstrap. This page is the
complete reference for its own options and methods; the shared widget methods are
under :doc:`Capabilities </reference/capabilities/index>`.

Items, ids, and tags
--------------------

``create_*`` returns an integer **id** that names one item. You can also attach
**tags** (string labels) to items, and any method that takes ``tagOrId`` acts on
a single id or on every item carrying a tag — so ``"all"`` (a predefined tag)
addresses the whole canvas. Coordinates are in canvas space, which the
``scrollregion`` and the ``xview``/``yview`` methods pan over.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``autostyle``
     - ``bool``
     - **Constructor only.** ``True`` (default) paints the canvas with the active
       theme and repaints on a theme switch; ``False`` opts out. This is
       ttkbootstrap's one addition — everything below is native tk.
   * - ``background`` (``bg``)
     - ``str``
     - The surface color.
   * - ``width``
     - ``int``
     - The requested width in pixels.
   * - ``height``
     - ``int``
     - The requested height in pixels.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The 3-D border width in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight around the widget.
   * - ``highlightcolor``
     - ``str``
     - The focus-highlight color when the widget has focus.
   * - ``highlightbackground``
     - ``str``
     - The focus-highlight color when the widget does not have focus.
   * - ``scrollregion``
     - ``tuple``
     - The scrollable area as ``(left, top, right, bottom)`` in canvas
       coordinates.
   * - ``confine``
     - ``bool``
     - Whether to keep the view inside ``scrollregion``.
   * - ``xscrollcommand``
     - ``callable``
     - A callback connecting the canvas to a horizontal scrollbar.
   * - ``yscrollcommand``
     - ``callable``
     - A callback connecting the canvas to a vertical scrollbar.
   * - ``xscrollincrement``
     - ``int``
     - The step size for horizontal "unit" scrolling, in pixels.
   * - ``yscrollincrement``
     - ``int``
     - The step size for vertical "unit" scrolling, in pixels.
   * - ``selectbackground``
     - ``str``
     - The background of selected text within an editable text item.
   * - ``selectforeground``
     - ``str``
     - The foreground of selected text within an editable text item.
   * - ``selectborderwidth``
     - ``int``
     - The border width of the selection, in pixels.
   * - ``insertbackground``
     - ``str``
     - The color of the text insert cursor.
   * - ``insertwidth``
     - ``int``
     - The width of the insert cursor, in pixels.
   * - ``insertborderwidth``
     - ``int``
     - The border width of the insert cursor, in pixels.
   * - ``insertontime``
     - ``int``
     - The insert-cursor blink on-time, in milliseconds.
   * - ``insertofftime``
     - ``int``
     - The insert-cursor blink off-time, in milliseconds.
   * - ``state``
     - ``str``
     - The default item state: ``"normal"``, ``"disabled"``, or ``"hidden"``.
   * - ``closeenough``
     - ``float``
     - How near (in pixels) the pointer must be to count as "over" an item.
   * - ``offset``
     - ``str``
     - The origin for tiled stipple/fill patterns.
   * - ``cursor``
     - ``str``
     - The mouse cursor over the canvas (see :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the canvas accepts keyboard focus.

Methods
-------

Creating items
~~~~~~~~~~~~~~

Each ``create_*`` takes the item's coordinates followed by keyword options and
returns the new item's integer id. Common options: ``fill``, ``outline``,
``width``, ``stipple``, ``dash``, ``state``, and ``tags``.

.. py:method:: create_line(x0, y0, x1, y1, ..., **options)
   :noindex:

   Draw a line (or multi-point path) through the given points.

   :param options: ``fill``, ``width``, ``dash``, ``arrow``
      (``"first"``/``"last"``/``"both"``), ``smooth``, ``capstyle``,
      ``joinstyle``, ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_rectangle(x0, y0, x1, y1, **options)
   :noindex:

   Draw a rectangle from two opposite corners.

   :param options: ``fill``, ``outline``, ``width``, ``dash``, ``state``,
      ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_oval(x0, y0, x1, y1, **options)
   :noindex:

   Draw an ellipse bounded by the given rectangle.

   :returns: the new item id.
   :rtype: int

.. py:method:: create_polygon(x0, y0, x1, y1, ..., **options)
   :noindex:

   Draw a closed polygon through three or more points.

   :param options: ``fill``, ``outline``, ``width``, ``smooth``, ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_arc(x0, y0, x1, y1, **options)
   :noindex:

   Draw an arc, chord, or pie slice within the bounding rectangle.

   :param options: ``start`` (degrees), ``extent`` (degrees), ``style``
      (``"pieslice"``/``"chord"``/``"arc"``), ``fill``, ``outline``, ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_text(x, y, **options)
   :noindex:

   Place a string of text at a point.

   :param options: ``text``, ``font``, ``fill``, ``anchor``, ``justify``,
      ``width`` (wrap), ``angle``, ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_image(x, y, **options)
   :noindex:

   Place an image at a point.

   :param options: ``image`` (a ``PhotoImage``), ``anchor``, ``state``, ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_bitmap(x, y, **options)
   :noindex:

   Place a bitmap at a point.

   :param options: ``bitmap``, ``anchor``, ``foreground``, ``background``,
      ``tags``.
   :returns: the new item id.
   :rtype: int

.. py:method:: create_window(x, y, **options)
   :noindex:

   Embed a child widget on the canvas at a point.

   :param options: ``window`` (an existing widget), ``anchor``, ``width``,
      ``height``, ``tags``.
   :returns: the new item id.
   :rtype: int

Coordinates and geometry
~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: coords(tagOrId, *coords)
   :noindex:

   Get or set an item's coordinates.

   :param tagOrId: the item to address.
   :param coords: new coordinates to set; omit to query.
   :returns: the current coordinates (flat list) when queried, else ``None``.
   :rtype: list | None

.. py:method:: move(tagOrId, dx, dy)
   :noindex:

   Shift matching items by an offset.

   :param dx: horizontal delta, in pixels.
   :param dy: vertical delta, in pixels.
   :returns: ``None``.

.. py:method:: moveto(tagOrId, x='', y='')
   :noindex:

   Move matching items so their top-left is at an absolute position.

   :returns: ``None``.

.. py:method:: scale(tagOrId, xOrigin, yOrigin, xScale, yScale)
   :noindex:

   Scale matching items about an origin point.

   :param xScale: horizontal scale factor.
   :param yScale: vertical scale factor.
   :returns: ``None``.

.. py:method:: bbox(*tagsOrIds)
   :noindex:

   Return the bounding box that encloses the matching items.

   :returns: ``(x1, y1, x2, y2)`` in pixels, or ``None`` if nothing matches.
   :rtype: tuple | None

.. py:method:: canvasx(screenx, gridspacing=None)
   :noindex:

   Convert a window x coordinate to a canvas x coordinate (accounting for
   scrolling), optionally snapped to a grid.

   :rtype: float

.. py:method:: canvasy(screeny, gridspacing=None)
   :noindex:

   Vertical counterpart of :py:meth:`canvasx`.

   :rtype: float

Configuring items
~~~~~~~~~~~~~~~~~

.. py:method:: itemconfigure(tagOrId, **options)
   :noindex:

   Set (or query) options on matching items. Alias: ``itemconfig``.

   :param tagOrId: the item(s) to change.
   :param options: any options valid for the item type (``fill``, ``outline``,
      ``width``, ``text``, ``state``, ``tags``, …).
   :returns: the option spec when queried with a single option name, else
      ``None``.

.. py:method:: itemcget(tagOrId, option)
   :noindex:

   Return one option of the first matching item.

.. py:method:: type(tagOrId)
   :noindex:

   Return the type of the first matching item.

   :returns: ``"line"``, ``"rectangle"``, ``"oval"``, ``"polygon"``, ``"arc"``,
      ``"text"``, ``"image"``, ``"bitmap"``, or ``"window"``.
   :rtype: str

Finding items
~~~~~~~~~~~~~

.. py:method:: find_all()
   :noindex:

   Return the ids of every item, in stacking order.

   :rtype: tuple[int, ...]

.. py:method:: find_withtag(tagOrId)
   :noindex:

   Return the ids of items matching a tag or id.

   :rtype: tuple[int, ...]

.. py:method:: find_closest(x, y, halo=None, start=None)
   :noindex:

   Return the single item nearest a point (topmost on ties).

   :param halo: treat items within this many pixels as touching the point.
   :param start: search below this item in the stacking order.
   :rtype: tuple[int]

.. py:method:: find_overlapping(x1, y1, x2, y2)
   :noindex:

   Return the ids of items that overlap the given rectangle.

   :rtype: tuple[int, ...]

.. py:method:: find_enclosed(x1, y1, x2, y2)
   :noindex:

   Return the ids of items completely enclosed by the given rectangle.

   :rtype: tuple[int, ...]

Tagging
~~~~~~~

.. py:method:: gettags(tagOrId)
   :noindex:

   Return the tags on the first matching item.

   :rtype: tuple[str, ...]

.. py:method:: addtag_withtag(newtag, tagOrId)
   :noindex:

   Add a tag to every item matching ``tagOrId``. (Companions select by position:
   ``addtag_above``/``_below``/``_closest``/``_enclosed``/``_overlapping``/
   ``_all``.)

   :returns: ``None``.

.. py:method:: dtag(tagOrId, tagToDelete=None)
   :noindex:

   Remove a tag from matching items (the items themselves remain).

   :returns: ``None``.

Deleting
~~~~~~~~

.. py:method:: delete(*tagsOrIds)
   :noindex:

   Delete every matching item from the canvas.

   :returns: ``None``.

Item events and stacking
~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: tag_bind(tagOrId, sequence=None, func=None, add=None)
   :noindex:

   Bind an event to items — the way to make canvas items clickable/hoverable.

   :param sequence: an event sequence, e.g. ``"<Button-1>"``.
   :param func: the callback, receiving the event object.
   :param add: ``"+"`` to add rather than replace.
   :returns: a binding id.
   :rtype: str

.. py:method:: tag_unbind(tagOrId, sequence, funcid=None)
   :noindex:

   Remove an item binding.

   :returns: ``None``.

.. py:method:: tag_raise(tagOrId, aboveThis=None)
   :noindex:

   Raise matching items in the stacking order (drawn on top). Alias: ``lift``.

   :returns: ``None``.

.. py:method:: tag_lower(tagOrId, belowThis=None)
   :noindex:

   Lower matching items in the stacking order. Alias: ``lower``.

   :returns: ``None``.

Editing text items
~~~~~~~~~~~~~~~~~~

These act on editable ``text`` (and ``window``) items, using a character index
or the special indices ``"insert"``, ``"end"``, ``"sel.first"``/``"sel.last"``.

.. py:method:: insert(tagOrId, index, string)
   :noindex:

   Insert text into an item at a character index.

   :returns: ``None``.

.. py:method:: dchars(tagOrId, first, last=None)
   :noindex:

   Delete characters from an item between two indices.

   :returns: ``None``.

.. py:method:: index(tagOrId, index)
   :noindex:

   Resolve a text-item index expression to an integer character position.

   :rtype: int

.. py:method:: icursor(tagOrId, index)
   :noindex:

   Move the insert cursor within a text item.

   :returns: ``None``.

Scrolling
~~~~~~~~~

.. py:method:: xview(*args)
   :noindex:

   Query or set the horizontal view; usually wired to a scrollbar via
   ``xscrollcommand``. ``yview`` is the vertical counterpart, and both have
   ``*_moveto(fraction)`` and ``*_scroll(number, what)`` variants.

   :returns: with no args, the visible fraction ``(first, last)``; else ``None``.
   :rtype: tuple | None

.. py:method:: scan_mark(x, y)
   :noindex:

   Record a starting point for a fast drag-scroll (paired with ``scan_dragto``).

   :returns: ``None``.

.. py:method:: scan_dragto(x, y, gain=10)
   :noindex:

   Scroll the view relative to the ``scan_mark`` point, multiplied by ``gain``.

   :returns: ``None``.

Export
~~~~~~

.. py:method:: postscript(**options)
   :noindex:

   Render the canvas (or a region of it) to PostScript.

   :param options: ``file=`` a path or ``None`` to return the text; ``x``/``y``/
      ``width``/``height`` for a region; ``colormode``
      (``"color"``/``"gray"``/``"mono"``); ``pagewidth``/``pageheight``.
   :returns: the PostScript text when no ``file`` is given, else ``None``.
   :rtype: str | None

Shared capabilities
-------------------

``Canvas`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- `Tk canvas manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/canvas.htm>`__
  — the canonical upstream reference (Tcl 8.6).
