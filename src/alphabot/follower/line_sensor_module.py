from array import array

import numpy as np

from alphabot.hardware.line_sensor_module import LineSensorsAdc


class LineSensorNormalizer:

    def __init__(self, sensors_adc: LineSensorsAdc, min_values: list = None, max_values: list = None):
        self._sensors_adc = sensors_adc
        if min_values is None:

            min_values = [311, 265, 272, 247, 270]
        if max_values is None:
            max_values = [783, 733, 861, 658, 660]
        self._min_values = min_values
        self._max_values = max_values

    def readSensors(self):
        raw_sensor_values = self._sensors_adc.readSensors()
        minimum_normalized = np.maximum(self._min_values, raw_sensor_values)
        maximum_normalized = np.minimum(self._max_values, minimum_normalized)
        return maximum_normalized.tolist()

    def getMaxValues(self):
        return self._max_values

    def getMinValues(self):
        return self._min_values
