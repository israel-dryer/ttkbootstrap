Open a second window
====================

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

   import ttkbootstrap as ttk

   app = ttk.App(title="Main", size=(320, 200))

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
       entry = ttk.Entry(dialog, textvariable=name)
       entry.pack(padx=10, pady=10, fill="x")

       result = {}
       def submit():
           result["name"] = name.get()
           dialog.destroy()
       ttk.Button(dialog, text="OK", command=submit,
                  bootstyle="primary").pack(pady=(0, 10))

       dialog.place_window_center()
       entry.focus_set()              # put the cursor in the field
       dialog.grab_set()
       parent.wait_window(dialog)     # blocks until the dialog is destroyed
       return result.get("name")      # None if closed without OK

   who = ask_name(app)

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The modal "Your name" dialog centered on screen, with the entry and OK button.

.. tip::

   For text prompts, yes/no questions, and file or color pickers, use the shipped
   dialogs (``Querybox``, ``Messagebox``) instead of building your own — they are
   already modal and return a value.

Intercept the close button
--------------------------

Run your own code when the user clicks **✕** — confirm, save, then close (or
don't). Hand the callback to ``on_close``:

.. code-block:: python

   from ttkbootstrap.dialogs import Messagebox

   def confirm_close():
       if Messagebox.yesno("Discard changes?", parent=win) != "Yes":
           return False               # cancel the close; the window stays

   win.on_close(confirm_close)

Return ``False`` to cancel the close. Return nothing and the window is destroyed
for you. You can pass the same callable at construction instead —
``ttk.Toplevel(on_close=confirm_close)``.

.. note::

   ``yesno`` returns the button's *displayed* text, which is translated when
   localization is active — so a bare ``== "Yes"`` misses under a non-English
   locale. See the :doc:`Dialogs guide </user-guide/feature-guides/dialogs>`.

Reuse a window instead of rebuilding it
---------------------------------------

To keep an expensive window around and show it again later, hide it rather than
destroying it — and intercept ✕ so the user's close hides it too:

.. code-block:: python

   def hide():
       win.withdraw()
       return False               # keep the window alive for next time

   win.on_close(hide)             # ✕ now hides instead of destroying
   win.deiconify()                # show it again later

That ``on_close`` is what makes the recipe work. Without it, ✕ destroys the
window for good and the next ``deiconify()`` raises ``TclError: bad window path
name``.

.. seealso::

   - :doc:`Focus, modality & lifecycle </user-guide/feature-guides/windows>` — the
     concepts.
   - :doc:`Structuring an app </user-guide/getting-started/app-structures>` — the
     single-root rule.
   - :doc:`Show a splash screen <splash-screen>` — a borderless window shown
     while the app starts up.

Reference
---------

- :doc:`Toplevel </reference/windows/toplevel>` — every constructor option and
  window method, including ``on_close`` and ``place_window_center``.
