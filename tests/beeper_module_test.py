import unittest
from alphabot.beeper_module import Beeper
from tests.gpio_mock_module import GpioWrapperMock
from unittest.mock import MagicMock
from unittest.mock import call


class TestBeeper(unittest.TestCase):

    def test_gpio_initialization(self):
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        beeper = Beeper(gpio)
        gpio.setup.assert_called_with(beeper._soundPin, gpio.OUT)

    def test_beep_on(self):
        gpio = GpioWrapperMock()
        gpio.output = MagicMock()
        beeper = Beeper(gpio)
        beeper.beepOn()
        gpio.output.assert_called_with(beeper._soundPin, gpio.HIGH)
        gpio.output.assert_called_once()

    def test_beep_on_time(self):
        gpio = GpioWrapperMock()
        gpio.output = MagicMock()
        beeper = Beeper(gpio)
        beeper.beepOn(0)
        calls = [call(beeper._soundPin, gpio.HIGH), call(beeper._soundPin, gpio.LOW)]
        gpio.output.assert_has_calls(calls)

    def test_beep_off(self):
        gpio = GpioWrapperMock()
        gpio.output = MagicMock()
        beeper = Beeper(gpio)
        beeper.beepOff()
        gpio.output.assert_called_with(beeper._soundPin, gpio.LOW)
        gpio.output.assert_called_once()


if __name__ == '__main__':
    unittest.main()
