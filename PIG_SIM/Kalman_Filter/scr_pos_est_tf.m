%% Theoretical Simulation with Transfer Function and Kalman Filter

% Define Transfer Function H(s) = num(s)/den(s)
num = [1]; 
den = [1 1 1]; 
H = tf(num, den);

% Convert to State-Space Representation
H_ss = ss(H);
[A, B, C, D] = ssdata(H_ss);

% Constants and Initializations
R = 0.1;  % Measurement noise covariance
Q = 0.01; % Process noise covariance
P = 1;    % Initial estimate of position uncertainty
x_est = zeros(2, 1);  % Initial state estimate

% Time vector
t = 0:0.1:10;

% True position (a sine wave for variation) and simulated impedance
true_position = sin(t);
Z_true = lsim(H, true_position, t); % Generating true impedance using the transfer function
Z_meas = Z_true + sqrt(R)*randn(size(Z_true)); % Add measurement noise

% Initialize arrays to store estimated positions
estimated_position = zeros(size(true_position));

% Kalman Filter Loop
for k = 2:length(t)
    % Prediction Step
    x_pred = A * x_est(:, k-1); % Predicted state estimate
    P_pred = A * P * A' + Q;     % Predicted error covariance
    
    % Update Step
    K = P_pred * C' / (C * P_pred * C' + R); % Kalman Gain
    x_est(:, k) = x_pred + K * (Z_meas(k) - C * x_pred); % Corrected state estimate
    P = (1 - K * C) * P_pred; % Updated error covariance
    
    % Store the estimated position
    estimated_position(k) = x_est(1, k); % Assuming position is the first state
end

% Visualization
figure;
plot(t, true_position, 'g', 'LineWidth', 1.5); hold on;
plot(t, Z_meas, 'b', 'LineWidth', 1.5);
plot(t, estimated_position, 'r', 'LineWidth', 1.5);
legend('True Position', 'Measured Impedance', 'Estimated Position');
xlabel('Time');
ylabel('Position/Impedance');
title('Position and Impedance Estimation with KF');
grid on;
