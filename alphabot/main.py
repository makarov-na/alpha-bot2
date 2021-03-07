import time
from beeper_module import Beeper
from gpio_module import GpioWrapper
from motor_module import LeftMotor, RightMotor
from ledstrip_module import LedStrip
from line_sensor_module import LineSensorsAdc

gpio = GpioWrapper()

leftMotor = LeftMotor(gpio)
rightMotor = RightMotor(gpio)
beeper = Beeper(gpio)
strip = LedStrip()
sensors_adc = LineSensorsAdc(gpio)

strip.setPixelColourRgb(0, 255, 0, 0)
strip.setPixelColourRgb(1, 0, 255, 0)
strip.setPixelColourRgb(2, 0, 0, 255)
strip.setPixelColourRgb(3, 255, 0, 255)
time.sleep(5)
strip.switchOffStrip()
time.sleep(5)

n = 0
while True:
    print(sensors_adc.readSensors())
    time.sleep(0.1)
