package shrink;

import java.util.ArrayList;

//https://stackoverflow.com/questions/736815/2-bytes-to-short-java

/**
 * Here all the compression and decompression happens.
 * This program uses 1 byte to describe the length of the next block, and 2 bytes for the backward references.
 */
public class LempelZ {
	private static final int REFERENCE_BYTES = 3;
	
	/**
	 * Compress the bytes as much as possible within the limits set by the reference bits.
	 * Complexity: Worst case approximately N (N * 32767 * 127). Best case N (less than worst, as we can skip some after successfully finding a match.)
	 */
	public static byte[] compress(byte[] data) {
		// Would be better to just use a write buffer and write directly. Would use significantly less memory.
		ArrayList<Byte> out = new ArrayList<Byte>();
		
		byte unreplaced = REFERENCE_BYTES;
		int i;
		for (i = REFERENCE_BYTES; i < data.length; i++) {
			boolean found = false;
			short distance = 0;
			byte lengthFound = 0;
			for (short d = 3; d <= i && d < 32767; d++) {
				if (data[i - d] == data[i]) {
					int find;
					for (find = 1; find < d && find < 127 && i + find < data.length;) {	// Poor search algorithm. Could be faster.
						if (data[i + find] == data[i - d + find]) {find++;}
						else {break;}
					}
					if (find > REFERENCE_BYTES && find > lengthFound) {
						found = true;
						lengthFound = (byte)find;
						distance = d;
						if (lengthFound == 127) {break;}
					}
				}
			}
			if (found) {
				if (unreplaced != 0) {
					out.add(unreplaced);
					for (int j = i - unreplaced; j < i; j++) {out.add(data[j]);}
					unreplaced = 0;
				}
				out.add((byte)(-lengthFound));	// REFERENCE_BYTES.
				out.add((byte)(distance & 0xff));
				out.add((byte)((distance >> 8) & 0xff));
				
				byte x0 = (byte)(distance & 0xff), x1 = (byte)((distance >> 8) & 0xff);
				
				System.out.println(i + " Byte data: " + -lengthFound + ", calculated distance: " + ((x0 & 0xff) | ((x1 & 0xff) << 8)) + ", from: " + x0+ "," + x1);
				i += ((int)(lengthFound) - 1);
			}
			else {unreplaced++;}
			if (unreplaced == 127) {
				out.add(unreplaced);
				for (int j = i - unreplaced + 1; j <= i; j++) {out.add(data[j]);}
				unreplaced = 0;
			}
		}
		out.add(unreplaced);
		for (int j = i - unreplaced; j < i; j++) {out.add(data[j]);}
		return listToArray(out);
	}

	/**
	 * Un-compress everything by following the block bits.
	 * If there exists an error in this structure, this probably won't work.
	 * Complexity: Ø(N) where N is the size of the original file.
	 *		If we think in terms of the input, it is still Ø(N),
	 *		as we skip the amount in the extra loop after a reference.
	 */
	public static byte[] decompress(byte[] data) {
		ArrayList<Byte> out = new ArrayList<Byte>();
		for (int i = 0, iOut = 0; i < data.length; i++) {
			byte x = data[i];
			if (x < 0) {
				short distance = (short)((data[i + 1] & 0xff) | ((data[i + 2] & 0xff) << 8));
				int start = iOut;
				for (int j = start - distance; j < start - distance - x; j++) {
					out.add(out.get(j));
					iOut++;
				}
				i += (REFERENCE_BYTES - 1);
			}
			else {
				for (int j = i + 1; j <= i + x && j < data.length; j++) {
					out.add(data[j]);
					iOut++;
				}
				i += (int)x;
			}
		}
		return listToArray(out);
	}
	
	/**
	 * Make the ArrayList of bytes into a standard byte[]. Ø(N). Could just use java method for this (.toArray).
	 */
	private static byte[] listToArray(ArrayList<Byte> out) {
		int length = out.size();
		byte[] result = new byte[length];
		for (int i = 0; i < length; i++) {result[i] = out.get(i);}
		return result;
	}
}
