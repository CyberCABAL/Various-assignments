package shrink;

import java.io.File;

/**
 * Clients make the programs separate, like the task demands.
 */
public class ZCompressClient {
	public static void main(String[] args) {
		System.out.println("Compression.");
		File[] f = ClientCommon.readInput();
		
		byte[] data = null;
		byte[] file = FileScanner.loadFile(f[0].getPath());
		int init = file.length;
		if (f[0].exists()) {data = LempelZ.compress(file);}
		else {System.out.println("Input file does not exist.");}
		file = null;
		
		ClientCommon.output(f[1], data);
		System.out.println("Compression complete.");
		System.out.println("Result: " + init + " bytes compressed to " + data.length + " bytes. Difference: " + (init - data.length) + " bytes.");
	}
}