import logging
import time

from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.telemetry.telemetry_module import Telemetry

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


sensors_adc = LineSensorsAdc(GpioWrapper())
telemetry = Telemetry()
prevent_time = None
current_time_before_all = time.time_ns()
for i in range(0, 1_001):
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
    time.sleep(0.01)
current_time_after_all = time.time_ns()
delta_time_all_test_ms = (current_time_after_all - current_time_before_all) / 1_000_000

logger.info("avg time: " + str(delta_time_all_test_ms / 1_000))
