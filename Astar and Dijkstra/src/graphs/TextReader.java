package graphs;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.File;

/**
 * Read various files.
 */
public class TextReader {
	File f = null;
	private int lineAmount;
	
	public TextReader() {}

	public TextReader(String file) {f = new File(file);}
	
	public int[][] loadMapEdges(int dataLength) {
		try (BufferedReader br = new BufferedReader(new FileReader(f))) {
			lineAmount = Integer.parseInt(hSplit(br.readLine(), 1, 0)[0]);
			int[][] data = new int[lineAmount][dataLength];
			
			String l = null;
			int i = 0;
			for (String[] temp; (l = br.readLine()) != null; i++) {
				temp = hSplit(l, dataLength, 0);
				for (int j = 0; j < temp.length; j++) {data[i][j] = Integer.parseInt(temp[j]);}
			}
			System.out.println("Edges read.");
			return data;
		}
		catch (IOException e) {e.printStackTrace();}
		return null;
	}
	
	public double[][] loadMapVertices(int dataLength) {
		try (BufferedReader br = new BufferedReader(new FileReader(f))) {
			lineAmount = Integer.parseInt(hSplit(br.readLine(), 1, 0)[0]);
			double[][] data = new double[lineAmount][dataLength];
			
			String l = null;
			int i = 0;
			for (String[] temp; (l = br.readLine()) != null; i++) {
				temp = hSplit(l, dataLength, 1);
				for (int j = 0; j < temp.length; j++) {data[i][j] = Double.parseDouble(temp[j]);}
			}
			System.out.println("Vertices read.");
			return data;
		}
		catch (IOException e) {e.printStackTrace();}
		return null;
	}
	
	// Teacher's split method lightly modified
	private String[] hSplit(String line, int amount, int start) {
		int j = 0, length = line.length();
		String[] fields = new String[amount];
		
		for (int i = 0; i < amount - start; ++i) {
			while (line.charAt(j) <= ' ') {++j;}
			if (start > 0) {
				start--;
				while (line.charAt(j) > ' ') {++j;}
				i--;
			}
			else {
				int s = j;
				while (j < length && line.charAt(j) > ' ') {++j;}
				fields[i] = line.substring(s, j);
			}
		}
		return fields;
	}
}
