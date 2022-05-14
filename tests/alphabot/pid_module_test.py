import unittest

from alphabot.pid_module import PidController


class TestPid(unittest.TestCase):

    def test_calculate_error(self):
        # GIVEN
        target_value = 10
        current_value = 5
        pid = self._create_pid()
        pid._target_value = target_value

        # WHEN
        error = pid._calculateError(current_value)

        # THEN
        self.assertEqual(target_value - current_value, error)

    def test_calculate_proportional(self):
        # GIVEN
        pid = self._create_pid()
        pid._kp = 2
        error = 10

        # WHEN
        out = pid._calculateProportionalOutput(error)

        # THEN
        self.assertEqual(pid._kp * error, out)

    def test_calculate_integral(self):
        # GIVEN
        pid = self._create_pid()
        pid._ki = 2
        error = 10
        delta_time_ms = 1

        # WHEN
        out = pid._calculateIntegralOutput(error, delta_time_ms)

        # THEN
        self.assertEqual(pid._ki * error, out)

    def test_calculate_integral_accumulation(self):
        # GIVEN
        pid = self._create_pid()
        pid._ki = 2
        error = 10
        delta_time_ms = 1
        iteration_count = 4

        # WHEN
        for i in range(0, iteration_count):
            out = pid._calculateIntegralOutput(error, delta_time_ms)

        # THEN
        self.assertEqual(iteration_count * error * pid._ki, out)

    def test_calculate_integral_anti_windup(self):
        # GIVEN
        pid = self._create_pid()
        pid._ki = 2
        error = 10
        delta_time_ms = 1
        iteration_count = 100

        # WHEN
        for i in range(0, iteration_count):
            out = pid._calculateIntegralOutput(error, delta_time_ms)

        # THEN
        self.assertEqual(pid._max_integral_out, out)

    def test_calculate_differential(self):
        # GIVEN
        pid = self._create_pid()
        pid._kd = 2
        error = 10
        delta_time_ms = 1

        # WHEN
        pid._calculateDifferentialOutput(10, delta_time_ms)
        out = pid._calculateDifferentialOutput(0, delta_time_ms)

        # THEN
        self.assertEqual(-pid._kd * error, out)

    def test_speed_power_positive_set(self):
        # GIVEN

        pid = self._create_pid()
        current_value = 0

        # WHEN
        output = pid.getOutput(current_value, 200)

        # THEN
        self.assertIsNotNone(output)
        self.assertEqual(10, output)

    def _create_pid(self) -> PidController:
        ki = 1
        kp = 1
        kd = 1
        target_value = 10
        max_out = 100
        pid = PidController(kp, ki, kd, target_value, max_out)
        return pid

    def test_with_real_sensor_target_value(self):

        # Делаем для левого датчика целевое значение 350 при этом воздействие только вправо в обратную сторону игнорируем.
        # При 350 значение выходного воздействия должно быть 0, при 700 - 100%
        # GIVEN

        target_value = 350
        pid = self._create_pid()
        pid._target_value = target_value
        current_value = 350

        # WHEN
        output = pid.getOutput(current_value, 200)

        # THEN
        self.assertIsNotNone(output)
        self.assertEqual(0, output)

    def test_with_real_sensor_target_value_max(self):

        # Делаем для левого датчика целевое значение 350 при этом воздействие только вправо в обратную сторону игнорируем.
        # При 350 значение выходного воздействия должно быть 0, при 700 - 100%
        # GIVEN

        target_value = 350
        pid = self._create_pid()
        pid._target_value = target_value
        current_value = 700

        # WHEN
        output = pid.getOutput(current_value, 200)

        # THEN
        self.assertIsNotNone(output)
        self.assertEqual(-100, output)

    def test_with_real_sensor_target_value_middle(self):

        # Делаем для левого датчика целевое значение 350 при этом воздействие только вправо в обратную сторону игнорируем.
        # При 350 значение выходного воздействия должно быть 0, при 700 - 100%
        # GIVEN
        target_value = 350
        pid = self._create_pid()
        pid._target_value = target_value
        pid._kp = 0.285
        current_value = (700 - 350) / 2 + 350

        # WHEN
        output = pid.getOutput(current_value, 200)

        # THEN
        self.assertIsNotNone(output)
        self.assertEqual(-50, round(output))

    def test_telemetry(self):

        # GIVEN
        target_value = 350
        pid = self._create_pid()
        pid._target_value = target_value
        current_value = 700

        # WHEN
        output = pid.getOutput(current_value, 200)

        # THEN
        self.assertEqual(output, pid.getTelemetryData()['o'])
        self.assertEqual(target_value - current_value, pid.getTelemetryData()['err'])


if __name__ == '__main__':
    unittest.main()
