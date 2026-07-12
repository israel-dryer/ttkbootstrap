Tooltip
=======

A **tooltip** is a small help popup that appears when the pointer hovers over a
widget. ``ToolTip`` is a ttkbootstrap widget (a real class with its own API,
imported as ``ttk.ToolTip``). This page covers attaching one, the hover delay and
wrapping, then the ``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A button with a tooltip popup showing beneath the pointer, in light and dark
   themes.

Usage
-----

You don't ``pack`` a tooltip — you **attach** it to an existing widget by passing
that widget and the ``text`` to show. It manages the hover itself:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import ToolTip

   app = ttk.App()

   save = ttk.Button(app, text="Save", bootstyle="primary")
   save.pack(padx=20, pady=20)

   ToolTip(save, text="Save the current file (Ctrl+S)")

   app.mainloop()

There is nothing to keep a reference to — the ``ToolTip`` wires itself to the
widget's enter/leave events.

Delay and wrapping
------------------

``delay`` is how long (in milliseconds) the pointer must rest before the tip shows
(default 500); ``wraplength`` (in pixels) wraps a long tip onto multiple lines:

.. code-block:: python

   ToolTip(save, text="A longer explanation that should wrap onto a few lines.",
           delay=250, wraplength=200)

Color
-----

``bootstyle`` colors the tooltip from the semantic palette — use it to match the
tip to the kind of control (``danger`` for a destructive action, say):

.. code-block:: python

   ToolTip(delete_button, text="This cannot be undone", bootstyle="danger")

API & reference
---------------

For the complete option list, see :class:`~ttkbootstrap.ToolTip` on the
:doc:`Widgets API page </reference/api/widgets>`:

.. autosummary::
   :nosignatures:

   ~ttkbootstrap.ToolTip

.. seealso::

   :doc:`Toast <toast>` for a temporary notification that appears on its own
   rather than on hover.
