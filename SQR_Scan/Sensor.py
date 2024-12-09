import Adafruit_DHT

# Configuración del sensor DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Pin GPIO al que está conectado el DHT11

def leer_temperatura():
    _,temp = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    return temp

