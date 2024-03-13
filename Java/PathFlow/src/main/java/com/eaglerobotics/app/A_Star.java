package com.eaglerobotics.app;
import java.lang.Math;
import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

/**
 * Hello world!
 *
 */


public class A_Star 
{
    private List<Node> grid = new ArrayList<Node>();
    private Double[] object_size;
    private Double[] grid_size;

    public A_Star(Double[] _object_size, Double[] _grid_size) {
        object_size = _object_size;
        grid_size = _grid_size;

        for (double i=object_size[0]; i<grid_size[0]; i+=object_size[0]) {
            for (double j=object_size[1]; j<grid_size[1]; j+=object_size[1]) {
                // System.out.printf("%s, %s\n", Math.round(1000.0*i)/1000.0, Math.round(1000.0*j)/1000.0);
                grid.add(new Node(round(i), round(j), false));
            }
        }
    }

    private Node findPointOnGrid(Node node) {
        for (Node g : grid) {
            if (Arrays.equals(g.getLocation(), node.getLocation())) {
                return g;
            }
        }
        return null;
    }

    private double round(double x) {
        return Math.round(1000.0*x)/1000.0;
    }

    private List<Node> getNeighbors(Node point) {
        List<Double[]> neighbors = new ArrayList<Double[]>();
        List<Node> final_neighbors = new ArrayList<Node>();
        Double[] location = point.getLocation();
        // System.out.printf("Computing Neighbors for (%s, %s)\n", location[0], location[1]);
        neighbors.add(new Double[] {round(location[0]+object_size[0]), round(location[1])});
        neighbors.add(new Double[] {round(location[0]-object_size[0]), round(location[1])});
        neighbors.add(new Double[] {round(location[0]), round(location[1]+object_size[1])});
        neighbors.add(new Double[] {round(location[0]), round(location[1]-object_size[1])});
        neighbors.add(new Double[] {round(location[0]-object_size[0]), round(location[1]-object_size[1])});
        neighbors.add(new Double[] {round(location[0]+object_size[0]), round(location[1]+object_size[1])});
        for (Double[] n : neighbors) {
            Node g = findPointOnGrid(new Node(n[0], n[1], false));
            if (g != null && g.obstacle == false) {
                // System.out.printf("Found neighbor (%s %s)\n", g.getLocation()[0], g.getLocation()[1]);
                final_neighbors.add(g);
            }
        }
        return final_neighbors;
    }

    private double getDistance(Node pointA, Node pointB) {
        Double[] coordA = pointA.getLocation();
        Double[] coordB = pointB.getLocation();
        double xDist = Math.abs(coordA[0] - coordB[0]);
        double yDist = Math.abs(coordA[1] - coordB[1]);
        return 14 * Math.min(xDist, yDist) + 10 * Math.abs(xDist - yDist);
    }

    public List<Node> compute(Node startNode, Node endNode) throws RuntimeException {
        startNode = findPointOnGrid(startNode.toNearestGrid(object_size));
        endNode = findPointOnGrid(endNode.toNearestGrid(object_size));
        System.out.println(Arrays.deepToString(startNode.getLocation()));
        System.out.println(Arrays.deepToString(endNode.getLocation()));
        if (startNode == null || startNode.obstacle) {
            throw new RuntimeException("Invalid Start Node!!!");
        }
        if (endNode.obstacle || endNode == null) {
            throw new RuntimeException("Invalid End Node!!!");
        }
        startNode.set_g_cost(0.0);
        List<Node> open = new ArrayList<Node>();
        open.add(startNode);
        List<Node> closed = new ArrayList<Node>();

        while (open.size() > 0) {
            Node currentNode = open.get(0);
            for (int i=1; i<open.size(); i++) {
                if (open.get(i).get_f_cost() < currentNode.get_f_cost() || (open.get(i).get_f_cost() == currentNode.get_f_cost() && open.get(i).get_h_cost() < currentNode.get_h_cost())) {
                    currentNode = open.get(i);
                }
            }
            open.remove(currentNode);
            closed.add(currentNode);

            // System.out.println(Arrays.deepToString(currentNode.getLocation()));

            if (currentNode == endNode) {
                Node lastNode = endNode;
                List<Node> chain = new ArrayList<Node>();
                while (lastNode.parent != null) {
                    chain.add(lastNode);
                    // System.out.println(Arrays.deepToString(lastNode.getLocation()));
                    lastNode = lastNode.parent;
                }
                chain.add(startNode);
                chain = chain.reversed();
                return chain;
            }

            for (Node n : getNeighbors(currentNode)) {
                if (closed.contains(n)) {
                    continue;
                }
                double newMoveToNeighborCost = currentNode.get_g_cost() + getDistance(currentNode, n);
                if (newMoveToNeighborCost < n.get_g_cost() || !open.contains(n)) {
                    n.set_g_cost(newMoveToNeighborCost);
                    n.set_h_cost(getDistance(n, endNode));
                    n.set_parent(currentNode);
                    if (!open.contains(n)) {
                        open.add(n);
                    }
                }
            }
        }
        // return new ArrayList<Node>();
        throw new RuntimeException("No path found");
    }

    public Double[][] nodeListToDouble(List<Node> path) {
        Double[][] finalList = new Double[path.size()][2];
        for (int i=0; i<path.size(); i++) {
            Double[] point = {path.get(i).getLocation()[0], path.get(i).getLocation()[1]};
            finalList[i] = point;
        }
        return finalList;
    }

    public void rectangularObstacle(Double[] topLeft, Double[] bottomRight) {
        for (Node g : grid) {
            Double[] gCoord = g.getLocation();
            if (gCoord[0] >= topLeft[0] && gCoord[0] <= bottomRight[0]) {
                if (gCoord[1] >= bottomRight[1] && gCoord[1] <= topLeft[1]) {
                    g.obstacle = true;
                    // System.out.printf("Obstacle at (%s, %s)\n", g.getLocation()[0], g.getLocation()[1]);
                }
            }
        }
    }

    public static void main( String[] args )
    {
        System.out.println( "Hello World from A*!" );
        Double[] o = {0.66,0.66};
        Double[] g = {8.2,16.0};
        A_Star a = new A_Star(o, g);
        // System.out.println(a.getNeighbors(new Node(1, 1, false)));
        // System.out.println(a.getDistance(new Node(1, 1, false), new Node(6, 3, false)));
        // a.rectangularObstacle(new Double[] {2.0,3.0}, new Double[] {4.0,3.0});
        System.out.println(Arrays.deepToString(a.nodeListToDouble(a.compute(new Node(1,1,false), new Node(2,4,false)))));
    }
}
