import unittest

from simulation.persistence_gated_estimator import (
    PersistenceGatedAdaptiveEstimator,
)


class PersistenceGatedAdaptiveEstimatorTests(
    unittest.TestCase
):

    def create_estimator(self):
        return PersistenceGatedAdaptiveEstimator(
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
            required_consistency_steps=3,
            consistency_decay=0.70,
            initial_state_estimate=0.0,
            initial_state_covariance=1.0,
        )

    def test_consistency_count_increments(self):
        estimator = self.create_estimator()

        estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        self.assertEqual(
            estimator.consistency_count,
            1,
        )

    def test_inconsistent_observation_resets_count(self):
        estimator = self.create_estimator()

        estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        estimator.update_consistency_state(
            normalized_innovation_squared=0.75
        )

        estimator.update_consistency_state(
            normalized_innovation_squared=2.0
        )

        self.assertEqual(
            estimator.consistency_count,
            0,
        )

    def test_gate_does_not_activate_before_required_steps(self):
        estimator = self.create_estimator()

        first = estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        second = estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        self.assertFalse(first)
        self.assertFalse(second)

    def test_gate_activates_after_required_steps(self):
        estimator = self.create_estimator()

        estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        third = estimator.update_consistency_state(
            normalized_innovation_squared=0.50
        )

        self.assertTrue(third)

        self.assertEqual(
            estimator.consistency_count,
            3,
        )

    def test_gate_accelerates_decay_only_after_persistence(self):
        estimator = self.create_estimator()

        estimator.mismatch_indicator = 1.0

        estimator.update_mismatch_indicator(
            normalized_innovation_squared=0.50,
            excess_normalized_innovation=0.0,
        )

        after_first = (
            estimator.mismatch_indicator
        )

        estimator.update_mismatch_indicator(
            normalized_innovation_squared=0.50,
            excess_normalized_innovation=0.0,
        )

        after_second = (
            estimator.mismatch_indicator
        )

        estimator.update_mismatch_indicator(
            normalized_innovation_squared=0.50,
            excess_normalized_innovation=0.0,
        )

        after_third = (
            estimator.mismatch_indicator
        )

        self.assertAlmostEqual(
            after_first,
            0.50,
            places=12,
        )

        self.assertAlmostEqual(
            after_second,
            0.25,
            places=12,
        )

        self.assertAlmostEqual(
            after_third,
            0.0875,
            places=12,
        )

    def test_mismatch_remains_nonnegative(self):
        estimator = self.create_estimator()

        estimator.mismatch_indicator = 0.5

        for _ in range(5):
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

        for mismatch in [
            0.0,
            0.1,
            1.0,
            10.0,
            1000.0,
        ]:
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