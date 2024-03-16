package com.eaglerobotics.app;
import java.awt.geom.Point2D;
import java.lang.Math;
/**
 * Hello world!
 *
 */


public class App 
{
    public static long factorial(long n) throws RuntimeException {
        if (n > 20) {
            throw new RuntimeException("Factorial too large for long...");
        }
        if (n<=0) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
    public static long nCr(long n, long k) {
        System.out.printf("Numerator: %s\n", factorial(n));
        System.out.printf("Denominator: %s\n", factorial(k)*factorial(n-k));
        return factorial(n)/(factorial(k)*factorial(n-k));
    }
    public static BezierFunction computeBezier(Point2D.Double[] points) {
        System.out.printf("Length of points: %s\n", points.length);
        int n = points.length - 1;
        return t -> {
            Point2D.Double pose = new Point2D.Double(0.0, 0.0);
            if (t <= 0.0) {
                return points[0];
            } else if (t >= 1.0) {
                return points[points.length - 1];
            } else {
                for (int i=0; i<points.length; i++) {
                    System.out.printf("%s, %s, %s\n", n, i, nCr(n, i));
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
        Point2D.Double[] points = {new Point2D.Double(1.98, 1.98), new Point2D.Double(2.64, 1.98), new Point2D.Double(3.3, 1.98), new Point2D.Double(3.96, 1.98), new Point2D.Double(4.62, 1.98), new Point2D.Double(5.28, 1.98), new Point2D.Double(5.94, 1.98), new Point2D.Double(6.6, 2.64), new Point2D.Double(6.6, 3.3), new Point2D.Double(6.6, 3.96), new Point2D.Double(6.6, 4.62), new Point2D.Double(6.6, 5.28), new Point2D.Double(6.6, 5.94), new Point2D.Double(6.6, 6.6)};
        System.out.println(factorial(21));
        // BezierFunction bezier = computeBezier(points);
        // System.out.println(bezier.apply(0.31415));
        // for (int i=0; i < 10; i++) {
        //   System.out.printf("%s, %s\n", i/10.0, bezier.apply(i/10.0));
        // }
    }
}
