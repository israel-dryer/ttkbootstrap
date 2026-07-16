Set the app icon
================

The icon your app shows in the titlebar, the taskbar, and the app switcher.
Out of the box a ttkbootstrap app wears the ttkbootstrap logo; this recipe
replaces it with your own.

Set it on the root
------------------

Pass ``iconphoto`` a path when you create the ``App``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="bootstrap-light", iconphoto="assets/logo.png")

That is the whole job for one window. The icon set on the root is the
application-wide default, so every dialog and ``Toplevel`` you open afterwards
inherits it — you do not repeat yourself per window.

.. note::

   PNG is the format to use. Tk reads PNG and GIF natively, and PNG keeps its
   transparency. A square source of 512×512 gives every platform enough pixels
   to scale down from.

The three values ``iconphoto`` accepts are worth knowing apart:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Value
     - Result
   * - a path
     - Load that image and use it as the icon.
   * - ``""`` (the default)
     - The ttkbootstrap logo.
   * - ``None``
     - Leave the icon alone — you get Tk's own feather.

A bad path is not fatal: ttkbootstrap warns and falls back to the default icon
rather than crashing your app on startup.

Give one window its own icon
----------------------------

A ``Toplevel`` inherits the app icon, which is usually what you want. Pass its
own ``iconphoto`` when it shouldn't — the override applies to that window only
and leaves the rest of the app alone:

.. code-block:: python

   report = ttk.Toplevel(title="Report", iconphoto="assets/report.png")

Windows: use an .ico
--------------------

Windows draws the icon at several sizes at once — small in the titlebar, larger
in the taskbar and Alt-Tab — and a single PNG gets scaled to all of them, which
looks soft. A multi-resolution ``.ico`` carries a purpose-made image for each
size. Pass one and ttkbootstrap applies it the Windows way:

.. code-block:: python

   app = ttk.App(theme="bootstrap-light", iconphoto="assets/logo.ico")

.. note::

   ``.ico`` files are only honored on Windows. To ship one app for every
   platform, pick the file at startup:

   .. code-block:: python

      import sys

      icon = "assets/logo.ico" if sys.platform == "win32" else "assets/logo.png"
      app = ttk.App(theme="bootstrap-light", iconphoto=icon)

You can build the ``.ico`` from your PNG with Pillow, which ttkbootstrap already
depends on:

.. code-block:: python

   from PIL import Image

   sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
   Image.open("assets/logo.png").save("assets/logo.ico", sizes=sizes)

Change the icon later
---------------------

The icon is not fixed at construction. ``iconphoto`` is also a method — pass it
a ``PhotoImage`` and a first argument of ``True`` to change the app-wide
default:

.. code-block:: python

   import tkinter

   badge = tkinter.PhotoImage(file="assets/unread.png", master=app)
   app.iconphoto(True, badge)

.. warning::

   Keep a reference to the ``PhotoImage``. A local that goes out of scope is
   garbage collected and the icon reverts. Assign it to an attribute
   (``app.badge = badge``) or any other name that outlives the call — the same
   gotcha covered in :doc:`Show images and icons <working-with-images>`.

.. seealso::

   - :doc:`Show images and icons <working-with-images>` — loading images, Pillow
     formats, and themed glyphs.
   - :doc:`Windows guide </user-guide/feature-guides/windows>` — titles,
     geometry, and window state.

Reference
---------

- :doc:`App </reference/windows/app>` — the ``iconphoto`` option and method.
- :doc:`Toplevel </reference/windows/toplevel>` — per-window icon overrides.