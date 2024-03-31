class Encoder:
    def __init__(self) -> None:
        self.shaft_theta = 0 # radians
        self.shaft_omega = 0 # radians/sec
        self.time = 0
    def update(self, omega, dt): # update the encoder
        self.shaft_theta += omega * dt
        self.shaft_omega = omega
        pass

class Motor:
    def __init__(self, shaft_mass=0.1, shaft_radius=0.1) -> None:
        self.encoder: Encoder = Encoder()
        self.voltage = 0
        self.time = 0
        self.moment_of_inertia = 0.5 * shaft_mass * shaft_radius**2
        self.motor_constant = 0.01 # N.m/A
        self.resistance = 1 # Ohms
        self.inductance = 0.5 # H
        self.net_shaft_fric = 0.01 # N.m
        self.shaft_mass = shaft_mass
        self.shaft_radius = shaft_radius    
        self.I = [0]
        self.V = [0]
        self.omega = [0]
    def set_power(self, voltage):
        self.voltage = voltage
        
    def update(self, dt):
        self.V.append(self.voltage)
        self.I.append(self.I[-1] + ((self.V[-1] - self.I[-1] * self.resistance) / self.inductance) * dt)
        torque = self.motor_constant * self.I[-1] #Torque equation\
        if self.omega[-1] > 0:
            torque -= self.net_shaft_fric
        alpha = torque / self.moment_of_inertia  # Angular acceleration
        self.omega.append(self.omega[-1] + alpha * dt)  # Angular velocity
        self.encoder.update(self.omega[-1], dt)

