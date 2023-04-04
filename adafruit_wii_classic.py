# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_wii_classic`
================================================================================

CircuitPython library for Nintendo Wii Classic controllers.


* Author(s): Liz Clark

Implementation Notes
--------------------

**Hardware:**

* `Wii Classic Controller <https://en.wikipedia.org/wiki/Classic_Controller>`_
* `Adafruit Wii Nunchuck Breakout Adapter <https://www.adafruit.com/product/4836>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time
from collections import namedtuple
from adafruit_bus_device.i2c_device import I2CDevice

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Wii_Classic.git"

_I2C_INIT_DELAY = 0.1


class Wii_Classic:
    """Class which provides interface to Nintendo Wii Classic controller.

    :param ~I2C i2c: The `busio.I2C` object to use.
    :param int address: (Optional) The I2C address of the device. Default is 0x52.
    :param float i2c_read_delay: (Optional) The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    """

    _Values = namedtuple(
        "Values",
        ("joystick_l", "joystick_r", "l_shoulder", "r_shoulder", "d_pad", "buttons"),
    )
    _Joystick_L = namedtuple("Joystick_L", ("LEFT_X", "LEFT_Y"))
    _Joystick_R = namedtuple("Joystick_R", ("RIGHT_X", "RIGHT_Y"))
    _L_Shoulder_Analog = namedtuple("L_Shoulder_Analog", ("LEFT_FORCE"))
    _R_Shoulder_Analog = namedtuple("R_Shoulder_Analog", ("RIGHT_FORCE"))
    _D_Pad = namedtuple("D_Pad", ("UP", "DOWN", "LEFT", "RIGHT"))
    _Buttons = namedtuple(
        "Buttons", ("A", "B", "START", "SELECT", "X", "Y", "HOME", "ZL", "ZR", "L", "R")
    )

    def __init__(
        self, i2c: I2C, address: int = 0x52, i2c_read_delay: float = 0.002
    ) -> None:
        print("Connecting to controller...")
        for i in range(10):
            try:
                self.buffer = bytearray(8)
                self.i2c_device = I2CDevice(i2c, address)
            except ValueError:
                # boot up delay for NES/SNES Classic Controllers
                time.sleep(1)
                if i < 10:
                    continue
                raise
            break
        print("Found controller!")
        self._i2c_read_delay = i2c_read_delay
        time.sleep(_I2C_INIT_DELAY)
        with self.i2c_device as i2c_dev:
            # turn off encrypted data
            # http://wiibrew.org/wiki/Wiimote/Extension_Controllers
            i2c_dev.write(b"\xF0\x55")
            time.sleep(_I2C_INIT_DELAY)
            i2c_dev.write(b"\xFB\x00")

    @property
    def values(self) -> _Values:
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joystick_l(do_read=False),
            self._joystick_r(do_read=False),
            self._l_shoulder(do_read=False),
            self._r_shoulder(do_read=False),
            self._d_pad(do_read=False),
            self._buttons(do_read=False),
        )

    @property
    def joystick_l(self) -> _Joystick_L:
        """The current left joystick position."""
        return self._joystick_l()

    @property
    def joystick_r(self) -> _Joystick_R:
        """The current right joystick position."""
        return self._joystick_r()

    @property
    def l_shoulder(self) -> _L_Shoulder_Analog:
        """The current left shoulder button pressure."""
        return self._l_shoulder()

    @property
    def r_shoulder(self) -> _R_Shoulder_Analog:
        """The current right shoulder button pressure."""
        return self._r_shoulder()

    @property
    def buttons(self) -> _Buttons:  # pylint: disable=invalid-name
        """The current pressed state of buttons"""
        return self._buttons()

    @property
    def d_pad(self) -> _D_Pad:
        """The current pressed state of d-pad buttons"""
        return self._d_pad()

    def _joystick_l(self, do_read: bool = True) -> _Joystick_L:
        if do_read:
            self._read_data()
        return self._Joystick_L((self.buffer[0] & 0x3F), (self.buffer[1] & 0x3F))

    def _joystick_r(self, do_read: bool = True) -> _Joystick_R:
        if do_read:
            self._read_data()
        return self._Joystick_R(
            ((self.buffer[0] & 0xC0) >> 3)
            | ((self.buffer[1] & 0xC0) >> 5)
            | ((self.buffer[2] & 0x40) >> 7),
            (self.buffer[2] & 0x1F),
        )

    def _l_shoulder(self, do_read: bool = True) -> _L_Shoulder_Analog:
        if do_read:
            self._read_data()
        return self._L_Shoulder_Analog(
            ((self.buffer[2] & 0x60) >> 2) | ((self.buffer[3] & 0xE0) >> 5)
        )

    def _r_shoulder(self, do_read: bool = True) -> _R_Shoulder_Analog:
        if do_read:
            self._read_data()
        return self._R_Shoulder_Analog(self.buffer[3] & 0x1C)

    def _joystick_l(self, do_read: bool = True) -> _Joystick_L:
        if do_read:
            self._read_data()
        return self._Joystick_L((self.buffer[0] & 0x3F), (self.buffer[1] & 0x3F))

    def _buttons(self, do_read: bool = True) -> _Buttons:
        if do_read:
            self._read_data()
        return self._Buttons(
            not bool(self.buffer[5] & 0x10),  # A
            not bool(self.buffer[5] & 0x40),  # B
            not bool(self.buffer[4] & 0x04),  # Start
            not bool(self.buffer[4] & 0x10),  # Select
            not bool(self.buffer[5] & 0x08),  # X
            not bool(self.buffer[5] & 0x20),  # Y
            not bool(self.buffer[4] & 0x08),  # Home
            not bool(self.buffer[5] & 0x80),  # ZL
            not bool(self.buffer[5] & 0x04),  # ZR
            not bool(self.buffer[4] & 0x20),  # L
            not bool(self.buffer[4] & 0x02),  # R
        )

    def _d_pad(self, do_read: bool = True) -> _D_Pad:
        if do_read:
            self._read_data()
        return self._D_Pad(
            not bool(self.buffer[5] & 0x01),  # Up
            not bool(self.buffer[4] & 0x40),  # Down
            not bool(self.buffer[5] & 0x02),  # Left
            not bool(self.buffer[4] & 0x80),  # Right
        )

    def _read_data(self) -> bytearray:
        return self._read_register(b"\x00")

    def _read_register(self, address) -> bytearray:
        with self.i2c_device as i2c:
            i2c.write(address)
            time.sleep(self._i2c_read_delay)  # at least 200us
            i2c.readinto(self.buffer)
        return self.buffer
