import cv2
import numpy as np
from collections import deque
from delimitador import actualizar_centroides_buffer, calcular_promedio_centroides, ordenar_centroides
from analisis import detectar_figuras
import time

# Inicializa la cámara y  parámetros de configuración
cap = cv2.VideoCapture(0)
buffer_size = 6 # Número de frames para el buffer temporal
centroids_buffer = deque(maxlen=buffer_size)
detections_buffer = deque(maxlen=buffer_size)  # Buffer para las detecciones de formas
analizar = False
verMin = [0, 115, 110]  # Límite inferior del verde
verMax = [90, 217, 189]  # Límite superior del verde
# Crea dos deslizadores para ajustar alpha y beta
cv2.namedWindow('Webcam')
cv2.createTrackbar('Alpha', 'Webcam', 10, 30, lambda x: None)  # Alpha [1, 30]
cv2.createTrackbar('Beta', 'Webcam', 0, 100, lambda x: None)   # Beta [-100, 100]

while True:
    # Captura frame por frame
    ret, frame = cap.read()
    if not ret:
        break

    # Espeja la imagen
    frame = cv2.flip(frame, 1)  # 1 para reflejar horizontalmente

    # Muestra el frame en la ventana
    cv2.imshow('Webcam', frame)

    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2

    # Convierte la imagen de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define los límites del color verde en el espacio HSV
    lower_green = np.array(verMin)  # Límite inferior del verde
    upper_green = np.array(verMax)  # Límite superior del verde

    # Crea una máscara para detectar los colores verdes
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Encuentra contornos en la imagen enmascarada
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    corners = []
    centroids = []  # Lista para almacenar los centroides
    sectors = {1: [], 2: [], 3: [], 4: []}  # Diccionario para almacenar centroides por sector

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

                    # Determina el sector de la imagen
                    if cX < center_x and cY < center_y:
                        sectors[1].append((cX, cY))
                    elif cX >= center_x and cY < center_y:
                        sectors[2].append((cX, cY))
                    elif cX < center_x and cY >= center_y:
                        sectors[3].append((cX, cY))
                    else:
                        sectors[4].append((cX, cY))

        # Actualiza el buffer de centroides
        if all(len(sectors[sector]) > 0 for sector in sectors):
            # Toma el primer centroide de cada sector
            selected_centroids = [sectors[1][0], sectors[2][0], sectors[3][0], sectors[4][0]]
            actualizar_centroides_buffer(selected_centroids, centroids_buffer)

        # Calcula el promedio de los centroides si hay suficiente historial en el buffer
        if len(centroids_buffer) == buffer_size:
            promedio_centroids = calcular_promedio_centroides(centroids_buffer)
            # Ordenar los centroides
            promedio_centroids = ordenar_centroides(promedio_centroids)

            # Definir el área delimitada usando los centroides promedio
            x_min = min([c[0] for c in promedio_centroids])
            x_max = max([c[0] for c in promedio_centroids])
            y_min = min([c[1] for c in promedio_centroids])
            y_max = max([c[1] for c in promedio_centroids])

            # Transforma a escala de grises
            gris_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Ajuste de brillo y contraste
            # Lee los valores de los deslizadores
            alpha = cv2.getTrackbarPos('Alpha', 'Webcam') / 10  # Normaliza a un rango adecuado
            beta = cv2.getTrackbarPos('Beta', 'Webcam') - 50  # Centra el rango de beta en torno a 0

            # Aplica el ajuste de brillo y contraste con los valores de los deslizadores
            ajustado_frame = cv2.convertScaleAbs(gris_frame, alpha=alpha, beta=beta)

            # Recortar la imagen en el área delimitada
            roi = ajustado_frame[y_min:y_max, x_min:x_max]

            if analizar:
                cv2.imshow("ROI - Region de Interes", roi)

                # Llama a la función para detectar formas dentro del área recortada
                resultado, imagen_procesada = detectar_figuras(roi)

                # Agrega los resultados actuales al buffer de detección
                detections_buffer.append(resultado)
                distancia_l = resultado["DistanciaL"]
                distancia_c = resultado["DistanciaC"]

                # Calcular el promedio de detecciones en el buffer
                cant_L = sum(d["L"] for d in detections_buffer) // len(detections_buffer)
                cant_cuadrados = sum(d["Cuadrados"] for d in detections_buffer) // len(detections_buffer)

                # Mostrar Resultados
                print(f"'L' detectadas: {cant_L}")
                print(f"Cuadrados detectados: {cant_cuadrados}")
                print(f"Distancia L shapes: {distancia_l}")
                print(f"Distancia Cuadrados: {distancia_c}")
                print("-----------------------------------------------------------------------------------")
                print("ENVIAR A SERVIDOR")
                print("-----------------------------------------------------------------------------------")
                print(f"{distancia_l}")
                print(f"{distancia_c}")
                print(f"{cant_L}")
                print(f"{cant_L + cant_cuadrados}")
                print("-----------------------------------------------------------------------------------")



                # Muestra la región de interés procesada en el mismo frame
                ajustado_frame[y_min:y_max, x_min:x_max] = imagen_procesada

                # Abre el ROI en una nueva ventana si se detectan cuadros
                if cant_cuadrados > 0:
                    cv2.imshow("Region de Interes", ajustado_frame)

                analizar = False

    # Manejo de teclas
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Rompe el bucle si se presiona la tecla 'q'
        break
    elif key == ord('s'):  # Rompe el bucle si se presiona la tecla 'q'
        analizar = True

# Libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
