package com.eaglerobotics.app;

public class Node
{
    public double x, y;
    public boolean obstacle;
    public Node parent = null;

    private double g_cost, h_cost, f_cost;

    public Node(double _x, double _y, boolean _obstacle) {
        x = _x;
        y = _y;
        obstacle = _obstacle;
    }

    public void set_g_cost(double _g_cost) {
        g_cost = _g_cost;
    }
    public void set_h_cost(double _h_cost) {
        h_cost = _h_cost;
    }
    public double get_f_cost() {
        return h_cost + g_cost;
    }
    public double get_g_cost() {
        return g_cost;
    }
    public double get_h_cost() {
        return h_cost;
    }

    public void set_parent(Node _parent) {
        parent = _parent;
    }
    public Double[] getLocation() {
        Double[] location = {x, y};
        return location;
    }

    public Node toNearestGrid(Double[] objectSize) {
        x -= x%objectSize[0];
        y -= y%objectSize[1];
        x = Math.round(x*1000.0)/1000.0;
        y = Math.round(y*1000.0)/1000.0;
        return this;
    }
}


