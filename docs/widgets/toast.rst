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
clicked. ``hide_toast()`` dismisses one early.

Where it appears
----------------

``position`` is an ``(x, y, anchor)`` tuple — the ``x``/``y`` offset from the
corner named by ``anchor`` (``"ne"``, ``"se"``, ``"sw"``, ``"nw"``). The default is
the bottom-right:

.. code-block:: python

   ToastNotification(title="Done", message="Export finished.", position=(10, 60, "ne"))

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
:doc:`ToastNotification API reference </reference/api/toastnotification>`.

.. seealso::

   The :doc:`Dialogs guide </user-guide/feature-guides/dialogs>` for a
   ``Messagebox`` when you need the user to acknowledge or answer, rather than a
   toast that fades on its own.
