package graphs;

public class WConnection {
	Vertex v;
	int weight;

	public WConnection(Vertex v, int weight) {
		this.v = v;
		this.weight = weight;
	}
	
	public boolean equals(Object o) {
		if (o == null) {return false;}
		if (!(o instanceof WConnection)) {return false;}
		WConnection w = (WConnection) o;
		return v.equals(w.v);
	}
}