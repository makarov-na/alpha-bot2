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

    def test_left_sensor_state_true(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        gpio.input = MagicMock()
        gpio.input.return_value = 1
        sensor = FrontalInfraredSensor(gpio)

        # WHEN
        left_sensor = sensor.isObstacleInFrontOfLeftSensor()

        # THEN
        self.assertTrue(left_sensor)
        gpio.input.assert_called_with(sensor._leftSensorPin)

    def test_left_sensor_state_false(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        gpio.input = MagicMock()
        gpio.input.return_value = 0
        sensor = FrontalInfraredSensor(gpio)

        # WHEN
        left_sensor = sensor.isObstacleInFrontOfLeftSensor()

        # THEN
        self.assertFalse(left_sensor)
        gpio.input.assert_called_with(sensor._leftSensorPin)

    def test_right_sensor_state_true(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        gpio.input = MagicMock()
        gpio.input.return_value = 1
        sensor = FrontalInfraredSensor(gpio)

        # WHEN
        right_sensor = sensor.isObstacleInFrontOfRightSensor()

        # THEN
        self.assertTrue(right_sensor)
        gpio.input.assert_called_with(sensor._rightSensorPin)

    def test_right_sensor_state_false(self):
        # GIVEN
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        gpio.input = MagicMock()
        gpio.input.return_value = 0
        sensor = FrontalInfraredSensor(gpio)

        # WHEN
        right_sensor = sensor.isObstacleInFrontOfRightSensor()

        # THEN
        self.assertFalse(right_sensor)
        gpio.input.assert_called_with(sensor._rightSensorPin)
