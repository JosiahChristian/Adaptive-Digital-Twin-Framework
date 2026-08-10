from dataclasses import dataclass


@dataclass
class KalmanState:
    estimate: float
    covariance: float


class ScalarKalmanFilter:
    """
    Scalar Kalman filter for the system:

        x_(k+1) = a * x_k + u_k + w_k

    with measurement model:

        y_k = x_k + v_k

    where:
        w_k ~ process noise
        v_k ~ measurement noise
    """

    def __init__(
        self,
        *,
        system_parameter: float,
        process_noise_variance: float,
        measurement_noise_variance: float,
        initial_estimate: float = 0.0,
        initial_covariance: float = 1.0,
    ):
        self.system_parameter = system_parameter
        self.process_noise_variance = process_noise_variance
        self.measurement_noise_variance = measurement_noise_variance

        self.state = KalmanState(
            estimate=initial_estimate,
            covariance=initial_covariance,
        )

    def predict(
        self,
        control_input: float,
    ) -> KalmanState:
        """
        Prediction step:

            x_hat_k^- = a * x_hat_(k-1) + u_k

            P_k^- = a^2 * P_(k-1) + Q
        """

        predicted_estimate = (
            self.system_parameter
            * self.state.estimate
            + control_input
        )

        predicted_covariance = (
            self.system_parameter ** 2
            * self.state.covariance
            + self.process_noise_variance
        )

        self.state = KalmanState(
            estimate=predicted_estimate,
            covariance=predicted_covariance,
        )

        return self.state

    def update(
        self,
        measurement: float,
    ) -> KalmanState:
        """
        Measurement update:

            K_k = P_k^- / (P_k^- + R)

            x_hat_k =
                x_hat_k^- +
                K_k * (y_k - x_hat_k^-)

            P_k =
                (1 - K_k) * P_k^-
        """

        predicted_estimate = (
            self.state.estimate
        )

        predicted_covariance = (
            self.state.covariance
        )

        innovation = (
            measurement
            - predicted_estimate
        )

        innovation_covariance = (
            predicted_covariance
            + self.measurement_noise_variance
        )

        kalman_gain = (
            predicted_covariance
            / innovation_covariance
        )

        updated_estimate = (
            predicted_estimate
            + kalman_gain * innovation
        )

        updated_covariance = (
            (1.0 - kalman_gain)
            * predicted_covariance
        )

        self.state = KalmanState(
            estimate=updated_estimate,
            covariance=updated_covariance,
        )

        return self.state

    def step(
        self,
        *,
        control_input: float,
        measurement: float,
    ) -> KalmanState:
        """
        Executes one complete predict/update cycle.
        """

        self.predict(
            control_input
        )

        return self.update(
            measurement
        )