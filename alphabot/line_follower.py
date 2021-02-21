import RPi.GPIO as GPIO
import threading
import time

class Bot:

    def __init__(self):
        self._SOUND_PIN = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._SOUND_PIN, GPIO.OUT)
        pass
    
    def start(self):
        self._waitForStartEvent()
        
        pass

    def _waitForStartEvent(self):
        pass

    def beep(self, seconds=1):
        GPIO.output(self._SOUND_PIN, GPIO.HIGH)

        def stopBeep():
            GPIO.output(self._SOUND_PIN, GPIO.LOW)
        start_time = threading.Timer(seconds, stopBeep)
        start_time.start()
        pass


bot = Bot()
bot.beep()

while True:
    time.sleep(1)
#bot.start()


