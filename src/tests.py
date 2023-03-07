import logging
import time
from math import sin, cos

import numpy as np

from alphabot.bot.hardware.camera_module import CameraServo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

servo = CameraServo()

while True:
    for i in np.arange(0, 6.28, 0.1):
        servo.vertical_position(45 * sin(i))
        servo.horizontal_position(45 * cos(i))
        print(45 * sin(i))
        time.sleep(0.1)

servo.stop_servo()
