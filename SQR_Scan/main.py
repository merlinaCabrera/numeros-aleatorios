import threading
import cv2
import numpy as np
from collections import deque
from analisis import detectar_figuras
import time
from UI_UX import *

#from Sensor import leer_temperatura
from Utils import *

# parámetros de configuración
kernel = np.ones((5, 5), np.uint8)  # Nucleo
minArea = 500

# Variables de Control
enviar = False
capturando = True
conMonitor = False

lock = threading.Lock()

# Temperatura
temperaturas = deque(maxlen=10)  # ultimas 10 lecturas del sensor

def captura_camara():
    global enviar
    evaluado = False
    inicio = time.time()

    # Define los límites del color verde en el espacio HSV
    verMin = [30, 100, 91]  # Límite inferior del verde
    verMax = [105, 255, 255]  # Límite superior del verde
    lower_green = np.array(verMin)  # Límite inferior del verde
    upper_green = np.array(verMax)  # Límite superior del verde

    # Variables para detectar el estado de las 4 áreas
    cuadrados_detectados = 0
    cuadrados_previos = 0  # Para evitar repetir la llamada a operar()
    coordenadas_cuadrados = deque(maxlen=4)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error al acceder a la cámara")
        return

    while capturando:
        tiempoActual = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Error al leer el frame")
            break

        # Espeja la imagen
        frame = cv2.flip(frame, 1)  # 1 para reflejar horizontalmente

        # Convierte la imagen de BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crea una máscara para detectar los colores verdes
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        closing = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
        closing = cv2.medianBlur(closing, 13)

        # Encuentra contornos en la imagen enmascarada
        contours, _ = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Contamos cuántos contornos son lo suficientemente grandes y aproximan a un cuadrado
        cuadrados_detectados = 0
        for cnt in contours:
            M = cv2.moments(cnt)
            area = M['m00']
            if area > minArea:
                (x, y, u, v) = cv2.boundingRect(cnt)
                aspect_ratio = float(u) / v
                # Se considera cuadrado si el aspecto es cercano a 1 (ajustar según sea necesario)
                if 0.5 < aspect_ratio < 1.5:
                    cuadrados_detectados += 1
                    coordenadas_cuadrados.append((x, y))  # Ultimas 4 coordenadas de cada cuadrado
                    # Dibuja rectangulos sobre los cuadros verdes
                    # cv2.rectangle(frame, (x, y), (x + u, y + v), (255, 0, 0), 3)

        # Si se detectan exactamente 4 cuadrados y antes no se detectaron, llamar a operar()
        if cuadrados_detectados == 4 and cuadrados_previos != 4:
            if tiempoActual - inicio >= 2:
                # Encuentra las coordenadas extremas (mínimas y máximas)
                min_x = min(coordenadas_cuadrados, key=lambda x: x[0])[0]
                min_y = min(coordenadas_cuadrados, key=lambda x: x[1])[1]
                max_x = max(coordenadas_cuadrados, key=lambda x: x[0])[0]
                max_y = max(coordenadas_cuadrados, key=lambda x: x[1])[1]

                # Recorte del área alrededor de los cuadrados
                recorte = frame[min_y:max_y, min_x:max_x]
                evaluado = True

                print("Encontrado")
                inicio = tiempoActual

        # Si las 4 áreas desaparecen y luego se vuelven a detectar, llamar nuevamente a operar()
        if cuadrados_detectados != 4:
            cuadrados_previos = 0
        else:
            cuadrados_previos = cuadrados_detectados

        if evaluado:
            recorte = cv2.convertScaleAbs(recorte, alpha=2.15, beta=20) # Ajustes de contraste y brillo para mejor contraste

            # Llama a la función para detectar formas dentro del área recortada
            resultado, imagen_procesada = detectar_figuras(recorte)

            distancia_l = resultado["DistanciaL"]
            distancia_c = resultado["DistanciaC"]
            cant_l = resultado["L"]
            cant_c = resultado["Cuadrados"]
            print(distancia_c, distancia_l, cant_l, cant_c)

            cv2.imshow("Region de Interes", imagen_procesada)
            evaluado = False

            # Generación de Clave
            #semilla, clave = generar_clave(transformar_decimal(23.5), cant_L + cant_cuadrados, cant_cuadrados,transformar_decimal(distancia_l))

            # Envío de Datos
            with lock:
                if enviar:
                    print("habilitado")
                else:
                    print("deshabilitado")
            #    enviarDatos(cant_L + cant_cuadrados, cant_cuadrados, distancia_l, 23.5, semilla, clave)

            # Abre el ROI en una nueva ventana si se detectan cuadros
            #if cant_cuadrados > 0:
             #   cv2.imshow("Region de Interes", imagen_procesada)

        # Muestra el frame en la ventana
        cv2.imshow('Webcam', frame)

        # Esperar por 1 milisegundo para que la ventana se actualice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la captura y cierra las ventanas
    cap.release()
    cv2.destroyAllWindows()

def consola_y_entrada():
    global capturando, enviar
    mostrar_cartel2()
    while True:
        tecla = input("Ingrese su eleccion: ")
        if tecla == 'e':
            with lock:
                enviar = not enviar
        elif tecla == 'q':
            capturando = False
            break

# Crear hilos
hilo_camara = threading.Thread(target=captura_camara)
hilo_consola = threading.Thread(target=consola_y_entrada)

# Inicializar hilos
hilo_camara.start()
hilo_consola.start()


hilo_camara.join()
time.sleep(1)
hilo_consola.join()
print("programa cerrado")
