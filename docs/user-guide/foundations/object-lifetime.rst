Object lifetime
===============

:doc:`What tkinter wraps <what-tkinter-wraps>` showed the seam between Python and
Tcl. That seam has a consequence for *lifetime*: a few of the things you create
in Python are owned by Python but referenced by Tk only **by name**. Let the
Python object be garbage-collected and Tk loses the thing behind the name — the
widget that pointed at it goes empty, blank, or back to a default, with no error.

This is the cause of the two most common "it just stopped working" bugs in
tkinter: the label that shows nothing, and the image that never appears.

Python owns, Tcl references by name
-----------------------------------

Three kinds of object work this way — a **variable**, an **image**, and a named
**font**. Each creates something inside the interpreter and hands the widget only
its *name*; the Python object owns that Tcl entity, so collecting it deletes the
entity too. The object has to live for as long as any widget needs it.

**Widgets are the exception**, and it's worth saying why up front: a widget is
kept alive by the widget tree — its parent holds it — so you never need to keep a
reference to a widget. That asymmetry is what makes the bug confusing: the entry
you built survives, but the ``StringVar`` you bound to it does not.

A variable that empties
-----------------------

A ``StringVar`` doesn't hold your text in Python; it names a Tcl variable and the
widget links to that name. So the moment the Python object is collected, the link
dangles:

.. code-block:: python

   def build_form(parent):
       name = ttk.StringVar(value="Ada")     # the only reference is this local
       ttk.Entry(parent, textvariable=name).pack()
       # build_form returns -> `name` goes out of scope and is collected.
       # The entry is still on screen, but bound to a variable that is gone,
       # so it shows empty.

The entry survives (the tree owns it); the variable does not. Keep it somewhere
that outlives the function — most naturally on the instance, where it lives as
long as the widget does:

.. code-block:: python

   class Form(ttk.Frame):
       def __init__(self, master):
           super().__init__(master)
           self.name = ttk.StringVar(value="Ada")   # lives as long as the Form
           ttk.Entry(self, textvariable=self.name).pack()

The :doc:`Variables guide </user-guide/feature-guides/variables>` covers the
one-owning-reference rule in full, including why a second same-named variable is
not a safe alias.

An image that vanishes
----------------------

It's the same mechanism, and the single most common tkinter image bug. A widget's
``image=`` option stores the image by name; it does not hold the Python object.
If the only reference is a local, the image is collected the moment the function
returns and the widget goes blank. The convention is to pin it to the widget it
feeds:

.. code-block:: python

   def add_logo(parent):
       photo = ttk.PhotoImage(file="logo.png")
       label = ttk.Label(parent, image=photo)
       label.image = photo          # keeps the image alive with the label
       label.pack()

The :doc:`Work with images </user-guide/how-to/working-with-images>` how-to has
the full treatment, Pillow included.

A font that reverts
-------------------

A named :class:`~ttkbootstrap.Font` **object** is the third case: it creates a
named font in the interpreter, and if it's collected, the named font is deleted
and the widget falls back to its default.

.. code-block:: python

   heading = ttk.Font(family="Helvetica", size=18)
   title = ttk.Label(app, text="Report", font=heading)
   # if `heading` is collected, the named font is deleted and the label
   # reverts -- keep the object (e.g. on self).

This only bites named font *objects*. A font passed as a tuple or string —
``font=("Helvetica", 18)`` — is plain data, copied into the option, with no
lifetime to manage. See the
:doc:`Typography guide </user-guide/feature-guides/typography>`.

Where to keep the reference
---------------------------

The fix is always the same shape: hold one reference for as long as the widget
needs it. Good homes for it:

- **On the instance** (``self.name = ...``). In a class this is automatic — the
  attribute lives as long as the instance — which is why the bug rarely appears in
  class-based apps and often appears in a plain function that builds UI and returns
  a container.
- **On the widget it feeds** (``label.image = photo``) — the conventional home for
  images.
- **Returned from the builder**, so the caller holds it:

  .. code-block:: python

     def build_form(parent):
         name = ttk.StringVar(value="Ada")
         ttk.Entry(parent, textvariable=name).pack()
         return name          # the caller keeps it alive

- **Module- or app-level**, for something that lives for the whole program.

A list counts as a reference too: build images in a loop into a local list,
discard the list, and every one of them is collected. Keep the list.

The opposite problem: outliving their welcome
----------------------------------------------

The same name-and-object seam runs the other way. A callback you register —
a ``command=``, a ``trace_add``, an ``after`` job — keeps a reference to the
callable, and a bound method keeps its whole object alive for as long as the
registration lives. That's a leak rather than a blank: the object you expected to
be gone is still there.

The sharp edge is a pending ``after`` job. It holds its callback and will fire on
schedule — even if the widget it touches was destroyed in between, which lands you
in a ``TclError`` about an invalid command. Cancel scheduled jobs when you tear a
widget down:

.. code-block:: python

   self._job = self.after(500, self._tick)
   # ...
   def destroy(self):
       if self._job is not None:
           self.after_cancel(self._job)
       super().destroy()

.. note::

   This is about objects **you** create. ttkbootstrap manages the lifetime of the
   images it generates for its own styles internally, so themed widgets never hit
   the image bug on their own — it's the images, variables, and fonts in your code
   that need a reference.

.. seealso::

   - :doc:`What tkinter wraps </user-guide/foundations/what-tkinter-wraps>` — the
     Python/Tcl seam this lifetime rule follows from.
   - :doc:`Variables guide </user-guide/feature-guides/variables>` — the
     one-owning-reference rule for ``StringVar`` and friends.
   - :doc:`Work with images </user-guide/how-to/working-with-images>` — keeping an
     image alive, with Pillow.