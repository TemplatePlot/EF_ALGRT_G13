# Trabajo Final - Análisis de Algoritmos (Grupo 13)
# Resolver un laberinto usando BFS (búsqueda en anchura)
#
# Idea simple: desde el inicio, exploramos "en ondas": primero todas las casillas
# a 1 paso, luego las de 2 pasos, luego 3, etc. La primera vez que llegamos a la
# salida es con el MENOR número de pasos posible. Por eso BFS siempre da el
# camino más corto (en un laberinto donde cada paso cuesta lo mismo).
#
# Leyenda:  I = inicio | S = salida | 0 = camino libre | 1 = pared

import os
import time
from collections import deque

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


def bfs(laberinto, inicio, salida):
    """
    BFS: explora el laberinto por "ondas" usando una COLA (primero en entrar,
    primero en salir).

    Devuelve un diccionario con:
      - camino: lista de (fila, col) de inicio a salida (o None si no hay salida)
      - explorados: cuántas casillas sacó de la cola
      - max_frontera: el tamaño máximo que tuvo la cola (sirve como medida de memoria)
      - tiempo: segundos que tardó
    """
    inicio_tiempo = time.perf_counter()
    filas = len(laberinto)
    columnas = len(laberinto[0])

    # La cola guarda las casillas pendientes de visitar
    cola = deque([inicio])

    # padre[casilla] = de qué casilla venimos. Sirve para dos cosas:
    #   1) saber qué casillas ya visitamos (si está aquí, ya la vimos)
    #   2) reconstruir el camino al final
    padre = {inicio: None}

    explorados = 0
    max_frontera = 1
    camino = None

    while cola:
        fila, col = cola.popleft()      # sacamos la casilla más antigua
        explorados += 1

        # ¿Llegamos a la salida? Terminamos y reconstruimos el camino
        if (fila, col) == salida:
            camino = []
            actual = salida
            while actual is not None:   # retrocedemos de padre en padre
                camino.append(actual)
                actual = padre[actual]
            camino.reverse()            # lo dábamos vuelta: ahora va de I a S
            break

        # Probamos los 4 vecinos
        for mov_fila, mov_col in movimientos:
            nf, nc = fila + mov_fila, col + mov_col

            if nf < 0 or nf >= filas or nc < 0 or nc >= columnas:
                continue                # se sale del laberinto
            if laberinto[nf][nc] == 1:
                continue                # es pared
            if (nf, nc) in padre:
                continue                # ya la visitamos

            padre[(nf, nc)] = (fila, col)   # la marcamos como visitada
            cola.append((nf, nc))           # y la dejamos pendiente

        max_frontera = max(max_frontera, len(cola))

    return {
        "camino": camino,
        "explorados": explorados,
        "max_frontera": max_frontera,
        "tiempo": time.perf_counter() - inicio_tiempo,
    }


def mostrar_laberinto(laberinto, camino):
    """Dibuja el laberinto. El camino se marca con puntos (.)"""
    en_camino = set(camino) if camino else set()
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
    os.system("cls" if os.name == "nt" else "clear")

    if len(laberinto) == 0:
        print("El laberinto no puede estar vacío.")
        return

    inicio = buscar_posicion(laberinto, I)
    salida = buscar_posicion(laberinto, S)

    if inicio is None or salida is None:
        print("El laberinto necesita un inicio (I) y una salida (S).")
        return

    resultado = bfs(laberinto, inicio, salida)

    if resultado["camino"] is None:
        print("No hay salida en este laberinto.")
    else:
        print("¡Se encontró la salida!")
        print("Pasos dados:", len(resultado["camino"]) - 1)
        print()
        mostrar_laberinto(laberinto, resultado["camino"])
        print()
        print("Camino (fila, columna):")
        print(resultado["camino"])

    print()
    print("--- Métricas BFS ---")
    print("Casillas exploradas:", resultado["explorados"])
    print("Tamaño máximo de la cola:", resultado["max_frontera"])
    print(f"Tiempo: {resultado['tiempo'] * 1000:.3f} ms")


if __name__ == "__main__":
    main()