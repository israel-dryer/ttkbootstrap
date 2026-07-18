Show images and icons
=====================

To show a picture in tkinter you wrap it in an *image object* and hand that to a
widget's ``image=`` option. There are two image classes, and one notorious
gotcha to know before anything else.

Which image class
-----------------

- ``ttk.PhotoImage`` — tkinter's built-in image. It reads **GIF, PNG, PGM, and
  PPM** files (and base64-encoded GIF/PNG data), and needs no extra library.
- Pillow's ``ImageTk.PhotoImage`` — reads **every common format** (JPEG, BMP,
  TIFF, WebP, …) and lets you resize, crop, and filter first. Pillow is already a
  dependency of ttkbootstrap, so it is always available.

Reach for Pillow for anything beyond a simple GIF/PNG — which is most real work.

.. _images-keep-a-reference:

Keep a reference (the image that vanishes)
------------------------------------------

.. important::

   **An image object must be kept alive by your own code, or it disappears.**
   Tk stores the image by *name*, and a widget's ``image=`` option does not hold
   the Python object — so if the only reference is a local variable, the garbage
   collector reclaims the image the moment the function returns and the widget
   goes blank.

This is the single most common tkinter image bug. It applies to **both** image
classes. The fix is to keep a reference somewhere that outlives the function —
conventionally on the widget itself, or on ``self``:

.. code-block:: python

   def add_logo(parent):
       photo = ttk.PhotoImage(file="logo.png")
       label = ttk.Label(parent, image=photo)
       label.image = photo          # <- keeps the image alive with the label
       label.pack()

Without the ``label.image = photo`` line, the label shows nothing. When you store
images on ``self`` (say in a class-based app), the same rule holds — just make
sure the attribute lives as long as the widget does.

Displaying an image
-------------------

Pass the image as ``image=``. To show it *alongside* text, add ``compound=`` to
say where the image sits relative to the label:

.. code-block:: python

   ttk.Button(app, text="Open", image=photo, compound="left")

``compound`` takes ``"left"``, ``"right"``, ``"top"``, ``"bottom"`` (the image on
that side of the text), ``"center"`` (text over image), ``"image"`` (image only),
``"text"`` (text only), or ``"none"`` (the image if there is one, otherwise the
text).

Loading and resizing with Pillow
--------------------------------

Open with Pillow, transform, then wrap the result. Keep a reference as always:

.. code-block:: python

   from PIL import Image, ImageTk

   pil = Image.open("photo.jpg")
   pil = pil.resize((120, 120))
   thumb = ImageTk.PhotoImage(pil)

   card = ttk.Label(app, image=thumb)
   card.image = thumb
   card.pack()

Embedding an image in your code
-------------------------------

To ship an image inside a ``.py`` file with no separate asset, base64-encode it
and pass it as ``data=`` to ``ttk.PhotoImage`` (GIF/PNG only):

.. code-block:: python

   LOGO = "iVBORw0KGgo..."          # base64 string of a PNG
   photo = ttk.PhotoImage(data=LOGO)

Themed glyph icons
------------------

For *icons* — the small symbols on buttons and menu items — you usually want a
crisp, theme-following glyph rather than a raster file. ttkbootstrap renders
those from a built-in Bootstrap Icons font. Just pass ``icon=`` — no image object
to build or keep alive, and the glyph recolors with the theme and widget state:

.. code-block:: python

   ttk.Button(app, text="Settings", icon="gear-fill")

See the :doc:`Icons guide </user-guide/feature-guides/icons>` for the full icon
API, and :doc:`Windows </user-guide/feature-guides/windows>`
for setting the *application* icon.

A worked example
----------------

Loads a Pillow image, scales it, and displays it — with the reference kept so it
stays on screen:

.. code-block:: python

   import ttkbootstrap as ttk
   from PIL import Image, ImageTk

   app = ttk.App(title="Image")

   pil = Image.open("photo.jpg").resize((200, 200))
   photo = ImageTk.PhotoImage(pil)

   label = ttk.Label(app, image=photo, padding=10)
   label.image = photo          # keep the reference
   label.pack()

   app.mainloop()

.. image:: /_static/examples/working-with-images-photo-light.png
   :class: tb-screenshot-light
   :width: 220px
   :alt: A resized photo displayed inside a padded label — light theme

.. image:: /_static/examples/working-with-images-photo-dark.png
   :class: tb-screenshot-dark
   :width: 220px
   :alt: A resized photo displayed inside a padded label — dark theme

.. seealso::

   - :doc:`Animate a GIF <animate-gif>` — swapping frames on a timer.
   - :doc:`Set the app icon <application-icon>` — the titlebar and taskbar icon.
   - :doc:`Icons guide </user-guide/feature-guides/icons>` — glyph names, sizing,
     and per-state icons.
   - The `Pillow <https://pillow.readthedocs.io/>`__ documentation — raster
     formats and image manipulation.

Reference
---------

- :doc:`Imaging </reference/imaging>` — the full ``PhotoImage`` API.
