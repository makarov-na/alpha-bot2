import time
#from alphabot.beeper_module import Beeper
from beeper_module import Beeper

class Bot:

    def __init__(self):
        pass

    def start(self):
        self._waitForStartEvent()

    def _waitForStartEvent(self):
        pass


beeper = Beeper()
beeper.beepOn(1)

while True:
    time.sleep(1)
# bot.start()
