Part 0 - Setting up
=======================

Create a separate anaconda environment (optional step)
--------------------------------------------------------------------


.. code::

    conda create -n sdl python=3.8 anaconda

When conda asks for you to proceed, type ``y``:

.. code::    

    proceed ([y]/n)?

Switch to our ``sdl`` environment:

.. code::    

    conda activate sdl

Install pysdl2
------------------

Install the python library

.. code::

    pip install -U pysdl2

Install the C library that pysdl2 is dependent on. According to the documentation of pysdl2 it works on Windows and MacOS, but not on Linux. 

.. code::

    pip install pysdl2-dll

or (if on Linux) download the SDL2 from the SDL2 download page `http://www.libsdl.org/` and follow the installation instructions from `https://pysdl2.readthedocs.io/en/latest/install.html`


Try to execute the following code in Python 

>>> import sdl2.ext
UserWarning: Using SDL2 binaries from pysdl2-dll 2.0.10

If there is no error then the library was successfully installed.

For the reference the version of sdl2 used in this tutorial:

>>> import sdl2
>>> sdl2.__version__
'0.9.7'