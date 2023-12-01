import random
import matplotlib.pyplot as plt
import numpy as np

# Parameters
pipe_length = 2000
initial_impedance = 50
noise_std_dev = 5
amplitude = 1  
frequency = 1
impedances = []
kf_estimates = []

kf_estimate = initial_impedance
kf_error = 1
kf_measure_error = noise_std_dev ** 2
kf_process_error = 1

def measure_impedance(pipe, time_step, amplitude, frequency, noise_std_dev):
    ac_signal = amplitude * np.sin(2 * np.pi * frequency * time_step)
    return pipe[-1] + ac_signal + np.random.normal(0, noise_std_dev)

def kalman_filter(kf_estimate, kf_error, measurement, kf_measure_error, kf_process_error):
    prediction = kf_estimate
    pred_error = kf_error + kf_process_error
    kalman_gain = pred_error / (pred_error + kf_measure_error)
    new_estimate = prediction + kalman_gain * (measurement - prediction)
    new_error = (1 - kalman_gain) * pred_error
    return new_estimate, new_error

fig, ax1 = plt.subplots()
pipe = [initial_impedance for _ in range(pipe_length)]

for step in range(pipe_length):
    pipe[-1] += 0.1  # should be a linear change?
    measured_impedance = measure_impedance(pipe, step, amplitude, frequency, noise_std_dev)
    
    # KF update
    kf_estimate, kf_error = kalman_filter(kf_estimate, kf_error, measured_impedance, kf_measure_error, kf_process_error)
    impedances.append(measured_impedance)
    kf_estimates.append(kf_estimate)
    
    # Dynamic plot
    ax1.clear()
    ax1.plot(impedances, label='Measured Impedance ')
    ax1.plot(kf_estimates, label='Estimate')
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Impedance (Ohms)')
    ax1.legend()
    plt.pause(0.1)

plt.show()
