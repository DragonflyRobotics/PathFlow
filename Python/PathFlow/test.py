import matplotlib.pyplot as plt
import numpy as np
# Constants
R = 1.0  # Resistance (ohms)
L = 0.5  # Inductance (henries)
K = 0.01  # Motor constant (N/A)
J = 0.02  # Moment of inertia (kg.m^2)
# Time parameters
dt = 0.01  # Time step
t = np.arange(0, 10, dt)  # Time array
# Input voltage (step function)
V = np.ones_like(t) * 10
V[t > 1] = 0  # Turn off voltage after 1 second
# Simulation
I = np.zeros_like(t)  # Current array
omega = np.zeros_like(t)  # Angular velocity array
for i in range(1, len(t)):
    I[i] = I[i - 1] + ((V[i - 1] - I[i - 1] * R) / L) * dt
    torque = K * I[i]  # Torque equation
    alpha = torque / J  # Angular acceleration
    omega[i] = omega[i - 1] + alpha * dt  # Angular velocity
# Plotting
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, V, label='Input Voltage (V)')
plt.legend()
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(t, omega, label='Angular Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (rad/s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
