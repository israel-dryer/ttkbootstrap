Events
======

The catalog of tkinter's event system: every event **type**, **modifier**, and
**key symbol** you can name in a pattern, every attribute of the event object a
callback receives, the options for synthesizing events, and the built-in
``<<virtual>>`` event names.

.. note::

   This is standard tkinter — it comes from Tk's ``bind`` and ``event``
   commands, which Tk documents only in C-oriented manual pages. This reference
   restates the names in Python terms. For **how to use** them — binding
   callbacks, stopping propagation, and generating your own events — see
   :doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>` in
   the User Guide.

Pattern grammar
---------------

An event pattern names *which* event fires a callback. Its full form is one or
more **modifiers**, a **type**, and an optional **detail**, inside angle
brackets:

.. code-block:: text

   <Control-Shift-KeyPress-Q>
    │       │     │        └─ detail     which key or button
    │       │     └───────── type        the kind of event
    └───────┴─────────────── modifiers   keys/buttons held down

- The **type** is required unless it can be inferred: a bare detail like
  ``<1>`` means ``<Button-1>`` and ``<q>`` means ``<KeyPress-q>``.
- **Detail** is a button number for button events or a
  :doc:`key symbol <modifiers-and-keys>` for key events; omit it to match any
  button or key.
- A ``<<Name>>`` pattern (double brackets) is a
  :doc:`virtual event <virtual-events>`; modifiers may not be combined
  with one.

.. toctree::
   :hidden:

   event-types
   modifiers-and-keys
   event-object
   event-generate-options
   virtual-events

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Event types
      :link: event-types
      :link-type: doc

      Every event type token — ``KeyPress``, ``Button``, ``Motion``,
      ``Configure``, ``<<virtual>>`` — and when each fires.

   .. grid-item-card:: Modifiers & keys
      :link: modifiers-and-keys
      :link-type: doc

      The modifier tokens (``Control``, ``Shift``, ``Double``, …) and the
      common key symbols used as the detail of a key event.

   .. grid-item-card:: The event object
      :link: event-object
      :link-type: doc

      Every attribute of the ``event`` passed to a callback, the Tk field it
      maps to, and which event types populate it.

   .. grid-item-card:: event_generate options
      :link: event-generate-options
      :link-type: doc

      The keyword options accepted by ``event_generate`` and the ``when``
      scheduling values.

   .. grid-item-card:: Built-in virtual events
      :link: virtual-events
      :link-type: doc

      The predefined ``<<virtual>>`` events Tk, ttk, and ttkbootstrap emit.
