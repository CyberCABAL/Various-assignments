package shrink;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

/**
 * Even though the task demands the programs to be separate, they do have much in common.
 * Similar elements are gathered here.
 */
class ClientCommon {
	/**
	 * Which files to use?
	 */
	static File[] readInput() {
		File[] f = new File[2];
		Scanner s = new Scanner(System.in);
		System.out.print("Enter input file name: ");
		f[0] = new File(s.nextLine());
		System.out.print("Enter output file name: ");
		f[1] = new File(s.nextLine());
		s.close();
		return f;
	}

	/**
	 * Put the result somewhere.
	 */
	static void output(File f, byte[] data) {
		if (data == null) {return;}
		if (f.exists()) {FileScanner.writeFile(f.getPath(), data);}
		else {
			try {f.createNewFile();} catch (IOException e) {e.printStackTrace();}
			FileScanner.writeFile(f.getPath(), data);
		}
	}
}