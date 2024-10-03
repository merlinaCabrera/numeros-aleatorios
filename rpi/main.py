import cv2
import numpy as np

# Inicializa la cámara
cap = cv2.VideoCapture(0)

# Configura el enfoque en "macro" (puede que no funcione en todas las cámaras)
cap.set(cv2.CAP_PROP_FOCUS, 10)  # Ajusta este valor según sea necesario

# Variable para controlar si la imagen está congelada
frozen = False
frozen_frame = None

while True:
    # Captura frame por frame solo si la imagen no está congelada
    if not frozen:
        ret, frame = cap.read()
        if not ret:
            break

        # Espeja la imagen
        frame = cv2.flip(frame, 1)  # 1 para reflejar horizontalmente

        # Convierte la imagen de BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define los límites del color verde en el espacio HSV
        lower_green = np.array([40, 100, 100])  # Límite inferior del verde
        upper_green = np.array([80, 255, 255])  # Límite superior del verde

        # Crea una máscara para detectar los colores verdes
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Encuentra contornos en la imagen enmascarada
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        corners = []
        centroids = []  # Lista para almacenar los centroides

        # Filtra los contornos para encontrar los cuadrados, limitando a 4
        for contour in contours:
            if len(corners) >= 4:  # Verifica si ya se han encontrado 4 cuadrados
                break

            # Aproxima el contorno a un polígono
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            # Verifica si es un cuadrado
            if len(approx) == 4:
                # Verifica que los lados sean aproximadamente iguales
                side_lengths = [np.linalg.norm(approx[i] - approx[(i + 1) % 4]) for i in range(4)]
                if all(abs(side_lengths[i] - side_lengths[i - 1]) < 10 for i in range(4)):
                    corners.append(approx)

                    # Dibuja un rectángulo alrededor del cuadrado detectado
                    cv2.rectangle(frame, tuple(approx[0][0]), tuple(approx[2][0]), (0, 0, 255), 2)

                    # Calcula el centroide del cuadrado
                    M = cv2.moments(approx)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        centroids.append((cX, cY))  # Guarda el centroide

        # Si se han detectado 4 cuadrados, determina su posición
        if len(corners) == 4:
            positions = {0: "arriba izquierda", 1: "arriba derecha", 2: "abajo izquierda", 3: "abajo derecha"}

            # Ordenar los centroides
            centroids.sort(key=lambda point: (point[1], point[0]))  # Ordenar por Y, luego por X

            # Etiqueta los cuadrados
            for idx, centroid in enumerate(centroids):
                cv2.putText(frame, positions[idx], (centroid[0], centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Crear una máscara negra del mismo tamaño que la imagen
            mask = np.zeros_like(frame)

            # Convierte los centroides en un array de puntos
            points = np.array(centroids, dtype=np.int32)

            # Dibuja un polígono (perímetro) en la máscara usando solo los puntos adyacentes
            cv2.fillConvexPoly(mask, points, (255, 255, 255))

            # Aplica la máscara a la imagen original
            frame = cv2.bitwise_and(frame, mask)

            # Congelar la imagen cuando se detectan los 4 cuadrados
            frozen_frame = frame.copy()
            frozen = True

    # Si la imagen está congelada, muestra el frame congelado
    if frozen:
        cv2.imshow('Webcam', frozen_frame)
    else:
        # Muestra el frame en una ventana
        cv2.imshow('Webcam', frame)

    # Manejo de teclas
    key = cv2.waitKey(1) & 0xFF

    # Rompe el bucle si se presiona la tecla 'q'
    if key == ord('q'):
        break
    # Reanuda la detección si se presiona la tecla 'espacio'
    elif key == ord(' '):
        frozen = False

# Libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
