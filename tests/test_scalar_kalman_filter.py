import unittest

from simulation.scalar_kalman_filter import (
    ScalarKalmanFilter,
)


class ScalarKalmanFilterTests(unittest.TestCase):

    def test_prediction_step_updates_state(self):
        kalman_filter = ScalarKalmanFilter(
            system_parameter=0.92,
            process_noise_variance=0.01,
            measurement_noise_variance=0.25,
            initial_estimate=1.0,
            initial_covariance=1.0,
        )

        state = kalman_filter.predict(
            control_input=1.0
        )

        self.assertAlmostEqual(
            state.estimate,
            1.92,
            places=10,
        )

        self.assertGreater(
            state.covariance,
            0.0,
        )

    def test_update_reduces_covariance(self):
        kalman_filter = ScalarKalmanFilter(
            system_parameter=0.92,
            process_noise_variance=0.01,
            measurement_noise_variance=0.25,
            initial_estimate=0.0,
            initial_covariance=1.0,
        )

        predicted_state = kalman_filter.predict(
            control_input=1.0
        )

        predicted_covariance = (
            predicted_state.covariance
        )

        updated_state = kalman_filter.update(
            measurement=1.2
        )

        self.assertLess(
            updated_state.covariance,
            predicted_covariance,
        )

    def test_update_moves_estimate_toward_measurement(self):
        kalman_filter = ScalarKalmanFilter(
            system_parameter=0.92,
            process_noise_variance=0.01,
            measurement_noise_variance=0.25,
            initial_estimate=0.0,
            initial_covariance=1.0,
        )

        predicted_state = kalman_filter.predict(
            control_input=1.0
        )

        predicted_estimate = (
            predicted_state.estimate
        )

        measurement = 1.5

        updated_state = kalman_filter.update(
            measurement=measurement
        )

        predicted_distance = abs(
            measurement
            - predicted_estimate
        )

        updated_distance = abs(
            measurement
            - updated_state.estimate
        )

        self.assertLess(
            updated_distance,
            predicted_distance,
        )

    def test_step_returns_positive_covariance(self):
        kalman_filter = ScalarKalmanFilter(
            system_parameter=0.92,
            process_noise_variance=0.01,
            measurement_noise_variance=0.25,
        )

        state = kalman_filter.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertGreater(
            state.covariance,
            0.0,
        )


if __name__ == "__main__":
    unittest.main()