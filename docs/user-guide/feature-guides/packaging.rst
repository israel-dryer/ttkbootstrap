Packaging an application
========================

ttkbootstrap depends on icon and font files inside the installed package. Freezing tools find code by following imports, and data only by being told about it — so a frozen application that looked correct in development can start up with no icons at all, and whatever it does instead happens at run time on a user's machine rather than at build time on yours.

This package ships PyInstaller hooks that collect that data, and registers them so PyInstaller finds them.

PyInstaller
-----------

There is nothing to configure:

.. code-block:: bash

   pip install pyinstaller
   pyinstaller --onefile your_app.py

The hooks are registered through PyInstaller's ``pyinstaller40`` entry point, so it discovers them itself and collects the font and glyph map of every pack you have installed. A pack you did not install has nothing to collect and is skipped.

.. versionadded:: 2.2.3
   The hooks are registered for automatic discovery.

Pointing at the hooks explicitly
--------------------------------

Automatic discovery needs the entry point to be visible, which it is for any normal install. If you are vendoring the package, running from a source tree that was never installed, or building with a tool that ignores entry points, name the directory yourself:

.. code-block:: python

   # your_app.spec
   from ttkbootstrap._pyinstaller import get_hook_dirs

   a = Analysis(
       ["your_app.py"],
       hookspath=get_hook_dirs(),
       ...
   )

Or on the command line:

.. code-block:: bash

   pyinstaller --additional-hooks-dir "$(python -c 'import ttkbootstrap._pyinstaller; print(ttkbootstrap._pyinstaller.get_hook_dirs()[0])')" your_app.py

:func:`~ttkbootstrap._pyinstaller.get_hook_dirs` returns the directory holding the hook

What the hook does
------------------

The hook consists of a single line of ``collect_data_files`` which collects all of the static assets required.


Check the build
---------------

Missing data shows up only in the frozen application, and it will show up as an error. Run it:

.. code-block:: bash

   ./dist/your_app        # Linux, macOS
   .\dist\your_app.exe    # Windows


Other freezers
--------------

cx_Freeze, Nuitka, and py2app do not read PyInstaller hooks, so data has to be listed explicitly:

.. code-block:: python

   # cx_Freeze, in setup.py
   from importlib.resources import files

   pack = files("ttkbootstrap")
   include_files = [(str(pack), "lib/ttkbootstrap")]

Verify by running the frozen application rather than by reading the configuration. The failure mode is silent.