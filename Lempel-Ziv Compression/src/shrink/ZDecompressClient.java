package shrink;

import java.io.File;

/**
 * Clients make the programs separate, like the task demands.
 */
public class ZDecompressClient {
	public static void main(String[] args) {
		System.out.println("Decompression.");
		File[] f = ClientCommon.readInput();
		
		byte[] data = null;
		if (f[0].exists()) {data = LempelZ.decompress(FileScanner.loadFile(f[0].getPath()));}
		else {System.out.println("Input file does not exist.");}
		
		ClientCommon.output(f[1], data);
		System.out.println("Decompression complete.");
	}
}