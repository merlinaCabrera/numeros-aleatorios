package com.example.sqr_gen;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;

import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public class IMG_Tools {
    public static Bitmap scaleImage(Bitmap originalImage) {
        // Obtener las dimensiones originales de la imagen
        int originalWidth = originalImage.getWidth();
        int originalHeight = originalImage.getHeight();

        // Determinar el nuevo tamaño basado en el lado más largo
        int newWidth = originalWidth;
        int newHeight = originalHeight;

        if (originalWidth > originalHeight) {
            newWidth = 1080;
            newHeight = (originalHeight * newWidth) / originalWidth;
        } else if (originalHeight > originalWidth) {
            newHeight = 1080;
            newWidth = (originalWidth * newHeight) / originalHeight;
        } else {
            newWidth = 1080;
            newHeight = 1080;
        }

        // Crear un nuevo Bitmap con el nuevo tamaño
        Bitmap scaledImage = Bitmap.createBitmap(newWidth, newHeight, Bitmap.Config.ARGB_8888);

        // Redimensionar pixel por pixel
        float xRatio = (float) originalWidth / newWidth;
        float yRatio = (float) originalHeight / newHeight;

        for (int y = 0; y < newHeight; y++) {
            for (int x = 0; x < newWidth; x++) {
                // Calcular las coordenadas correspondientes en la imagen original
                int origX = (int) (x * xRatio);
                int origY = (int) (y * yRatio);

                // Obtener el color del píxel de la imagen original
                int pixelColor = originalImage.getPixel(origX, origY);

                // Establecer el color del píxel en la nueva imagen
                scaledImage.setPixel(x, y, pixelColor);
            }
        }

        return scaledImage;
    }

    private static boolean isAreaFree(int x, int y, int width, int height, Set<String> occupiedPositions) {
        for (int i = x; i < x + width+1; i++) {
            for (int j = y; j < y + height+1; j++) {
                if (occupiedPositions.contains(i + "," + j)) {
                    return false; // Si algún píxel está ocupado, no se puede dibujar
                }
            }
        }
        return true; // Si toda el área está libre, podemos dibujar la figura
    }

    // Marca los píxeles ocupados por una figura en el conjunto de posiciones ocupadas
    private static void markOccupiedArea(int x, int y, int width, int height, Set<String> occupiedPositions) {
        for (int i = x; i < x + width+1; i++) {
            for (int j = y; j < y + height+1; j++) {
                occupiedPositions.add(i + "," + j); // Marca como ocupado el píxel
            }
        }
    }

    public static void addPatterns(Canvas canvas, Paint paint, int width, int height, int margin) {
        Random random = new Random();
        Set<String> occupiedPositions = new HashSet<>();

        int numL = random.nextInt(Math.max(1, Math.max(width, height) / 4)); // Número de figuras "L"
        int numSquares = random.nextInt(Math.max(1, Math.max(width, height) / 4)); // Número de cuadrados 3x3

        // Dibuja las figuras "L"
        for (int i = 0; i < numL; i++) {
            int x = random.nextInt(width - 8) + margin;
            int y = random.nextInt(height - 8) + margin;

            // Verifica si el área donde se quiere dibujar la figura "L" está ocupada
            if (isAreaFree(x, y, 5, 5, occupiedPositions)) {
                // Dibuja la figura "L"
                for (int j = 0; j < 5; j++) {
                    canvas.drawRect(x + j, y, x + j + 1, y + 1, paint); // Parte horizontal
                    canvas.drawRect(x, y + j, x + 1, y + j + 1, paint); // Parte vertical
                }
                // Marca los píxeles ocupados por la figura "L"
                markOccupiedArea(x, y, 5, 5, occupiedPositions);
            }
        }

        // Dibuja los cuadrados 3x3
        for (int i = 0; i < numSquares; i++) {
            int x = random.nextInt(width - 4) + margin;
            int y = random.nextInt(height - 4) + margin;

            // Verifica si el área donde se quiere dibujar el cuadrado 3x3 está ocupada
            if (isAreaFree(x, y, 3, 3, occupiedPositions)) {
                // Dibuja el cuadrado 3x3
                canvas.drawRect(x, y, x + 3, y + 3, paint);
                // Marca los píxeles ocupados por el cuadrado
                markOccupiedArea(x, y, 3, 3, occupiedPositions);
            }
        }
    }


    public static void drawCorners(Canvas canvas, Paint paint, int width, int height, int size) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                canvas.drawPoint(i, j, paint);
                canvas.drawPoint(width - 1 - i, j, paint);
                canvas.drawPoint(i, height - 1 - j, paint);
                canvas.drawPoint(width - 1 - i, height - 1 - j, paint);
            }
        }
    }
}
