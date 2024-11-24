import cv2
import numpy as np

def funcion_B(square_coords, l_shape_coords):
    # Sumar coordenadas de cuadrados y L
    posCuadroGeneral = np.sum(square_coords, axis=0) if len(square_coords) > 0 else (0, 0)
    posLGeneral = np.sum(l_shape_coords, axis=0) if len(l_shape_coords) > 0 else (0, 0)

    # Calcular distancias desde (0, 0)
    distance_squares = np.sqrt(posCuadroGeneral[0]**2 + posCuadroGeneral[1]**2)
    distance_l_shapes = np.sqrt(posLGeneral[0]**2 + posLGeneral[1]**2)

    return posCuadroGeneral, distance_squares, posLGeneral, distance_l_shapes

def detectar_figuras(image):
    # Convertir la imagen a binaria aplicando un umbral
    _, binary_image = cv2.threshold(image, 75, 255, cv2.THRESH_BINARY_INV)

    # Hacer una copia de la imagen para dibujar los contornos
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convierte a BGR para dibujar en color

    # Obtener dimensiones de la imagen
    height, width = image.shape[:2]

    # Encontrar contornos en la imagen binaria
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Contadores de formas
    square_count = 0
    l_shape_count = 0

    # Listas para almacenar las coordenadas
    square_coords = []
    l_shape_coords = []

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

        # Normalizar las coordenadas entre 0 y 100
        norm_x = (cX / width) * 100 - 50
        norm_y = (((height - cY) / height) * 100) - 50  # Invertir Y para que (0,0) esté en la esquina inferior izquierda

        # Redondear las coordenadas a dos decimales
        norm_x = round(norm_x, 2)
        norm_y = round(norm_y, 2)

        # Clasificar en base a la cantidad de vértices y dibujar
        if len(approx) == 4:
            square_count += 1
            square_coords.append((norm_x, norm_y))  # Guardar coordenadas de cuadrados
            # Dibujar contorno en verde
            cv2.drawContours(output_image, [approx], -1, (0, 255, 0), 2)
            # Crear texto con etiqueta y coordenadas
            texto = f"C ({norm_x}, {norm_y})"
            # Colocar el texto en la imagen
            cv2.putText(output_image, texto, (cX - 30, cY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Imprimir en consola
            print(f"Cuadrado detectado en: ({norm_x}, {norm_y})")
        elif len(approx) == 6:
            l_shape_count += 1
            l_shape_coords.append((norm_x, norm_y))  # Guardar coordenadas de L
            # Dibujar contorno en azul
            cv2.drawContours(output_image, [approx], -1, (255, 0, 0), 2)
            # Crear texto con etiqueta y coordenadas
            texto = f"L ({norm_x}, {norm_y})"
            # Colocar el texto en la imagen
            cv2.putText(output_image, texto, (cX - 10, cY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            # Imprimir en consola
            print(f"Figura 'L' detectada en: ({norm_x}, {norm_y})")

    # Llamar a funcion_B con las coordenadas de cuadrados y L
    posCuadroGeneral, distance_squares, posLGeneral, distance_l_shapes = funcion_B(square_coords, l_shape_coords)

    # Imprimir resultados de las distancias
    print(f"Distancia desde (0, 0) hasta coordenadas de cuadrados: {distance_squares}")
    print(f"Distancia desde (0, 0) hasta coordenadas de L: {distance_l_shapes}")

    # Devolver los resultados y la imagen procesada
    return {"Cuadrados": square_count, "L": l_shape_count, "DistanciaL": distance_l_shapes, "DistanciaC": distance_squares}, cv2.cvtColor(output_image, cv2.COLOR_BGR2GRAY)
