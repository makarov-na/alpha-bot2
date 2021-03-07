import time
from gpio_module import GpioWrapper


# TLC1543 ANALOG-TO-DIGITAL CONVERTER
class LineSensorsAdc:

    def __init__(self, gpio: GpioWrapper):
        self._numSensors = 5
        self._CS_PIN = 5
        self._CLOCK_PIN = 25
        self._ADDRESS_PIN = 24
        self._DATA_OUT_PIN = 23

        self._gpio = gpio
        self._gpio.setup(self._CLOCK_PIN, self._gpio.OUT)
        self._gpio.setup(self._ADDRESS_PIN, self._gpio.OUT)
        self._gpio.setup(self._CS_PIN, self._gpio.OUT)
        self._gpio.setup(self._DATA_OUT_PIN, self._gpio.IN, self._gpio.PUD_UP)

    def readSensors(self):
        sensor_values = [0] * self._numSensors
        for sensor_address in range(0, self._numSensors):
            self._setCsToLowLevel()
            prev_sensor_value = self._writeCurrentAddressAndReadPrevValue(sensor_address)
            if sensor_address == 0:
                sensor_values[self._numSensors - 1] = prev_sensor_value
            else:
                sensor_values[sensor_address - 1] = prev_sensor_value
            self._setCsToHighLevel()
        return sensor_values

    def _writeCurrentAddressAndReadPrevValue(self, sensor_address):
        prev_sensor_value = 0
        for cycle_number in range(1, 11):
            if cycle_number < 5:
                self._writeAddressBit(sensor_address, cycle_number - 1)
            prev_sensor_value = self._readDataBit(prev_sensor_value)
            self._sendCycleSignal()
        return prev_sensor_value

    def _readDataBit(self, prev_sensor_value):
        prev_sensor_value <<= 1
        if self._gpio.input(self._DATA_OUT_PIN):
            prev_sensor_value |= 0x01
        return prev_sensor_value

    def _sendCycleSignal(self):
        self._gpio.output(self._CLOCK_PIN, self._gpio.HIGH)
        self._gpio.output(self._CLOCK_PIN, self._gpio.LOW)

    def _setCsToHighLevel(self):
        time.sleep(0.0001)
        self._gpio.output(self._CS_PIN, self._gpio.HIGH)

    def _setCsToLowLevel(self):
        self._gpio.output(self._CS_PIN, self._gpio.LOW)

    def _getBitValue(self, value, bit_position):
        self
        # shift target bit to right position and reset all other bits to zero
        return (value >> (3 - bit_position)) & 0x01

    def _writeAddressBit(self, sensor_address, bit_number):
        if self._getBitValue(sensor_address, bit_number):
            self._gpio.output(self._ADDRESS_PIN, self._gpio.HIGH)
        else:
            self._gpio.output(self._ADDRESS_PIN, self._gpio.LOW)
