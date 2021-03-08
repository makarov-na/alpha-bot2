import time
from alphabot.hardware.beeper_module import Beeper
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.hardware.ledstrip_module import LedStrip
from alphabot.hardware.line_sensor_module import LineSensorsAdc

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

n = 0
while True:
    print(sensors_adc.readSensors())
    time.sleep(0.1)
