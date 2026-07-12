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

A copy action, wired to a button or a shortcut, is just those two calls:

.. code-block:: python

   def copy_result():
       app.clipboard_clear()
       app.clipboard_append(result_var.get())

   ttk.Button(app, text="Copy", command=copy_result, bootstyle="secondary").pack()
   app.bind_all("<Control-c>", lambda e: copy_result())

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

   The **PRIMARY** selection is an X11 (Linux) convention — highlighting text
   makes it available to paste with the middle mouse button. On Windows and macOS
   there is no persistent PRIMARY selection, so for portable copy/paste use the
   **clipboard** methods above; keep PRIMARY for Linux-specific niceties.

.. seealso::

   The :doc:`Events guide </user-guide/feature-guides/events>` for binding the
   copy/paste shortcuts, and the ``<<Copy>>`` / ``<<Paste>>`` / ``<<Cut>>``
   virtual events that Entry and Text already handle for you.
