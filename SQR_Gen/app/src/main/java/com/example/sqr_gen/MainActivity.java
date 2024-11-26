package com.example.sqr_gen;
import android.annotation.SuppressLint;
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

public class MainActivity extends AppCompatActivity {

    private int xValue = 40;
    private int yValue = 40;
    private ImageView imgDisplay;

    @SuppressLint("SetTextI18n")
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
        IMG_Tools.addPatterns(canvas, blackPaint, xValue, yValue, margin);

        // Add green corners
        Paint greenPaint = new Paint();
        greenPaint.setColor(Color.GREEN);
        int squareSize = Math.max(1, Math.min(xValue, yValue) / 10);
        IMG_Tools.drawCorners(canvas, greenPaint, totalWidth, totalHeight, squareSize);

        Bitmap generatedImage = IMG_Tools.scaleImage(bitmap);
        imgDisplay.setImageBitmap(generatedImage);
    }

    interface SeekBarListener {
        void onProgressChanged(int value);
    }

    static class SimpleSeekBarChangeListener implements SeekBar.OnSeekBarChangeListener {
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