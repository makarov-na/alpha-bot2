import numpy as np

from alphabot.hardware.line_sensor_module import LineSensorsAdc


class LineSensorNormalizer:

    def __init__(self, sensors_adc: LineSensorsAdc, min_values: list = None, max_values: list = None):
        self._sensors_adc = sensors_adc
        #TODO Реализовать автоматическое определение min/max
        if min_values is None:
            min_values = [311, 265, 272, 247, 270]
        if max_values is None:
            max_values = [783, 733, 861, 658, 660]
        self._min_values = np.array(min_values)
        self._max_values = np.array(max_values)
        self._sensor_range = (np.array(self._max_values) - np.array(self._min_values)) / 100

    def readSensors(self):
        raw_sensor_values = self._sensors_adc.readSensors()
        min_normalized = self._cut_bottom_values(raw_sensor_values)
        min_max_normalized = self._cut_top_values(min_normalized)
        value_normalized = np.rint((min_max_normalized - self._min_values) / self._sensor_range).astype(int)
        return value_normalized.tolist()

    def _cut_top_values(self, min_normalized):
        return np.minimum(self._max_values, min_normalized)

    def _cut_bottom_values(self, raw_sensor_values):
        return np.maximum(self._min_values, raw_sensor_values)

    def getMaxValues(self):
        return self._max_values

    def getMinValues(self):
        return self._min_values
