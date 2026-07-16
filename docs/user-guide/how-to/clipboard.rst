Copy and paste text
===================

Copy text to the system clipboard, read it back, and work with the current
selection — all through methods every widget already has (they live on
``Misc``, the common base), so you can call them on ``app`` or any widget.

Copy and paste text
-------------------

Three methods cover the clipboard. Clear it, append your text, then it is
available to other applications:

.. code-block:: python

   app.clipboard_clear()
   app.clipboard_append("copied text")

Read what is on the clipboard with ``clipboard_get``:

.. code-block:: python

   text = app.clipboard_get()

.. note::

   ``clipboard_append`` **adds** to the clipboard; it does not replace. Call
   ``clipboard_clear()`` first (as above) so you don't concatenate onto whatever
   was there. ``clipboard_get`` raises ``TclError`` when the clipboard is empty or
   holds non-text data — guard it if that's possible:

   .. code-block:: python

      from tkinter import TclError

      try:
          text = app.clipboard_get()
      except TclError:
          text = ""

.. note::

   On Linux the clipboard belongs to the app that set it, so what you copy is
   typically gone once your app exits — unless the user runs a clipboard manager
   that holds onto it. Windows and macOS hand the text to the system, where it
   outlives the process. Nothing to code around; just don't rely on a copy
   surviving your own shutdown on Linux.

A copy action, wired to a button, is just those two calls:

.. code-block:: python

   def copy_result():
       app.clipboard_clear()
       app.clipboard_append(result_var.get())

   ttk.Button(app, text="Copy", command=copy_result, bootstyle="secondary").pack()

To put it on a keyboard shortcut too, pick the key for the platform — macOS
copies with **Command-c**, Windows and Linux with **Control-c**:

.. code-block:: python

   copy_key = "<Command-c>" if ttk.windowing_system(app) == "aqua" else "<Control-c>"
   app.bind(copy_key, lambda e: copy_result())

.. warning::

   Bind the shortcut on a specific widget or frame, not with ``bind_all``. The
   copy key is already the native copy gesture inside every Entry and Text —
   ``bind_all`` fires on top of that handling, so a user who selects text in a
   field and copies it gets your value on the clipboard instead of their
   selection.

The current selection
---------------------

Entry, Text, and Listbox widgets track a **selection** — the highlighted range.
Read the selected text with ``selection_get``:

.. code-block:: python

   entry.select_range(0, "end")          # select all (Entry)
   selected = entry.selection_get()      # the highlighted text

By default ``selection_get`` reads the **PRIMARY** selection (the X11
"highlight" selection). Pass ``selection="CLIPBOARD"`` to read the clipboard
through the same call instead:

.. code-block:: python

   entry.selection_get(selection="CLIPBOARD")   # same as clipboard_get()

.. note::

   Reading your own app's selection with ``selection_get`` works on every
   platform. What differs is **sharing** it with other applications: on Linux
   (X11), PRIMARY is a system-wide channel — highlighting text makes it pastable
   with the middle mouse button. On Windows and macOS, Tk provides PRIMARY only
   within your own application. For copy and paste that crosses application
   boundaries, use the **clipboard** methods above everywhere.

.. seealso::

   - :doc:`Events guide </user-guide/feature-guides/events>` — binding the
     copy/paste shortcuts.
   - :doc:`Menus guide </user-guide/feature-guides/menus>` — putting Copy and
     Paste on a menu with the right accelerator per platform.

Reference
---------

- :doc:`Clipboard </reference/capabilities/clipboard>` — ``clipboard_clear``,
  ``clipboard_append``, and ``clipboard_get``.
- :doc:`Selection </reference/capabilities/selection>` — ``selection_get`` and
  the ``selection=`` argument.
- :doc:`Built-in virtual events </reference/events/virtual-events>` — the
  ``<<Copy>>`` / ``<<Cut>>`` / ``<<Paste>>`` events Entry and Text already handle.
