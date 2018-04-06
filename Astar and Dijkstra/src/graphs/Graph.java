package graphs;

import java.io.File;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Graph {
	private Vertex[] vertices;
	final static int INFINITE = 2147483640;
	static int maxSpeed = 110;	// km/h
	final static double HAVER_CONSTANT = 12742 * (360000 / maxSpeed);
	private TextReader tr = new TextReader();
	private int vertexAmount;

	public Graph() {}

	public void createVertices(double[][] coords) {
		int amount = coords.length;
		vertices = new Vertex[amount];
		for (int i = 0; i < amount; i++) {vertices[i] = new Vertex(i, new Coordinate(coords[i]));}
	}

	public void readMapFile(String vertexFile, String edgeFile) {
		tr.f = new File(vertexFile);
		createVertices(tr.loadMapVertices(2));
		System.out.println("Vertices loaded.");
		
		tr.f = new File(edgeFile);
		loadGraph(tr.loadMapEdges(3));
		System.out.println("Edges loaded.\nMap loaded.");
	}

	void loadGraph(int[][] data) {
		for (int i = 0; i < data.length; i++) {
			vertices[data[i][0]].connections.add(new WConnection(vertices[data[i][1]], data[i][2]));
		}
	}
	
	/**
	 * Allow to run the program again without also reading files again.
	 */
	void refresh() {
		for (Vertex v : vertices) {
			v.past = null;
			v.distance = INFINITE;
		}
	}

	/**
	 * @param dijkstra disable distance estimate and turn the algorithm into dijkstra.
	 */
	public void aStar(int startVertex, int endVertex, boolean dijkstra) {
		PriorityQueue<Vertex> pq = setup(startVertex);
		vertexAmount = 0;

		Vertex v, end = vertices[endVertex];
		// Can be optimised to prevent processing the same vertex too many times.
		while ((v = pq.poll()) != null && !v.equals(end)) {
			if (v.distance != INFINITE) {
				WConnection w;
				for (int i = 0; i < v.connections.size(); i++) {
					w = v.connections.get(i);
					if (!dijkstra && w.v.estimate == 0) {w.v.estimate = haversine(w.v.location, end.location);}
					int newDist = v.distance + w.weight;
					if (newDist < w.v.distance || w.v.distance == INFINITE) {
						w.v.distance = newDist;
						w.v.past = v;
						pq.add(w.v);
					}
				}
				vertexAmount++;
			}
		}
	}

	private PriorityQueue<Vertex> setup(int startVertex) {
		vertices[startVertex].distance = 0;
		PriorityQueue<Vertex> pq = new PriorityQueue<Vertex>(new CompareVDistance());
		pq.add(vertices[startVertex]);
		return pq;
	}
	
	/**
	 * Estimate function for surface of a sphere.
	 */
	private int haversine(Coordinate c0, Coordinate c1) {
		double sin0 = Math.sin((c0.xR - c1.xR) / 2), sin1 = Math.sin((c0.yR - c1.yR) / 2);
		return (int) (HAVER_CONSTANT * Math.asin(Math.sqrt(sin0 * sin0 + c0.cosX * c1.cosX * sin1 * sin1)));
	}
	
	/**
	 * After search is done, get the path.
	 */
	private void findPath(int end) {
		Vertex v = vertices[end];
		String[] output = new String[vertexAmount];
		int i = 0;
		do {
			output[i++] = v.location.toString() + "\n";
			System.out.println(v.location);
		} while ((v = v.past) != null);
		System.out.println("Time: " + timeSplit(vertices[end].distance / 100) + "\nVertices: " + vertexAmount);
		Output.output(output);
	}
	
	private String timeSplit(int time) {
		int h = (int)(time / 3600);
		time -= h * 3600;
		int min = (int)(time / 60);
		time -= min * 60;
		int sec = (int)(time);
		return h + " h " + min + " min " + sec + " sec.";
	}

	public static void main(String[] args) {
		Graph g = new Graph();
		Scanner s = new Scanner(System.in);
		System.out.println("Enter vertex file name, then edge file name: ");
		g.readMapFile(s.nextLine(), s.nextLine());
		
		System.out.println("Enter 0 to stop, 1 for A*, 2 for Dijkstra.");
		int control;
		while ((control = s.nextInt()) > 0) {
			boolean dijkstra = (control == 2);
			System.out.println(((control == 1) ? "(A*)" : (dijkstra ? "(Dijkstra)" : "")) + " Enter start vertex, then end vertex: ");
			int sV = s.nextInt(), sE = s.nextInt();
			long start = System.currentTimeMillis();
			g.aStar(sV, sE, dijkstra);
			long end = System.currentTimeMillis();
			g.findPath(sE);
			System.out.println("Time (ms): " + (end - start));
			g.refresh();
		}
		s.close();
	}
}