package graphs;

import java.util.Comparator;

public class CompareVDistance implements Comparator<Vertex> {

	@Override
	public int compare(Vertex arg0, Vertex arg1) {
		int dist0 = arg0.distance + arg0.estimate, dist1 = arg1.distance + arg1.estimate;
		if (dist0 > dist1) {return 1;}
		else if (dist0 < dist1) {return -1;}
		else {return 0;}
	}
}