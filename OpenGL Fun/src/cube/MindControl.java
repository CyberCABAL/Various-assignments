package cube;

import java.awt.Dimension;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import com.jogamp.opengl.GL2;
import com.jogamp.opengl.GLAutoDrawable;
import com.jogamp.opengl.GLEventListener;
import com.jogamp.opengl.awt.GLCanvas;
import com.jogamp.opengl.glu.GLU;
import com.jogamp.opengl.util.FPSAnimator;

@SuppressWarnings("serial")
public class MindControl extends GLCanvas implements GLEventListener {

	private static final int WIDTH = 800, HEIGHT = 600, FPS_MAX = 30;
	private GLU glu = new GLU();

	private double camera = 0, rot0 = 0, rot1 = 0;

	double rotate = 0, cubes = 12;

	boolean invert = false;

	public MindControl() {this.addGLEventListener(this);}

	public float[][] verts = {
			{-1.0f, -1.0f, -1.0f}, // 0
			{1.0f, -1.0f, -1.0f}, // 1
			{1.0f, 1.0f, -1.0f}, // 2
			{-1.0f, 1.0f, -1.0f}, // 3
			{-1.0f, 1.0f, 1.0f}, // 4
			{1.0f, 1.0f, 1.0f}, // 5
			{1.0f, -1.0f, 1.0f}, // 6
			{-1.0f, -1.0f, 1.0f} // 7
	};

	float[][] v3D = {{10.0f, 0.0f, 0.0f}, {0.0f, 10.0f, 0.0f}, {0.0f, 0.0f, 10.0f}};

	public float[][][] drawVerts = {
			{verts[0], verts[1], verts[2], verts[3]}, // Bottom
			{verts[0], verts[1], verts[6], verts[7]},
			{verts[1], verts[2], verts[5], verts[6]},
			{verts[2], verts[3], verts[4], verts[5]},
			{verts[3], verts[0], verts[7], verts[4]},
			{verts[4], verts[5], verts[6], verts[7]} // Top
	};

	public float[][] colours = {
			{1.0f, 0.0f, 0.0f},
			{0.0f, 1.0f, 0.0f},
			{0.0f, 0.0f, 1.0f},
			{1.0f, 0.0f, 1.0f},
			{1.0f, 1.0f, 0.0f},
			{0.0f, 1.0f, 1.0f}
	};

	public float[] coloursB = {1.0f, 0.35f, 0.0f, 0.0f};

	public float[][] invertC = {
			{1.0f, 0.0f, 0.0f},
			{0.0f, 1.0f, 0.0f},
			{0.0f, 0.0f, 1.0f},
			{1.0f, 0.0f, 1.0f},
			{1.0f, 1.0f, 0.0f},
			{0.0f, 1.0f, 1.0f}
	};

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				GLCanvas canvas = new MindControl();

				canvas.setPreferredSize(new Dimension(WIDTH, HEIGHT));

				final FPSAnimator anim = new FPSAnimator(canvas, FPS_MAX, true);

				final JFrame frame = new JFrame();
				frame.getContentPane().add(canvas);
				frame.addWindowListener(new WindowAdapter() {
					@Override
					public void windowClosing(WindowEvent e) {
						new Thread() {
							@Override
							public void run() {
								if (anim.isStarted()) {anim.stop();}
								System.exit(0);
							}
						}.start();
					}
				});
				frame.setTitle("EMPTY YOUR MIND");
				frame.pack();
				frame.setVisible(true);

				anim.start();
			}
		});
	}

	public void init(GLAutoDrawable draw) {
		GL2 gl = draw.getGL().getGL2();
		gl.glClearColor(1.0f, 0.35f, 0.0f, 0.0f);
		gl.glClearDepth(1.0f);

		gl.glEnable(GL2.GL_DEPTH_TEST);
		gl.glDepthFunc(GL2.GL_LEQUAL);

		gl.glHint(GL2.GL_PERSPECTIVE_CORRECTION_HINT, GL2.GL_NICEST);
		gl.glShadeModel(GL2.GL_SHININESS);
	}

	public void reshape(GLAutoDrawable draw, int x, int y, int width, int height) {
		GL2 gl = draw.getGL().getGL2();

		if (height == 0) {height = 1;} // Don't divide by zero
		float aspect = (float) (width / height);

		gl.glViewport(0, 0, width, height);

		gl.glMatrixMode(GL2.GL_PROJECTION);
		gl.glLoadIdentity();

		glu.gluPerspective(45.0, aspect, 1.0, 100.0);

		gl.glMatrixMode(GL2.GL_MODELVIEW);
		gl.glLoadIdentity();
	}

	public void display(GLAutoDrawable draw) {
		GL2 gl = draw.getGL().getGL2();
		gl.glClear(GL2.GL_COLOR_BUFFER_BIT | GL2.GL_DEPTH_BUFFER_BIT);
		gl.glClearColor(coloursB[0], coloursB[1], coloursB[2], coloursB[3]);

		gl.glLoadIdentity();
		gl.glViewport(0, 0, WIDTH, HEIGHT);
		glu.gluLookAt(rot0, rot1, 28, 0, 0, 0, 0, 0, 1);

		gl.glPushMatrix();
		for (float n = 0; n < Math.PI * 2; n += (float) ((Math.PI * 2) / cubes)) {
			gl.glPushMatrix();
			transformation(
					gl,
					(float) Math.sin(n) * 10,
					(float) Math.cos(n) * 10,
					0, 0, n * 3, n * 3 + rotate
					, 0.5f, 0.5f, 0.5f
					);
			allFaces(draw, drawVerts, invertC);
			gl.glPopMatrix();
		}
		gl.glPopMatrix();

		invert = true;
		update();

		gl.glFlush();
	}

	public void update() {
		camera += 0.005f;
		rot1 = Math.sin(Math.PI * camera) * 10;
		rot0 = Math.cos(Math.PI * camera) * 10;
		rotate += 0.1;

		if (invert) {
			for (int i = 0; i < invertC.length; i++) {
				for (int j = 0; j < invertC[i].length; j++) {invertC[i][j] = 1 - invertC[i][j];}
			}
			for (int i = 0; i < coloursB.length; i++) {coloursB[i] = 1 - coloursB[i];}
			invert = false;
		}
	}

	public void allFaces(GLAutoDrawable draw, float[][][] coords, float[][] colours) {
		for (int i = 0; i < coords.length; i++) {singleFace(draw, coords[i], colours[i]);}
	}

	public void singleFace(GLAutoDrawable draw, float[][] coords, float[] colours) {
		GL2 gl = draw.getGL().getGL2();

		gl.glBegin(GL2.GL_QUADS);
		gl.glColor3fv(colours, 0);
		for (int i = 0; i < coords.length; i++) {gl.glVertex3fv(coords[i], 0);}
		gl.glEnd();
	}

	public void colouredLines(GLAutoDrawable draw) {
		for (int i = 0; i < 3; i++) {colouredLine(draw, v3D[i], colours[i]);}
	}

	public void colouredLine(GLAutoDrawable draw, float[] verts3D, float[] colours3D) {
		GL2 gl = draw.getGL().getGL2();

		gl.glBegin(GL2.GL_LINES);
		gl.glColor3fv(colours3D, 0);
		gl.glVertex3f(0.0f, 0.0f, 0.0f);
		gl.glVertex3fv(verts3D, 0);
		gl.glEnd();
	}

	public void colouredLine(GLAutoDrawable draw, double[] verts3D, float[] colours3D) {
		GL2 gl = draw.getGL().getGL2();

		gl.glBegin(GL2.GL_LINES);
		gl.glColor3fv(colours3D, 0);
		gl.glVertex3f(0.0f, 0.0f, 0.0f);
		gl.glVertex3dv(verts3D, 0);
		gl.glEnd();
	}

	public void transformation(GL2 gl, float tX, float tY, float tZ, float rX, float rY, float rZ, float sX, float sY,
			float sZ) {
		float[] move = {1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, tX, tY, tZ, 1.0f};

		float[] rotateX = {1.0f, 0.0f, 0.0f, 0.0f, 0.0f, (float) Math.cos(rX), (float) -Math.sin(rX), 0.0f, 0.0f,
				(float) Math.sin(rX), (float) Math.cos(rX), 0.0f, 0.0f, 0.0f, 0.0f, 1.0f};

		float[] rotateY = {(float) Math.cos(rY), 0.0f, (float) Math.sin(rY), 0.0f, 0.0f, 1.0f, 0.0f, 0.0f,
				(float) -Math.sin(rY), 0.0f, (float) Math.cos(rY), 0.0f, 0.0f, 0.0f, 0.0f, 1.0f};

		float[] rotateZ = {(float) Math.cos(rZ), (float) -Math.sin(rZ), 0.0f, 0.0f, (float) Math.sin(rZ),
				(float) Math.cos(rZ), 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f};

		float[] scale = {sX, 0.0f, 0.0f, 0.0f, 0.0f, sY, 0.0f, 0.0f, 0.0f, 0.0f, sZ, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f};
		gl.glMultMatrixf(move, 0);
		gl.glMultMatrixf(rotateX, 0);
		gl.glMultMatrixf(rotateY, 0);
		gl.glMultMatrixf(rotateZ, 0);
		gl.glMultMatrixf(scale, 0);
	}

	public void transformation(GL2 gl, double tX, double tY, double tZ, double rX, double rY, double rZ, double sX,
			double sY, double sZ) {
		double[] move = { 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f, tX, tY, tZ, 1.0f };

		double[] rotateX = { 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, Math.cos(rX), -Math.sin(rX), 0.0f, 0.0f, Math.sin(rX),
				Math.cos(rX), 0.0f, 0.0f, 0.0f, 0.0f, 1.0f };

		double[] rotateY = { Math.cos(rY), 0.0f, Math.sin(rY), 0.0f, 0.0f, 1.0f, 0.0f, 0.0f, -Math.sin(rY), 0.0f,
				Math.cos(rY), 0.0f, 0.0f, 0.0f, 0.0f, 1.0f };

		double[] rotateZ = { Math.cos(rZ), -Math.sin(rZ), 0.0f, 0.0f, Math.sin(rZ), Math.cos(rZ), 0.0f, 0.0f, 0.0f,
				0.0f, 1.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f };

		double[] scale = { sX, 0.0f, 0.0f, 0.0f, 0.0f, sY, 0.0f, 0.0f, 0.0f, 0.0f, sZ, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f };
		gl.glMultMatrixd(move, 0);
		gl.glMultMatrixd(rotateX, 0);
		gl.glMultMatrixd(rotateY, 0);
		gl.glMultMatrixd(rotateZ, 0);
		gl.glMultMatrixd(scale, 0);
	}

	public void dispose(GLAutoDrawable draw) {}
}