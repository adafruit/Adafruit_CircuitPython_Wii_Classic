Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-wii-classic/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/wii_classic/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Wii_Classic/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_Wii_Classic/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for Nintendo Wii Classic controllers.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Works with the Wii Nunchuck Breakout Adapter and a Wii Classic Controller.

`Purchase one from the Adafruit shop <http://www.adafruit.com/products/4836>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/Adafruit-circuitpython-wii-classic/>`_.
To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-wii-classic

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-wii-classic

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install Adafruit-circuitpython-wii-classic

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install adafruit_wii_classic

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

	import time
	import board
	import adafruit_wii_classic

	i2c = board.STEMMA_I2C()
	ctrl_pad = adafruit_wii_classic.Wii_Classic(i2c)

	while True:
		left_x, left_y = ctrl_pad.joystick_l
		right_x, right_y = ctrl_pad.joystick_r
		left_pressure = ctrl_pad.l_shoulder.LEFT_FORCE
		right_pressure = ctrl_pad.r_shoulder.RIGHT_FORCE
		print("joystick_l = {},{}".format(left_x, left_y))
		print("joystick_r = {},{}".format(right_X, left_y))
		print("left shoulder = {}".format(left_pressure))
		print("right shoulder = {}".format(right_pressure))
		if ctrl_pad.buttons.A:
			print("button A")
		if ctrl_pad.buttons.B:
			print("button B")
		if ctrl_pad.d_pad.UP:
			print("d_pad Up")
		time.sleep(0.5)

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/wii_classic/en/latest/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_Wii_Classic/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
