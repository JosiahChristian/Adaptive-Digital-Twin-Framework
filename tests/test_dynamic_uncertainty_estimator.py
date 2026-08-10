import unittest

from simulation.dynamic_uncertainty_estimator import (
    DynamicUncertaintyAdaptiveEstimator,
)


class DynamicUncertaintyAdaptiveEstimatorTests(
    unittest.TestCase
):

    def create_estimator(self):
        return DynamicUncertaintyAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            base_process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
            innovation_memory=0.50,
            min_inflation_strength=0.05,
            max_inflation_strength=0.20,
            transition_scale=0.25,
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )

    def test_zero_mismatch_uses_minimum_inflation(self):
        estimator = self.create_estimator()

        dynamic_lambda = (
            estimator
            .calculate_dynamic_inflation_strength()
        )

        self.assertAlmostEqual(
            dynamic_lambda,
            0.05,
            places=12,
        )

    def test_large_mismatch_moves_inflation_toward_maximum(self):
        estimator = self.create_estimator()

        estimator.mismatch_indicator = 1000.0

        dynamic_lambda = (
            estimator
            .calculate_dynamic_inflation_strength()
        )

        self.assertGreater(
            dynamic_lambda,
            0.19,
        )

        self.assertLessEqual(
            dynamic_lambda,
            0.20,
        )

    def test_dynamic_inflation_stays_within_bounds(self):
        estimator = self.create_estimator()

        mismatch_values = [
            0.0,
            0.01,
            0.10,
            1.0,
            10.0,
            1000.0,
        ]

        for mismatch in mismatch_values:

            estimator.mismatch_indicator = (
                mismatch
            )

            dynamic_lambda = (
                estimator
                .calculate_dynamic_inflation_strength()
            )

            self.assertGreaterEqual(
                dynamic_lambda,
                0.05,
            )

            self.assertLessEqual(
                dynamic_lambda,
                0.20,
            )

    def test_effective_process_noise_increases_with_mismatch(self):
        estimator = self.create_estimator()

        initial_q = (
            estimator
            .calculate_effective_process_noise()
        )

        estimator.mismatch_indicator = 2.0

        inflated_q = (
            estimator
            .calculate_effective_process_noise()
        )

        self.assertGreater(
            inflated_q,
            initial_q,
        )

    def test_covariance_remains_positive(self):
        estimator = self.create_estimator()

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertGreater(
            result.state_covariance,
            0.0,
        )


if __name__ == "__main__":
    unittest.main()