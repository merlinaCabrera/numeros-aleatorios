import time
import RPi.GPIO as GPIO
from collections import deque
import hashlib

GPIO_PIN = 4
GPIO.setmode(GPIO.BCM)


def leer_temperatura():
    # lectura de temperatura del sensor DHT22
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, GPIO.LOW)

    time.sleep(0.02)
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # variables
    data = []
    tiempo_inicio = time.time()

    while GPIO.input(GPIO_PIN) == GPIO.HIGH:
        if time.time() - tiempo_inicio > 0.1:
            return None

    # recibimiento de datos
    for i in range(0, 5000):
        longitud = 0
        while GPIO.input(GPIO_PIN) == GPIO.LOW:
            continue

        while GPIO.input(GPIO_PIN) == GPIO.HIGH:
            longitud += 1
            if longitud > 100:
                break

        data.append(longitud)

    # procesamiento de datos
    bits = []
    for longitud in data:
        if longitud > 50:
            bits.append(1)
        else:
            bits.append(0)

    if len(bits) < 40:
        return None
    bytes_dht = [bits[i:i + 8] for i in range(0, len(bits), 8)]

    resultado = []
    for byte in bytes_dht:
        resultado.append(int(''.join(map(str, byte)), 2))

    if sum(resultado[:4]) & 0xFF != resultado[4]:
        return None

    # extraccion de temperatura
    temperatura = ((resultado[2] << 8) + resultado[3]) / 10
    if resultado[2] & 0x80:
        temperatura *= -1

    return round(temperatura, 2)

