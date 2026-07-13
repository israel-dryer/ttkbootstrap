Bind
====

**Binding** attaches a callback to an event on a widget. The event pattern names
*which* event fires the callback — its full grammar (types, modifiers, key
symbols, and built-in virtual events) is the :doc:`Events reference
</reference/events/index>`. Every widget carries these methods.

The canonical upstream references are the Tk
`bind <https://www.tcl-lang.org/man/tcl8.6/TkCmd/bind.htm>`__ and
`bindtags <https://www.tcl-lang.org/man/tcl8.6/TkCmd/bindtags.htm>`__ manual
pages (Tcl 8.6).

Binding callbacks
-----------------

.. py:method:: bind(sequence=None, func=None, add=None)
   :noindex:

   Bind ``func`` to the event ``sequence`` on this widget. ``func`` is called
   with one :doc:`event object </reference/events/event-object>` argument. Return
   ``"break"`` from the callback to stop further handling of that event.

   :param sequence: an event pattern such as ``"<Button-1>"`` or ``"<<Custom>>"``.
   :param func: the callback; receives one ``event`` argument.
   :param add: ``"+"`` to add to the existing bindings instead of replacing them.
   :returns: the binding's function id (a string) — pass it to ``unbind`` — when
      ``func`` is given; otherwise the current binding.

.. py:method:: bind_all(sequence=None, func=None, add=None)
   :noindex:

   Like ``bind``, but application-wide — the binding applies to every widget, via
   the ``all`` bind tag.

   :returns: the binding's function id.

.. py:method:: bind_class(className, sequence=None, func=None, add=None)
   :noindex:

   Bind at the widget-*class* level: every widget whose bind tags include
   ``className`` (e.g. ``"TButton"``) responds, current and future.

   :returns: the binding's function id.

.. py:method:: unbind(sequence, funcid=None)
   :noindex:

   Remove the binding for ``sequence`` on this widget. Pass the ``funcid``
   returned by ``bind`` to remove a single added callback rather than all of them.

   :returns: ``None``.

Bind tags
---------

.. py:method:: bindtags(tagList=None)
   :noindex:

   Get or set this widget's **bind tags** — the ordered list of names Tk searches
   for bindings when an event fires (by default: the widget, its class, its
   toplevel, and ``all``). Pass a list or tuple to reorder or replace them — for
   example to insert a custom tag shared by several widgets. Call with no argument
   to read the current tags.

   :param tagList: the new ordered tags, or omit to query.
   :returns: the current tags (a tuple) when queried, otherwise ``None``.

Synthesizing events
-------------------

To *send* an event rather than receive one, use ``event_generate``; custom
``<<virtual>>`` names are managed with ``event_add`` / ``event_delete``. These
belong to the event system — their options live in the :doc:`Events reference
</reference/events/event-generate-options>`.

See also
--------

- :doc:`Events reference </reference/events/index>` — the pattern grammar, the
  event object, and the built-in virtual events.
- :doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>` and the
  :doc:`Events feature guide </user-guide/feature-guides/events>` — how to *use*
  bindings (scope, stopping propagation, dispatching your own virtual events).
