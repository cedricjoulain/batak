"""Platform dependent code"""
from sys import platform

class MyDisplay():
    """Mock 7 leds right.left displays"""
    def __init__(self, indent):
        self.indent = indent

    def print(self, str):
        print(self.indent, str)

    def fill(self, nbr):
        return
"""
        b1         b2
    0b00111111, 0b11000000,  # *
    0b00001100, 0b00111111,  # 0
    0b00000000, 0b00000110,  # 1
    0b00000000, 0b11011011,  # 2
    0b00000000, 0b10001111,  # 3
    0b00000000, 0b11100110,  # 4
"""

def convertor(b1: int, b2: int, index: int) -> Tuple[int, int]:
    bitmask = 0x0000
    extend = 0x0000
    if b2 & 0b00000001:
        bitmask |= 0x0010
    if b2 & 0b00000010:
        bitmask |= 0x0040
    if b2 & 0b00000100:
        bitmask |= 0x0020
    if b2 & 0b00001000:
        bitmask |= 0x0400
    if b2 & 0b00010000:
        bitmask |= 0x0008
    if b2 & 0b00100000:
        bitmask |= 0x4000
    if b2 & 0b01000000:
        bitmask |= 0x0200
    if b2 & 0b10000000:
        bitmask |= 0x0100

    if b1 & 0b00000001:
        bitmask |= 0x0080
    if b1 & 0b00000010:
        bitmask |= 0x2000
    if b1 & 0b00000100:
        if index == 0:
            extend |= 0x0010
        if index == 1:
            extend |= 0x0040
        if index == 2:
            extend |= 0x0020
        if index == 3:
            extend |= 0x0400
    if b1 & 0b00001000:
        bitmask |= 0x1000
    if b1 & 0b00010000:
        bitmask |= 0x0800
    if b1 & 0b00100000:
        if index == 0:
            extend |= 0x0008
        if index == 1:
            extend |= 0x4000
        if index == 2:
            extend |= 0x0200
        if index == 3:
            extend |= 0x0100

    return bitmask, extend

if platform == "darwin":
    import random
    # OS X
    #Mock GPIO
    class MyGPIO:
        def __init__(self):
            """mock const"""
            self.BCM = 1
            self.IN = 2
            self.OUT = 3
            self.PUD_UP = 4

        def setmode(self, mode):
            """mock setmode"""
            return

        def setup(self, gpio, inout, pull_up_down=None):
            """mock setup"""
            return

        def output(self, gpio, value):
            """mock output"""
            return

        def input(self, gpio):
            """mock input, pressed is False"""
            if random.randint(0, 10) == 0:
                return False
            return True

        def cleanup(self):
            """mock cleanup"""
            return

    GPIO = MyGPIO()
    def get_displays():
        return MyDisplay(""), MyDisplay("     ")

else:
    import RPi.GPIO as GPIO
    import board
<<<<<<< HEAD
    from adafruit_ht16k33.segments import Seg14x4
=======
    from adafruit_ht16k33.segments import BigSeg7x4, CHARS
    from adafruit_ht16k33.ht16k33 import HT16K33

    try:
        from typing import Dict, List, Optional, Tuple, Union

        from busio import I2C
    except ImportError:
        pass

    class Seg14x4(HT16K33):
        """Alpha-Numeric 14-segment x 4 display.

        :param I2C i2c: The I2C bus object
        :param int|list|tuple address: The I2C address(es) for the display. Can be a tuple or
            list for multiple displays.
        :param bool auto_write: True if the display should immediately change when set. If False,
            `show` must be called explicitly.
        """

        def __init__(
            self,
            i2c: I2C,
            address: Union[int, List[int], Tuple[int, ...]] = 0x70,
            auto_write: bool = True,
        ) -> None:
            super().__init__(i2c, address, auto_write)

            self._chars = 6 * len(self.i2c_device)
            self._bytes_per_char = 2
            self._last_nb_scroll_time = -1
            self._nb_scroll_text = None
            self._nb_scroll_index = -1
            self._nb_prev_char_is_dot = False

        def print(self, value: str) -> None:
            """Print the value to the display.

            :param str value: The value to print
            """

            if isinstance(value, str):
                #erase all
                self.fill(0)
                self._text(value)
            else:
                raise ValueError(f"Unsupported display value type: {type(value)}")
            if self._auto_write:
                self.show()


        def print_hex(self, value: Union[int, str]) -> None:
            """Print the value as a hexidecimal string to the display.

            :param int|str value: The number to print
            """

            if isinstance(value, int):
                self.print(f"{value:X}")
            else:
                self.print(value)

        def _put(self, char: str, index: int = 0) -> None:
            """Put a character at the specified place."""
            if not 0 <= 4:
                return
            if not 32 <= ord(char) <= 127:
                return
            character = ord(char) * 2 - 64
            bitmask, extend = convertor(CHARS[character], CHARS[1 + character], index)
            self._set_buffer(self._adjusted_index(index * 2), bitmask & 0xFF)
            self._set_buffer(self._adjusted_index(index * 2 + 1), (bitmask >> 8) & 0xFF)
            prev = self._get_buffer(self._adjusted_index(4 * 2))
            self._set_buffer(self._adjusted_index(4 * 2), (prev | extend) & 0xFF)
            prev = self._get_buffer(self._adjusted_index(4 * 2 + 1))
            self._set_buffer(self._adjusted_index(4 * 2 + 1), (prev | (extend>>8)) & 0xFF)

        def _text(self, text: str) -> None:
            """Display the specified text."""
            for index, character in enumerate(text):
                if index < 4:
                    self._put(character, index=index)

        def _adjusted_index(self, index: int) -> int:
            # Determine which part of the buffer to use and adjust index
            # this start at 1 ...
            index += 1
            offset = (index // self._bytes_per_buffer()) * self._buffer_size
            return offset + index % self._bytes_per_buffer()

        def _chars_per_buffer(self) -> int:
            return self._chars // len(self.i2c_device)

        def _bytes_per_buffer(self) -> int:
            return self._bytes_per_char * self._chars_per_buffer()

        def _char_buffer_index(self, char_pos: int) -> int:
            offset = (char_pos // self._chars_per_buffer()) * self._buffer_size
            return offset + (char_pos % self._chars_per_buffer()) * self._bytes_per_char

        def set_digit_raw(self, index: int, bitmask: Union[int, List[int], Tuple[int, int]]) -> None:
            """Set digit at position to raw bitmask value. Position should be a value
            of 0 to 3 with 0 being the left most character on the display.

            :param int index: The index of the display to set
            :param bitmask: A 2 byte number corresponding to the segments to set
            :type bitmask: int, or a list/tuple of int
            """
            if not isinstance(index, int) or not 0 <= index <= self._chars - 1:
                raise ValueError(f"Index value must be an integer in the range: 0-{self._chars - 1}")

            if isinstance(bitmask, (tuple, list)):
                bitmask = ((bitmask[0] & 0xFF) << 8) | (bitmask[1] & 0xFF)

            # Use only the valid potion of bitmask
            bitmask &= 0xFFFF

            # Set the digit bitmask value at the appropriate position.
            self._set_buffer(self._adjusted_index(index * 2), bitmask & 0xFF)
            self._set_buffer(self._adjusted_index(index * 2 + 1), (bitmask >> 8) & 0xFF)

            if self._auto_write:
                self.show()
>>>>>>> dev

    def get_displays():
        """Returns the 2 x 4 x 7 leds displays"""
        i2c = board.I2C()
        display1 = MyDisplay("") #Seg14x4(i2c, address=0x71)
        display2 = Seg14x4(i2c, address=0x71)
        display1.brightness = 0.2
        display2.brightness = 0.2
        display1.fill(0)
        display2.fill(0)
        return display1, display2
