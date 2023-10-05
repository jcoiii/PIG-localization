a = 1;  b = 0;  % linear coef
R = 0.1;  % measurement nc
Q = 0.1; % process nc
P = 1;    % initial estimate of position uncertainty
pos_est = 0;   % initial position estimate

% Hyp true position of the pig in the pipe
true_position = linspace(0, 10, 100);

% impedance measurements with noise
Z_true = a * true_position + b;
Z_meas = Z_true + sqrt(R) * randn(size(Z_true)); % Add measurement noise

estimated_position = zeros(size(true_position));

% KF
for k = 1:length(true_position)
    % Prediction Step
    pos_pred = pos_est;  
    P_pred = P + Q; 
    
    % Update Step
    K = P_pred / (P_pred + R);  % Kalman Gain
    pos_est = pos_pred + K * (Z_meas(k) - (a * pos_pred + b));  % Corrected position estimate
    P = (1 - K) * P_pred;  % Updated estimate uncertainty
    
    estimated_position(k) = pos_est;
end

figure;
plot(true_position, 'g', 'LineWidth', 1.5); hold on;
plot(Z_meas, 'b', 'LineWidth', 1.5);
plot(estimated_position, 'r', 'LineWidth', 1.5);
legend('True Position', 'Measured Impedance', 'Estimated Position');
xlabel('Time Step');
ylabel('Position/Impedance');
title('Position and Impedance Estimation with KF');
grid on;