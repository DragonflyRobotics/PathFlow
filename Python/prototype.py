import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

points = [[0,0],[1,1], [2,0]]

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def compute_bezier(points):
    points = np.array(points)
    n = len(points) - 1
    def bezier(t):
        # print(t)
        pose = np.array([0.0, 0.0])
        if t<=0:
            return points[0]
        elif t>=1:
            return points[-1]
        else:
            for i in range(n+1):
                print(i)
                # print(n, i)
                pose += math.comb(n, i)*np.power(1-t, n-i)*np.power(t, i)*points[i]
        return pose  
    return bezier

b = compute_bezier(points)
print(b(0.4))
def animate(i):
    # print(b(i/100))
    ax1.clear()
    ax1.plot(b(i/10)[0], b(i/10)[1], 'o')
    ax1.plot(list(zip(*points))[0], list(zip(*points))[1], 'o')
    # ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=100)
# plt.show()


