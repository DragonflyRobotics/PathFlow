from collections.abc import Callable
from types import FunctionType
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class Bezier:
    def __init__(self) -> None:
        pass
    def compute_bezier(self, points: list[list[float, float]]) -> Callable[[float], list[float, float]]:
        points = np.array(points)
        n = len(points) - 1
        def bezier(t):
            pose = np.array([0.0, 0.0])
            if t<=0:
                return points[0]
            elif t>=1:
                return points[-1]
            else:
                for i in range(len(points)):
                    pose += math.comb(n, i)*np.power(1-t, n-i)*np.power(t, i)*points[i]
            return pose  
        return bezier
    def visualize(self, bezier_function: Callable[[float], list[float, float]], points: list[list[float, float]], steps: int):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        def animate(i):
            #print(b(i/100))
            ax1.clear()
            ax1.plot(bezier_function(i/steps)[0], bezier_function(i/steps)[1], 'o')
            ax1.plot(list(zip(*points))[0], list(zip(*points))[1], 'o')
        ani = animation.FuncAnimation(fig, animate, interval=1, frames=steps)
        # writervideo = animation.FFMpegWriter(fps=60) 
        # ani.save('bezier.mp4', writer=writervideo) 
        plt.show()        
    def save_animation(self, file: str, bezier_function: Callable[[float], list[float, float]], points: list[list[float, float]], steps: int):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        def animate(i):
            #print(b(i/100))
            ax1.clear()
            ax1.plot(bezier_function(i/steps)[0], bezier_function(i/steps)[1], 'o')
            ax1.plot(list(zip(*points))[0], list(zip(*points))[1], 'o')
        ani = animation.FuncAnimation(fig, animate, interval=1, frames=steps)
        writervideo = animation.FFMpegWriter(fps=60) 
        ani.save(file, writer=writervideo) 



