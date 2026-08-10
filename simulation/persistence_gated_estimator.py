from dataclasses import dataclass

from simulation.scalar_kalman_filter import (
    KalmanState,
    ScalarKalmanFilter,
)


@dataclass
class PersistenceGatedEstimate:
    state_estimate: float
    state_covariance: float
    parameter_estimate: float
    innovation: float
    innovation_covariance: float
    normalized_innovation_squared: float
    excess_normalized_innovation: float
    mismatch_indicator: float
    dynamic_inflation_strength: float
    effective_process_noise_variance: float
    parameter_update: float
    consistency_count: int
    persistence_gate_active: bool


class PersistenceGatedAdaptiveEstimator:
    """
    Adaptive estimator using normalized innovation with
    persistence-gated uncertainty decay.

    A single statistically consistent observation is not
    sufficient to trigger accelerated decay.

    The estimator requires multiple consecutive observations
    satisfying:

        NIS <= consistency_threshold

    before the persistence gate activates.
    """

    def __init__(
        self,
        *,
        initial_parameter_estimate: float,
        learning_rate: float,
        normalization_epsilon: float,
        base_process_noise_variance: float,
        measurement_noise_variance: float,
        innovation_memory: float,
        min_inflation_strength: float,
        max_inflation_strength: float,
        transition_scale: float,
        consistency_threshold: float,
        required_consistency_steps: int,
        consistency_decay: float,
        initial_state_estimate: float = 0.0,
        initial_state_covariance: float = 1.0,
        initial_mismatch_indicator: float = 0.0,
    ):
        self.parameter_estimate = (
            initial_parameter_estimate
        )

        self.learning_rate = (
            learning_rate
        )

        self.normalization_epsilon = (
            normalization_epsilon
        )

        self.base_process_noise_variance = (
            base_process_noise_variance
        )

        self.measurement_noise_variance = (
            measurement_noise_variance
        )

        self.innovation_memory = (
            innovation_memory
        )

        self.min_inflation_strength = (
            min_inflation_strength
        )

        self.max_inflation_strength = (
            max_inflation_strength
        )

        self.transition_scale = (
            transition_scale
        )

        self.consistency_threshold = (
            consistency_threshold
        )

        self.required_consistency_steps = (
            required_consistency_steps
        )

        self.consistency_decay = (
            consistency_decay
        )

        self.mismatch_indicator = (
            initial_mismatch_indicator
        )

        self.consistency_count = 0

        self.kalman_filter = ScalarKalmanFilter(
            system_parameter=(
                self.parameter_estimate
            ),
            process_noise_variance=(
                self.base_process_noise_variance
            ),
            measurement_noise_variance=(
                self.measurement_noise_variance
            ),
            initial_estimate=(
                initial_state_estimate
            ),
            initial_covariance=(
                initial_state_covariance
            ),
        )

    def calculate_dynamic_inflation_strength(
        self,
    ) -> float:

        mismatch = (
            self.mismatch_indicator
        )

        fraction = (
            mismatch
            / (
                mismatch
                + self.transition_scale
            )
        )

        return (
            self.min_inflation_strength
            +
            (
                self.max_inflation_strength
                - self.min_inflation_strength
            )
            * fraction
        )

    def calculate_effective_process_noise(
        self,
    ) -> float:

        dynamic_lambda = (
            self.calculate_dynamic_inflation_strength()
        )

        return (
            self.base_process_noise_variance
            +
            dynamic_lambda
            * self.mismatch_indicator
        )

    def update_consistency_state(
        self,
        *,
        normalized_innovation_squared: float,
    ) -> bool:

        if (
            normalized_innovation_squared
            <= self.consistency_threshold
        ):
            self.consistency_count += 1
        else:
            self.consistency_count = 0

        return (
            self.consistency_count
            >= self.required_consistency_steps
        )

    def update_mismatch_indicator(
        self,
        *,
        normalized_innovation_squared: float,
        excess_normalized_innovation: float,
    ) -> bool:

        self.mismatch_indicator = (
            self.innovation_memory
            * self.mismatch_indicator
            +
            (
                1.0
                - self.innovation_memory
            )
            * excess_normalized_innovation
        )

        persistence_gate_active = (
            self.update_consistency_state(
                normalized_innovation_squared=(
                    normalized_innovation_squared
                )
            )
        )

        if persistence_gate_active:
            self.mismatch_indicator *= (
                self.consistency_decay
            )

        return persistence_gate_active

    def update_parameter(
        self,
        *,
        innovation: float,
        previous_state_estimate: float,
    ) -> float:

        normalization = (
            self.normalization_epsilon
            + previous_state_estimate ** 2
        )

        parameter_update = (
            self.learning_rate
            * innovation
            * previous_state_estimate
            / normalization
        )

        self.parameter_estimate += (
            parameter_update
        )

        return parameter_update

    def step(
        self,
        *,
        control_input: float,
        measurement: float,
    ) -> PersistenceGatedEstimate:

        previous_state_estimate = (
            self.kalman_filter.state.estimate
        )

        self.kalman_filter.system_parameter = (
            self.parameter_estimate
        )

        self.kalman_filter.process_noise_variance = (
            self.calculate_effective_process_noise()
        )

        predicted_state: KalmanState = (
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

        persistence_gate_active = (
            self.update_mismatch_indicator(
                normalized_innovation_squared=(
                    normalized_innovation_squared
                ),
                excess_normalized_innovation=(
                    excess_normalized_innovation
                ),
            )
        )

        dynamic_lambda = (
            self.calculate_dynamic_inflation_strength()
        )

        self.kalman_filter.process_noise_variance = (
            self.calculate_effective_process_noise()
        )

        updated_state: KalmanState = (
            self.kalman_filter.update(
                measurement
            )
        )

        parameter_update = (
            self.update_parameter(
                innovation=innovation,
                previous_state_estimate=(
                    previous_state_estimate
                ),
            )
        )

        return PersistenceGatedEstimate(
            state_estimate=(
                updated_state.estimate
            ),
            state_covariance=(
                updated_state.covariance
            ),
            parameter_estimate=(
                self.parameter_estimate
            ),
            innovation=innovation,
            innovation_covariance=(
                innovation_covariance
            ),
            normalized_innovation_squared=(
                normalized_innovation_squared
            ),
            excess_normalized_innovation=(
                excess_normalized_innovation
            ),
            mismatch_indicator=(
                self.mismatch_indicator
            ),
            dynamic_inflation_strength=(
                dynamic_lambda
            ),
            effective_process_noise_variance=(
                self.calculate_effective_process_noise()
            ),
            parameter_update=(
                parameter_update
            ),
            consistency_count=(
                self.consistency_count
            ),
            persistence_gate_active=(
                persistence_gate_active
            ),
        )