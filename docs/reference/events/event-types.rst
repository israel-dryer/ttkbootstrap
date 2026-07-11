Event types
===========

The **type** is the core of an event pattern — the kind of thing that happened.
Use it in a :doc:`pattern <index>` as ``<Type>`` or ``<Type-detail>``, e.g.
``<KeyPress-Return>`` or ``<Button-1>``.

Commonly used types
-------------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 64

   * - Type
     - Alias
     - Fires when
   * - ``KeyPress``
     - ``Key``
     - A key is pressed. The detail is a :doc:`key symbol <modifiers-and-keys>`
       (``<KeyPress-a>``, ``<Return>``).
   * - ``KeyRelease``
     -
     - A key is released.
   * - ``ButtonPress``
     - ``Button``
     - A mouse button is pressed. The detail is the button number
       (``<Button-1>`` = left, ``2`` = middle, ``3`` = right).
   * - ``ButtonRelease``
     -
     - A mouse button is released.
   * - ``Motion``
     -
     - The pointer moves. Combine with a button modifier for drags:
       ``<B1-Motion>``.
   * - ``MouseWheel``
     -
     - The mouse wheel turns; the rotation is in ``event.delta`` (see the note
       below).
   * - ``Enter``
     -
     - The pointer enters the widget.
   * - ``Leave``
     -
     - The pointer leaves the widget.
   * - ``FocusIn``
     -
     - The widget (or a descendant) gains keyboard focus.
   * - ``FocusOut``
     -
     - The widget (or a descendant) loses keyboard focus.
   * - ``Configure``
     -
     - The widget changes size or position; new size is ``event.width`` /
       ``event.height``.
   * - ``Map``
     -
     - The widget becomes visible (mapped).
   * - ``Unmap``
     -
     - The widget becomes hidden (unmapped).
   * - ``Visibility``
     -
     - The widget's visible/obscured state changes.
   * - ``Expose``
     -
     - All or part of the widget needs redrawing.
   * - ``Destroy``
     -
     - The widget is being destroyed.
   * - ``Activate``
     -
     - The toplevel becomes the active window.
   * - ``Deactivate``
     -
     - The toplevel stops being the active window.
   * - ``Property``
     -
     - An X property on the window changes (X11).
   * - ``Colormap``
     -
     - The window's colormap changes (X11).

.. note::

   **MouseWheel is platform-split.** On Windows and macOS, bind ``<MouseWheel>``
   and read ``event.delta`` (multiples of 120 on Windows, ±1 on macOS). On X11
   (Linux) the wheel arrives as ``<Button-4>`` (up) and ``<Button-5>`` (down)
   instead. Cross-platform code binds all three.

Rarely used types
-----------------

``Circulate``, ``Gravity``, and ``Reparent`` report low-level X11 window changes
and are seldom useful in applications. The ``CirculateRequest``,
``ConfigureRequest``, ``MapRequest``, ``ResizeRequest``, and ``Create`` types are
**only** delivered to an X11 window manager, never to an ordinary application.

Virtual event types
-------------------

A type written in double brackets — ``<<Paste>>``, ``<<ThemeChanged>>`` — is a
:doc:`virtual event <virtual-events>`, a named notification decoupled from any
one physical event.
