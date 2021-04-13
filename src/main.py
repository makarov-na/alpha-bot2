import time
from alphabot.hardware.beeper_module import Beeper
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.hardware.ledstrip_module import LedStrip
from alphabot.hardware.line_sensor_module import LineSensorsAdc
import numpy as np

gpio = GpioWrapper()

leftMotor = LeftMotor(gpio)
rightMotor = RightMotor(gpio)
beeper = Beeper(gpio)
strip = LedStrip()
sensors_adc = LineSensorsAdc(gpio)

# strip.setPixelColourRgb(0, 255, 0, 0)
# strip.setPixelColourRgb(1, 0, 255, 0)
# strip.setPixelColourRgb(2, 0, 0, 255)
# strip.setPixelColourRgb(3, 255, 0, 255)

n = 0
min_val = None
max_val = None

while True:
    curr_val = sensors_adc.readSensors()
    if min_val is None:
        min_val = curr_val
    if max_val is None:
        max_val = curr_val
    min_val = np.minimum(curr_val, min_val)
    max_val = np.maximum(curr_val, max_val)
    print(curr_val, min_val, max_val)
    time.sleep(0.1)

# White [840 771 877 672 704]
#       [695 648 699 572 606]
#       [889 796 891 690 759]
# Black - 200-320
#       [303 278 279 252 292]
#       [238 225 220 193 206]
#       [342 316 307 269 301]
# Middle on the border
#       [281 252 572 652 682]
#       [244 239 380 623 649]
#       [358 323 672 684 719]
# Tree middle on the black