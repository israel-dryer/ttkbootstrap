Multiple windows & modal dialogs
================================

Task recipes for working with more than one window. For the mechanics behind
them — focus, modality, stacking, and lifecycle — see
:doc:`Focus, modality & lifecycle </user-guide/feature-guides/windows>` in the
Windows guide.

.. note::

   Every extra window is a ``Toplevel``; keep a single ``App``/``Window`` per
   program (see :doc:`Structuring an app
   </user-guide/getting-started/app-structures>`). ``Toplevel``'s first
   positional argument is the **title** — pass the parent as ``master=``.

Open a second window
--------------------

.. code-block:: python

   win = ttk.Toplevel(master=app, title="Details")
   ttk.Label(win, text="A second window").pack(padx=20, pady=20)

It inherits the app's theme and icon automatically.

Show a modal dialog that returns a value
----------------------------------------

Make the window transient, grab input, and wait for it to close; read the result
the dialog left behind:

.. code-block:: python

   def ask_name(parent):
       dialog = ttk.Toplevel(master=parent, title="Your name", transient=parent)

       name = ttk.StringVar()
       ttk.Entry(dialog, textvariable=name).pack(padx=10, pady=10, fill="x")

       result = {}
       def submit():
           result["name"] = name.get()
           dialog.destroy()
       ttk.Button(dialog, text="OK", command=submit,
                  bootstyle="primary").pack(pady=(0, 10))

       dialog.grab_set()
       parent.wait_window(dialog)     # blocks until the dialog is destroyed
       return result.get("name")      # None if closed without OK

   who = ask_name(app)

.. tip::

   For text prompts, yes/no questions, and file or color pickers, use the shipped
   dialogs (``Querybox``, ``Messagebox``) instead of building your own — they are
   already modal and return a value.

Intercept the close button
--------------------------

Run your own code when the user clicks **✕** — confirm, save, then close (or
don't):

.. code-block:: python

   from ttkbootstrap.dialogs import Messagebox

   def on_close():
       if Messagebox.yesno("Discard changes?", parent=win) == "Yes":
           win.destroy()

   win.protocol("WM_DELETE_WINDOW", on_close)

The window closes only if your handler calls ``destroy()``.

Reuse a window instead of rebuilding it
---------------------------------------

Hide an expensive window and bring it back rather than recreating it:

.. code-block:: python

   win.withdraw()        # hide
   win.deiconify()       # show again

.. seealso::

   :doc:`Focus, modality & lifecycle </user-guide/feature-guides/windows>` for
   the concepts, and :doc:`Structuring an app
   </user-guide/getting-started/app-structures>` for the single-root rule.
