import cv2
import numpy as np

def detectar_figuras(image):
    # Convertir la imagen a binaria aplicando un umbral
    _, binary_image = cv2.threshold(image, 75, 255, cv2.THRESH_BINARY_INV)

    # Hacer una copia de la imagen para dibujar los contornos
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convierte a BGR para dibujar en color

    # Encontrar contornos en la imagen binaria
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Contadores de formas
    square_count = 0
    l_shape_count = 0

    # Rango de área para ignorar el borde de la imagen y el ruido
    min_area = 50     # Área mínima para considerar un contorno
    max_area = 5000   # Área máxima para evitar el borde grande de la imagen

    # Clasificar cada contorno
    for cnt in contours:
        # Filtrar contornos por área
        area = cv2.contourArea(cnt)
        if area < min_area or area > max_area:
            continue  # Ignorar contornos fuera del rango de área

        # Aproximar el contorno
        epsilon = 0.035 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Obtener el centro de cada contorno para etiquetar
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Clasificar en base a la cantidad de vértices y dibujar
        if len(approx) == 4:
            square_count += 1
            cv2.drawContours(output_image, [approx], -1, (0, 255, 0), 2)  # Verde para cuadrados
            cv2.putText(output_image, "Cuadrado", (cX - 30, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        elif len(approx) == 6:
            l_shape_count += 1
            cv2.drawContours(output_image, [approx], -1, (255, 0, 0), 2)  # Azul para "L"
            cv2.putText(output_image, "L", (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Devolver los resultados y la imagen procesada
    return {"Cuadrados": square_count, "L": l_shape_count}, cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)