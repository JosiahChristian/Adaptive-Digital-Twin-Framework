import unittest

from simulation.integrated_adaptive_estimator import (
    IntegratedAdaptiveEstimator,
)


class IntegratedAdaptiveEstimatorTests(unittest.TestCase):

    def test_step_returns_finite_estimates(self):
        estimator = IntegratedAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
        )

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertTrue(
            abs(result.state_estimate) < 1000.0
        )

        self.assertTrue(
            abs(result.parameter_estimate) < 1000.0
        )

    def test_covariance_remains_positive(self):
        estimator = IntegratedAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
        )

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertGreater(
            result.state_covariance,
            0.0,
        )

    def test_first_parameter_update_is_zero_from_zero_initial_state(self):
        estimator = IntegratedAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
            initial_state_estimate=0.0,
        )

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertAlmostEqual(
            result.parameter_update,
            0.0,
            places=12,
        )

    def test_parameter_can_update_after_state_information_exists(self):
        estimator = IntegratedAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
        )

        estimator.step(
            control_input=1.0,
            measurement=1.0,
        )

        result = estimator.step(
            control_input=1.0,
            measurement=2.0,
        )

        self.assertNotAlmostEqual(
            result.parameter_update,
            0.0,
            places=12,
        )


if __name__ == "__main__":
    unittest.main()