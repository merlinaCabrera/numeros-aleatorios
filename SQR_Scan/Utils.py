import hashlib
import requests

url = "https://two024-g5-numeros-aleatorios-cloudfare.onrender.com/api/data"

def enviarDatos(figure_count, square_count, unique_position_value, temperature, seed, generated_number):
    body = {
        "figure_count": figure_count,
        "square_count": square_count,
        "unique_position_value": unique_position_value,
        "temperature": temperature,
        "seed": seed,
        "generated_number": generated_number
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=body, headers=headers)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200 or response.status_code == 201:
            print("Solicitud exitosa:")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Ocurrió un error al realizar la solicitud:", e)
        
def transformar_decimal(numero):
    # Convertir el número a string para eliminar el punto decimal
    numero_str = str(numero).replace('.', '')
    # Convertirlo de nuevo a entero
    return int(numero_str)
    
def generar_clave(*numeros):
    semilla = ''.join(map(str, numeros))
    
    # Generar la clave hash SHA-256
    clave = hashlib.sha256(semilla.encode()).hexdigest()
    return semilla, clave

