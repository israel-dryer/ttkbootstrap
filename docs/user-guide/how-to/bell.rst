Ring the system bell
====================

A beep is the cheapest way to get a user's attention — a flag for an invalid
action, or a nudge that a long job has finished.

Beep with ``bell``
------------------

``bell()`` rings the system alert sound. Every widget has it, so call it on
``app`` or on whatever widget is at hand:

.. code-block:: python

   app.bell()

It plays the platform's default alert; there is no volume or tone control.

Beep on a rejected action
-------------------------

The usual job: the user did something the app can't accept, and you want to say
so without a dialog. Beep, and put the reason on screen:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Bell", size=(320, 140))

   amount = ttk.Entry(app)
   amount.pack(padx=20, pady=(20, 4), fill="x")
   message = ttk.Label(app, text="", bootstyle="danger")
   message.pack()

   def submit():
       if not amount.get().isdigit():
           app.bell()
           message.configure(text="Enter a number")
           return
       message.configure(text="")
       save(amount.get())

   ttk.Button(app, text="Save", command=submit, bootstyle="primary").pack(pady=10)

   app.mainloop()

The beep is the alert; the label is the explanation. A beep on its own tells the
user something was wrong but not what — so pair it with something visible.

.. note::

   Use it sparingly. A beep on every keystroke gets old fast, and a user who has
   silenced their system alert sound hears nothing at all — so never let a beep
   be the *only* way you report something.

Let a dialog beep for you
-------------------------

The shipped dialogs and toasts can ring the bell themselves. ``Messagebox``
error dialogs already do; ``ToastNotification`` takes ``alert=True``:

.. code-block:: python

   ttk.ToastNotification(
       title="Export finished",
       message="Your report is ready.",
       alert=True,
   ).show_toast()

.. seealso::

   - :doc:`Mark a window busy <busy>` — the other half of telling the user what
     is going on.
   - :doc:`Dialogs guide </user-guide/feature-guides/dialogs>` — ``Messagebox``
     and ``Querybox``, which beep on error for you.
   - :doc:`Validation guide </user-guide/feature-guides/validation>` — rejecting
     bad input before it reaches your handler.

Reference
---------

- :doc:`Toast </widgets/toast>` — ``ToastNotification`` and its ``alert`` option.