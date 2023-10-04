% Constants and Initializations
a = 1;  b = 0;  % Linear coefficients for impedance
R = 0.1;  % Measurement noise covariance
Q = 0.01; % Process noise covariance
P = 1;    % Initial estimate of position uncertainty
pos_est = 0;   % Initial position estimate

% Hypothetical true position of the pig in the pipe
true_position = linspace(0, 10, 100);

% Simulate impedance measurements with noise
Z_true = a * true_position + b;
Z_meas = Z_true + sqrt(R) * randn(size(Z_true)); % Add measurement noise

% Initialize array to store estimated positions
estimated_position = zeros(size(true_position));

% Kalman Filter Loop
for k = 1:length(true_position)
    % Prediction Step
    pos_pred = pos_est;  % As we have no dynamic model, the prediction is the previous estimate
    P_pred = P + Q;  % Update uncertainty estimate with process noise
    
    % Update Step
    K = P_pred / (P_pred + R);  % Kalman Gain
    pos_est = pos_pred + K * (Z_meas(k) - (a * pos_pred + b));  % Corrected position estimate
    P = (1 - K) * P_pred;  % Updated estimate uncertainty
    
    % Store the estimated position
    estimated_position(k) = pos_est;
end

% Visualization
figure;
plot(true_position, 'g', 'LineWidth', 1.5); hold on;
plot(Z_meas, 'b', 'LineWidth', 1.5);
plot(estimated_position, 'r', 'LineWidth', 1.5);
legend('True Position', 'Measured Impedance', 'Estimated Position');
xlabel('Time Step');
ylabel('Position/Impedance');
title('Position and Impedance Estimation with KF');
grid on;