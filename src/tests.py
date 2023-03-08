import logging
import time
from math import sin, cos

import numpy as np

from alphabot.bot.hardware.camera_module import CameraServo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

servo = CameraServo()

for j in range(1, 4, 1):
    for i in np.arange(0, 6.28, 0.01):
        servo.setVerticalPosition(45 * sin(i))
        servo.setHorizontalPosition(45 * cos(i))
        time.sleep(0.01)

servo.stop_servos()
