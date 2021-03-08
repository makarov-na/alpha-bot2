import unittest

from alphabot.hardware.line_sensor_module import LineSensorsAdc
from tests.alphabot.hardware.gpio_mock_module import GpioWrapperMock
from unittest.mock import MagicMock
from unittest.mock import call


class LineSensorsAdcTest(unittest.TestCase):

    def testInitialization(self):
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        adc = LineSensorsAdc(gpio)
        calls = [call(adc._CLOCK_PIN, gpio.OUT), call(adc._ADDRESS_PIN, gpio.OUT), call(adc._CS_PIN, gpio.OUT), call(adc._DATA_OUT_PIN, gpio.IN, gpio.PUD_UP)]
        gpio.setup.assert_has_calls(calls)

    def testReadSensors(self):
        gpio = GpioWrapperMock()
        gpio.setup = MagicMock()
        adc = LineSensorsAdc(gpio)
        values = adc.readSensors()
        self.assertTrue(len(values) == 5)


if __name__ == '__main__':
    unittest.main()
