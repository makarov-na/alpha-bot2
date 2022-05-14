from queue import Queue
from typing import List

import numpy as np

from alphabot.hardware.line_sensor_module import LineSensor


class LineSensorSoft(LineSensor):

    def __init__(self, line_sensor_hard: LineSensor):
        self.black_level = range(0, 21)
        self.white_level = range(80, 101)
        self._sensor: LineSensor = LineSensorNormalizer(LineSensorFilter(line_sensor_hard))

    def readSensors(self) -> List:
        return self._sensor.readSensors()

    def isSensorOnWhite(self, value):
        return value in self.white_level

    def isSensorOnBlack(self, value):
        return value in self.black_level


class LineSensorNormalizer(LineSensor):

    def __init__(self, sensors_adc: LineSensor, min_values: list = None, max_values: list = None):
        self._sensors_adc = sensors_adc
        # TODO Реализовать автоматическое определение min/max
        if min_values is None:
            min_values = [311, 265, 272, 247, 270]
        if max_values is None:
            max_values = [783, 733, 861, 658, 660]
        self._min_values = np.array(min_values)
        self._max_values = np.array(max_values)
        self._sensor_range = (np.array(self._max_values) - np.array(self._min_values)) / 100

    def readSensors(self) -> List:
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


class AgvFilter:

    def __init__(self, size: int = 3) -> None:
        self._values_history = Queue(size)

    def filter(self, param):
        if self._values_history.full():
            self._values_history.get()
        self._values_history.put(param)
        items_count = self._values_history.qsize()
        items_sum = 0
        tmp_history = Queue()
        while not self._values_history.empty():
            item = self._values_history.get()
            tmp_history.put(item)
            items_sum = items_sum + item
        while not tmp_history.empty():
            self._values_history.put(tmp_history.get())
        return items_sum / items_count


class LineSensorFilter(LineSensor):

    def __init__(self, sensor_normalizer: LineSensor, size: int = 3) -> None:
        self._sensor_normalizer = sensor_normalizer
        self._sensor_filters = [AgvFilter(size), AgvFilter(size), AgvFilter(size), AgvFilter(size), AgvFilter(size)]

    def readSensors(self) -> List:
        sensor_values = self._sensor_normalizer.readSensors()
        filtered_values = [self._sensor_filters[i].filter(sensor_values[i]) for i in range(0, len(sensor_values))]
        return filtered_values
