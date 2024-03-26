class PIDController:
    def __init__(self, kP, kI, kD, i_clamp=1000) -> None:
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.i_clamp = i_clamp
        self.setpoint = None
        self.error = 0
        self.prev_error = 0
        self.iSum = 0
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
    def step(self, position):
        if self.setpoint is None:
            raise ValueError("Setpoint not set")
        self.error = self.setpoint - position
        p = self.kP * self.error
        self.iSum = self.iSum + self.error
        i = min(self.iSum * self.kI, self.i_clamp)
        d = self.kD * (self.error - self.prev_error)
        self.prev_error = self.error
        # print(f"Error: {self.error}, Position: {position}, P: {p}, I: {i}, D: {d}")
        return p + i + d
