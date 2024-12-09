import Adafruit_DHT

# Configuración del sensor DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 2  # Pin GPIO al que está conectado el DHT11

def leer_temperatura():
    _, temperatura = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return temperatura
