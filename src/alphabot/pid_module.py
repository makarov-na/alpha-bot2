import time


class PidController(object):

    def __init__(self, kp, ki, kd, target_value, max_out) -> None:
        self._max_out = max_out
        self._max_integral_out = max_out
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._target_value = target_value
        self._prevent_time = None
        self._prevent_value = None
        self._prevent_error = None
        self._integral_value = 0
        self._differential_value = 0
        self._telemetry_data = None

    def getOutput(self, current_value, delta_time):
        error = self._calculateError(current_value)
        if delta_time is None or error is None:
            return None
        proportional_out = self._calculateProportionalOutput(error)
        integral_out = self._calculateIntegralOutput(error, delta_time)
        differential_out = self._calculateDifferentialOutput(error, delta_time)

        out = proportional_out + integral_out + differential_out
        if abs(out) > self._max_out:
            out = out * (self._max_out / abs(out))

        self._telemetry_data = {'dt': delta_time, 'err': error, 'o': out, 'po': proportional_out, 'io': integral_out, 'do': differential_out}
        return out

    def _calculateError(self, current_value):
        return self._target_value - current_value

    def _calculateProportionalOutput(self, error):
        return self._kp * error

    def _calculateIntegralOutput(self, error, delta_time):
        integral_value = self._integral_value + error * delta_time
        if abs(self._ki * integral_value) <= self._max_integral_out:
            self._integral_value = integral_value
        return self._ki * self._integral_value

    def _calculateDifferentialOutput(self, error, delta_time):
        if self._prevent_error is None:
            self._prevent_error = error
            return 0
        differential_value = (error - self._prevent_error) / delta_time
        self._prevent_error = error
        return self._kd * differential_value

    def getTelemetryData(self) -> dict:
        return self._telemetry_data
