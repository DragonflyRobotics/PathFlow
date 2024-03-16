import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import warnings

from pathflow.motionplanning import Bezier

class A_Star:
    def __init__(self, object_size: tuple[int, int], grid_size: tuple[int, int]) -> None:
        warnings.warn("The Python implementation does not yet support floating point grids or locations!")
        self.object_size = object_size
        self.grid_size = grid_size
        self.grid = []
        for i in range(object_size[0], grid_size[0], object_size[0]):
            for j in range(object_size[1], grid_size[1], object_size[1]):
                self.grid.append(Point([i, j], False))
        self.fig, self.ax1 = plt.subplots()
        self.obstacleRects = []
    def findPointOnGrid(self, point):
        for g in self.grid:
            if g.location == point.location:
                return g
        return None
    def _drawGrid(self):
        rect = patches.Rectangle((0, 0), self.grid_size[0], self.grid_size[1], linewidth=1, edgecolor='blue', facecolor='none')
        self.ax1.add_patch(rect)
        for g in self.grid:
            if g.obstacle:
                plt.plot(g.location[0], g.location[1], 'o', color='r')
            else:
                plt.plot(g.location[0], g.location[1], 'o', color='b')
    def _getNeighbors(self, point):
        neighbors = []
        location = point.location
        neighbors.append([location[0]+self.object_size[0], location[1]])
        neighbors.append([location[0]-self.object_size[0], location[1]])
        neighbors.append([location[0], location[1]+self.object_size[1]])
        neighbors.append([location[0], location[1]-self.object_size[1]])
        neighbors.append([location[0]-self.object_size[0], location[1]-self.object_size[1]])
        neighbors.append([location[0]+self.object_size[0], location[1]+self.object_size[1]])
        for n in neighbors:
            if self.findPointOnGrid(Point(n)) != None and self.findPointOnGrid(Point(n)).obstacle == False:
                yield self.findPointOnGrid(Point(n))
    def _getDistance(self, pointA, pointB):
        coordA = pointA.location
        coordB = pointB.location
        xDist = abs(coordA[0]-coordB[0])
        yDist = abs(coordA[1]-coordB[1])
        return 14*min(xDist, yDist) + 10*abs(yDist-xDist)
 
    def visualize(self, path, steps):
        b = Bezier()
        func = b.compute_bezier(path)
        trailx = []
        traily = []
        def animate(i):
            #print(b(i/100))
            self.ax1.clear()
            for r in self.obstacleRects:
                self.ax1.add_patch(r)
            self._drawGrid()
            self.ax1.plot(func(i/steps)[0], func(i/steps)[1], 'o', color='purple')
            trailx.append(func(i/steps)[0])
            traily.append(func(i/steps)[1])
            self.ax1.plot(trailx, traily, '--', color='black')
            self.ax1.plot(list(zip(*path))[0], list(zip(*path))[1], 'o', color='green')
        ani = animation.FuncAnimation(self.fig, animate, interval=1, frames=steps, repeat=False)
        # writervideo = animation.FFMpegWriter(fps=60) 
        # ani.save('bezier.mp4', writer=writervideo) 
        #plt.show()
        plt.draw()
        plt.waitforbuttonpress(0) # this will wait for indefinite time
        plt.close(self.fig)

    def rectangularObstacle(self, topLeft: list[float, float], bottomRight: list[float, float]):
        rect = patches.Rectangle(topLeft, bottomRight[0]-topLeft[0], bottomRight[1]-topLeft[1], linewidth=1, edgecolor='red', facecolor='red')
        self.obstacleRects.append(rect)
        for g in self.grid:
            gCoord = g.location
            print(gCoord)
            if gCoord[0] >= topLeft[0] and gCoord[0] <= bottomRight[0]:
                if gCoord[1] >= bottomRight[1] and gCoord[1] <= topLeft[1]:
                    g.obstacle = True



    def compute(self, start_point, end_point):
        start_point = self.findPointOnGrid(Point(start_point))
        end_point = self.findPointOnGrid(Point(end_point))
        for g in self.grid:
            g.fcost = 0
            g.gcost = 0
            g.hcost = 0
        start_point.gcost = 0
        open = [start_point]
        closed = []

        count = 0

        while len(open) > 0:
            current_node = open[0]
            for i in range(1, len(open)):
                if (open[i].fcost < current_node.fcost or (open[i].fcost == current_node.fcost and open[i].hcost < current_node.hcost)):
                    current_node = open[i]
            open.remove(current_node)
            closed.append(current_node)

            if (current_node == end_point):
                path = [end_point.location]
                currentNode = end_point
                while currentNode.parent != None:
                    path.append(currentNode.parent.location)
                    currentNode = currentNode.parent

                return list(reversed(path))
            for n in list(self._getNeighbors(current_node)):
                if n in closed:
                    continue
                newMoveCostToNeighbor = current_node.gcost + self._getDistance(current_node, n)
                if n.gcost == None or newMoveCostToNeighbor < n.gcost or n not in open:
                    n.gcost = newMoveCostToNeighbor
                    n.hcost = self._getDistance(n, end_point)
                    n.fcost = n.gcost + n.hcost
                    n.parent = current_node
                    if n not in open:
                        open.append(n)









# object_size = (1,1)
# grid_size = (5,5)
# grid = []



class Point:
    def __init__(self, location, obstacle=False) -> None:
        self.location = location
        self.obstacle = obstacle
        self.gcost = None
        self.hcost = None
        self.fcost = None
        self.parent = None
        pass



#obstacles = [[2,3], [3,3], [4,3]]
#for o in obstacles:
#    findPointOnGrid(grid, Point(o)).obstacle = True





#    print(open)




#end = a_star(findPointOnGrid(grid, Point([1,1])), findPointOnGrid(grid, Point([2,4])))
#path = [end.location]
#currentNode = end
#while currentNode.parent != None:
#    print(currentNode.parent.location)
#    path.append(currentNode.parent.location)
#    currentNode = currentNode.parent

#path = list(reversed(path))
#xs = list(zip(*path))[0]
#ys = list(zip(*path))[1]

#import numpy as np
#import matplotlib.animation as animation
#import math
#def compute_bezier(points):
#    points = np.array(points)
#    n = len(points) - 1
#    def bezier(t):
#        # print(t)
#        pose = np.array([0.0, 0.0])
#        if t<=0:
#            return points[0]
#        elif t>=1:
#            return points[-1]
#        else:
#            for i in range(n+1):
#                print(i)
#                # print(n, i)
#                pose += math.comb(n, i)*np.power(1-t, n-i)*np.power(t, i)*points[i]
#        return pose  
#    return bezier

#b = compute_bezier(path)
## print(b(0.31415))
#def animate(i):
#    #print(b(i/100))
#    ax.clear()
#    drawGrid(grid)
#    plt.plot(xs, ys, '-')
#    ax.plot(b(i/100)[0], b(i/100)[1], 'o')
#    ax.plot(list(zip(*path))[0], list(zip(*path))[1], 'o')
#    # ax1.plot(xar,yar)
#ani = animation.FuncAnimation(fig, animate, interval=1, frames=100)
#writervideo = animation.FFMpegWriter(fps=60) 
#ani.save('bezier.mp4', writer=writervideo) 
#plt.show()





#plt.show()

