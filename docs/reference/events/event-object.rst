The event object
================

A callback bound with ``bind`` receives one argument: an ``event`` object whose
attributes describe what happened. tkinter fills these from the underlying Tk
event; **an attribute that does not apply to the event type holds the string
``"??"``** (or a meaningless value), so read only the ones relevant to the event
you bound.

.. list-table::
   :header-rows: 1
   :widths: 20 12 44 24

   * - Attribute
     - Tk field
     - Meaning
     - Populated for
   * - ``widget``
     - ``%W``
     - The widget instance the event fired on.
     - all events
   * - ``x``, ``y``
     - ``%x`` ``%y``
     - Pointer position relative to the widget's top-left.
     - pointer & key events
   * - ``x_root``, ``y_root``
     - ``%X`` ``%Y``
     - Pointer position relative to the whole screen.
     - pointer & key events
   * - ``num``
     - ``%b``
     - Button number (1–5).
     - Button events
   * - ``delta``
     - ``%D``
     - Wheel rotation amount and direction.
     - MouseWheel
   * - ``char``
     - ``%A``
     - The character produced (``""`` for non-printing keys).
     - key events
   * - ``keysym``
     - ``%K``
     - The :doc:`key symbol <modifiers-and-keys>` name (``"Left"``, ``"a"``).
     - key events
   * - ``keysym_num``
     - ``%N``
     - The key symbol as a number.
     - key events
   * - ``keycode``
     - ``%k``
     - The hardware key code.
     - key events
   * - ``state``
     - ``%s``
     - Modifier/button state as a bitmask integer (see below).
     - pointer, key & other events
   * - ``time``
     - ``%t``
     - Server timestamp in milliseconds.
     - most events
   * - ``width``, ``height``
     - ``%w`` ``%h``
     - New size of the widget.
     - Configure, Expose
   * - ``type``
     - ``%T``
     - The event type as an ``EventType`` enum (see below).
     - all events
   * - ``focus``
     - ``%f``
     - Whether the pointer's window has focus.
     - Enter, Leave
   * - ``send_event``
     - ``%E``
     - ``True`` if the event was synthesized.
     - all events
   * - ``serial``
     - ``%#``
     - The event's serial number.
     - all events

``event.type``
--------------

``event.type`` is an ``EventType`` enum member, not a bare string. Read its name
or compare against the enum:

.. code-block:: python

   import tkinter as tk

   def handler(event):
       print(event.type.name)              # -> "ButtonPress"
       if event.type == tk.EventType.KeyPress:
           ...

``event.state``
---------------

``state`` is a bitmask of the modifiers and buttons held when the event fired
(``Shift`` = ``0x0001``, ``Lock`` = ``0x0002``, ``Control`` = ``0x0004``,
``Button1`` = ``0x0100``, …). Decoding it by hand is rarely worth it — prefer
naming the modifier in the pattern (``<Shift-Button-1>``) so tkinter matches it
for you.

Fields tkinter does not expose
------------------------------

Tk defines several event fields that tkinter's ``event`` object omits — notably
the *detail / user-data* field (``%d``) of a virtual event. This means a value
passed to ``event_generate(..., data="…")`` is **not** readable on the Python
event; to pass information alongside a
:doc:`virtual event <virtual-events>`, keep it somewhere both sides can see (an
attribute, a variable) rather than on the event. The X11-internal fields (``%a``,
``%c``, ``%m``, ``%o``, ``%p``, ``%B``, ``%P``, ``%R``, ``%S``, ``%i``) are
likewise not exposed.
