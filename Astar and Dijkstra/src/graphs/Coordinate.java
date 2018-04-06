package graphs;

public class Coordinate {
	// Makes program go faster by only computing cos once.
	public double x, y, xR, yR, cosX;
	private final static double RADIANS = (Math.PI / 180);
	
	Coordinate(double[] xy) {
		this.x = xy[0];
		this.y = xy[1];
		this.xR = RADIANS * x;
		this.yR = RADIANS * y;
		this.cosX = Math.cos(this.xR);
	}	// Two coordinates.
	
	public String toString() {return x + "," + y;}
}