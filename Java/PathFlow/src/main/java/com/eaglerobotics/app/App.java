package com.eaglerobotics.app;
import java.awt.geom.Point2D;
import java.lang.Math;
/**
 * Hello world!
 *
 */


public class App 
{
    public static int factorial(int n){
        if (n<=1) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
    public static int nCr(int n, int k) {
        return factorial(n)/(factorial(k)*factorial(n-k));
    }
    public static BezierFunction computeBezier(Point2D.Double[] points) {
        int n = points.length - 1;
        return t -> {
            Point2D.Double pose = new Point2D.Double(0.0, 0.0);
            if (t <= 0.0) {
                return points[0];
            } else if (t >= 1.0) {
                return points[points.length - 1];
            } else {
                for (int i=0; i<points.length; i++) {
                    double X = nCr(n, i) * Math.pow(1-t, n-i) * Math.pow(t, i) * points[i].getX();
                    double Y = nCr(n, i) * Math.pow(1-t, n-i) * Math.pow(t, i) * points[i].getY();
                    pose = new Point2D.Double(pose.getX()+X, pose.getY()+Y);
                }
                return pose;
            }
        };
    }
 
    @FunctionalInterface
    interface BezierFunction {
        Point2D.Double apply(double t);
    }

    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
        Point2D.Double[] points = {new Point2D.Double(0, 0), new Point2D.Double(1, 1), new Point2D.Double(2, 0)};
        BezierFunction bezier = computeBezier(points);
        System.out.println(bezier.apply(0.4));
    }
}
