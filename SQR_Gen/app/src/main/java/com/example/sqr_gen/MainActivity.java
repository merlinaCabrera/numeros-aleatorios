package com.example.sqr_gen;
import android.app.AlertDialog;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public class MainActivity extends AppCompatActivity {

    private int xValue = 40;
    private int yValue = 40;
    private ImageView imgDisplay;
    private Bitmap generatedImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SeekBar xSlider = findViewById(R.id.seekBarX);
        SeekBar ySlider = findViewById(R.id.seekBarY);
        TextView xLabel = findViewById(R.id.textViewX);
        TextView yLabel = findViewById(R.id.textViewY);
        Button generateButton = findViewById(R.id.buttonGenerate);
        imgDisplay = findViewById(R.id.imageView);

        xSlider.setProgress(xValue);
        ySlider.setProgress(yValue);
        xLabel.setText("Ancho seleccionado: " + xValue);
        yLabel.setText("Alto seleccionado: " + yValue);

        xSlider.setOnSeekBarChangeListener(new SimpleSeekBarChangeListener(value -> {
            xValue = value;
            xLabel.setText("Ancho seleccionado: " + xValue);
        }));

        ySlider.setOnSeekBarChangeListener(new SimpleSeekBarChangeListener(value -> {
            yValue = value;
            yLabel.setText("Alto seleccionado: " + yValue);
        }));

        generateButton.setOnClickListener(v -> generateImage());

        imgDisplay.setOnClickListener(v -> showFullImage());
    }

    private void generateImage() {
        int margin = Math.max(1, Math.min(xValue, yValue) / 10);
        int totalWidth = xValue + 2 * margin;
        int totalHeight = yValue + 2 * margin;

        Bitmap bitmap = Bitmap.createBitmap(totalWidth, totalHeight, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        Paint paint = new Paint();
        paint.setColor(Color.WHITE);
        canvas.drawRect(0, 0, totalWidth, totalHeight, paint);

        Paint blackPaint = new Paint();
        blackPaint.setColor(Color.BLACK);

        // Add patterns
        addPatterns(canvas, blackPaint, xValue, yValue, margin);

        // Add green corners
        Paint greenPaint = new Paint();
        greenPaint.setColor(Color.GREEN);
        int squareSize = Math.max(1, Math.min(xValue, yValue) / 10);
        drawCorners(canvas, greenPaint, totalWidth, totalHeight, squareSize);

        generatedImage = bitmap;
        imgDisplay.setImageBitmap(bitmap);
    }

    private void addPatterns(Canvas canvas, Paint paint, int width, int height, int margin) {
        Random random = new Random();
        Set<String> occupiedPositions = new HashSet<>();

        int numL = random.nextInt(Math.max(1, Math.max(width, height) / 4));
        int numSquares = random.nextInt(Math.max(1, Math.max(width, height) / 4));

        // Draw "L" patterns
        for (int i = 0; i < numL; i++) {
            int x = random.nextInt(width - 8) + margin;
            int y = random.nextInt(height - 8) + margin;
            if (!occupiedPositions.contains(x + "," + y)) {
                for (int j = 0; j < 5; j++) {
                    canvas.drawRect(x + j, y, x + j + 1, y + 1, paint);
                    canvas.drawRect(x, y + j, x + 1, y + j + 1, paint);
                }
                occupiedPositions.add(x + "," + y);
            }
        }

        // Draw 3x3 squares
        for (int i = 0; i < numSquares; i++) {
            int x = random.nextInt(width - 4) + margin;
            int y = random.nextInt(height - 4) + margin;
            if (!occupiedPositions.contains(x + "," + y)) {
                canvas.drawRect(x, y, x + 3, y + 3, paint);
                occupiedPositions.add(x + "," + y);
            }
        }
    }

    private void drawCorners(Canvas canvas, Paint paint, int width, int height, int size) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                canvas.drawPoint(i, j, paint);
                canvas.drawPoint(width - 1 - i, j, paint);
                canvas.drawPoint(i, height - 1 - j, paint);
                canvas.drawPoint(width - 1 - i, height - 1 - j, paint);
            }
        }
    }

    private void showFullImage() {
        if (generatedImage == null) return;

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        ImageView imageView = new ImageView(this);
        imageView.setImageBitmap(generatedImage);
        builder.setView(imageView);
        builder.setPositiveButton("Cerrar", (dialog, which) -> dialog.dismiss());
        builder.show();
    }

    interface SeekBarListener {
        void onProgressChanged(int value);
    }

    class SimpleSeekBarChangeListener implements SeekBar.OnSeekBarChangeListener {
        private final SeekBarListener listener;

        public SimpleSeekBarChangeListener(SeekBarListener listener) {
            this.listener = listener;
        }

        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            listener.onProgressChanged(progress);
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
        }
    }
}