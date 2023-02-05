import logging
import time

from alphabot.bot.bot_module import Bot
from alphabot.bot.hardware.gpio_module import GpioWrapper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
gpio = GpioWrapper()

bot = Bot(gpio)

while True:

    logger.warning("sns1 {} sns2 {}".format(bot.frontal_sensor.isObstacleInFrontOfLeftSensor(), bot.frontal_sensor.isObstacleInFrontOfRightSensor()))
    if bot.frontal_sensor.isObstacleInFrontOfRightSensor() or bot.frontal_sensor.isObstacleInFrontOfLeftSensor():
        logger.warning("obstacle")
        bot.truck.stop()
        bot.truck.setTurnPower(30)
        time.sleep(0.3)
    else:
        logger.warning("clear")
        bot.truck.setTurnPower(0)
        bot.truck.setSpeedPower(30)
    time.sleep(0.1)
