from dataclasses import dataclass

from simulation.scalar_kalman_filter import (
    KalmanState,
    ScalarKalmanFilter,
)


@dataclass
class DynamicUncertaintyEstimate:
    state_estimate: float
    state_covariance: float
    parameter_estimate: float
    innovation: float
    parameter_update: float
    mismatch_indicator: float
    dynamic_inflation_strength: float
    effective_process_noise_variance: float


class DynamicUncertaintyAdaptiveEstimator:
    """
    Coupled adaptive estimator with dynamically scheduled
    process-covariance inflation.

    The mismatch indicator is:

        U_k =
            beta * U_(k-1)
            +
            (1 - beta) * r_k^2

    Dynamic inflation strength is:

        lambda_k =
            lambda_min
            +
            (lambda_max - lambda_min)
            * U_k / (U_k + c)

    Effective process covariance:

        Q_effective =
            Q_base
            +
            lambda_k * U_k
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

        self.mismatch_indicator = (
            initial_mismatch_indicator
        )

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

    def update_mismatch_indicator(
        self,
        *,
        innovation: float,
    ) -> float:

        self.mismatch_indicator = (
            self.innovation_memory
            * self.mismatch_indicator
            +
            (
                1.0
                - self.innovation_memory
            )
            * innovation ** 2
        )

        return self.mismatch_indicator

    def calculate_dynamic_inflation_strength(
        self,
    ) -> float:

        mismatch = self.mismatch_indicator

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
    ) -> DynamicUncertaintyEstimate:

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

        self.update_mismatch_indicator(
            innovation=innovation
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

        return DynamicUncertaintyEstimate(
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
            parameter_update=(
                parameter_update
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
        )