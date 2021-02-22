import unittest
from alphabot.beeper_module import Beeper
from tests.gpio_mock_module import GpioWrapperMock
from unittest.mock import MagicMock


class TestBeeper(unittest.TestCase):

    def test_gpio_initialization(self):
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        beeper = Beeper(gpio)
        gpio.setup.assert_called_with(beeper._soundPin, gpio.OUT)


if __name__ == '__main__':
    unittest.main()
