package graphs;

import java.util.ArrayList;

public class Vertex {
	private final int num;
	int distance = Graph.INFINITE;
	Vertex past = null;
	Coordinate location = null;
	int estimate = 0;	// Estimated distance to goal
	ArrayList<WConnection> connections = new ArrayList<WConnection>();
	
	public Vertex(int num) {this.num = num;}
	
	public Vertex(int num, Coordinate location) {
		this.location = location;
		this.num = num;
	}

	public int getNum() {return num;}
	
	public Coordinate getLocation() {return location;}
	public void setLocation(Coordinate location) {this.location = location;}

	public boolean equals(Object o) {
		if (o == null) {return false;}
		if (!(o instanceof Vertex)) {return false;}
		Vertex n = (Vertex) o;
		return num == n.getNum();
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < connections.size(); i++) {sb.append(connections.get(i).v.getNum() + "\n");}
		return "Vertex: " + num + "\nConnections:\n" + sb.toString() + "\n";
	}
	
	String getVertexData() {
		StringBuilder sb = new StringBuilder();
		sb.append("Vertex: " + num + ", Previous: ");
		if (past != null) {sb.append("" + past.getNum());}
		else {sb.append("None");}
		if (distance == Graph.INFINITE) {sb.append(", Distance: Eternal\n");}
		else {sb.append(", Distance: " + distance + "\n");}
		return sb.toString();
	}
}