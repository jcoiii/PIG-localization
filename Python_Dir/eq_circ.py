import numpy as np
import matplotlib.pyplot as plt

def transfer_function(R_fixed, R_variable):
    return R_variable / (R_fixed + R_variable)

# input signal
V_amplitude = 5  
frequency = 60 
phase = 0
time = np.linspace(0, 1, 1000) 
V_in = V_amplitude * np.sin(2 * np.pi * frequency * time + phase)

R_variable = 10000 
R_fixed = np.linspace(10000, 100000, 1000)
V_peak = V_amplitude # V_amplitude/np.sqrt(2) --> rms

V_out = transfer_function(R_fixed, R_variable) * V_peak

gain = V_out / V_peak
gain_dB = (20 * np.log10(gain))

plt.figure()
plt.plot(R_fixed, gain_dB)
plt.xlabel('Water Resistance (Ohms)')
plt.ylabel('Gain (dB)')
plt.title('Gain vs. Water Resistance')
plt.grid(True)
plt.show()