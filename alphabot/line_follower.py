import time
from beeper_module import Beeper
from gpio_module import GpioWrapper
from motor_module import LeftMotor, RightMotor
from ledstrip_module import LedStrip

leftMotor = LeftMotor(GpioWrapper())
rightMotor = RightMotor(GpioWrapper())
beeper = Beeper(GpioWrapper())
strip = LedStrip()

strip.setPixelColourRgb(0, 255, 0, 0)
strip.setPixelColourRgb(1, 0, 255, 0)
strip.setPixelColourRgb(2, 0, 0, 255)
strip.setPixelColourRgb(3, 255, 0, 255)
time.sleep(5)
strip.switchOffStrip()
time.sleep(5)

n = 0
while True:
    strip.setPixelColourRgb(n, 255, 0, 0)
    time.sleep(1)
    strip.switchOffPixel(n)
    n += 1
    if n > 3:
        n = 0
