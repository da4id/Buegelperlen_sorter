# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_tcs34725`
====================================================
CircuitPython module for the TCS34725 color sensor.
Ported from the
`micropython-adafruit-tcs34725 <https://github.com/adafruit/micropython-adafruit-tcs34725>`_
module by Radomir Dopieralski
See examples/tcs34725_simpletest.py for an example of the usage.
* Author(s): Tony DiCola, Carter Nelson
Implementation Notes
--------------------
**Hardware:**
* Adafruit `RGB Color Sensor with IR filter and White LED - TCS34725
  <https://www.adafruit.com/product/1334>`_ (Product ID: 1334)
* Flora `Color Sensor with White Illumination LED - TCS34725
  <https://www.adafruit.com/product/1356>`_ (Product ID: 1356)
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
import time

import ustruct
from machine import I2C

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_TCS34725.git"

# Register and command constants:
_COMMAND_BIT = 0x80
_REGISTER_ENABLE = 0x00
_REGISTER_ATIME = 0x01
_REGISTER_WTIME = 0x03
_REGISTER_AILT = 0x04
_REGISTER_AIHT = 0x06
_REGISTER_ID = 0x12
_REGISTER_APERS = 0x0C
_REGISTER_CONFIG = 0x0D
_REGISTER_CONTROL = 0x0F
_REGISTER_SENSORID = 0x12
_REGISTER_STATUS = 0x13
_REGISTER_CDATA = 0x14
_REGISTER_RDATA = 0x16
_REGISTER_GDATA = 0x18
_REGISTER_BDATA = 0x1A
_ENABLE_AIEN = 0x10
_ENABLE_WEN = 0x08
_ENABLE_AEN = 0x02
_ENABLE_PON = 0x01
_GAINS = (1, 4, 16, 60)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
_INTEGRATION_TIME_THRESHOLD_LOW = 2.4
_INTEGRATION_TIME_THRESHOLD_HIGH = 614.4


class TCS34725:
    """Driver for the TCS34725 color sensor.
    :param ~busio.I2C i2c: The I2C bus the device is connected to
    :param int address: The I2C device address. Defaults to :const:`0x29`
    **Quickstart: Importing and using the device**
        Here is an example of using the :class:`TCS34725`.
        First you will need to import the libraries to use the sensor
        .. code-block:: python
            import board
            import adafruit_tcs34725
        Once this is done you can define your `board.I2C` object and define your sensor object
        .. code-block:: python
            i2c = board.I2C()  # uses board.SCL and board.SDA
            sensor = adafruit_tcs34725.TCS34725(i2c)
        Now you have access to the :attr:`color_temperature`, :attr:`lux` attributes
        .. code-block:: python
            temp = sensor.color_temperature
            lux = sensor.lux
    """

    # Class-level buffer for reading and writing data with the sensor.
    # This reduces memory allocations but means the code is not re-entrant or
    # thread safe!
    _BUFFER = bytearray(3)

    def __init__(self, i2c: I2C, address: int = 0x29):
        self._bus = i2c
        self._i2c_address = address

        self.glass_attenuation = 1.0

        self._write_u8(_REGISTER_CONFIG, 2)
        # Check sensor ID is expectd value.
        sensor_id = self._read_u8(_REGISTER_SENSORID)
        if sensor_id not in (0x44, 0x10):
            raise RuntimeError("Could not find sensor, check wiring!")

    def _writeCommandRegister(self, integrationtime: int, clearInterrupt: bool):
        if not 0 <= integrationtime <= 3:
            raise RuntimeError("Integration Time outside Range")
        value = 0
        if clearInterrupt:
            value = 6

        self.writeI2CRegister(_COMMAND_BIT | (integrationtime << 5) | value)

    def _writeEnableRegister(self, rgbcInterruptEnable: bool, waitEnable: bool, rbgcEnable: bool, powerOn: bool):
        self._write_u8(_REGISTER_ENABLE, (rgbcInterruptEnable << 4) | (waitEnable << 3) | (rbgcEnable << 1) | powerOn)

    def _writeRGBCTimingRegister(self, timeMs: float):
        if (
                not _INTEGRATION_TIME_THRESHOLD_LOW
                    <= timeMs
                    <= _INTEGRATION_TIME_THRESHOLD_HIGH
        ):
            raise ValueError(
                "Integration Time must be between '{0}' and '{1}'".format(
                    _INTEGRATION_TIME_THRESHOLD_LOW, _INTEGRATION_TIME_THRESHOLD_HIGH
                )
            )
        cycles = int(timeMs / 2.4)
        print("_writeRGBCTimingRegister: ", 256 - cycles)
        self._write_u8(_REGISTER_ATIME, 256 - cycles)

    def _writeWaitTimeRegister(self, timeMs: int):
        if (
                not _INTEGRATION_TIME_THRESHOLD_LOW
                    <= timeMs
                    <= _INTEGRATION_TIME_THRESHOLD_HIGH
        ):
            raise ValueError(
                "Integration Time must be between '{0}' and '{1}'".format(
                    _INTEGRATION_TIME_THRESHOLD_LOW, _INTEGRATION_TIME_THRESHOLD_HIGH
                )
            )
        cycles = int(timeMs / 2.4)
        print("_writeRGBCTimingRegister: ", 256 - cycles)
        self._write_u8(_REGISTER_WTIME, 256 - cycles)

    def _writeInterruptThresholdRegisters(self, clearLow, clearHigh):
        self._write_u16(_REGISTER_AILT, clearLow)
        self._write_u16(_REGISTER_AIHT, clearHigh)

    def _writePersistenceRegister(self, cycles: int):
        if cycles not in _CYCLES:
            raise ValueError("Cycles not valid")
        value = _CYCLES.index(cycles)
        self._write_u8(_REGISTER_APERS, value)

    def _writeConfigurationRegister(self, waitLong: bool):
        self._write_u8(_REGISTER_CONFIG, waitLong << 1)

    def _writeControlRegister(self, gain):
        if gain not in _GAINS:
            raise ValueError("Gain not valid")
        self._write_u8(_REGISTER_CONTROL, _GAINS.index(gain))

    def _readStatusRegister(self):
        val = self._read_u8(_REGISTER_STATUS)
        aint = (val & 0x10) >> 16
        avalid = (val & 0x01)
        if aint > 0:
            aint = True
        else:
            aint = False
        if avalid > 0:
            avalid = True
        else:
            avalid = False
        return aint, avalid

    def _readColorRaw(self):
        data = tuple(
            self._read_u16(reg)
            for reg in (
                _REGISTER_RDATA,
                _REGISTER_GDATA,
                _REGISTER_BDATA,
                _REGISTER_CDATA,
            )
        )
        return data

    def lux(self):
        """The lux value computed from the color channels."""
        return self._temperature_and_lux_dn40()[0]

    def color_temperature(self):
        """The color temperature in degrees Kelvin."""
        return self._temperature_and_lux_dn40()[1]

    def color_rgb_bytes(self):
        """Read the RGB color detected by the sensor.  Returns a 3-tuple of
        red, green, blue component values as bytes (0-255).
        """
        r, g, b, clear = self.color_raw()

        # Avoid divide by zero errors ... if clear = 0 return black
        if clear == 0:
            return 0, 0, 0

        # Each color value is normalized to clear, to obtain int values between 0 and 255.
        # A gamma correction of 2.5 is applied to each value as well, first dividing by 255,
        # since gamma is applied to values between 0 and 1
        red = int(pow((int((r / clear) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g / clear) * 256) / 255), 2.5) * 255)
        blue = int(pow((int((b / clear) * 256) / 255), 2.5) * 255)

        # Handle possible 8-bit overflow
        red = min(red, 255)
        green = min(green, 255)
        blue = min(blue, 255)
        return red, green, blue

    def color(self):
        """Read the RGB color detected by the sensor. Returns an int with 8 bits per channel.
        Examples: Red = 16711680 (0xff0000), Green = 65280 (0x00ff00),
        Blue = 255 (0x0000ff), SlateGray = 7372944 (0x708090)
        """
        r, g, b = self.color_rgb_bytes()
        return (r << 16) | (g << 8) | b

    def color_raw(self):
        """Read the raw RGBC color detected by the sensor.  Returns a 4-tuple of
        16-bit red, green, blue, clear component byte values (0-65535).
        """
        pass

    def _temperature_and_lux_dn40(self) -> tuple[float, float]:
        """Converts the raw R/G/B values to color temperature in degrees
        Kelvin using the algorithm described in DN40 from Taos (now AMS).
        Also computes lux. Returns tuple with both values or tuple of Nones
        if computation can not be done.
        """
        # pylint: disable=invalid-name, too-many-locals

        # Initial input values
        ATIME = self._read_u8(_REGISTER_ATIME)
        ATIME_ms = (256 - ATIME) * 2.4
        AGAINx = self.gain
        R, G, B, C = self.color_raw

        # Device specific values (DN40 Table 1 in Appendix I)
        GA = self.glass_attenuation  # Glass Attenuation Factor
        DF = 310.0  # Device Factor
        R_Coef = 0.136  # |
        G_Coef = 1.0  # | used in lux computation
        B_Coef = -0.444  # |
        CT_Coef = 3810  # Color Temperature Coefficient
        CT_Offset = 1391  # Color Temperatuer Offset

        # Analog/Digital saturation (DN40 3.5)
        SATURATION = 65535 if 256 - ATIME > 63 else 1024 * (256 - ATIME)

        # Ripple saturation (DN40 3.7)
        if ATIME_ms < 150:
            SATURATION -= SATURATION / 4

        # Check for saturation and mark the sample as invalid if true
        if C >= SATURATION:
            return None, None

        # IR Rejection (DN40 3.1)
        IR = (R + G + B - C) / 2 if R + G + B > C else 0.0
        R2 = R - IR
        G2 = G - IR
        B2 = B - IR

        # Lux Calculation (DN40 3.2)
        G1 = R_Coef * R2 + G_Coef * G2 + B_Coef * B2
        CPL = (ATIME_ms * AGAINx) / (GA * DF)
        CPL = 0.001 if CPL == 0 else CPL
        lux = G1 / CPL

        # CT Calculations (DN40 3.4)
        R2 = 0.001 if R2 == 0 else R2
        CT = CT_Coef * B2 / R2 + CT_Offset

        return lux, CT

    def getGlass_attenuation(self):
        """The Glass Attenuation (FA) factor used to compensate for lower light
        levels at the device due to the possible presence of glass. The GA is
        the inverse of the glass transmissivity (T), so :math:`GA = 1/T`. A transmissivity
        of 50% gives GA = 1 / 0.50 = 2. If no glass is present, use GA = 1.
        See Application Note: DN40-Rev 1.0 – Lux and CCT Calculations using
        ams Color Sensors for more details.
        """
        return self.glass_attenuation

    def setGlass_attenuation(self, value: float):
        if value < 1:
            raise ValueError("Glass attenuation factor must be at least 1.")
        self.glass_attenuation = value

    def _read_u8(self, address: int) -> int:
        # Read an 8-bit unsigned value from the specified 8-bit address.
        reg = (address | _COMMAND_BIT) & 0xFF
        self.writeI2CRegister(reg)
        time.sleep_ms(1)
        buf = self._bus.readfrom(self._i2c_address, 1)
        return ustruct.unpack("<B", buf)[0]

    def _read_u16(self, address: int) -> int:
        # Read a 16-bit unsigned value from the specified 8-bit address.
        reg = (address | _COMMAND_BIT) & 0xFF
        self.writeI2CRegister(reg)
        time.sleep_ms(1)
        buf = self._bus.readfrom(self._i2c_address, 2)
        r = ustruct.unpack("<H", buf)[0]
        return r

    def _write_u8(self, address: int, val: int):
        # Write an 8-bit unsigned value to the specified 8-bit address.

        buf = bytearray(2)
        buf[0] = address | _COMMAND_BIT
        buf[1] = val

        self._bus.writeto(self._i2c_address, buf)

    def _write_u16(self, address: int, val: int):
        # Write a 16-bit unsigned value to the specified 8-bit address.
        buf = ustruct.pack("<BH", address | _COMMAND_BIT, val)
        self._bus.writeto(self._i2c_address, buf)

    def writeI2CRegister(self, reg):
        buf = bytearray(1)
        buf[0] = reg
        self._bus.writeto(self._i2c_address, buf)