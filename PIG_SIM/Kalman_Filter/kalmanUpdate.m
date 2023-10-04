function [pos_est, P_est] = kalmanUpdate(pos_pred, P_pred, Z_meas, R, a, b)
    % Innovation: difference between measured and predicted impedance
    innov = Z_meas - calculateImpedance(pos_pred, a, b);
    
    K = P_pred / (P_pred + R); % Kalman gain

    pos_est = pos_pred + K * innov; % Updated (a posteriori) position estimate
    P_est = (1 - K) * P_pred; % Updated (a posteriori) estimate covariance

end