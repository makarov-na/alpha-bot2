from alphabot.follower.line_sensor_module import LineSensorNormalizer, LineSensorFilter
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc, LineSensor
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.pid_module import PidController
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.truck_module import Truck
import time
import logging


class LineFollowerConfig:
    # TODO Вынести конфигурацию

    pass


class LineFollower:

    def __init__(self, configuration: LineFollowerConfig = None, gpio: GpioWrapper = None):

        # TODO Убрать эту инициализацию
        if gpio is None:
            gpio = GpioWrapper()

        KP = 0.3
        KD = 20
        KI = 0
        MAX_OUT = 40
        SPEED_POWER = 20
        SLEEP_TIME = 1 / 1_000_000 * 10
        TARGET_VALUE_LEFT = 0
        TARGET_VALUE_RIGHT = 0

        self._sensor: LineSensor = LineSensorNormalizer(LineSensorFilter(LineSensorsAdc(gpio)))
        self._prevent_time = None
        self._logger = logging.getLogger(__name__)
        self._speed_power = SPEED_POWER
        self._sleep_time = SLEEP_TIME
        self._left_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_LEFT, MAX_OUT)
        self._right_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_RIGHT, MAX_OUT)
        self._bot_truck = Truck(LeftMotor(gpio), RightMotor(gpio))
        self._telemetry = Telemetry()

    def run(self):
        while True:
            time.sleep(self._sleep_time)

            delta_time_ns = self._calculateDeltaTimeInNanos()
            if delta_time_ns is None:
                continue
            delta_time = self.to_ms(delta_time_ns)

            all_sensors_values = self._sensor.readSensors()
            left_sensor_value = all_sensors_values[1]
            right_sensor_value = all_sensors_values[3]
            left_sensor_pid_out = self._left_sensor_pid.getOutput(left_sensor_value, delta_time)
            right_sensor_pid_out = self._right_sensor_pid.getOutput(right_sensor_value, delta_time)

            if left_sensor_pid_out is None or right_sensor_pid_out is None:
                continue

            if left_sensor_pid_out < 0 and right_sensor_pid_out < 0:
                if left_sensor_pid_out < right_sensor_pid_out:
                    right_sensor_pid_out = 0
                elif right_sensor_pid_out < left_sensor_pid_out:
                    left_sensor_pid_out = 0

            if left_sensor_pid_out < 0:
                self._bot_truck.setTurnPower(-left_sensor_pid_out)
                self._sendTelemetry(all_sensors_values, delta_time)
                continue

            if right_sensor_pid_out < 0:
                self._bot_truck.setTurnPower(right_sensor_pid_out)
                self._sendTelemetry(all_sensors_values, delta_time)
                continue

            self._bot_truck.setTurnPower(0)
            self._bot_truck.setSpeedPower(self._speed_power)
            self._sendTelemetry(all_sensors_values, delta_time)

    def _sendTelemetry(self, all_sensors_values, delta_time):
        self._telemetry.send(
            {
                'flv':
                    {
                        'tm': time.time_ns(),
                        'dt': delta_time,
                        'sns': all_sensors_values,
                        'sp': self._bot_truck.getSpeedPower(),
                        'tn': self._bot_truck.getTurnPower()
                    },
                'lp': self._left_sensor_pid.getTelemetryData(),
                'rp': self._right_sensor_pid.getTelemetryData()
            }
        )

    @property
    def logger(self):
        return self._logger

    def _calculateDeltaTimeInNanos(self):
        current_time_ns = time.time_ns()
        if self._prevent_time_ns is None:
            self._prevent_time_ns = current_time_ns
            return None
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        return delta_time_ns

    def to_ms(self, time_ns):
        return time_ns / 1_000_000

    def to_mcs(self, time_ns):
        return time_ns / 1_000
