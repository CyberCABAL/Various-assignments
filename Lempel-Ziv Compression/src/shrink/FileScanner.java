package shrink;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class FileScanner {
	/**
	 * Read every byte of the file. Buffers could be used to save memory.
	 */
	public static byte[] loadFile(String path) {
		try {return Files.readAllBytes(Paths.get(path));}
		catch (IOException e) {return null;}
	}
	
	/**
	 * Write every byte of the file. Buffers could be used to save memory.
	 */
	public static boolean writeFile(String path, byte[] data) {
		try {Files.write(Paths.get(path), data);}
		catch (IOException e) {return false;}
		return true;
	}
}