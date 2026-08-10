import unittest

from simulation.uncertainty_aware_adaptive_estimator import (
    UncertaintyAwareAdaptiveEstimator,
)


class UncertaintyAwareAdaptiveEstimatorTests(
    unittest.TestCase
):

    def create_estimator(self):
        return UncertaintyAwareAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            base_process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
            innovation_memory=0.90,
            inflation_strength=0.05,
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )

    def test_mismatch_indicator_increases_with_innovation(self):
        estimator = self.create_estimator()

        initial_indicator = (
            estimator.mismatch_indicator
        )

        estimator.update_mismatch_indicator(
            innovation=2.0
        )

        self.assertGreater(
            estimator.mismatch_indicator,
            initial_indicator,
        )

    def test_effective_process_noise_exceeds_base_when_mismatch_exists(
        self
    ):
        estimator = self.create_estimator()

        estimator.update_mismatch_indicator(
            innovation=2.0
        )

        effective_q = (
            estimator.calculate_effective_process_noise()
        )

        self.assertGreater(
            effective_q,
            estimator.base_process_noise_variance,
        )

    def test_zero_innovation_does_not_create_mismatch_from_zero(self):
        estimator = self.create_estimator()

        estimator.update_mismatch_indicator(
            innovation=0.0
        )

        self.assertAlmostEqual(
            estimator.mismatch_indicator,
            0.0,
            places=12,
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

    def test_persistent_large_innovation_increases_effective_q(self):
        estimator = self.create_estimator()

        initial_q = (
            estimator.calculate_effective_process_noise()
        )

        for _ in range(5):
            estimator.update_mismatch_indicator(
                innovation=2.0
            )

        inflated_q = (
            estimator.calculate_effective_process_noise()
        )

        self.assertGreater(
            inflated_q,
            initial_q,
        )


if __name__ == "__main__":
    unittest.main()