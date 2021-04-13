from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.pid_module import PidController
from alphabot.truck_module import Truck
import time
import logging


class Joystick:
    def __init__(self) -> None:
        super().__init__()

    def waitForCentralKeyPressed(self):
        pass


class LineSensor(object):
    def calibrate(self):
        pass

    def getTargetValue(self):
        return 0

    def getCurrentValue(self):
        return 0


# kp = 0.285
kp = 0.1
speed_power = 20
sleep_time = 0.01

'''
joystick = Joystick()
joystick.waitForCentralKeyPressed()

line_sensor = LineSensor()
line_sensor.calibrate()
'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

gpio = GpioWrapper()
sensors_adc = LineSensorsAdc(gpio)
leftMotor = LeftMotor(gpio)
rightMotor = RightMotor(gpio)
bot_truck = Truck(leftMotor, rightMotor)


def create_pid_for_left_sensor() -> PidController:
    ki = 0
    # kp = 0.285
    kd = 0
    target_value_left = 350
    max_out = 100
    pid = PidController(kp, ki, kd, target_value_left, max_out)
    return pid


def create_pid_for_right_sensor() -> PidController:
    ki = 0
    # kp = 0.285
    kd = 0
    target_value_left = 300
    max_out = 100
    pid = PidController(kp, ki, kd, target_value_left, max_out)
    return pid


def setTurnPowerMock(out):
    logger.info("bot_truck.setTurnPower({})".format(out))


def setSpeedPowerMock(speed_power):
    logger.info("bot_truck.setSpeedPower({})".format(speed_power))


# bot_truck.setTurnPower = setTurnPowerMock
# bot_truck.setSpeedPower = setSpeedPowerMock

left_sensor_pid = create_pid_for_left_sensor()
right_sensor_pid = create_pid_for_right_sensor()

while True:
    time.sleep(sleep_time)
    values = sensors_adc.readSensors()
    left_sensor_value = values[1]
    right_sensor_value = values[3]
    left_sensor_pid_out = left_sensor_pid.getOutput(left_sensor_value)
    right_sensor_pid_out = right_sensor_pid.getOutput(right_sensor_value)

    if left_sensor_pid_out is None or right_sensor_pid_out is None:
        continue

    if left_sensor_pid_out < 0:
        bot_truck.setSpeedPower(1)
        bot_truck.setTurnPower(-left_sensor_pid_out)
        continue

    if right_sensor_pid_out < 0:
        bot_truck.setSpeedPower(1)
        bot_truck.setTurnPower(right_sensor_pid_out)
        continue
    bot_truck.setTurnPower(0)
    bot_truck.setSpeedPower(speed_power)

# Делаем контроль по вторым датчикам
# Для левого датчика target_value = 225-316
# Для правого датчика target_value = 193-269
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

# Делаем для левого датчика целевое значение 350 при этом воздействие только вправо в обратную сторону игнорируем.
# При 350 значение выходного воздействия должно быть 0, при 700 - 100%
# Делаем для правого датчика целевое значение 300 при этом воздействие только вправо в обратную сторону игнорируем.
# При 300 значение выходного воздействия должно быть 0, при 650 - 100%
