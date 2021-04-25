from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.pid_module import PidController
from alphabot.truck_module import Truck
import time
import logging


class LineFollower:

    def __init__(self):
        # KP = 0.285
        KP = 0.1
        KD = 0.1
        KI = 0
        TARGET_VALUE_LEFT = 350
        TARGET_VALUE_RIGHT = 300
        MAX_OUT = 100
        SPEED_POWER = 20
        SLEEP_TIME = 0.01

        self._logger = logging.getLogger(__name__)
        self._speed_power = SPEED_POWER
        self._sleep_time = SLEEP_TIME
        self._left_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_LEFT, MAX_OUT)
        self._right_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_RIGHT, MAX_OUT)
        gpio = GpioWrapper()
        self._sensors_adc = LineSensorsAdc(gpio)
        self._bot_truck = Truck(LeftMotor(gpio), RightMotor(gpio))

    def run(self):
        while True:
            values = self._sensors_adc.readSensors()
            left_sensor_value = values[1]
            right_sensor_value = values[3]
            left_sensor_pid_out = self._left_sensor_pid.getOutput(left_sensor_value)
            right_sensor_pid_out = self._right_sensor_pid.getOutput(right_sensor_value)

            if left_sensor_pid_out is None or right_sensor_pid_out is None:
                continue

            if left_sensor_pid_out < 0:
                self._bot_truck.setSpeedPower(0)  # without stops bot doe not follow line
                self._bot_truck.setTurnPower(-left_sensor_pid_out)
                continue

            if right_sensor_pid_out < 0:
                self._bot_truck.setSpeedPower(1)
                self._bot_truck.setTurnPower(right_sensor_pid_out)
                continue
            self._bot_truck.setTurnPower(0)
            self._bot_truck.setSpeedPower(self._speed_power)
            time.sleep(self._sleep_time)

    @property
    def logger(self):
        return self._logger


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    follower = LineFollower()
    follower.logger.setLevel(level=logging.INFO)
    follower.run()

