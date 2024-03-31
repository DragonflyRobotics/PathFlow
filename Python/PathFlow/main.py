from pathflow.controlsystems import PIDController
import time
from pathflow.simulation.motor import Motor
import matplotlib.pyplot as plt

motor = Motor()
current_time = 0
dt = 0.01

controller = PIDController(1, 0.0, 0.0)
controller.set_setpoint(3.14159)

times = []
voltages = []
thetas = []
omega = []
while current_time <= 100:
    voltage = controller.step(motor.encoder.shaft_theta)
    # if current_time > 1:
    #     voltage = 0
    # else:
    #     voltage = 10
    motor.set_power(voltage)
    motor.update(dt)
    current_time += dt
    times.append(current_time)
    voltages.append(voltage)
    thetas.append(motor.encoder.shaft_theta)
    omega.append(motor.encoder.shaft_omega)
#    time.sleep(dt)

# plt.plot(times, voltages)
# plt.xlabel('Time (s)')
# plt.ylabel('Voltage (V)')
# plt.title('Motor Voltage Over Time')
# plt.show()
#
plt.plot(times, thetas)
plt.xlabel('Time (s)')
plt.ylabel('Theta (rad)')
plt.title('Motor Theta Over Time')
plt.show()

# plt.plot(times, omega)
# plt.xlabel('Time (s)')
# plt.ylabel('Omega (rad/s)')
# plt.title('Motor Omega Over Time')
# plt.show()

