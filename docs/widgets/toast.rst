Toast
=====

A **toast** is a small notification that pops up, lingers, and fades on its own —
non-blocking feedback like "Saved" or "Copied". ``ToastNotification`` is a
ttkbootstrap widget (a real class with its own API, imported as
``ttk.ToastNotification``). This page covers showing one, how long it stays, where
it appears, then the ``bootstyle`` color and icon.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A success toast in the bottom-right corner reading "Saved — your file was
   saved", in light and dark themes.

Usage
-----

Unlike most widgets you don't ``pack`` a toast — you build it with a ``title`` and
``message`` and call ``show_toast()`` to display it:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import ToastNotification

   app = ttk.App()

   def save():
       toast = ToastNotification(
           title="Saved",
           message="Your file was saved.",
           duration=3000,               # visible for 3 seconds
           bootstyle="success",
       )
       toast.show_toast()

   ttk.Button(app, text="Save", command=save, bootstyle="primary").pack(padx=20, pady=20)

   app.mainloop()

``duration`` is in milliseconds; **omit it** and the toast stays until it is
clicked. ``show_toast()`` returns the toast, so keep the reference to dismiss it
early with ``.hide()`` (in the example above the toast is a local, so hold onto it
if you need to close it yourself).

Where it appears
----------------

``position`` is an ``(x, y, anchor)`` tuple — the ``x``/``y`` offset from the
corner or edge named by ``anchor``, which accepts any of the eight compass points
(``"n"``, ``"e"``, ``"s"``, ``"w"``, ``"nw"``, ``"ne"``, ``"sw"``, ``"se"``). The
default is **platform-specific** — bottom-right (``"se"``) on Windows and Linux,
top-right (``"ne"``) on macOS:

.. code-block:: python

   ToastNotification(title="Done", message="Export finished.", position=(10, 60, "ne"))

Toasts anchored to the same corner **stack** automatically instead of overlapping,
and reflow when one is dismissed.

Color and icon
--------------

``bootstyle`` colors the toast from the semantic palette, and ``icon`` sets the
glyph shown beside the text (a Bootstrap Icons name):

.. code-block:: python

   ToastNotification(title="Heads up", message="Low disk space.",
                     bootstyle="warning", icon="exclamation-triangle")

Set ``alert=True`` to also ring the system bell when the toast appears.

API & reference
---------------

For the complete option list, see the
:doc:`ToastNotification API reference </reference/dialogs/toast>`.

.. seealso::

   The :doc:`Dialogs guide </user-guide/feature-guides/dialogs>` for a
   ``Messagebox`` when you need the user to acknowledge or answer, rather than a
   toast that fades on its own.
