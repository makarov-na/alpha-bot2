import unittest
from unittest.mock import MagicMock, Mock

from alphabot.bot.line_sensor_module import LineSensorNormalizer, AgvFilter, LineSensorAvgFilter
from alphabot.bot.hardware.line_sensor_module import LineSensor


class TestLineSensorFilter(unittest.TestCase):

    def test_sensors_filtered(self):
        # GIVEN
        test_values = [200, 100, 200, 122, 333]
        line_sensor = MagicMock()
        line_sensor.readSensors = Mock()
        line_sensor.readSensors.side_effect = [[400, 200, 400, 244, 666], [0, 0, 0, 0, 0]]
        line_sensor_filter: LineSensor = LineSensorAvgFilter(line_sensor, 3)

        # WHEN
        line_sensor_filter.readSensors()
        sensor_values = line_sensor_filter.readSensors()

        # THEN
        self.assertEqual(test_values, sensor_values)


class TestAvgFilter(unittest.TestCase):

    def test_filter(self):
        # GIVEN

        test_values = [3, 3, 96, 0, 0, 6]
        avg_filter = AgvFilter(3)

        # WHEN
        filtered_values = list(map(avg_filter.filter, test_values))

        # THEN
        self.assertEqual(3, filtered_values[0])
        self.assertEqual(3, filtered_values[1])
        self.assertEqual(34, filtered_values[2])
        self.assertEqual(33, filtered_values[3])
        self.assertEqual(32, filtered_values[4])
        self.assertEqual(2, filtered_values[5])


class TestLineSensorNormalizer(unittest.TestCase):

    def test_output_calibrated(self):
        # GIVEN
        min_values = [311, 265, 272, 247, 270]
        max_values = [783, 733, 861, 658, 660]

        def readSensorsMock():
            return [400, 200, 400, 244, 666]

        line_sensor = MagicMock()
        line_sensor.readSensors = readSensorsMock
        line_sensor_normalizer = LineSensorNormalizer(line_sensor, min_values, max_values)

        # WHEN
        sensor_values = line_sensor_normalizer.readSensors()

        # THEN
        self.assertIsNotNone(sensor_values)
        self.assertTrue(len(sensor_values) == 5)
        self.assertTrue(0 < sensor_values[0] < 100, 'Value ' + str(sensor_values[0]))
        self.assertTrue(sensor_values[1] == 0, 'Value ' + str(sensor_values[0]))
        self.assertTrue(0 < sensor_values[2] < 100, 'Value ' + str(sensor_values[0]))
        self.assertTrue(sensor_values[3] == 0, 'Value ' + str(sensor_values[0]))
        self.assertTrue(sensor_values[4] == 100, 'Value ' + str(sensor_values[0]))

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
        max_values = line_sensor_normalizer.getMaxValues().tolist()
        min_values = line_sensor_normalizer.getMinValues().tolist()

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
        max_values = line_sensor_normalizer.getMaxValues().tolist()
        min_values = line_sensor_normalizer.getMinValues().tolist()
        values = line_sensor_normalizer.readSensors()

        # THEN
        self.assertEqual(max_values_expected, max_values)
        self.assertEqual(min_values_expected, min_values)
        self.assertTrue(len(values) == 5)
