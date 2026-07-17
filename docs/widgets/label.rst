Label
=====

A **label** displays a line of read-only text (or an image) — a caption, a field
name, a status line. ``Label`` is the native ``ttk.Label``, styled with
``bootstyle=``. This page covers showing static and dynamic text, coloring it,
wrapping long text, then fonts and images.

.. image:: /_static/examples/label-hero-light.png
   :class: tb-screenshot-light
   :width: 166px
   :alt: A heading label and a colored status label — light theme

.. image:: /_static/examples/label-hero-dark.png
   :class: tb-screenshot-dark
   :width: 166px
   :alt: A heading label and a colored status label — dark theme

Usage
-----

Pass ``text=`` for a fixed string. For text that changes at runtime, bind a
``StringVar`` with ``textvariable=`` and ``set`` it — the label updates itself:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   ttk.Label(app, text="Welcome").pack(padx=10, pady=10)

   status = ttk.StringVar(value="Ready")
   ttk.Label(app, textvariable=status).pack()

   status.set("Loading…")            # the label follows

   app.mainloop()

You can also change a fixed label later with ``label.configure(text="…")``.

Color
-----

``bootstyle`` colors the **text** from the semantic palette — use it to signal
status (``success``, ``danger``, ``secondary`` for muted):

.. code-block:: python

   ttk.Label(app, text="Saved", bootstyle="success")
   ttk.Label(app, text="Failed", bootstyle="danger")

To put a label on a **colored fill** (inside a colored :doc:`Frame <frame>`, say),
give it an ``@<color>`` **surface** token — it paints the background that palette
color and picks the text to read against it:

.. code-block:: python

   ttk.Label(app, text="Header", bootstyle="@primary")

Setting colors directly
~~~~~~~~~~~~~~~~~~~~~~~~~

``bootstyle`` and ``@<color>`` both draw from the theme palette. For any **other**
color, ``Label`` is one of the few ttk widgets that accept ``foreground`` and
``background`` directly (most take their colors only from a style); a value set this
way overrides the ``bootstyle`` color. Pass a raw color, or read one from the active
theme through ``style.colors`` — an accent, an interface role, or a ramp step:

.. code-block:: python

   colors = app.style.colors

   ttk.Label(app, text="Note",    foreground="#b02a37", background="#fff3cd")
   ttk.Label(app, text="Balance", foreground=colors.success)
   ttk.Label(app, text="Tag",     foreground=colors.primary, background=colors.primary[100])

A :doc:`color helper </reference/utilities>` can compute one — ``contrast_color``
picks black or white to read against a background:

.. code-block:: python

   from ttkbootstrap import contrast_color

   bg = colors.info
   ttk.Label(app, text="Info", background=bg, foreground=contrast_color(bg, "hex"))

A direct color — raw or read from ``style.colors`` — is a **fixed snapshot**: it
stays as you set it across theme switches but does not adapt to the new theme. Use
``bootstyle`` / ``@<color>`` for theme-following colors; see
:doc:`Theming & Colors </user-guide/feature-guides/theming>` for the palette and
rebuilding on a theme change.

Wrapping long text
------------------

A label is a single line by default and will run off the edge. Set ``wraplength=``
(in pixels) to wrap it into a block, and ``justify=`` for the alignment of the
wrapped lines:

.. code-block:: python

   ttk.Label(app, text="A long paragraph that should wrap…", wraplength=200, justify="left")

Aligning and sizing
-------------------

Two options are easy to confuse. ``justify=`` (above) aligns **multiple wrapped
lines** against each other; ``anchor=`` positions the whole text/image block
**within the label's own area** (``"w"`` left, ``"center"``, ``"e"`` right, plus
the corners) — visible only when the label is bigger than its content. Give a
label a fixed ``width=`` (in characters) so a column of field-name labels lines up
its values:

.. code-block:: python

   ttk.Label(app, text="Name", width=12, anchor="e").pack()

A filled ``@<color>`` label with a little ``padding=`` reads as a tag or badge — a
status pill, a category chip:

.. code-block:: python

   ttk.Label(app, text="NEW", bootstyle="@success", padding=(8, 2))

Fonts and images
----------------

Set ``font=`` to change the type — a Tk font spec, a named font, or a
:class:`~ttkbootstrap.Font`:

.. code-block:: python

   ttk.Label(app, text="Heading", font="-size 18 -weight bold")

A label can also show an image (with or without text) via ``image=`` and
``compound=``, which places the image relative to the text (``"left"``, ``"top"``,
``"center"``, or ``"image"`` / ``"text"`` to show just one). Building and keeping a
reference to images is covered in
:doc:`Show images and icons </user-guide/how-to/working-with-images>`; type styling
in the :doc:`Typography guide </user-guide/feature-guides/typography>`.

Reference
---------

``Label`` is the native ``ttk.Label``; ttkbootstrap adds only the ``bootstyle``
keyword.

- :doc:`Label API reference </reference/api/label>` — every option and method.
- :ref:`Label styling options <label-styling>` — restyle it yourself, with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Typography guide </user-guide/feature-guides/typography>` — fonts and type.
   - :doc:`Show images and icons </user-guide/how-to/working-with-images>` — the image side.
