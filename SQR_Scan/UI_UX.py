def mostrar_cartel_bienvedida():
    print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print("█                                              █")
    print("█ BIENVENIDO AL GENERADOR DE CLAVES ALEATORIAS █")
    print("█                                              █")
    print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")

def mostrar_cartel1():
    print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print("█        ↓↓↓ CONFIGURACION INICIAL ↓↓↓         █")
    print("█                                              █")
    print("█  Presione:                                   █")
    print("█   '1': Cuenta con un monitor                 █")
    print("█   '2': No Cuenta con un monitor              █")
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")

def mostrar_cartel2(env):

    print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print("█                                              █")
    print("█        GENERADOR DE CLAVES ALEATORIAS        █")
    print("█              Ya puede escanear               █")
    print("█                                              █")
    print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print("█          ↓↓↓ COMANDOS POSIBLES ↓↓↓           █")
    print("█                                              █")
    print("█  Presione:                                   █")
    print("█   e: Habilita/Deshabilita el envío de datos  █")
    if env:
        print("█      (Habilitado)                            █")
    else:
        print("█      (Deshabilitado)                         █")
    print("█   q: Cierra el Programa                      █")
    print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
