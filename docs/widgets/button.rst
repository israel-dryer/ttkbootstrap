Button
======

A clickable action trigger. ``Button`` is the native ``ttk.Button``, styled with
``bootstyle=``.

.. Screenshots (light/dark pairs) are added in a later documentation slice. The
   directives below are the intended pattern:

   .. image:: /_static/examples/button-hero-light.png
      :class: tb-screenshot-light
      :alt: Button — light theme

   .. image:: /_static/examples/button-hero-dark.png
      :class: tb-screenshot-dark
      :alt: Button — dark theme

Semantic styling
----------------

Set intent with ``bootstyle=``. The button renders correctly across every theme
without hard-coding a color.

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   ttk.Button(app, text="Primary",   bootstyle="primary").pack(padx=8, pady=4)
   ttk.Button(app, text="Secondary", bootstyle="secondary").pack(padx=8, pady=4)
   ttk.Button(app, text="Success",   bootstyle="success").pack(padx=8, pady=4)
   ttk.Button(app, text="Info",      bootstyle="info").pack(padx=8, pady=4)
   ttk.Button(app, text="Warning",   bootstyle="warning").pack(padx=8, pady=4)
   ttk.Button(app, text="Danger",    bootstyle="danger").pack(padx=8, pady=4)

   app.mainloop()

Variants
--------

Combine a color with a modifier to change visual weight — ``outline``, ``link``,
or ``ghost``:

.. code-block:: python

   ttk.Button(app, text="Solid",   bootstyle="primary")
   ttk.Button(app, text="Outline", bootstyle="primary-outline")
   ttk.Button(app, text="Link",    bootstyle="primary-link")
   ttk.Button(app, text="Ghost",   bootstyle="primary-ghost")

Colors
------

The nine semantic colors — ``primary``, ``secondary``, ``success``, ``info``,
``warning``, ``danger``, ``light``, ``dark``, and ``neutral`` — combine with any
variant. A bare ``Button`` with no ``bootstyle`` uses the ``neutral`` default.

States
------

Disable a button through the standard ttk state; the theme mutes it
automatically:

.. code-block:: python

   btn = ttk.Button(app, text="Disabled", bootstyle="primary")
   btn.state(["disabled"])

API & reference
---------------

``Button`` is the native ``ttk.Button`` — ttkbootstrap adds no Python API of its
own. For its constructor and options, see the
`tkinter.ttk.Button <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Button>`__
reference. For the full hand-styling surface (the ``bootstyle`` → ttk style-name
mapping, element layout, configurable options, and supported states) see the
:doc:`Style Reference </reference/style-reference/index>`.
