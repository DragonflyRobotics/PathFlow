# def demo1():
#     from pathflow.motionplanning import Bezier
#     from pathflow.pathfinding import A_Star, Point, a_star
#     bezierGenerator = Bezier()
#     points = [[1,2], [4,4], [1,5]]
#     bezfunc = bezierGenerator.compute_bezier(points)
#
#     # bezierGenerator.visualize(bezfunc, points, 100)
#     # bezierGenerator.save_animation("hehe.mp4", bezfunc, points, 100)
#
#     a = A_Star([1,1], [5,5])
#     a.rectangularObstacle([1,3], [3,2])
#     end = a.compute([1,1], [2,4])
#     a.visualize(end, 100)
#
from pathflow.controlsystems import PIDController
import time
controller = PIDController(25000, 0.0, 0.1)
controller.set_setpoint(10)

class Motor:
    def __init__(self) -> None:
        self.pos = 0
        self.time = 0
        self.mass = 1
    def step(self, force, dt):
        self.time += dt
        self.pos += ((force/self.mass)/2.0) * dt**2
motor = Motor()

while motor.pos != 10:
    motor.step(controller.step(motor.pos), 0.01)
    #motor.step(10, 0.01)
    #print(motor.time, motor.pos)
    time.sleep(0.01)

