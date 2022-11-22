import asyncio
import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.line_follower_module import LineFollower


class TestLineFollower(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    #def test_start_following_loop_and_exit_from_loop(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.stop = MagicMock()
        line_follower._sleepAndMeasureTime = MagicMock()
        line_follower._sleepAndMeasureTime.return_value = 11
        line_follower._sensor.readSensors = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._sensor.readSensors.return_value = [1, 2, 3, 4, 5]
        loop = asyncio.get_event_loop()

        async def startFollowing():
            await loop.run_in_executor(None, line_follower.startFollowing)

        async def stopFollowing():
            while True:
                if line_follower._keep_following is True:
                    line_follower._keep_following = False
                    return
                await asyncio.sleep(0)

        # WHEN
        loop.run_until_complete(asyncio.gather(startFollowing(), stopFollowing()))

        # THEN
        line_follower._bot_truck.stop.assert_called()
        line_follower._sensor.readSensors.assert_called()
        line_follower._sleepAndMeasureTime.assert_called()
        line_follower._sendTelemetry.assert_called()


