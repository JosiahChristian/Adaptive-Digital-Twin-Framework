import unittest

from simulation.adaptive_scalar_system import (
    INITIAL_TWIN_A,
    TRUE_A,
    run_experiment,
)


class AdaptiveScalarSystemTests(unittest.TestCase):

    def test_experiment_produces_expected_number_of_records(self):
        records = run_experiment()

        self.assertEqual(len(records), 60)

    def test_normalized_adaptation_remains_bounded(self):
        records = run_experiment()

        estimates = [
            record["estimated_a"]
            for record in records
        ]

        self.assertTrue(
            all(abs(estimate) < 2.0 for estimate in estimates)
        )

    def test_parameter_estimate_improves(self):
        records = run_experiment()

        final_estimate = records[-1]["estimated_a"]

        initial_error = abs(
            TRUE_A - INITIAL_TWIN_A
        )

        final_error = abs(
            TRUE_A - final_estimate
        )

        self.assertLess(
            final_error,
            initial_error
        )

    def test_final_parameter_estimate_is_close_to_true_value(self):
        records = run_experiment()

        final_estimate = records[-1]["estimated_a"]

        self.assertAlmostEqual(
            final_estimate,
            TRUE_A,
            delta=0.01
        )


if __name__ == "__main__":
    unittest.main()