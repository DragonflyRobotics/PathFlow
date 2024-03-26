class Encoder:
    def __init__(self) -> None:
        self.shaft_theta = 0 # radians
        self.shaft_omega = 0 # radians/sec
        self.time = 0
    def _update(self, omega, dt): 
        pass

class Motor:
    def __init__(self, shaft_mass=0.1, shaft_radius=0.1) -> None:
        self.encoder: Encoder = Encoder()
        self.voltage = 0
        self.time = 0
        self.moment_of_inertia = 0.5 * shaft_mass * shaft_radius**2
        self.viscous_fric_constant = 0.1 # N.m.s
        self.electromotive_force_constant = 0.01 # V/(rad/s)
        self.motor_torque_constant = 0.01 # N.m/A
        self.resistance = 0.1 # Ohms
        self.inductance = 0.5 # H
    def set_power(self, voltage):
        self.voltage = voltage
        self._update()
        pass
    def _update(self, dt):
        pass

class SimpleEncoder(Encoder):
    def __init__(self) -> None:
        super().__init__()
        self.previous_pos = 0
    def _update(self, pos, dt):
        self.shaft_theta = pos
        self.shaft_omega = (pos - self.previous_pos) / dt


class SimpleMotor(Motor):
    def __init__(self, shaft_mass, shaft_radius) -> None:
        super().__init__(shaft_mass, shaft_radius)
    def _update(self, dt):
        omega = self.motor_torque_constant / ()
