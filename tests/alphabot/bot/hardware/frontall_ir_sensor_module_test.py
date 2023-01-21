import unittest
from alphabot.bot.hardware.frontal_infrared_sensor_module import FrontalInfraredSensor
from tests.alphabot.bot.hardware.gpio_mock_module import GpioWrapperMock
from unittest.mock import MagicMock
from unittest.mock import call


class TestInfraredSensor(unittest.TestCase):

    def test_gpio_initialization(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()

        # WHEN
        sensor = FrontalInfraredSensor(gpio)

        # THEN
        gpio.setup.assert_has_calls([call(sensor._leftSensorPin, gpio.IN, gpio.PUD_UP), call(sensor._rightSensorPin, gpio.IN, gpio.PUD_UP)])

    def test_sensors_(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()

        # WHEN
        sensor = FrontalInfraredSensor(gpio)

        # THEN
        gpio.setup.assert_has_calls([call(sensor._leftSensorPin, gpio.IN, gpio.PUD_UP), call(sensor._rightSensorPin, gpio.IN, gpio.PUD_UP)])
