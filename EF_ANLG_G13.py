# Trabajo Final - Análisis de Algoritmos (Grupo 13)
# Resolver un laberinto usando BACKTRACKING (vuelta atrás)
#
# Idea simple: caminamos por el laberinto probando un camino.
# Si llegamos a un lugar sin salida, RETROCEDEMOS y probamos otro camino.
#
# Leyenda:  I = inicio | S = salida | 0 = camino libre | 1 = pared

I = "I"
S = "S"

laberinto = [
    [I,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,0,0,0,1,0,0,1,1,0,0,0,1,1,1,1,1,0,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0],
    [1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
    [0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0],
    [0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1],
    [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0],
    [1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0],
    [0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
    [0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,S],
]

# Los 4 movimientos posibles: abajo, derecha, arriba, izquierda
movimientos = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def buscar_posicion(laberinto, letra):
    """Busca la fila y columna donde está la letra (I o S)."""
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            if laberinto[fila][col] == letra:
                return (fila, col)
    return None


def resolver(laberinto, fila, col, camino, visitados):
    """
    Backtracking: prueba caminos y retrocede cuando no hay salida.
    Devuelve True si encontró la salida, False si no.
    """
    # 1. Si esta casilla se sale del laberinto, es pared o ya la pisamos: no sirve
    if fila < 0 or fila >= len(laberinto):
        return False
    if col < 0 or col >= len(laberinto[0]):
        return False
    if laberinto[fila][col] == 1:
        return False
    if (fila, col) in visitados:
        return False

    # 2. Pisamos la casilla: la anotamos en el camino
    visitados.add((fila, col))
    camino.append((fila, col))

    # 3. Si es la salida, terminamos
    if laberinto[fila][col] == S:
        return True

    # 4. Probamos los 4 movimientos
    for mov_fila, mov_col in movimientos:
        if resolver(laberinto, fila + mov_fila, col + mov_col, camino, visitados):
            return True

    # 5. RETROCEDER: ningún movimiento llegó a la salida,
    #    así que quitamos esta casilla del camino y volvemos atrás
    camino.pop()
    return False


def mostrar_laberinto(laberinto, camino):
    """Dibuja el laberinto. El camino se marca con puntos (.)"""
    en_camino = set(camino)
    for fila in range(len(laberinto)):
        linea = ""
        for col in range(len(laberinto[0])):
            celda = laberinto[fila][col]
            if celda == I or celda == S:
                linea += celda + " "
            elif (fila, col) in en_camino:
                linea += ". "
            elif celda == 1:
                linea += "# "
            else:
                linea += "  "
        print(linea)


def main():
    if len(laberinto) == 0:
        print("El laberinto no puede estar vacío.")
        return

    inicio = buscar_posicion(laberinto, I)
    salida = buscar_posicion(laberinto, S)

    if inicio is None or salida is None:
        print("El laberinto necesita un inicio (I) y una salida (S).")
        return

    camino = []
    visitados = set()

    if resolver(laberinto, inicio[0], inicio[1], camino, visitados):
        print("¡Se encontró la salida!")
        print("Pasos dados:", len(camino) - 1)
        print()
        mostrar_laberinto(laberinto, camino)
        print()
        print("Camino (fila, columna):")
        print(camino)
    else:
        print("No hay salida en este laberinto.")


main()
