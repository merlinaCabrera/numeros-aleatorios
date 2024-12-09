import cv2
import numpy as np

def funcion_B(coord_cuadrado, cord_L):
    # Sumar coordenadas de cuadrados y L
    posCuadroGeneral = np.sum(coord_cuadrado, axis=0) if len(coord_cuadrado) > 0 else (0, 0)
    posLGeneral = np.sum(cord_L, axis=0) if len(cord_L) > 0 else (0, 0)

    # Calcular distancias desde (0, 0)
    dist_cuadrados = np.sqrt(posCuadroGeneral[0]**2 + posCuadroGeneral[1]**2)
    dist_L = np.sqrt(posLGeneral[0]**2 + posLGeneral[1]**2)

    return posCuadroGeneral, dist_cuadrados, posLGeneral, dist_L

def detectar_figuras(image):
    # Convertir la imagen a binaria aplicando un umbral

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_image, 75, 255, cv2.THRESH_BINARY_INV)

    # Hacer una copia de la imagen para dibujar los contornos
    img_salida = image.copy()

    # Obtener dimensiones de la imagen
    height, width = image.shape[:2]

    # Encontrar contornos en la imagen binaria
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Contadores de formas
    cant_cuad = 0
    cant_L = 0

    # Listas para almacenar las coordenadas
    coord_Cuadrado = []
    coord_L = []

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
            cant_cuad += 1
            coord_Cuadrado.append((norm_x, norm_y))  # Guardar coordenadas de cuadrados
            # Dibujar contorno en verde
            cv2.drawContours(img_salida, [approx], -1, (0, 255, 0), 2)
            # Crear texto con etiqueta y coordenadas
            texto = f"C ({norm_x}, {norm_y})"
            # Colocar el texto en la imagen
            cv2.putText(img_salida, texto, (cX - 30, cY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # print(f"Cuadrado detectado en: ({norm_x}, {norm_y})")

        elif len(approx) == 6:
            cant_L += 1
            coord_L.append((norm_x, norm_y))  # Guardar coordenadas de L
            # Dibujar contorno en azul
            cv2.drawContours(img_salida, [approx], -1, (255, 0, 0), 2)
            # Crear texto con etiqueta y coordenadas
            texto = f"L ({norm_x}, {norm_y})"
            # Colocar el texto en la imagen
            cv2.putText(img_salida, texto, (cX - 10, cY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # print(f"Figura 'L' detectada en: ({norm_x}, {norm_y})")

    # Llamar a funcion_B con las coordenadas de cuadrados y L
    posCuadroGeneral, dist_cuadrados, posLGeneral, dist_L = funcion_B(coord_Cuadrado, coord_L)

    res = cv2.cvtColor(img_salida, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("resultado",res)

    # Devolver los resultados y la imagen procesada
    return {"Cuadrados": cant_cuad, "L": cant_L, "DistanciaL": dist_L, "DistanciaC": dist_cuadrados}, res
