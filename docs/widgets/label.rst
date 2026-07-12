Label
=====

A **label** displays a line of read-only text (or an image) — a caption, a field
name, a status line. ``Label`` is the native ``ttk.Label``, styled with
``bootstyle=``. This page covers showing static and dynamic text, coloring it,
wrapping long text, then fonts and images.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A heading label and a colored status label in light and dark themes.

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
use ``inverse-<color>`` — it paints the background the color and the text to read
against it:

.. code-block:: python

   ttk.Label(app, text="Header", bootstyle="inverse-primary")

.. note::

   ``Label`` is one of the few ttk widgets that also accepts ``foreground``,
   ``background``, and ``font`` **directly** as options — most ttk widgets take
   their colors only from a style. A value set this way overrides the
   ``bootstyle`` color, which is handy for a one-off:

   .. code-block:: python

      ttk.Label(app, text="Note", foreground="#b02a37", background="#fff3cd")

   Prefer ``bootstyle`` for anything themed, though — a hard-coded color here does
   not follow a theme switch.

Wrapping long text
------------------

A label is a single line by default and will run off the edge. Set ``wraplength=``
(in pixels) to wrap it into a block, and ``justify=`` for the alignment of the
wrapped lines:

.. code-block:: python

   ttk.Label(app, text="A long paragraph that should wrap…", wraplength=200, justify="left")

Fonts and images
----------------

Set ``font=`` to change the type — a Tk font spec, a named font, or a
:class:`~ttkbootstrap.Font`:

.. code-block:: python

   ttk.Label(app, text="Heading", font="-size 18 -weight bold")

A label can also show an image (with or without text) via ``image=`` and
``compound=``. Building and keeping a reference to images is covered in
:doc:`Show images and icons </user-guide/how-to/working-with-images>`; type styling
in the :doc:`Typography guide </user-guide/feature-guides/typography>`.

API & reference
---------------

``Label`` is the native ``ttk.Label`` — ttkbootstrap adds ``bootstyle=`` but no
other Python API. For its constructor and options (``text``, ``textvariable``,
``font``, ``image``, ``compound``, ``wraplength``, ``justify``, ``anchor``,
``width``, …) see the
`tkinter.ttk.Label <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Label>`__
reference.

.. seealso::

   The :doc:`Typography guide </user-guide/feature-guides/typography>` for fonts,
   and :doc:`Show images and icons </user-guide/how-to/working-with-images>` for
   the image side. Want to restyle the label yourself? The
   :doc:`Style Reference › Label </reference/style-reference/label>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
