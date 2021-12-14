import logging
import time

from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.truck_module import Truck


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
gpio = GpioWrapper()
sensors_adc = LineSensorsAdc(GpioWrapper())
telemetry = Telemetry()
prevent_time = None
current_time_before_all = time.time_ns()



speed_power = 25
truck = Truck(LeftMotor(gpio), RightMotor(gpio))
truck.setSpeedPower(speed_power)
for i in range(0, 5000):
    all_sensors_values = sensors_adc.readSensors()
    current_time = time.time_ns()
    if prevent_time is None:
        prevent_time = current_time
        continue
    delta_time_ms = (current_time - prevent_time) / 1_000_000
    prevent_time = current_time
    telemetry_item = {'dt': delta_time_ms, 'sns': all_sensors_values}
    telemetry.send(telemetry_item)
    logging.info(telemetry_item)
    time.sleep(0.001)
truck.setTurnPower(0)


