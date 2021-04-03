import unittest
from unittest.mock import MagicMock

from alphabot.truck_module import Truck


class TestTruck(unittest.TestCase):

    def test_speed_power_positive_set(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 10

        # WHEN
        truck.setSpeedPower(power_value)

        # THEN
        left_motor_mock.forward.assert_called_with(power_value)
        right_motor_mock.forward.assert_called_with(power_value)

    def test_speed_power_positive_with_turn_power_positive_big(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(100)

        # THEN
        left_motor_mock.forward.assert_called_with(100)
        right_motor_mock.forward.assert_called_with(0)

    def test_speed_power_positive_big_with_turn_power_positive_big(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 80
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(100)

        # THEN
        left_motor_mock.forward.assert_called_with(100)
        right_motor_mock.forward.assert_called_with(0)

    def test_speed_power_positive_with_turn_power_negative_big(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(-100)

        # THEN
        left_motor_mock.forward.assert_called_with(0)
        right_motor_mock.forward.assert_called_with(100)

    def test_speed_power_positive_big_with_turn_power_negative_big(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 80
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(-100)

        # THEN
        left_motor_mock.forward.assert_called_with(0)
        right_motor_mock.forward.assert_called_with(100)

    def test_speed_power_positive_with_turn_power_negative_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(-20)

        # THEN
        left_motor_mock.forward.assert_called_with(10)
        right_motor_mock.forward.assert_called_with(30)

    def test_speed_power_positive_with_turn_power_positive_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(20)

        # THEN
        left_motor_mock.forward.assert_called_with(30)
        right_motor_mock.forward.assert_called_with(10)

    def test_speed_power_zero_with_turn_power_positive_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 0
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(20)

        # THEN
        left_motor_mock.forward.assert_called_with(10)
        right_motor_mock.backward.assert_called_with(10)

    def test_speed_power_zero_with_turn_power_negative_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 0
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(-20)

        # THEN
        left_motor_mock.backward.assert_called_with(10)
        right_motor_mock.forward.assert_called_with(10)

    def test_speed_power_negative_set(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = -10

        # WHEN
        truck.setSpeedPower(power_value)

        # THEN
        left_motor_mock.backward.assert_called_with(-power_value)
        right_motor_mock.backward.assert_called_with(-power_value)

    def test_speed_power_zero_set(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 0

        # WHEN
        truck.setSpeedPower(power_value)

        # THEN
        left_motor_mock.stop.assert_called()
        right_motor_mock.stop.assert_called()

    def test_speed_power_more_than_max_set(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = 101

        # WHEN
        # THEN
        self.assertRaises(Exception, truck.setSpeedPower, power_value)
        self.assertRaises(Exception, truck.setSpeedPower, -power_value)

    def test_stop(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)

        # WHEN
        truck.stop()

        # THEN
        left_motor_mock.stop.assert_called()
        right_motor_mock.stop.assert_called()

    def test_speed_power_negative_with_turn_power_positive_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = -10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(20)

        # THEN
        left_motor_mock.backward.assert_called_with(30)
        right_motor_mock.backward.assert_called_with(10)

    def test_speed_power_negative_with_turn_power_negative_small(self):
        # GIVEN
        left_motor_mock = self.create_mock_motor()
        right_motor_mock = self.create_mock_motor()
        truck = Truck(left_motor_mock, right_motor_mock)
        power_value = -10
        truck.setSpeedPower(power_value)

        # WHEN

        truck.setTurnPower(-20)

        # THEN
        left_motor_mock.backward.assert_called_with(10)
        right_motor_mock.backward.assert_called_with(30)

    def create_mock_motor(self):
        motor_mock = MagicMock()
        motor_mock.forward = MagicMock()
        motor_mock.backward = MagicMock()
        motor_mock.stop = MagicMock()
        return motor_mock


if __name__ == '__main__':
    unittest.main()
