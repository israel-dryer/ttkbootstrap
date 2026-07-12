Text
====

``Text`` is tkinter's multi-line text widget (``tk.Text``), themed by
ttkbootstrap. This page is the complete reference for its **own** options and
methods — the shared capabilities every widget has (configuration, lifecycle,
focus, introspection) are listed at the bottom.

For a task-oriented walkthrough — indices, tags, marks, search, undo — see the
:doc:`Text widget guide </widgets/text>`.

.. note::

   Python's standard library doesn't document ``tk.Text`` in full. This reference
   is maintained by ttkbootstrap. The canonical upstream source is the
   `Tk text manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/text.htm>`__
   (Tcl 8.6, the version Python ships) — where a Tcl subcommand like
   ``tag configure`` is the Python method ``tag_configure``.

Options
-------

Set at construction or with ``configure(...)``; read with ``cget("name")``.

.. rubric:: Text and wrapping

.. list-table::
   :widths: 26 74

   * - ``font``
     - The default font for the text (a family/size tuple or a named font).
   * - ``wrap``
     - How lines that exceed the width wrap: ``"char"``, ``"word"``, or
       ``"none"`` (no wrap — scroll horizontally instead).
   * - ``tabs``
     - Tab stops, as a list of distances (optionally each followed by
       ``"left"``/``"right"``/``"center"``/``"numeric"``).
   * - ``tabstyle``
     - How tabs interact with the ``tabs`` list: ``"tabular"`` or ``"wordprocessor"``.
   * - ``spacing1``
     - Extra vertical space above the first display line of each text line.
   * - ``spacing2``
     - Extra vertical space between the display lines of a single wrapped line.
   * - ``spacing3``
     - Extra vertical space below the last display line of each text line.

.. rubric:: Colors

.. list-table::
   :widths: 26 74

   * - ``foreground`` (``fg``)
     - The text color.
   * - ``background`` (``bg``)
     - The page (background) color.
   * - ``selectforeground``
     - Text color within the selection.
   * - ``selectbackground``
     - Background color of the selection.
   * - ``inactiveselectbackground``
     - Selection background when the widget doesn't have focus (empty string
       hides the selection when unfocused).

.. rubric:: Insert cursor

.. list-table::
   :widths: 26 74

   * - ``insertbackground``
     - Color of the blinking insert cursor.
   * - ``insertwidth``
     - Width of the insert cursor, in pixels.
   * - ``insertborderwidth``
     - 3-D border width drawn around the insert cursor.
   * - ``insertontime`` / ``insertofftime``
     - Milliseconds the cursor is shown / hidden per blink (``insertofftime=0``
       disables blinking).
   * - ``insertunfocussed``
     - How the cursor is drawn when the widget lacks focus: ``"none"``,
       ``"hollow"``, or ``"solid"``.
   * - ``blockcursor``
     - ``True`` draws the insert cursor as a block over the next character
       rather than a thin bar.

.. rubric:: Size and border

.. list-table::
   :widths: 26 74

   * - ``width`` / ``height``
     - The requested size in **characters** and **lines** (not pixels).
   * - ``padx`` / ``pady``
     - Internal padding between the text and the widget border, in pixels.
   * - ``relief``
     - Border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, ``"solid"``.
   * - ``borderwidth`` (``bd``)
     - Width of the 3-D border, in pixels.
   * - ``selectborderwidth``
     - Border width drawn around selected text.
   * - ``highlightthickness``
     - Width of the focus highlight drawn around the widget.
   * - ``highlightcolor`` / ``highlightbackground``
     - Focus-highlight color when the widget has / doesn't have focus.

.. rubric:: Undo

.. list-table::
   :widths: 26 74

   * - ``undo``
     - ``True`` enables the built-in undo/redo stack.
   * - ``autoseparators``
     - ``True`` auto-inserts undo boundaries as the user types.
   * - ``maxundo``
     - Maximum number of undo steps to keep (``-1`` for unlimited).

.. rubric:: Behavior

.. list-table::
   :widths: 26 74

   * - ``state``
     - ``"normal"`` (editable) or ``"disabled"`` (read-only; the widget also
       ignores ``insert``/``delete`` while disabled).
   * - ``cursor``
     - Mouse cursor shown over the widget.
   * - ``takefocus``
     - Whether the widget accepts focus during keyboard traversal.
   * - ``exportselection``
     - Whether a selection is exported to the X selection / clipboard.
   * - ``setgrid``
     - ``True`` makes the containing window resize in whole character cells.
   * - ``startline`` / ``endline``
     - Restrict the widget to a range of the underlying store's lines (used by
       peer widgets; ``None`` for the full range).
   * - ``xscrollcommand`` / ``yscrollcommand``
     - Callbacks that connect the widget to a horizontal / vertical scrollbar.

Methods
-------

.. rubric:: Content and editing

.. list-table::
   :widths: 34 66

   * - ``insert(index, text, tags=None)``
     - Insert ``text`` at ``index``, optionally applying one or more tags.
   * - ``delete(index1, index2=None)``
     - Delete from ``index1`` up to (not including) ``index2`` — one character
       if ``index2`` is omitted.
   * - ``replace(index1, index2, text, tags=None)``
     - Delete the range and insert ``text`` in its place.
   * - ``get(index1, index2=None)``
     - Return the text in the range (one character if ``index2`` is omitted).
   * - ``count(index1, index2, *options)``
     - Count units (``"chars"``, ``"lines"``, ``"displaylines"``, …) between two
       indices.
   * - ``dump(index1, index2=None, **what)``
     - Return the content of a range broken into its text, tags, marks, and
       embedded items.

.. rubric:: Positions and display

.. list-table::
   :widths: 34 66

   * - ``index(index)``
     - Resolve any index expression to a concrete ``"line.column"`` string.
   * - ``compare(index1, op, index2)``
     - Compare two indices (``op`` is ``"<"``, ``"<="``, ``"=="``, …); returns a
       bool.
   * - ``see(index)``
     - Scroll so that ``index`` is visible.
   * - ``dlineinfo(index)``
     - Bounding box ``(x, y, width, height, baseline)`` of the display line
       holding ``index`` (``None`` if not visible).
   * - ``bbox(index)``
     - Bounding box of the character at ``index``.
   * - ``scan_mark(x, y)`` / ``scan_dragto(x, y)``
     - Anchor and then fast-drag-scroll the view (used for click-drag panning).

.. rubric:: Tags

.. list-table::
   :widths: 34 66

   * - ``tag_add(tag, index1, index2=None, *more)``
     - Apply ``tag`` to one or more ranges.
   * - ``tag_remove(tag, index1, index2=None, *more)``
     - Remove ``tag`` from a range (the tag still exists).
   * - ``tag_delete(*tags)``
     - Delete tags entirely, removing them everywhere.
   * - ``tag_configure(tag, **options)``
     - Set a tag's appearance (``foreground``, ``background``, ``font``,
       ``underline``, ``justify``, spacing, …). Alias: ``tag_config``.
   * - ``tag_cget(tag, option)``
     - Read one option of a tag.
   * - ``tag_bind(tag, sequence, func, add=None)``
     - Bind an event to every range wearing ``tag`` (this is how text becomes
       clickable).
   * - ``tag_unbind(tag, sequence, funcid=None)``
     - Remove a tag binding.
   * - ``tag_names(index=None)``
     - The tags defined (or the tags covering ``index``).
   * - ``tag_ranges(tag)``
     - The list of index pairs a tag covers.
   * - ``tag_nextrange(tag, index1, index2=None)`` / ``tag_prevrange(...)``
     - The next / previous range of ``tag`` from a starting index.
   * - ``tag_raise(tag, above=None)`` / ``tag_lower(tag, below=None)``
     - Reorder tags in the priority stack (later-priority tags win on
       conflicting options).

.. rubric:: Marks

.. list-table::
   :widths: 34 66

   * - ``mark_set(name, index)``
     - Create or move a mark (a floating named position) to ``index``.
   * - ``mark_unset(*names)``
     - Delete marks.
   * - ``mark_gravity(name, direction=None)``
     - Get or set which side (``"left"``/``"right"``) a mark sticks to when text
       is inserted at it.
   * - ``mark_names()``
     - All mark names (including the built-in ``"insert"`` and ``"current"``).
   * - ``mark_next(index)`` / ``mark_previous(index)``
     - The next / previous mark from an index.

.. rubric:: Search

.. list-table::
   :widths: 34 66

   * - ``search(pattern, index, stopindex=None, ...)``
     - Return the index of the next match of ``pattern`` (a string or, with
       ``regexp=True``, a regular expression). Options: ``backwards``,
       ``forwards``, ``nocase``, ``count`` (an ``IntVar`` that receives the match
       length), ``elide``. Returns ``""`` if nothing matches.

.. rubric:: Undo stack

.. list-table::
   :widths: 34 66

   * - ``edit_undo()`` / ``edit_redo()``
     - Undo / redo one step (raises if there's nothing to do). Requires
       ``undo=True``.
   * - ``edit_separator()``
     - Insert an undo boundary manually.
   * - ``edit_reset()``
     - Clear the undo and redo stacks.
   * - ``edit_modified(value=None)``
     - Get, or set, the "modified since last saved" flag.
   * - ``edit(*args)``
     - The generic edit subcommand the helpers above wrap.

.. rubric:: Embedded images

.. list-table::
   :widths: 34 66

   * - ``image_create(index, **options)``
     - Embed an image at ``index`` (``image=``, ``align=``, ``padx=``, ``pady=``).
   * - ``image_cget(index, option)`` / ``image_configure(index, **options)``
     - Read / change an embedded image's options.
   * - ``image_names()``
     - The names of all embedded images.

.. rubric:: Embedded windows

.. list-table::
   :widths: 34 66

   * - ``window_create(index, **options)``
     - Embed a child widget at ``index`` (``window=`` an existing widget, or
       ``create=`` a factory).
   * - ``window_cget(index, option)`` / ``window_configure(index, **options)``
     - Read / change an embedded window's options.
   * - ``window_names()``
     - The child widgets currently embedded.

.. rubric:: Scrolling (view)

.. list-table::
   :widths: 34 66

   * - ``yview(*args)`` / ``xview(*args)``
     - Query or set the vertical / horizontal view. Usually connected to a
       scrollbar via ``yscrollcommand`` rather than called directly.
   * - ``yview_moveto(fraction)`` / ``xview_moveto(fraction)``
     - Scroll so a fraction (0.0–1.0) of the content is off the top / left.
   * - ``yview_scroll(number, what)`` / ``xview_scroll(number, what)``
     - Scroll by ``number`` of ``"units"`` or ``"pages"``.
   * - ``yview_pickplace(index)``
     - Scroll the view to make ``index`` visible (older spelling of ``see``).

.. rubric:: Peer widgets

.. list-table::
   :widths: 34 66

   * - ``peer_create(newname, **options)``
     - Create a second text widget sharing this one's content store.
   * - ``peer_names()``
     - The peers sharing this widget's store.

Shared capabilities
-------------------

.. include:: ../../shared/common-widget-methods.rst

See also
--------

- :doc:`Text widget guide </widgets/text>` — the usage walkthrough.
- `Tk text manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/text.htm>`__ —
  the canonical upstream reference (Tcl 8.6).
