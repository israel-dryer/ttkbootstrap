Styling
=======

Styling in ttkbootstrap runs through one engine and reaches widgets three ways.
The ``Style`` engine owns the active theme and builds ttk styles on demand. The
shipped widgets carry the ``bootstyle`` keyword; to put that keyword on a widget
ttkbootstrap does not ship, use the delivery helpers below. And when a name in
the ``bootstyle`` vocabulary can't describe the look you want, the toolkit builds
a ttk style by hand. The :doc:`Custom styles
</user-guide/feature-guides/custom-styles>` guide shows the toolkit in use.

The style engine
----------------

``Style`` is a process-wide singleton, bound to the first application window and
reachable as its ``style`` attribute (or ``Style.get_instance()``). It holds the
theme definitions, switches the active theme, and exposes the current theme's
colors.

.. autoclass:: ttkbootstrap.Style
   :members:

Applying styles to any widget
-----------------------------

The widgets ttkbootstrap ships already accept ``bootstyle``. These helpers extend
that keyword to widgets it does not ship — a third-party ttk widget, or a plain
``tkinter.ttk`` widget you created yourself.

.. autofunction:: ttkbootstrap.bootify

.. autofunction:: ttkbootstrap.apply_bootstyle

.. autofunction:: ttkbootstrap.enable_global_api

Building custom styles
----------------------

For a look ``bootstyle`` can't name, compose a ttk style from **assets**,
**elements**, a **state map**, and a **layout** — each a small toolkit call.
``Assets`` renders cached images, ``image_element`` turns one into a named ttk
element, ``state_map`` is a validated ``style.map``, and ``layout`` arranges the
elements into the widget's element tree and registers the style. See the
:doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide for a
worked example.

.. autoclass:: ttkbootstrap.Assets
   :members:

.. autofunction:: ttkbootstrap.image_element

.. autofunction:: ttkbootstrap.state_map

.. autofunction:: ttkbootstrap.statespec

.. autofunction:: ttkbootstrap.layout

.. autoclass:: ttkbootstrap.El
   :members:

.. autofunction:: ttkbootstrap.register_style

.. autoclass:: ttkbootstrap.StyleName
   :members:

.. note::

   To render a glyph as an element in a custom layout, see
   :func:`~ttkbootstrap.icon_element` on the :doc:`Imaging <imaging>` page.

See also
--------

- :doc:`Custom styles </user-guide/feature-guides/custom-styles>` — how to build
  and apply your own styles, with examples.
- :doc:`Theming & Colors </user-guide/feature-guides/theming>` — the theme model
  behind the engine.
