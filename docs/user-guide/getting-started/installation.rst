Installation
============

ttkbootstrap installs from PyPI with ``pip``:

.. code-block:: bash

   pip install ttkbootstrap

That is everything you need on Windows and macOS if you installed Python from
`python.org <https://www.python.org/downloads/>`_. On Linux — and on a few other
setups — you also need tkinter, which :ref:`the next section <install-tkinter>`
covers.

Requirements
------------

- **Python 3.10 or newer.**
- **tkinter**, Python's built-in interface to the Tcl/Tk toolkit. ttkbootstrap
  styles tkinter's ttk widgets, so it needs this module (and the Tcl/Tk libraries
  behind it). The python.org installers for Windows and macOS include it; on Linux
  it is usually a separate system package.
- **Pillow**, the imaging library ttkbootstrap uses to render widget assets. It is
  the only third-party runtime dependency, and ``pip`` installs it for you.


Install in a virtual environment
--------------------------------

A virtual environment keeps ttkbootstrap and Pillow out of your system Python.
Create one, activate it, then install into it:

.. tab-set::

   .. tab-item:: Windows

      .. code-block:: bat

         py -m venv .venv
         .venv\Scripts\activate
         pip install ttkbootstrap

      In PowerShell the activate command is ``.venv\Scripts\Activate.ps1``.

   .. tab-item:: macOS / Linux

      .. code-block:: bash

         python3 -m venv .venv
         source .venv/bin/activate
         pip install ttkbootstrap

Activate the environment in each new terminal before you run your app.


.. _install-tkinter:

Make sure tkinter is available
------------------------------

Most Python installations include tkinter, but some do not. Ask Python directly:

.. code-block:: bash

   python -m tkinter

That opens a small window showing the Tcl/Tk version. If instead you get
``ModuleNotFoundError: No module named 'tkinter'`` (or ``_tkinter``), install it
for your platform:

.. tab-set::

   .. tab-item:: Windows

      Re-run the `python.org <https://www.python.org/downloads/>`_ installer and
      make sure **"tcl/tk and IDLE"** is checked — it is by default. The Microsoft
      Store build of Python also includes tkinter.

   .. tab-item:: macOS

      The `python.org <https://www.python.org/downloads/>`_ installer bundles a
      current Tcl/Tk. If you use Homebrew's Python, add tkinter with:

      .. code-block:: bash

         brew install python-tk

      Avoid the old system ``/usr/bin/python3`` for GUI work — it links an
      outdated Tcl/Tk that renders poorly.

   .. tab-item:: Linux

      tkinter is packaged separately from Python on most distributions:

      .. code-block:: bash

         sudo apt install python3-tk        # Debian, Ubuntu, Mint
         sudo dnf install python3-tkinter   # Fedora
         sudo pacman -S tk                  # Arch, Manjaro
         sudo zypper install python3-tk     # openSUSE


Check your install
------------------

With the environment active, confirm ttkbootstrap imports and draws. This opens a
demo window with a theme picker and a sample of every widget:

.. code-block:: bash

   python -m ttkbootstrap

Or write the smallest possible app yourself:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="It works", theme="bootstrap-light")
   ttk.Button(app, text="Hello", bootstyle="success").pack(padx=20, pady=20)
   app.mainloop()

A themed window means everything is in place. From here, head to the
:doc:`Quickstart <quickstart>`.


Multi-monitor window positioning (optional)
-------------------------------------------

ttkbootstrap centers and places windows using Tk's own screen metrics, which
assume a single display. To center on the monitor under the pointer and keep
windows on the correct screen in a multi-monitor setup, install the optional
`screeninfo <https://pypi.org/project/screeninfo/>`_ package:

.. code-block:: bash

   pip install screeninfo

ttkbootstrap uses it automatically when it is present; without it, window
positioning falls back to single-screen behavior. It is never required.


See also
--------

- :doc:`Quickstart <quickstart>` — your first themed window in about a minute.
- :doc:`Build your first app <build-your-first-app>` — a complete app, built step
  by step.
- :doc:`Migrating to 2.0 <migrating>` — upgrading an existing 1.x project.
