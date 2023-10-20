function dydt = dynamics_ode(t, y, params)

    m = params.m;
    mu = params.mu;
    g = params.g;
    Cd = params.Cd;
    rho = params.rho;
    A = params.A;
    V = params.V;
    Fapplied = params.Fapplied(t);

    position = y(1);
    velocity = y(2);

    % Forces
    F_N = m * g;
    F_friction = mu * F_N;
    F_drag = 0.5 * Cd * rho * A * velocity^2;
    F_buoyancy = rho * g * V;

    % Dynamics: "F = ma"
    F_net = Fapplied - F_friction - F_drag + F_buoyancy;
    a = F_net / m;
    
    dydt = [velocity; a];
end