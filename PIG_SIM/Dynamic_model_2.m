clc; clear; close all;

params.m = 0.6;                         % Kg
params.mu = 0.15;                        % Cf
params.g = 9.81;                        % g
params.Cd = 1;                          % Cd flat surface 1?
params.rho = 1000;                      % Water density -kg/m^3
params.A = pi/4*0.047*0.047;            % PIG Face A
params.V = pi/4*0.047*0.047*0.06;       % PIG body Vol
params.Fapplied = @(t) appliedForce(t);
T = 0:0.1:10; 
x_0 = [0;0];

[t, y] = ode45(@(t, y) dynamics_ode(t, y, params), T, x_0);

subplot(2,1,1);
plot(t, y(:,1), 'k-', 'LineWidth', 2); 
xlabel('Time ($s$)', 'Interpreter','latex', 'fontsize', 12);
ylabel('Position ($m$)', 'Interpreter','latex', 'fontsize', 12);
title('PIG Position - Velocity', 'Interpreter','latex', 'fontsize', 15);
grid on;

subplot(2,1,2);
plot(t, y(:,2), 'k-', 'LineWidth', 2); 
xlabel('Time ($s$)', 'Interpreter','latex', 'fontsize', 12);
ylabel('Velocity ($m/s$)', 'Interpreter','latex', 'fontsize', 12);
grid on;

% Simulated force 
function F = appliedForce(t)
    if t < 5
        F = 1e-10;
    else
        F = 0;
    end
end

