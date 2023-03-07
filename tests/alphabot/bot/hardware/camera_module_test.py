import unittest
from unittest.mock import MagicMock

from alphabot.bot.hardware.camera_module import CameraServo


class MyTestCase(unittest.TestCase):

    def test_left_turn_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        servo.horizontal_position(-45)

        # THEN

    def test_right_turn_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        servo.horizontal_position(45)

        # THEN

    def test_up_more_than_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        with self.assertRaises(AssertionError) as error:
            servo.vertical_position(-46)

        # THEN
        self.assertEqual("Vertical position must be between -45 and 45", str(error.exception))

    def test_down_more_than_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        with self.assertRaises(AssertionError) as error:
            servo.vertical_position(46)

        # THEN
        self.assertEqual("Vertical position must be between -45 and 45", str(error.exception))

    def test_left_turn_more_than_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        with self.assertRaises(AssertionError) as error:
            servo.horizontal_position(-91)

        # THEN
        self.assertEqual("Horizontal position must be between -45 and 45", str(error.exception))

    def test_right_turn_more_than_45(self):
        # GIVEN
        servo = CameraServo(MagicMock())

        # WHEN
        with self.assertRaises(AssertionError) as error:
            servo.horizontal_position(91)

        # THEN
        self.assertEqual("Horizontal position must be between -45 and 45", str(error.exception))


if __name__ == '__main__':
    unittest.main()
