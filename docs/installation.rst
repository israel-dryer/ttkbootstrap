Installation
============

Installing ttkbootstrap is easy! There are a few options for installing.

PyPI
----
Installing from PyPI is the easiest and recommended method. It will contain the most up-to-date *stable*
distribution:

.. code-block:: python

    python -m pip install ttkbootstrap

This also installs ``pillow`` as a required dependency if it is not already installed. This library is used to handle
some of the image processing used in ttkbootstrap.

.. note::
    If you are on **Linux**, you may not have a font with emojii support. To prevent the program from crashing, I recommend you also install the `Symbola` font.
    
    ``sudo apt-get install fonts-symbola``
    


Source
------
You may also install using git.

.. code-block:: python

    python -m pip install git+https://github.com/israel-dryer/ttkbootstrap

.. warning::

    While installing from Source will give you the most up-to-date features, it is also more likely
    to include developing and untested changes.
