import time
from gpio_module import GpioWrapper

CS = 5
Clock = 25
Address = 24
DataOut = 23


class TRSensor:
    def __init__(self, gpio: GpioWrapper, numSensors=5):
        self._gpio = gpio;
        self._numSensors = 5
        self._gpio.setup(Clock, self._gpio.OUT)
        self._gpio.setup(Address, self._gpio.OUT)
        self._gpio.setup(CS, self._gpio.OUT)
        self._gpio.setup(DataOut, self._gpio.IN, self._gpio.PUD_UP)

    def AnalogRead(self):
        value = [0] * (self._numSensors + 1)
        # Read Channel0~channel6 AD value
        for j in range(0, self._numSensors + 1):
            self._gpio.output(CS, self._gpio.LOW)
            for i in range(0, 4):
                # sent 4-bit Address
                if (((j) >> (3 - i)) & 0x01):
                    self._gpio.output(Address, self._gpio.HIGH)
                else:
                    self._gpio.output(Address, self._gpio.LOW)
                # read MSB 4-bit data
                value[j] <<= 1
                if (self._gpio.input(DataOut)):
                    value[j] |= 0x01
                self._gpio.output(Clock, self._gpio.HIGH)
                self._gpio.output(Clock, self._gpio.LOW)
            for i in range(0, 6):
                # read LSB 8-bit data
                value[j] <<= 1
                if (self._gpio.input(DataOut)):
                    value[j] |= 0x01
                self._gpio.output(Clock, self._gpio.HIGH)
                self._gpio.output(Clock, self._gpio.LOW)
            # no mean ,just delay
            #			for i in range(0,6):
            #				self._gpio.output(Clock,self._gpio.HIGH)
            #				self._gpio.output(Clock,self._gpio.LOW)
            time.sleep(0.0001)
            self._gpio.output(CS, self._gpio.HIGH)
        #		print value[1:]
        return value[1:]


# Simple example prints accel/mag data once per second:
if __name__ == '__main__':
    TR = TRSensor(GpioWrapper())
    print("TRSensor Example")
    while True:
        print(TR.AnalogRead())
        time.sleep(0.2)
