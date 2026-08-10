import unittest

from simulation.normalized_innovation_estimator import (
    NormalizedInnovationAdaptiveEstimator,
)


class NormalizedInnovationAdaptiveEstimatorTests(
    unittest.TestCase
):

    def create_estimator(self):
        return NormalizedInnovationAdaptiveEstimator(
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

    def test_zero_excess_innovation_keeps_zero_mismatch(self):
        estimator = self.create_estimator()

        estimator.update_mismatch_indicator(
            excess_normalized_innovation=0.0
        )

        self.assertAlmostEqual(
            estimator.mismatch_indicator,
            0.0,
            places=12,
        )

    def test_positive_excess_innovation_increases_mismatch(self):
        estimator = self.create_estimator()

        estimator.update_mismatch_indicator(
            excess_normalized_innovation=2.0
        )

        self.assertGreater(
            estimator.mismatch_indicator,
            0.0,
        )

    def test_dynamic_inflation_stays_within_bounds(self):
        estimator = self.create_estimator()

        mismatch_values = [
            0.0,
            0.1,
            1.0,
            10.0,
            1000.0,
        ]

        for mismatch in mismatch_values:
            estimator.mismatch_indicator = mismatch

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

    def test_effective_q_increases_with_mismatch(self):
        estimator = self.create_estimator()

        base_q = (
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
            base_q,
        )

    def test_step_produces_nonnegative_nis(self):
        estimator = self.create_estimator()

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertGreaterEqual(
            result.normalized_innovation_squared,
            0.0,
        )

    def test_step_produces_positive_innovation_covariance(self):
        estimator = self.create_estimator()

        result = estimator.step(
            control_input=1.0,
            measurement=1.1,
        )

        self.assertGreater(
            result.innovation_covariance,
            0.0,
        )

    def test_excess_nis_is_zero_when_nis_below_one(self):
        estimator = self.create_estimator()

        result = estimator.step(
            control_input=1.0,
            measurement=1.0,
        )

        if result.normalized_innovation_squared <= 1.0:
            self.assertAlmostEqual(
                result.excess_normalized_innovation,
                0.0,
                places=12,
            )


if __name__ == "__main__":
    unittest.main()