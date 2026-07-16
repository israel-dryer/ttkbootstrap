User Guide
==========

Learn ttkbootstrap by working through it: set up and build your first window,
grasp the core styling concepts (the ``bootstyle`` grammar and how styling is
delivered), reach for a feature guide when you need a whole subsystem — fonts,
localization, validation, windowing — or grab a how-to when you have a specific
task in mind. For the complete lookup of every public name see the
:doc:`Reference </reference/index>`; for the visual widget catalog see
:doc:`Widgets </widgets/index>`.

Getting Started
---------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Installation
      :link: getting-started/installation
      :link-type: doc

      Install from PyPI; supported Python versions.

   .. grid-item-card:: Quickstart
      :link: getting-started/quickstart
      :link-type: doc

      Your first themed window; ``App`` vs ``Tk``; choosing a theme.

   .. grid-item-card:: Build your first app
      :link: getting-started/build-your-first-app
      :link-type: doc

      A guided, end-to-end tutorial: a contact book with a form, validation,
      and a data table.

   .. grid-item-card:: Structuring an app
      :link: getting-started/app-structures
      :link-type: doc

      ``App`` vs ``Tk``, the single-root rule, and a real app skeleton.

   .. grid-item-card:: Migrating to 2.0
      :link: getting-started/migrating
      :link-type: doc

      bootstyle strings, theme names, removed shims, and icons.

Foundations
-----------

New to tkinter? These pages cover the mental models everything else builds on —
how an app runs, how widgets are arranged, how they bind to your data, how they
respond to input, and how ttkbootstrap styles them.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: How a tkinter app runs
      :link: foundations/how-a-tkinter-app-runs
      :link-type: doc

      The event loop, ``mainloop``, callbacks, ``after``, and not freezing the UI.

   .. grid-item-card:: The widget model
      :link: foundations/the-widget-model
      :link-type: doc

      The widget tree, options (``configure``/``cget``), and ttk states.

   .. grid-item-card:: What tkinter wraps
      :link: foundations/what-tkinter-wraps
      :link-type: doc

      The Tcl/Tk layer underneath — path names, dashed options, and how to read
      a ``TclError``.

   .. grid-item-card:: Arranging widgets
      :link: foundations/arranging-widgets
      :link-type: doc

      The three geometry managers and when to use each — start here, then the
      grid and pack tutorials.

   .. grid-item-card:: Variables & reactivity
      :link: foundations/state-and-variables
      :link-type: doc

      Binding widgets to ``StringVar``/``IntVar``/``BooleanVar`` and reacting to
      changes.

   .. grid-item-card:: Events & callbacks
      :link: foundations/events-and-callbacks
      :link-type: doc

      ``command``, ``bind`` and event objects, virtual events, and ``after``.

   .. grid-item-card:: Styling with bootstyle
      :link: foundations/bootstyle-grammar
      :link-type: doc

      The canonical grammar for styling any widget, with the full reference
      table.

   .. grid-item-card:: How styling is delivered
      :link: foundations/delivery-model
      :link-type: doc

      How the ``bootstyle`` API reaches your widgets — the widget subclasses,
      ``enable_global_api``, ``bootify``, and ``apply_bootstyle``.

Feature guides
--------------

Each subsystem, end to end — its concepts and its usage in one place.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Typography
      :link: feature-guides/typography
      :link-type: doc

      ``Fonts`` and ``set_global_family`` over the standard named fonts.

   .. grid-item-card:: Localization
      :link: feature-guides/localization
      :link-type: doc

      ``L()``, ``LocaleVar``, ``set_locale``, and live language switching.

   .. grid-item-card:: Input validation
      :link: feature-guides/validation
      :link-type: doc

      ``add_*_validation`` helpers and the ``@validator`` decorator.

   .. grid-item-card:: Variables
      :link: feature-guides/variables
      :link-type: doc

      Variable types, traces (read/write/unset), computed fields, and
      ``LocaleVar``.

   .. grid-item-card:: Events
      :link: feature-guides/events
      :link-type: doc

      The binding system in depth — scope & bindtags, stopping events, and
      dispatching your own virtual events.

   .. grid-item-card:: Icons
      :link: feature-guides/icons
      :link-type: doc

      Theme-aware Bootstrap Icons glyphs — the ``icon=`` keyword, ``apply_icon``,
      and the standalone ``Icon`` image.

   .. grid-item-card:: Windows
      :link: feature-guides/windows
      :link-type: doc

      ``App``/``Toplevel`` setup, focus & modality, positioning, high-DPI, and the
      deferred-config seam.

   .. grid-item-card:: Menus
      :link: feature-guides/menus
      :link-type: doc

      Menu bars, submenus, stateful items, context menus, and the cross-platform
      macOS application menu.

   .. grid-item-card:: Dialogs
      :link: feature-guides/dialogs
      :link-type: doc

      ``Messagebox`` and ``Querybox``, the date/font/color pickers, ``filedialog``,
      and what each returns.

   .. grid-item-card:: Theming & Colors
      :link: feature-guides/theming
      :link-type: doc

      Choosing and switching themes, light/dark, the built-in catalog, reading
      the theme's colors (``style.colors``, ramps), and building your own theme.

   .. grid-item-card:: Custom styles
      :link: feature-guides/custom-styles
      :link-type: doc

      The custom style-construction toolkit — assets, layouts, and icons.

How-To
------

Task-focused recipes — common tkinter jobs done the ttkbootstrap way.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Show images and icons
      :link: how-to/working-with-images
      :link-type: doc

      ``PhotoImage`` and Pillow, the keep-a-reference gotcha, and themed glyphs.

   .. grid-item-card:: Scroll long content
      :link: how-to/scrollable
      :link-type: doc

      ``ScrolledFrame`` and ``ScrolledText`` for content that outgrows the window.

   .. grid-item-card:: Open a second window
      :link: how-to/multiple-windows
      :link-type: doc

      A second ``Toplevel``, a modal that returns a value, and the close button.

   .. grid-item-card:: Run background work
      :link: how-to/threads
      :link-type: doc

      ``after`` and worker threads, updating widgets safely from the main loop.

   .. grid-item-card:: Copy and paste text
      :link: how-to/clipboard
      :link-type: doc

      The clipboard methods, the copy shortcut, and the current selection.

   .. grid-item-card:: Handle callback errors
      :link: how-to/error-handling
      :link-type: doc

      Take over ``report_callback_exception`` and deal with ``TclError``.

   .. grid-item-card:: Ring the system bell
      :link: how-to/bell
      :link-type: doc

      A system beep to flag a rejected action or a finished job.

   .. grid-item-card:: Mark a window busy
      :link: how-to/busy
      :link-type: doc

      A wait cursor and a block on clicks while a slow job runs.

   .. grid-item-card:: Animate a GIF
      :link: how-to/animate-gif
      :link-type: doc

      Frame-by-frame animation with ``PhotoImage`` and ``after``.

   .. grid-item-card:: Show a splash screen
      :link: how-to/splash-screen
      :link-type: doc

      A borderless startup window that hands off to the main one.

   .. grid-item-card:: Set the app icon
      :link: how-to/application-icon
      :link-type: doc

      The titlebar and taskbar icon, and the Windows ``.ico`` case.

.. toctree::
   :hidden:
   :caption: Getting Started

   getting-started/installation
   getting-started/quickstart
   getting-started/build-your-first-app
   getting-started/app-structures
   getting-started/migrating

.. toctree::
   :hidden:
   :caption: Foundations

   foundations/how-a-tkinter-app-runs
   foundations/the-widget-model
   foundations/what-tkinter-wraps
   foundations/arranging-widgets
   foundations/layout-with-grid
   foundations/layout-with-pack
   foundations/state-and-variables
   foundations/events-and-callbacks
   foundations/bootstyle-grammar
   foundations/delivery-model

.. toctree::
   :hidden:
   :caption: Feature guides

   feature-guides/typography
   feature-guides/localization
   feature-guides/validation
   feature-guides/variables
   feature-guides/events
   feature-guides/icons
   feature-guides/windows
   feature-guides/menus
   feature-guides/dialogs
   feature-guides/theming
   feature-guides/custom-styles

.. toctree::
   :hidden:
   :caption: How-To

   how-to/working-with-images
   how-to/scrollable
   how-to/multiple-windows
   how-to/threads
   how-to/clipboard
   how-to/error-handling
   how-to/bell
   how-to/busy
   how-to/animate-gif
   how-to/splash-screen
   how-to/application-icon
