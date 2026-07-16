How styling is delivered
========================

ttkbootstrap delivers its styling API through **concrete widget subclasses**.
``ttk.Button``, ``ttk.Entry``, ``ttk.Combobox``, … are real classes that carry
the ``bootstyle`` keyword (via :class:`~ttkbootstrap.BootMixin`), so you build
widgets from ``ttkbootstrap`` and style them inline. Importing the library
changes nothing about tkinter — the widgets keep real signatures and docstrings
your editor can see.

The one rule to internalize: to get ``bootstyle``, use ttkbootstrap's widget
classes rather than ``tkinter.ttk``'s.

.. admonition:: Coming from 1.x
   :class: note

   1.x monkey-patched tkinter at import so *every* ttk widget grew ``bootstyle``,
   even ones built through plain ``tkinter.ttk``. 2.0 patches nothing at import.
   To opt back into that global behavior, see `The global API (opt-in)`_.

Use ttkbootstrap's widgets
--------------------------

Import ``ttkbootstrap as ttk`` and build widgets from it:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   ttk.Button(app, text="Save", bootstyle="success").pack()
   ttk.Entry(app, bootstyle="primary").pack()

   app.mainloop()

That is the whole delivery model for everyday use — the sections below are for the
edges: legacy ``tk`` widgets, widgets ttkbootstrap doesn't ship, and opting back
into the old global behavior.

Fluent geometry
---------------

``pack``, ``grid``, and ``place`` (and their ``*_configure`` spellings) return the
widget, so you can construct and place in one expression:

.. code-block:: python

   save = ttk.Button(app, text="Save", bootstyle="success").pack(side="left")

``save`` is the button, not ``None`` as it would be with stock tkinter.

Blessed tk widgets
------------------

A few widgets have no ttk equivalent — the toplevels and the classic ``tk``
controls. ttkbootstrap ships themed versions that pick up the theme's colors
automatically (via :class:`~ttkbootstrap.AutoStyleMixin`): ``ttk.Tk``,
``ttk.Toplevel``, ``ttk.Menu``, ``ttk.Text``, ``ttk.Canvas``, ``ttk.Listbox``,
``ttk.TkFrame``, and ``ttk.TkLabel``. Use them in place of the ``tkinter``
originals and they theme themselves:

.. code-block:: python

   ttk.Text(app, height=4).pack()   # background/foreground follow the theme

Widgets you didn't subclass
---------------------------

For a third-party ttk widget, or a plain ``tkinter.ttk`` one you already created,
there are two escape hatches:

- **A reusable class** — ``bootify(cls)`` returns a ``bootstyle``-enabled subclass
  of any ttk widget class:

  .. code-block:: python

     from third_party import FancyWidget

     FancyBoot = ttk.bootify(FancyWidget)
     FancyBoot(app, bootstyle="info").pack()

- **One instance** — ``apply_bootstyle(widget, style)`` styles a single
  already-created vanilla widget and returns the resolved style name:

  .. code-block:: python

     import tkinter.ttk as tkttk

     legacy = tkttk.Button(app, text="Legacy")
     ttk.apply_bootstyle(legacy, "primary")

The global API (opt-in)
-----------------------

``enable_global_api()`` makes *vanilla* ``tkinter`` and ``tkinter.ttk`` widgets
accept ``bootstyle`` and gain fluent geometry, without subclassing. Call it once,
before creating widgets:

.. code-block:: python

   import tkinter.ttk as tkttk
   import ttkbootstrap as ttk

   ttk.enable_global_api()

   app = ttk.App()
   tkttk.Button(app, text="Vanilla", bootstyle="success").pack()

This is opt-in and global — the escape hatch for gradual migration, not the
recommended default. New code should prefer ttkbootstrap's own widget classes.
