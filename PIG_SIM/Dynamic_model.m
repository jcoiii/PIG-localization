% Parameters
rho = 1000; % Fluid density (kg/m^3) 
Cd = 0.5; % Drag coefficient, need to find this
A = pi * 0.047^2; % Frontal area of the PIG (m^2)
m = 1; % Mass of the PIG (kg)
P = 100; % Pressure difference, need to find this

% Initial conditions
v0 = 0;
s0 = 0;
y0 = [v0; s0];
tspan = [0 100];
[t, y] = ode45(@(t,y)pig_motion(y, rho, Cd, A, m, P), tspan, y0);

subplot(2,1,1);
plot(t, y(:,2));
xlabel('Time (s)');
ylabel('Position (m)');
title('Position - Time');
subplot(2,1,2);
plot(t, y(:,1));
xlabel('Time (s)');
ylabel('Velocity (m/s)');
title('Velocity - Time');


function dydt = pig_motion(y, rho, Cd, A, m, P)
    v = y(1); 
    drag_force = 0.5 * rho * v^2 * Cd * A;
    propelling_force = P * A;
    a = (propelling_force - drag_force) / m;
    dydt = [a; v];
end