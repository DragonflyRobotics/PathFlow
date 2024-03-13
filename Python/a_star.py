from functools import cache
from math import sqrt
from os import remove
import matplotlib.pyplot as plt
import matplotlib.patches as patches

object_size = (1,1)
grid_size = (5,5)
grid = []

fig, ax = plt.subplots()


class Point:
    def __init__(self, location, obstacle=False) -> None:
        self.location = location
        self.obstacle = obstacle
        self.gcost = None
        self.hcost = None
        self.fcost = None
        self.parent = None
        pass


def findPointOnGrid(grid, point):
    for g in grid:
        if g.location == point.location:
            return g
    return None


for i in range(object_size[0], grid_size[0], object_size[0]):
    for j in range(object_size[1], grid_size[1], object_size[1]):
        grid.append(Point([i, j], False))

obstacles = [[2,3], [3,3], [4,3]]
for o in obstacles:
    findPointOnGrid(grid, Point(o)).obstacle = True


def drawGrid(grid):
    rect = patches.Rectangle((0, 0), grid_size[0], grid_size[1], linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    for g in grid:
        if g.obstacle:
            plt.plot(g.location[0], g.location[1], 'o', color='r')
        else:
            plt.plot(g.location[0], g.location[1], 'o', color='b')

def getNeighbors(grid, point, object_size):
    neighbors = []
    location = point.location
    print(f"Finding neighbors of {location}")
    neighbors.append([location[0]+object_size[0], location[1]])
    neighbors.append([location[0]-object_size[0], location[1]])
    neighbors.append([location[0], location[1]+object_size[1]])
    neighbors.append([location[0], location[1]-object_size[1]])
    neighbors.append([location[0]-object_size[0], location[1]-object_size[1]])
    neighbors.append([location[0]+object_size[0], location[1]+object_size[1]])
    for n in neighbors:
        if findPointOnGrid(grid, Point(n)) != None and findPointOnGrid(grid, Point(n)).obstacle == False:
            print(f"Found {n}")
            yield findPointOnGrid(grid, Point(n))


def getDistance(pointA, pointB):
    coordA = pointA.location
    coordB = pointB.location
    xDist = abs(coordA[0]-coordB[0])
    yDist = abs(coordA[1]-coordB[1])
    return 14*min(xDist, yDist) + 10*abs(yDist-xDist)


def a_star(start_point, end_point):
    start_point.gcost = 0
    open = [start_point]
    closed = []

    count = 0

    while len(open) > 0:
        print(f"ENTER: {count}")
        current_node = open[0]
        for i in range(1, len(open)):
            if (open[i].fcost < current_node.fcost or (open[i].fcost == current_node.fcost and open[i].hcost < current_node.hcost)):
                current_node = open[i]
        open.remove(current_node)
        closed.append(current_node)

        if (current_node == end_point):
            return end_point
        for n in list(getNeighbors(grid, current_node, object_size)):
            if n in closed:
                continue
            newMoveCostToNeighbor = current_node.gcost + getDistance(current_node, n)
            if n.gcost == None or newMoveCostToNeighbor < n.gcost or n not in open:
                n.gcost = newMoveCostToNeighbor
                n.hcost = getDistance(n, end_point)
                n.fcost = n.gcost + n.hcost
                n.parent = current_node
                if n not in open:
                    open.append(n)


    print(open)




end = a_star(findPointOnGrid(grid, Point([1,1])), findPointOnGrid(grid, Point([2,4])))
path = [end.location]
currentNode = end
while currentNode.parent != None:
    print(currentNode.parent.location)
    path.append(currentNode.parent.location)
    currentNode = currentNode.parent

path = list(reversed(path))
xs = list(zip(*path))[0]
ys = list(zip(*path))[1]

import numpy as np
import matplotlib.animation as animation
import math
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

b = compute_bezier(path)
# print(b(0.31415))
def animate(i):
    #print(b(i/100))
    ax.clear()
    drawGrid(grid)
    plt.plot(xs, ys, '-')
    ax.plot(b(i/100)[0], b(i/100)[1], 'o')
    ax.plot(list(zip(*path))[0], list(zip(*path))[1], 'o')
    # ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1, frames=100)
writervideo = animation.FFMpegWriter(fps=60) 
ani.save('bezier.mp4', writer=writervideo) 
plt.show()





plt.show()

