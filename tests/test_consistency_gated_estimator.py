import unittest

from simulation.consistency_gated_estimator import (
    ConsistencyGatedAdaptiveEstimator,
)


class ConsistencyGatedAdaptiveEstimatorTests(
    unittest.TestCase
):

    def create_estimator(self):
        return ConsistencyGatedAdaptiveEstimator(
            initial_parameter_estimate=0.50,
            learning_rate=0.08,
            normalization_epsilon=1.0,
            base_process_noise_variance=0.0025,
            measurement_noise_variance=0.25,
            innovation_memory=0.50,
            min_inflation_strength=0.05,
            max_inflation_strength=0.20,
            transition_scale=0.25,
            consistency_threshold=1.0,
            consistency_decay=0.70,
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )

    def test_consistency_gate_activates_below_threshold(self):
        estimator = self.create_estimator()

        gate_active = (
            estimator.update_mismatch_indicator(
                normalized_innovation_squared=0.50,
                excess_normalized_innovation=0.0,
            )
        )

        self.assertTrue(
            gate_active
        )

    def test_consistency_gate_does_not_activate_above_threshold(self):
        estimator = self.create_estimator()

        gate_active = (
            estimator.update_mismatch_indicator(
                normalized_innovation_squared=2.0,
                excess_normalized_innovation=1.0,
            )
        )

        self.assertFalse(
            gate_active
        )

    def test_gate_accelerates_mismatch_decay(self):
        estimator = self.create_estimator()

        estimator.mismatch_indicator = 1.0

        estimator.update_mismatch_indicator(
            normalized_innovation_squared=0.50,
            excess_normalized_innovation=0.0,
        )

        # Standard memory decay would give:
        #
        # 0.50 * 1.0 = 0.50
        #
        # The consistency gate then applies:
        #
        # 0.70 * 0.50 = 0.35

        self.assertAlmostEqual(
            estimator.mismatch_indicator,
            0.35,
            places=12,
        )

    def test_mismatch_remains_nonnegative(self):
        estimator = self.create_estimator()

        estimator.mismatch_indicator = 0.5

        estimator.update_mismatch_indicator(
            normalized_innovation_squared=0.0,
            excess_normalized_innovation=0.0,
        )

        self.assertGreaterEqual(
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

    def test_step_produces_positive_covariance(self):
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