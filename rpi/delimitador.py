import numpy as np

def actualizar_centroides_buffer(centroids, buffer):
    if len(buffer) == buffer.maxlen:
        buffer.popleft()
    buffer.append(centroids)

# Genera una detección más robusta entre frames
def calcular_promedio_centroides(buffer):
    promedio = np.mean(buffer, axis=0)
    return [(int(x), int(y)) for x, y in promedio]

# Ayuda a la correcta implementacion de la mascara que recubre la imagen
def ordenar_centroides(centroids):
    centroids = sorted(centroids, key=lambda point: point[1])
    top_two = sorted(centroids[:2], key=lambda point: point[0])
    bottom_two = sorted(centroids[2:], key=lambda point: point[0])
    return [top_two[0], top_two[1], bottom_two[1], bottom_two[0]]