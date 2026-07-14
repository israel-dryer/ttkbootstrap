Reference
=========

The lookup layer:

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Widgets
      :link: api/index
      :link-type: doc

      Every widget's options, methods, and — for ttk widgets — styling. The
      native ttk widgets, the ones ttkbootstrap ships, and the classic tk
      widgets, grouped by what they do.

   .. grid-item-card:: Windows
      :link: windows/index
      :link-type: doc

      The application window classes — ``App`` (the root) and ``Toplevel`` — and
      their constructor, theme, and window-management surface.

   .. grid-item-card:: Dialogs & overlays
      :link: dialogs/index
      :link-type: doc

      Message, input, and picker dialogs — ``Messagebox``, ``Querybox``, and the
      dialog classes — plus toasts and tooltips.

   .. grid-item-card:: Styling
      :link: styling
      :link-type: doc

      The style engine and the tools to build your own styles — ``Style``,
      the ``bootstyle`` delivery helpers, and the custom-style toolkit.

   .. grid-item-card:: Theming
      :link: theming
      :link-type: doc

      Declare and consume color themes — ``Theme``, ``ThemeDefinition``,
      ``Colors``, and the legacy-theme bridge.

   .. grid-item-card:: Imaging
      :link: imaging
      :link-type: doc

      Images on widgets — the ``PhotoImage`` primitive and the Bootstrap Icons
      glyph engine (``Icon``, ``apply_icon``, ``icon_element``).

   .. grid-item-card:: Localization
      :link: localization
      :link-type: doc

      Translate built-in strings and switch locales — ``L``, ``set_locale``,
      ``LocaleVar``, ``MessageCatalog``.

   .. grid-item-card:: Fonts
      :link: fonts
      :link-type: doc

      Manage the application's named fonts and the global family.

   .. grid-item-card:: Validation
      :link: validation
      :link-type: doc

      Attach input validation to entries — ready-made checks plus custom
      validators.

   .. grid-item-card:: Variables
      :link: variables
      :link-type: doc

      The typed value holders that bind to widgets — ``StringVar``, ``IntVar``,
      ``DoubleVar``, ``BooleanVar``, and ``LocaleVar``.

   .. grid-item-card:: Geometry
      :link: geometry/index
      :link-type: doc

      The geometry managers that size and place widgets — pack, grid, place, and
      stacking order.

   .. grid-item-card:: Utilities
      :link: utilities
      :link-type: doc

      Standalone helpers — color conversion and contrast, high-DPI awareness
      and scaling, and theme-change hooks.

   .. grid-item-card:: Capabilities
      :link: capabilities/index
      :link-type: doc

      The methods every widget inherits, grouped by area — configuration, focus,
      grab, after, clipboard, and ``winfo`` — each mirroring its Tcl/Tk manual
      page.

   .. grid-item-card:: Events
      :link: events/index
      :link-type: doc

      The tkinter event system — event types, modifiers, key symbols, the event
      object, and the built-in ``<<virtual>>`` events.

   .. grid-item-card:: Cursors
      :link: cursors
      :link-type: doc

      The mouse-pointer names the ``cursor`` option accepts — the common set,
      the full portable list, and the platform-specific pointers.

.. toctree::
   :hidden:

   api/index
   windows/index
   dialogs/index
   styling
   theming
   imaging
   localization
   fonts
   validation
   variables
   geometry/index
   utilities
   capabilities/index
   events/index
   cursors
