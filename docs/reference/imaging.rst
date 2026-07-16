Imaging
=======

Two kinds of image reach a widget's ``image`` option. ``PhotoImage`` is Tk's
own image primitive — load a PNG or GIF from a file or base-64 data, or draw one
pixel by pixel, then pass it to a ``Button``, ``Label``, or any widget that
takes an image. The icon engine renders a named `Bootstrap Icons
<https://icons.getbootstrap.com/>`_ glyph as a theme-colored image, so you can
put a crisp, recolorable icon on a widget without shipping image files. The
:doc:`Icons </user-guide/feature-guides/icons>` guide shows the icon engine in
use.

Photo images
------------

.. py:class:: PhotoImage(name=None, cnf={}, master=None, *, data=None, file=None, format=None, width=0, height=0)
   :noindex:

   A full-color image you can display on a widget. Create an empty canvas by
   giving ``width``/``height``, or load one from ``file`` (a PNG or GIF path) or
   ``data`` (the image bytes, or base-64 text). Hold a reference to the object
   for as long as the widget shows it — Tk does not, and a garbage-collected
   ``PhotoImage`` blanks the widget.

   :param file: path to a PNG or GIF image to load.
   :param data: the image as bytes or a base-64 string (an alternative to ``file``).
   :param format: the image format, when it can't be inferred (e.g. ``"gif"``).
   :param width: the width in pixels of a blank image.
   :param height: the height in pixels of a blank image.

.. py:method:: width()
   :noindex:

   Return the image width in pixels.

.. py:method:: height()
   :noindex:

   Return the image height in pixels.

.. py:method:: get(x, y)
   :noindex:

   Return the color of the pixel at ``(x, y)`` as an ``(r, g, b)`` tuple.

.. py:method:: put(data, to=None)
   :noindex:

   Write colors into the image. ``data`` is a color string or a nested
   sequence of color rows; ``to`` is the ``(x, y)`` corner (or an ``(x1, y1,
   x2, y2)`` box) to write into.

   :param data: a color, or rows of colors, to write.
   :param to: where to write — a corner or a bounding box.

.. py:method:: blank()
   :noindex:

   Clear the image to transparent, keeping its size.

.. py:method:: copy()
   :noindex:

   Return a new ``PhotoImage`` with the same contents.

   :rtype: PhotoImage

.. py:method:: zoom(x, y=None)
   :noindex:

   Return a copy magnified by integer factor ``x`` horizontally and ``y``
   vertically (``y`` defaults to ``x``).

   :rtype: PhotoImage

.. py:method:: subsample(x, y=None)
   :noindex:

   Return a copy reduced by integer factor ``x`` horizontally and ``y``
   vertically (``y`` defaults to ``x``).

   :rtype: PhotoImage

.. py:method:: write(filename, format=None, from_coords=None)
   :noindex:

   Save the image to ``filename``.

   :param filename: the path to write to.
   :param format: the output format (e.g. ``"png"``).
   :param from_coords: an optional region of the image to save.

.. py:method:: configure(**options)
   :noindex:

   Get or set image options (``width``, ``height``, ``data``, ``file``, …).
   Alias: ``config``.

.. py:method:: cget(option)
   :noindex:

   Return the value of one image option.

One related method lives on the **widget**, not on ``PhotoImage``:

.. py:method:: image_types()
   :noindex:

   The image types this Tk build can create — ``('photo', 'bitmap')``. Call it on
   any widget.

   :returns: the available image type names.
   :rtype: tuple

Icons
-----

.. autofunction:: ttkbootstrap.Icon

.. autofunction:: ttkbootstrap.apply_icon

.. autofunction:: ttkbootstrap.icon_element

See also
--------

- :doc:`Icons </user-guide/feature-guides/icons>` — how to use icons on widgets,
  with examples.
- :doc:`styling` — the ``Assets`` toolkit that ``icon_element`` builds on.
