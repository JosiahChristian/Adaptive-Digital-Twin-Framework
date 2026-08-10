from dataclasses import dataclass

from simulation.scalar_kalman_filter import (
    KalmanState,
    ScalarKalmanFilter,
)


@dataclass
class AdaptiveEstimate:
    state_estimate: float
    state_covariance: float
    parameter_estimate: float
    innovation: float
    parameter_update: float


class IntegratedAdaptiveEstimator:
    """
    Coupled scalar estimator for:

        x_(k+1) = a * x_k + u_k + w_k

    with measurement:

        y_k = x_k + v_k

    The estimator does not know the true system parameter a.
    Instead, it uses the current estimate a_hat_k inside
    the Kalman prediction and updates that parameter online.
    """

    def __init__(
        self,
        *,
        initial_parameter_estimate: float,
        learning_rate: float,
        normalization_epsilon: float,
        process_noise_variance: float,
        measurement_noise_variance: float,
        initial_state_estimate: float = 0.0,
        initial_state_covariance: float = 1.0,
    ):
        self.parameter_estimate = (
            initial_parameter_estimate
        )

        self.learning_rate = learning_rate
        self.normalization_epsilon = (
            normalization_epsilon
        )

        self.kalman_filter = ScalarKalmanFilter(
            system_parameter=(
                self.parameter_estimate
            ),
            process_noise_variance=(
                process_noise_variance
            ),
            measurement_noise_variance=(
                measurement_noise_variance
            ),
            initial_estimate=(
                initial_state_estimate
            ),
            initial_covariance=(
                initial_state_covariance
            ),
        )

    def update_parameter(
        self,
        *,
        innovation: float,
        previous_state_estimate: float,
    ) -> float:
        """
        Normalized parameter update:

            a_hat_(k+1)
            =
            a_hat_k
            +
            eta *
            innovation * x_hat_k
            /
            (epsilon + x_hat_k^2)

        The Kalman innovation is used as the adaptation signal.
        """

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
    ) -> AdaptiveEstimate:
        """
        Executes one coupled estimation/adaptation step.
        """

        previous_state_estimate = (
            self.kalman_filter.state.estimate
        )

        self.kalman_filter.system_parameter = (
            self.parameter_estimate
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

        return AdaptiveEstimate(
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
        )