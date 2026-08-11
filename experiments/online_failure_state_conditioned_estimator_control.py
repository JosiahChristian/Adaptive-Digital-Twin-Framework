import csv
import math
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from experiments.independent_aggregated_evidence_validation import (
    BASE_PROCESS_NOISE_STD,
    BASE_TRUE_A,
    EVENT_STEP,
    INNOVATION_MEMORY,
    LEARNING_RATE,
    MAX_INFLATION_STRENGTH,
    MIN_INFLATION_STRENGTH,
    NORMALIZATION_EPSILON,
    PROCESS_INPUT,
    STEPS,
    TRANSITION_SCALE,
)

from simulation.normalized_innovation_estimator import (
    NormalizedInnovationAdaptiveEstimator,
)


REFERENCE_PATH = Path(
    "results/criterion_failure_decomposition.csv"
)

OUTPUT_PATH = Path(
    "results/online_failure_state_conditioned_estimator_control.csv"
)


RUNS_PER_CONDITION = 100
BASE_SEED = 38000


CONDITIONS = [
    {
        "class": "measurement_noise",
        "reference_condition":
            "measurement_noise_0.850",
        "name":
            "measurement_noise_0.850",
        "measurement_noise_std": 0.85,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "process_disturbance",
        "reference_condition":
            "process_disturbance_2.70",
        "name":
            "process_disturbance_2.70",
        "measurement_noise_std": 0.50,
        "process_disturbance": 2.70,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": None,
    },
    {
        "class": "parameter_mismatch",
        "reference_condition":
            "parameter_mismatch_delta_0.520",
        "name":
            "parameter_mismatch_delta_0.520",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.40,
        "changed_true_a": None,
    },
    {
        "class": "structural_change",
        "reference_condition":
            "structural_change_delta_0.060",
        "name":
            "structural_change_delta_0.060",
        "measurement_noise_std": 0.50,
        "process_disturbance": 0.0,
        "initial_parameter_estimate": 0.50,
        "changed_true_a": 0.86,
    },
]


@dataclass
class EstimatorControl:
    parameter_learning_scale: float
    process_uncertainty_scale: float
    allow_commitment: bool
    allow_structural_intervention: bool
    action_name: str


def load_reference_distributions() -> dict:

    with REFERENCE_PATH.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    groups = defaultdict(list)

    for row in rows:

        groups[
            row["condition"]
        ].append(
            row
        )

    output = {}

    for condition, group in groups.items():

        total = len(group)

        output[condition] = {
            "p_pass":
                sum(
                    row[
                        "evidence_sufficient"
                    ]
                    == "True"
                    for row in group
                )
                / total,

            "p_fail_A":
                sum(
                    row["fail_A"]
                    == "True"
                    for row in group
                )
                / total,

            "p_fail_C":
                sum(
                    row["fail_C"]
                    == "True"
                    for row in group
                )
                / total,

            "p_fail_S":
                sum(
                    row["fail_S"]
                    == "True"
                    for row in group
                )
                / total,
        }

    return output


REFERENCE_DISTRIBUTIONS = (
    load_reference_distributions()
)


def baseline_control() -> EstimatorControl:

    return EstimatorControl(
        parameter_learning_scale=1.0,
        process_uncertainty_scale=1.0,
        allow_commitment=True,
        allow_structural_intervention=True,
        action_name="normal",
    )


def generic_control(
    reference: dict,
) -> EstimatorControl:

    failure_probability = (
        1.0
        - reference["p_pass"]
    )

    if failure_probability < 0.50:

        return baseline_control()

    # Important change from Experiment 037:
    # preserve parameter learning.
    return EstimatorControl(
        parameter_learning_scale=1.0,
        process_uncertainty_scale=1.50,
        allow_commitment=False,
        allow_structural_intervention=False,
        action_name="generic_uncertainty",
    )


def failure_aware_control(
    reference: dict,
) -> EstimatorControl:

    p_a = reference[
        "p_fail_A"
    ]

    p_c = reference[
        "p_fail_C"
    ]

    p_s = reference[
        "p_fail_S"
    ]

    dominant = max(
        [
            ("A", p_a),
            ("C", p_c),
            ("S", p_s),
        ],
        key=lambda item:
            item[1],
    )[0]

    # Coverage failure:
    # preserve parameter learning.
    # Delay commitment rather than freezing adaptation.
    if dominant == "C":

        return EstimatorControl(
            parameter_learning_scale=1.0,
            process_uncertainty_scale=1.10,
            allow_commitment=False,
            allow_structural_intervention=False,
            action_name="coverage_wait",
        )

    # Hard-accuracy failure:
    # preserve most parameter learning but broaden
    # state/process uncertainty.
    if dominant == "A":

        return EstimatorControl(
            parameter_learning_scale=0.90,
            process_uncertainty_scale=1.75,
            allow_commitment=False,
            allow_structural_intervention=False,
            action_name="accuracy_guard",
        )

    # Selective-accuracy failure:
    # preserve estimation, but prohibit high-impact
    # intervention.
    return EstimatorControl(
        parameter_learning_scale=1.0,
        process_uncertainty_scale=1.25,
        allow_commitment=False,
        allow_structural_intervention=False,
        action_name="selective_guard",
    )


class ControlledNormalizedInnovationEstimator(
    NormalizedInnovationAdaptiveEstimator
):

    def controlled_step(
        self,
        *,
        control_input: float,
        measurement: float,
        control: EstimatorControl,
    ) -> dict:

        previous_state_estimate = (
            self.kalman_filter.state.estimate
        )

        self.kalman_filter.system_parameter = (
            self.parameter_estimate
        )

        base_effective_process_noise = (
            self.calculate_effective_process_noise()
        )

        controlled_process_noise = (
            base_effective_process_noise
            * control.process_uncertainty_scale
        )

        self.kalman_filter.process_noise_variance = (
            controlled_process_noise
        )

        predicted_state = (
            self.kalman_filter.predict(
                control_input
            )
        )

        innovation = (
            measurement
            - predicted_state.estimate
        )

        innovation_covariance = (
            predicted_state.covariance
            + self.measurement_noise_variance
        )

        normalized_innovation_squared = (
            innovation ** 2
            / innovation_covariance
        )

        excess_normalized_innovation = max(
            0.0,
            normalized_innovation_squared
            - 1.0,
        )

        self.update_mismatch_indicator(
            excess_normalized_innovation=(
                excess_normalized_innovation
            )
        )

        dynamic_lambda = (
            self.calculate_dynamic_inflation_strength()
        )

        updated_effective_process_noise = (
            self.calculate_effective_process_noise()
            * control.process_uncertainty_scale
        )

        self.kalman_filter.process_noise_variance = (
            updated_effective_process_noise
        )

        updated_state = (
            self.kalman_filter.update(
                measurement
            )
        )

        normalization = (
            self.normalization_epsilon
            + previous_state_estimate ** 2
        )

        raw_parameter_update = (
            self.learning_rate
            * innovation
            * previous_state_estimate
            / normalization
        )

        parameter_update = (
            raw_parameter_update
            * control.parameter_learning_scale
        )

        self.parameter_estimate += (
            parameter_update
        )

        return {
            "state_estimate":
                updated_state.estimate,

            "state_covariance":
                updated_state.covariance,

            "parameter_estimate":
                self.parameter_estimate,

            "innovation":
                innovation,

            "innovation_covariance":
                innovation_covariance,

            "normalized_innovation_squared":
                normalized_innovation_squared,

            "mismatch_indicator":
                self.mismatch_indicator,

            "dynamic_inflation_strength":
                dynamic_lambda,

            "effective_process_noise":
                updated_effective_process_noise,

            "raw_parameter_update":
                raw_parameter_update,

            "parameter_update":
                parameter_update,
        }


def create_estimator(
    condition: dict,
) -> ControlledNormalizedInnovationEstimator:

    return ControlledNormalizedInnovationEstimator(
        initial_parameter_estimate=(
            condition[
                "initial_parameter_estimate"
            ]
        ),
        learning_rate=LEARNING_RATE,
        normalization_epsilon=(
            NORMALIZATION_EPSILON
        ),
        base_process_noise_variance=(
            BASE_PROCESS_NOISE_STD ** 2
        ),
        measurement_noise_variance=(
            condition[
                "measurement_noise_std"
            ] ** 2
        ),
        innovation_memory=(
            INNOVATION_MEMORY
        ),
        min_inflation_strength=(
            MIN_INFLATION_STRENGTH
        ),
        max_inflation_strength=(
            MAX_INFLATION_STRENGTH
        ),
        transition_scale=(
            TRANSITION_SCALE
        ),
        initial_state_estimate=0.0,
        initial_state_covariance=1.0,
    )


def choose_control(
    *,
    policy: str,
    reference: dict,
) -> EstimatorControl:

    if policy == "baseline":

        return baseline_control()

    if policy == "generic_uncertainty":

        return generic_control(
            reference
        )

    if policy == "failure_aware":

        return failure_aware_control(
            reference
        )

    raise ValueError(
        policy
    )


def rmse(
    values: list[float],
) -> float:

    return math.sqrt(
        statistics.mean(
            value ** 2
            for value in values
        )
    )


def recovery_time(
    errors: list[float],
    *,
    threshold: float = 0.05,
    required_run: int = 5,
) -> int | None:

    run = 0

    for relative_index, error in enumerate(
        errors
    ):

        if abs(error) <= threshold:

            run += 1

            if run >= required_run:

                return (
                    relative_index
                    - required_run
                    + 1
                )

        else:

            run = 0

    return None


def run_controlled_trajectory(
    *,
    condition: dict,
    seed: int,
    policy: str,
) -> dict:

    random.seed(
        seed
    )

    estimator = create_estimator(
        condition
    )

    reference = (
        REFERENCE_DISTRIBUTIONS[
            condition[
                "reference_condition"
            ]
        ]
    )

    control = choose_control(
        policy=policy,
        reference=reference,
    )

    true_state = 0.0
    true_a = BASE_TRUE_A

    true_states = []
    state_estimates = []
    parameter_estimates = []
    parameter_updates = []
    innovations = []
    nis_values = []

    for step in range(
        STEPS
    ):

        if (
            condition[
                "changed_true_a"
            ]
            is not None
            and step == EVENT_STEP
        ):

            true_a = (
                condition[
                    "changed_true_a"
                ]
            )

        true_state = (
            true_a
            * true_state
            + PROCESS_INPUT
            + random.gauss(
                0.0,
                BASE_PROCESS_NOISE_STD,
            )
        )

        if (
            condition[
                "process_disturbance"
            ]
            != 0.0
            and step == EVENT_STEP
        ):

            true_state += (
                condition[
                    "process_disturbance"
                ]
            )

        measurement = (
            true_state
            + random.gauss(
                0.0,
                condition[
                    "measurement_noise_std"
                ],
            )
        )

        result = (
            estimator.controlled_step(
                control_input=PROCESS_INPUT,
                measurement=measurement,
                control=control,
            )
        )

        true_states.append(
            true_state
        )

        state_estimates.append(
            result[
                "state_estimate"
            ]
        )

        parameter_estimates.append(
            result[
                "parameter_estimate"
            ]
        )

        parameter_updates.append(
            result[
                "parameter_update"
            ]
        )

        innovations.append(
            result[
                "innovation"
            ]
        )

        nis_values.append(
            result[
                "normalized_innovation_squared"
            ]
        )

    target_parameters = [
        (
            BASE_TRUE_A
            if (
                condition[
                    "changed_true_a"
                ]
                is None
                or step < EVENT_STEP
            )
            else condition[
                "changed_true_a"
            ]
        )
        for step in range(
            STEPS
        )
    ]

    state_errors = [
        estimate - truth
        for estimate, truth in zip(
            state_estimates,
            true_states,
        )
    ]

    parameter_errors = [
        estimate - target
        for estimate, target in zip(
            parameter_estimates,
            target_parameters,
        )
    ]

    post_state_errors = (
        state_errors[
            EVENT_STEP:
        ]
    )

    post_parameter_errors = (
        parameter_errors[
            EVENT_STEP:
        ]
    )

    rec_time = recovery_time(
        post_parameter_errors
    )

    return {
        "condition":
            condition["name"],

        "true_class":
            condition["class"],

        "seed":
            seed,

        "policy":
            policy,

        "selected_action":
            control.action_name,

        "parameter_learning_scale":
            control.parameter_learning_scale,

        "process_uncertainty_scale":
            control.process_uncertainty_scale,

        "allow_commitment":
            control.allow_commitment,

        "allow_structural_intervention":
            control.allow_structural_intervention,

        "reference_p_pass":
            reference["p_pass"],

        "reference_p_fail_A":
            reference["p_fail_A"],

        "reference_p_fail_C":
            reference["p_fail_C"],

        "reference_p_fail_S":
            reference["p_fail_S"],

        "post_event_state_rmse":
            rmse(
                post_state_errors
            ),

        "post_event_parameter_rmse":
            rmse(
                post_parameter_errors
            ),

        "final_parameter_error":
            abs(
                parameter_errors[-1]
            ),

        "cumulative_abs_parameter_update":
            sum(
                abs(update)
                for update in parameter_updates
            ),

        "mean_post_event_nis":
            statistics.mean(
                nis_values[
                    EVENT_STEP:
                ]
            ),

        "recovered":
            rec_time is not None,

        "recovery_time":
            (
                rec_time
                if rec_time is not None
                else ""
            ),
    }


def run_experiment() -> list[dict]:

    rows = []

    policies = [
        "baseline",
        "generic_uncertainty",
        "failure_aware",
    ]

    for (
        condition_index,
        condition,
    ) in enumerate(
        CONDITIONS
    ):

        for seed_offset in range(
            RUNS_PER_CONDITION
        ):

            seed = (
                BASE_SEED
                + condition_index
                * RUNS_PER_CONDITION
                + seed_offset
            )

            for policy in policies:

                rows.append(
                    run_controlled_trajectory(
                        condition=condition,
                        seed=seed,
                        policy=policy,
                    )
                )

    return rows


def save_results(
    rows: list[dict],
) -> None:

    OUTPUT_PATH.parent.mkdir(
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )


def print_summary(
    rows: list[dict],
) -> None:

    print("=" * 126)

    print(
        "ADAPTIVE DIGITAL TWIN - "
        "ONLINE FAILURE-STATE-CONDITIONED ESTIMATOR CONTROL"
    )

    print("=" * 126)

    for policy in [
        "baseline",
        "generic_uncertainty",
        "failure_aware",
    ]:

        group = [
            row
            for row in rows
            if row["policy"] == policy
        ]

        state_rmse = statistics.mean(
            float(
                row["post_event_state_rmse"]
            )
            for row in group
        )

        parameter_rmse = statistics.mean(
            float(
                row[
                    "post_event_parameter_rmse"
                ]
            )
            for row in group
        )

        final_error = statistics.mean(
            float(
                row[
                    "final_parameter_error"
                ]
            )
            for row in group
        )

        recovery = (
            sum(
                row["recovered"]
                for row in group
            )
            / len(group)
        )

        print(
            f"{policy:<24}"
            f"state_rmse="
            f"{state_rmse:.4f} "
            f"param_rmse="
            f"{parameter_rmse:.4f} "
            f"final_err="
            f"{final_error:.4f} "
            f"recovery="
            f"{recovery:.3%}"
        )

    print("=" * 126)


def main() -> None:

    rows = run_experiment()

    save_results(
        rows
    )

    print_summary(
        rows
    )

    print(
        f"Results saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()