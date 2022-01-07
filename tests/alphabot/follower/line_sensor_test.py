import unittest
from unittest.mock import MagicMock

from alphabot.follower.line_sensor_module import LineSensorNormalizer
from tests.alphabot.hardware.gpio_mock_module import GpioWrapperMock


class TestLineSensorNormalizer(unittest.TestCase):

    def test_output_in_max_min_range(self):
        # GIVEN
        min_values = [311, 265, 272, 247, 270]
        max_values = [783, 733, 861, 658, 660]

        def readSensorsMock():
            return [785, 200, 300, 244, 666]

        line_sensor = MagicMock()
        line_sensor.readSensors = readSensorsMock

        line_sensor_normalizer = LineSensorNormalizer(line_sensor, min_values, max_values)

        # WHEN
        sensor_values = line_sensor_normalizer.readSensors()

        # THEN
        self.assertIsNotNone(sensor_values)
        self.assertTrue(len(sensor_values) == 5)
        self.assertEqual([783, 265, 300, 247, 660], sensor_values)

    def test_configuration(self):
        # GIVEN
        min_values_expected = [311, 265, 272, 247, 270]
        max_values_expected = [783, 733, 861, 658, 660]

        def readSensorsMock():
            return [785, 200, 300, 244, 666]

        line_sensor = MagicMock()
        line_sensor.readSensors = readSensorsMock
        line_sensor_normalizer = LineSensorNormalizer(line_sensor, min_values_expected, max_values_expected)

        # WHEN
        max_values = line_sensor_normalizer.getMaxValues()
        min_values = line_sensor_normalizer.getMinValues()

        # THEN
        self.assertEqual(max_values_expected, max_values)
        self.assertEqual(min_values_expected, min_values)

    def test_create_with_defaults(self):

        # GIVEN
        min_values_expected = [311, 265, 272, 247, 270]
        max_values_expected = [783, 733, 861, 658, 660]

        def readSensorsMock():
            return [785, 200, 300, 244, 666]

        line_sensor = MagicMock()
        line_sensor.readSensors = readSensorsMock

        line_sensor_normalizer = LineSensorNormalizer(line_sensor)

        # WHEN
        max_values = line_sensor_normalizer.getMaxValues()
        min_values = line_sensor_normalizer.getMinValues()
        values = line_sensor_normalizer.readSensors()

        # THEN
        self.assertEqual(max_values_expected, max_values)
        self.assertEqual(min_values_expected, min_values)
        self.assertTrue(len(values) == 5)
