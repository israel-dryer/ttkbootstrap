Package your app
================

Turn your app into a standalone program with PyInstaller, so people can run it
without installing Python or ttkbootstrap.

Build it
--------

Install PyInstaller into the same environment as your app, then point it at your
entry script:

.. code-block:: bash

   pip install pyinstaller
   pyinstaller --onefile your_app.py

The program is written to ``dist/``. ttkbootstrap's icon font and widget images
are bundled automatically — there is nothing to add to the command or to a spec
file.

Run it before you ship it
-------------------------

Start the built program from a terminal, so any error is printed where you can
read it:

.. code-block:: bash

   ./dist/your_app        # Linux, macOS
   .\dist\your_app.exe    # Windows

A program built without ttkbootstrap's data files stops at startup with a
``FileNotFoundError`` naming a file under ``ttkbootstrap/assets``.

Name the hook directory yourself
--------------------------------

PyInstaller finds ttkbootstrap's hook through the installed package. When
ttkbootstrap is vendored into your project, or runs from a source tree that was
never installed, pass the directory to ``Analysis`` in your spec file:

.. code-block:: python

   # your_app.spec
   from ttkbootstrap._pyinstaller import get_hook_dirs

   a = Analysis(
       ["your_app.py"],
       hookspath=get_hook_dirs(),
       # ...the rest of your Analysis arguments
   )

Or print the directory and pass it on the command line:

.. code-block:: bash

   python -c "from ttkbootstrap._pyinstaller import get_hook_dirs; print(get_hook_dirs()[0])"
   pyinstaller --onefile --additional-hooks-dir <printed directory> your_app.py
