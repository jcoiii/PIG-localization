import random
import matplotlib.pyplot as plt
import numpy as np

# Parameters
pipe_length = 200  
initial_impedance = 50  # Initial impedance in Ohms
pig_impedance = 10  # Impedance change 
pig_position = random.randint(0, pipe_length-1)  
noise_std_dev = 5  
impedances = []
kf_estimates = []

# Kalman filter parameters
kf_estimate = initial_impedance  # Initial est
kf_error = 1  # Initial e
kf_measure_error = noise_std_dev ** 2  # Measurement e (var)
kf_process_error = 1  # Process e (var)

pipe = [initial_impedance for _ in range(pipe_length)]


def update_impedance(pipe, pig_position, pig_impedance):
    pipe[pig_position] += pig_impedance
def measure_impedance(pipe, noise_std_dev):
    return pipe[-1] + np.random.normal(0, noise_std_dev)

def kalman_filter(kf_estimate, kf_error, measurement, kf_measure_error, kf_process_error):
    # Prediction step
    prediction = kf_estimate
    pred_error = kf_error + kf_process_error
    
    # Update step
    kalman_gain = pred_error / (pred_error + kf_measure_error)
    new_estimate = prediction + kalman_gain * (measurement - prediction)
    new_error = (1 - kalman_gain) * pred_error
    
    return new_estimate, new_error

fig, ax1 = plt.subplots()

for step in range(pipe_length):
    pipe[pig_position] = initial_impedance
    pig_position = (pig_position + 1) % pipe_length
    update_impedance(pipe, pig_position, pig_impedance)
    measured_impedance = measure_impedance(pipe, noise_std_dev)
    kf_estimate, kf_error = kalman_filter(kf_estimate, kf_error, measured_impedance, kf_measure_error, kf_process_error)
    impedances.append(measured_impedance)
    kf_estimates.append(kf_estimate)
    ax1.clear()
    ax1.plot(impedances, label='Measured Imp')
    ax1.plot(kf_estimates, label='Estimated Imp')
    ax1.set_xlabel('Position in pijp')
    ax1.set_ylabel('Impedance (Ohms)')
    ax1.legend()
    plt.pause(0.1)

plt.show()
