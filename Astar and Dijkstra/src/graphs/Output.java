package graphs;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Output {
	static File f = new File("output.txt");
	
	// Write result.
	public static void output(String[] text) {
		try (BufferedWriter bw = new BufferedWriter(new FileWriter(f, true))) {
			for (int i = 0; i < text.length; i++) {if (text[i] != null) {bw.write(text[i]);}}
		}
		catch (IOException e) {e.printStackTrace();}
	}
}