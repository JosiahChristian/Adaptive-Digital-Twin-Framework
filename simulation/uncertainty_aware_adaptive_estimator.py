from dataclasses import dataclass

from simulation.scalar_kalman_filter import (
    KalmanState,
    ScalarKalmanFilter,
)


@dataclass
class UncertaintyAwareEstimate:
    state_estimate: float
    state_covariance: float
    parameter_estimate: float
    innovation: float
    parameter_update: float
    mismatch_indicator: float
    effective_process_noise_variance: float


class UncertaintyAwareAdaptiveEstimator:
    """
    Coupled scalar adaptive estimator with innovation-driven
    process-covariance inflation.

    The estimator uses:

        x_(k+1) = a_hat_k * x_hat_k + u_k

    for state prediction, while updating a_hat online.

    Persistent prediction mismatch is tracked using an
    exponentially weighted squared-innovation signal:

        U_k =
            beta * U_(k-1)
            +
            (1 - beta) * r_k^2

    where r_k is the Kalman innovation.

    Effective process-noise variance is then:

        Q_effective =
            Q_base
            +
            inflation_strength * U_k
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
        inflation_strength: float,
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

        self.inflation_strength = (
            inflation_strength
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
        """
        Exponentially weighted innovation-energy update:

            U_k =
                beta * U_(k-1)
                +
                (1 - beta) * r_k^2
        """

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

    def calculate_effective_process_noise(
        self,
    ) -> float:
        """
        Computes innovation-driven covariance inflation:

            Q_effective =
                Q_base
                +
                lambda * U_k
        """

        return (
            self.base_process_noise_variance
            +
            self.inflation_strength
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
    ) -> UncertaintyAwareEstimate:

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

        return UncertaintyAwareEstimate(
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
            effective_process_noise_variance=(
                self.calculate_effective_process_noise()
            ),
        )