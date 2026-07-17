Text
====

``Text`` is tkinter's multi-line text widget (``tk.Text``), themed by
ttkbootstrap. This page is the complete reference for its **own** options and
methods — the shared capabilities every widget has (configuration, lifecycle,
focus, introspection) are listed at the bottom.

For a task-oriented walkthrough — indices, tags, marks, search, undo — see the
:doc:`Text widget guide </widgets/text>`.

Options
-------

Set at construction or with ``configure(...)``; read with ``cget("name")``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``autostyle``
     - ``bool``
     - **Constructor only.** ``True`` (the default) paints the widget with the
       active theme and repaints it on a theme switch; ``False`` opts out,
       leaving tkinter's default appearance for you to style yourself. This is
       ttkbootstrap's one addition to the widget — everything below is native tk.
   * - ``font``
     - ``str | Font``
     - The default font for the text.
   * - ``wrap``
     - ``str``
     - How lines that exceed the width wrap: ``"char"``, ``"word"``, or
       ``"none"`` (no wrap — scroll horizontally instead).
   * - ``tabs``
     - ``str``
     - Tab stops, as a list of distances (optionally each followed by
       ``"left"``/``"right"``/``"center"``/``"numeric"``).
   * - ``tabstyle``
     - ``str``
     - How tabs interact with the ``tabs`` list: ``"tabular"`` or
       ``"wordprocessor"``.
   * - ``spacing1``
     - ``int``
     - Extra vertical space above the first display line of each text line.
   * - ``spacing2``
     - ``int``
     - Extra vertical space between the display lines of a single wrapped line.
   * - ``spacing3``
     - ``int``
     - Extra vertical space below the last display line of each text line.
   * - ``foreground`` (``fg``)
     - ``str``
     - The text color.
   * - ``background`` (``bg``)
     - ``str``
     - The page (background) color.
   * - ``selectforeground``
     - ``str``
     - The text color within the selection.
   * - ``selectbackground``
     - ``str``
     - The background color of the selection.
   * - ``inactiveselectbackground``
     - ``str``
     - The selection background when the widget doesn't have focus (an empty
       string hides the selection when unfocused).
   * - ``insertbackground``
     - ``str``
     - The color of the blinking insert cursor.
   * - ``insertwidth``
     - ``int``
     - The width of the insert cursor, in pixels.
   * - ``insertborderwidth``
     - ``int``
     - The 3-D border width drawn around the insert cursor.
   * - ``insertontime``
     - ``int``
     - Milliseconds the cursor is shown per blink.
   * - ``insertofftime``
     - ``int``
     - Milliseconds the cursor is hidden per blink (``0`` disables blinking).
   * - ``insertunfocussed``
     - ``str``
     - How the cursor is drawn when the widget lacks focus: ``"none"``,
       ``"hollow"``, or ``"solid"``.
   * - ``blockcursor``
     - ``bool``
     - ``True`` draws the insert cursor as a block over the next character rather
       than a thin bar.
   * - ``width``
     - ``int``
     - The requested width in characters (not pixels).
   * - ``height``
     - ``int``
     - The requested height in lines (not pixels).
   * - ``padx``
     - ``int``
     - Internal horizontal padding between the text and the border, in pixels.
   * - ``pady``
     - ``int``
     - Internal vertical padding between the text and the border, in pixels.
   * - ``relief``
     - ``str``
     - The border style: ``"flat"``, ``"raised"``, ``"sunken"``, ``"groove"``,
       ``"ridge"``, or ``"solid"``.
   * - ``borderwidth`` (``bd``)
     - ``int``
     - The width of the 3-D border, in pixels.
   * - ``selectborderwidth``
     - ``int``
     - The border width drawn around selected text.
   * - ``highlightthickness``
     - ``int``
     - The width of the focus highlight drawn around the widget.
   * - ``highlightcolor``
     - ``str``
     - The focus-highlight color when the widget has focus.
   * - ``highlightbackground``
     - ``str``
     - The focus-highlight color when the widget does not have focus.
   * - ``undo``
     - ``bool``
     - ``True`` enables the built-in undo/redo stack.
   * - ``autoseparators``
     - ``bool``
     - ``True`` auto-inserts undo boundaries as the user types.
   * - ``maxundo``
     - ``int``
     - The maximum number of undo steps to keep (``-1`` for unlimited).
   * - ``state``
     - ``str``
     - ``"normal"`` (editable) or ``"disabled"`` (read-only; the widget also
       ignores ``insert``/``delete`` while disabled).
   * - ``cursor``
     - ``str``
     - The mouse cursor shown over the widget (see
       :doc:`Cursors </reference/cursors>`).
   * - ``takefocus``
     - ``bool``
     - Whether the widget accepts focus during keyboard traversal.
   * - ``exportselection``
     - ``bool``
     - Whether a selection is exported to the X selection / clipboard.
   * - ``setgrid``
     - ``bool``
     - ``True`` makes the containing window resize in whole character cells.
   * - ``startline``
     - ``int``
     - Restrict the widget to start at this line of the underlying store (used by
       peer widgets; ``None`` for the full range).
   * - ``endline``
     - ``int``
     - Restrict the widget to end at this line of the underlying store (used by
       peer widgets; ``None`` for the full range).
   * - ``xscrollcommand``
     - ``callable``
     - A callback connecting the widget to a horizontal scrollbar.
   * - ``yscrollcommand``
     - ``callable``
     - A callback connecting the widget to a vertical scrollbar.

Methods
-------

Content and editing
~~~~~~~~~~~~~~~~~~~~

.. py:method:: insert(index, chars, *args)
   :noindex:

   Insert text at a position. Any trailing ``args`` alternate a tag (or tuple of
   tags) with more text, so text can be tagged as it is inserted.

   :param index: where to insert — any index expression (e.g. ``"insert"``,
      ``"end"``, ``"1.0"``).
   :param str chars: the text to insert.
   :param args: optional alternating *tag* / *text* values applied to the
      inserted runs.
   :returns: ``None``.

.. py:method:: delete(index1, index2=None)
   :noindex:

   Delete a character or a range of text.

   :param index1: start of the range.
   :param index2: end of the range, **exclusive**. If omitted, only the single
      character at ``index1`` is deleted.
   :returns: ``None``.

.. py:method:: replace(index1, index2, chars, *args)
   :noindex:

   Delete the text between two indices and insert ``chars`` in its place — a
   ``delete`` followed by an ``insert`` at ``index1``.

   :param index1: start of the range to replace.
   :param index2: end of the range, exclusive.
   :param str chars: the replacement text.
   :param args: optional alternating *tag* / *text* values, as for ``insert``.
   :returns: ``None``.

.. py:method:: get(index1, index2=None)
   :noindex:

   Return text from the widget.

   :param index1: start of the range.
   :param index2: end of the range, exclusive. If omitted, returns the single
      character at ``index1``.
   :returns: the text in the range.
   :rtype: str

.. py:method:: count(index1, index2, *options, return_ints=False)
   :noindex:

   Count text units between two indices.

   :param index1: start of the range.
   :param index2: end of the range.
   :param options: one or more units to count, each a string —
      ``"chars"``, ``"indices"``, ``"lines"``, ``"displaylines"``,
      ``"xpixels"``, ``"ypixels"``, and so on.
   :param bool return_ints: return a bare ``int`` when a single unit is
      requested, instead of a one-tuple.
   :returns: the counts, in the order the options were given.
   :rtype: tuple[int, ...] | int

.. py:method:: dump(index1, index2=None, command=None, **kinds)
   :noindex:

   Return the contents of a range broken into its pieces — text, tags, marks,
   and embedded images/windows — as ``(key, value, index)`` triples.

   :param index1: start of the range.
   :param index2: end of the range; if omitted, dumps at ``index1``.
   :param command: a callback invoked once per piece instead of returning them.
   :param kinds: booleans selecting which piece types to include —
      ``text``, ``tag``, ``mark``, ``image``, ``window``, or ``all``.
   :returns: a list of ``(key, value, index)`` triples (``None`` if ``command``
      is given).
   :rtype: list[tuple[str, str, str]]

Positions and display
~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: index(index)
   :noindex:

   Resolve any index expression to a concrete position.

   :param index: an index expression (``"insert"``, ``"end-1c"``, ``"1.0"``, …).
   :returns: the position as ``"line.column"``.
   :rtype: str

.. py:method:: compare(index1, op, index2)
   :noindex:

   Compare two positions.

   :param index1: the first index.
   :param str op: a comparison operator — ``"<"``, ``"<="``, ``"=="``, ``"!="``,
      ``">="``, ``">"``.
   :param index2: the second index.
   :returns: the result of the comparison.
   :rtype: bool

.. py:method:: see(index)
   :noindex:

   Scroll the view so that ``index`` is visible.

   :param index: the position to reveal.
   :returns: ``None``.

.. py:method:: dlineinfo(index)
   :noindex:

   Return the bounding box of the display line containing ``index``.

   :param index: a position on the line.
   :returns: ``(x, y, width, height, baseline)`` in pixels, or ``None`` if the
      line is not visible.
   :rtype: tuple | None

.. py:method:: bbox(index)
   :noindex:

   Return the bounding box of the character at ``index``.

   :param index: the character's position.
   :returns: ``(x, y, width, height)`` in pixels, or ``None`` if not visible.
   :rtype: tuple | None

.. py:method:: scan_mark(x, y)
   :noindex:

   Record a starting point for a fast drag-scroll (paired with ``scan_dragto``).

   :param int x: pointer x, in pixels.
   :param int y: pointer y, in pixels.
   :returns: ``None``.

.. py:method:: scan_dragto(x, y)
   :noindex:

   Scroll the view relative to the ``scan_mark`` point, accelerated for
   click-drag panning.

   :param int x: current pointer x, in pixels.
   :param int y: current pointer y, in pixels.
   :returns: ``None``.

Tags
~~~~

.. py:method:: tag_add(tagName, index1, *args)
   :noindex:

   Apply a tag to one or more ranges.

   :param str tagName: the tag to apply.
   :param index1: start of the first range.
   :param args: an end index, then optional further start/end index pairs.
   :returns: ``None``.

.. py:method:: tag_remove(tagName, index1, index2=None)
   :noindex:

   Remove a tag from a range. The tag itself still exists and keeps its config.

   :param str tagName: the tag to remove.
   :param index1: start of the range.
   :param index2: end of the range, exclusive; one character if omitted.
   :returns: ``None``.

.. py:method:: tag_delete(*tagNames)
   :noindex:

   Delete tags entirely, removing them from all text and discarding their config.

   :param tagNames: the tag names to delete.
   :returns: ``None``.

.. py:method:: tag_configure(tagName, **options)
   :noindex:

   Set (or query) a tag's appearance. Alias: ``tag_config``.

   :param str tagName: the tag to configure.
   :param options: appearance options — ``foreground``, ``background``, ``font``,
      ``underline``, ``overstrike``, ``justify``, ``lmargin1``/``lmargin2``,
      ``rmargin``, ``spacing1``/``2``/``3``, ``tabs``, ``elide``.
   :returns: the option spec when queried with a single option name, else
      ``None``.

.. py:method:: tag_cget(tagName, option)
   :noindex:

   Return one option of a tag.

   :param str tagName: the tag.
   :param str option: the option name.
   :returns: the option's value.

.. py:method:: tag_bind(tagName, sequence, func, add=None)
   :noindex:

   Bind an event to every range wearing a tag — the way to make text clickable.

   :param str tagName: the tag.
   :param str sequence: an event sequence, e.g. ``"<Button-1>"``.
   :param func: the callback, receiving the event object.
   :param add: ``"+"`` to add a handler rather than replace.
   :returns: a binding id (for ``tag_unbind``).
   :rtype: str

.. py:method:: tag_unbind(tagName, sequence, funcid=None)
   :noindex:

   Remove a tag binding.

   :param str tagName: the tag.
   :param str sequence: the bound sequence.
   :param funcid: the id returned by ``tag_bind``, to remove one handler.
   :returns: ``None``.

.. py:method:: tag_names(index=None)
   :noindex:

   Return tag names.

   :param index: if given, only the tags covering that position.
   :returns: the tag names, in priority order (lowest first).
   :rtype: tuple[str, ...]

.. py:method:: tag_ranges(tagName)
   :noindex:

   Return the ranges a tag covers.

   :param str tagName: the tag.
   :returns: a flat sequence of alternating start/end indices.
   :rtype: tuple

.. py:method:: tag_nextrange(tagName, index1, index2=None)
   :noindex:

   Find the next range of a tag at or after a position.

   :param str tagName: the tag.
   :param index1: where to start searching.
   :param index2: where to stop; optional.
   :returns: ``(start, end)`` of the next range, or an empty tuple if none.
   :rtype: tuple

.. py:method:: tag_prevrange(tagName, index1, index2=None)
   :noindex:

   Find the previous range of a tag before a position (counterpart of
   :py:meth:`tag_nextrange`).

   :returns: ``(start, end)`` of the previous range, or an empty tuple.
   :rtype: tuple

.. py:method:: tag_raise(tagName, aboveThis=None)
   :noindex:

   Raise a tag's priority. When tags overlap, the higher-priority tag wins on any
   conflicting option.

   :param str tagName: the tag to raise.
   :param aboveThis: raise just above this tag; if omitted, raise to the top.
   :returns: ``None``.

.. py:method:: tag_lower(tagName, belowThis=None)
   :noindex:

   Lower a tag's priority (counterpart of :py:meth:`tag_raise`).

   :param str tagName: the tag to lower.
   :param belowThis: lower just below this tag; if omitted, lower to the bottom.
   :returns: ``None``.

Marks
~~~~~

.. py:method:: mark_set(markName, index)
   :noindex:

   Create a mark, or move an existing one, to a position. A mark is a named
   position that floats with the text as it changes.

   :param str markName: the mark name (``"insert"`` is the cursor).
   :param index: where to place the mark.
   :returns: ``None``.

.. py:method:: mark_unset(*markNames)
   :noindex:

   Delete marks.

   :param markNames: the marks to remove.
   :returns: ``None``.

.. py:method:: mark_gravity(markName, direction=None)
   :noindex:

   Get or set a mark's gravity — which side it sticks to when text is inserted
   exactly at it.

   :param str markName: the mark.
   :param direction: ``"left"`` or ``"right"``; omit to query.
   :returns: the current gravity when queried, else ``None``.
   :rtype: str | None

.. py:method:: mark_names()
   :noindex:

   Return all mark names, including the built-in ``"insert"`` and ``"current"``.

   :rtype: tuple[str, ...]

.. py:method:: mark_next(index)
   :noindex:

   Return the name of the next mark at or after a position.

   :param index: where to start.
   :returns: the mark name, or ``""`` if none.
   :rtype: str

.. py:method:: mark_previous(index)
   :noindex:

   Return the name of the previous mark before a position (counterpart of
   :py:meth:`mark_next`).

   :rtype: str

Search
~~~~~~

.. py:method:: search(pattern, index, stopindex=None, *, forwards=None, \
                      backwards=None, exact=None, regexp=None, nocase=None, \
                      count=None, elide=None)
   :noindex:

   Search the text for ``pattern``.

   :param str pattern: the text to find, or a Tcl regular expression when
      ``regexp=True``.
   :param index: where to start searching.
   :param stopindex: where to stop; wraps around the whole widget if omitted.
   :param bool forwards: search forward (the default).
   :param bool backwards: search backward instead.
   :param bool exact: match ``pattern`` literally (the default unless
      ``regexp``).
   :param bool regexp: treat ``pattern`` as a regular expression.
   :param bool nocase: case-insensitive match.
   :param count: an ``IntVar`` that receives the match length in characters.
   :param bool elide: also search elided (hidden) text.
   :returns: the index of the first match, or ``""`` if none.
   :rtype: str

Undo stack
~~~~~~~~~~

Each ``edit_*`` method wraps the generic ``edit(*args)`` dispatcher.

.. py:method:: edit_undo()
   :noindex:

   Undo the changes back to the last separator. Requires ``undo=True``.

   :returns: ``None``.
   :raises tkinter.TclError: if there is nothing to undo.

.. py:method:: edit_redo()
   :noindex:

   Redo the changes undone by the last :py:meth:`edit_undo`.

   :returns: ``None``.
   :raises tkinter.TclError: if there is nothing to redo.

.. py:method:: edit_separator()
   :noindex:

   Insert a separator (an undo boundary) onto the undo stack.

   :returns: ``None``.

.. py:method:: edit_reset()
   :noindex:

   Clear the undo and redo stacks.

   :returns: ``None``.

.. py:method:: edit_modified(arg=None)
   :noindex:

   Get or set the widget's "modified" flag.

   :param bool arg: the new flag value; omit to query.
   :returns: the current flag when queried, else ``None``.
   :rtype: bool | None

Embedded images
~~~~~~~~~~~~~~~

.. py:method:: image_create(index, **options)
   :noindex:

   Embed an image in the text at a position.

   :param index: where to insert the image.
   :param options: ``image=`` a ``PhotoImage``, ``align=``
      (``"baseline"``/``"top"``/``"center"``/``"bottom"``), ``padx=``, ``pady=``,
      ``name=``.
   :returns: the name of the embedded image.
   :rtype: str

.. py:method:: image_cget(index, option)
   :noindex:

   Return one option of the embedded image at ``index``.

   :rtype: str

.. py:method:: image_configure(index, **options)
   :noindex:

   Set (or query) the options of the embedded image at ``index``.

.. py:method:: image_names()
   :noindex:

   Return the names of all embedded images.

   :rtype: tuple[str, ...]

Embedded windows
~~~~~~~~~~~~~~~~

.. py:method:: window_create(index, **options)
   :noindex:

   Embed a child widget in the text at a position.

   :param index: where to insert the widget.
   :param options: ``window=`` an existing widget, or ``create=`` a factory
      called to build it lazily; plus ``align=``, ``padx=``, ``pady=``,
      ``stretch=``.
   :returns: ``None``.

.. py:method:: window_cget(index, option)
   :noindex:

   Return one option of the embedded window at ``index``.

.. py:method:: window_configure(index, **options)
   :noindex:

   Set (or query) the options of the embedded window at ``index``.

.. py:method:: window_names()
   :noindex:

   Return the embedded child widgets.

   :rtype: tuple

Scrolling (view)
~~~~~~~~~~~~~~~~

.. py:method:: yview(*args)
   :noindex:

   Query or set the vertical view. Usually connected to a scrollbar via the
   ``yscrollcommand`` option rather than called directly.

   :returns: with no args, the visible fraction ``(first, last)``; otherwise
      ``None``.
   :rtype: tuple | None

.. py:method:: yview_moveto(fraction)
   :noindex:

   Scroll vertically so that ``fraction`` of the content is above the top edge.

   :param float fraction: a value from 0.0 to 1.0.
   :returns: ``None``.

.. py:method:: yview_scroll(number, what)
   :noindex:

   Scroll vertically by a number of units or pages.

   :param int number: how far, positive or negative.
   :param str what: ``"units"`` (lines) or ``"pages"``.
   :returns: ``None``.

.. py:method:: xview(*args)
   :noindex:

   Horizontal counterpart of :py:meth:`yview`; ``xview_moveto`` and
   ``xview_scroll`` mirror the vertical versions.

Peer widgets
~~~~~~~~~~~~

.. py:method:: peer_create(newPathName, **options)
   :noindex:

   Create a second text widget that shares this one's underlying content — edits
   to either show in both.

   :param str newPathName: the Tk path name for the new peer.
   :param options: any ``Text`` options for the peer.
   :returns: ``None``.

.. py:method:: peer_names()
   :noindex:

   Return the peers sharing this widget's content store.

   :rtype: tuple

Shared capabilities
-------------------

``Text`` also has the methods every widget inherits — configuration, placement,
event binding, lifecycle, focus, and introspection. These are documented under
:doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Text widget guide </widgets/text>` — the usage walkthrough.
- `Tk text manual page <https://www.tcl-lang.org/man/tcl8.6/TkCmd/text.htm>`__ —
  the canonical upstream reference (Tcl 8.6).
