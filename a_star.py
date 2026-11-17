import time
from collections import deque
import heapq

# Definimos los movimientos posibles: Abajo, Derecha, Arriba, Izquierda
MOVIMIENTOS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def buscar_posicion(laberinto, letra):
    """Busca y retorna las coordenadas (fila, col) de la letra indicada (I o F)."""
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            if laberinto[fila][col] == letra:
                return (fila, col)
    return None

def heuristica(nodo_actual, nodo_destino):
    """Calcula la distancia Manhattan entre dos puntos como heurística para A*."""
    return abs(nodo_actual[0] - nodo_destino[0]) + abs(nodo_actual[1] - nodo_destino[1])

def resolver_a_star(laberinto, inicio, salida):
    """
    Resuelve el laberinto usando el algoritmo A* (A-Star).
    Utiliza f(n) = g(n) + h(n), donde:
    - g(n): costo real desde el inicio hasta el nodo actual.
    - h(n): costo estimado (heurística) desde el nodo actual hasta la salida.
    """
    inicio_tiempo = time.perf_counter()
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    # Cola de prioridad que almacena tuplas: (f_coste, g_coste, (fila, col))
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, 0, inicio))
    
    # Diccionarios para rastrear el camino y los costos g
    padre = {inicio: None}
    g_costes = {inicio: 0}
    
    explorados = 0
    max_frontera = 1
    camino_encontrado = None
    
    while cola_prioridad:
        max_frontera = max(max_frontera, len(cola_prioridad))
        
        # Extraemos el nodo con menor costo total f(n)
        f_actual, g_actual, actual = heapq.heappop(cola_prioridad)
        explorados += 1
        
        # Verificamos si llegamos a la meta
        if actual == salida:
            camino_encontrado = []
            nodo = salida
            while nodo is not None:
                camino_encontrado.append(nodo)
                nodo = padre[nodo]
            camino_encontrado.reverse()
            break
            
        # Exploramos los vecinos
        for df, dc in MOVIMIENTOS:
            vecino = (actual[0] + df, actual[1] + dc)
            
            # Validamos límites y que no sea una pared (1)
            if (0 <= vecino[0] < filas) and (0 <= vecino[1] < columnas):
                if laberinto[vecino[0]][vecino[1]] != 1:
                    nuevo_g = g_actual + 1  # Costo uniforme de 1 por movimiento
                    
                    # Si encontramos un camino mejor hacia el vecino
                    if vecino not in g_costes or nuevo_g < g_costes[vecino]:
                        g_costes[vecino] = nuevo_g
                        h_coste = heuristica(vecino, salida)
                        f_coste = nuevo_g + h_coste
                        
                        heapq.heappush(cola_prioridad, (f_coste, nuevo_g, vecino))
                        padre[vecino] = actual
                        
    fin_tiempo = time.perf_counter()
    tiempo_total = (fin_tiempo - inicio_tiempo) * 1000  # en milisegundos
    
    return {
        "camino": camino_encontrado,
        "explorados": explorados,
        "max_frontera": max_frontera,
        "tiempo_ms": tiempo_total
    }

# ==========================================
# EJEMPLO DE PRUEBA Y EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Definimos el laberinto de prueba (I = Inicio, F = Fin, 0 = Camino, 1 = Pared)
    laberinto_prueba = [
        ['I', 0, 1, 0, 0],
        [ 1,  0, 1, 0, 1],
        [ 0,  0, 0, 0, 0],
        [ 0,  1, 1, 1, 0],
        [ 0,  0, 0, 1, 'F']
    ]
    
    inicio = buscar_posicion(laberinto_prueba, 'I')
    salida = buscar_posicion(laberinto_prueba, 'F')
    
    print("--- EJECUTANDO ALGORITMO A* ---")
    resultado = resolver_a_star(laberinto_prueba, inicio, salida)
    
    if resultado["camino"]:
        print(f"¡Camino encontrado con éxito!")
        print(f"Ruta de coordenadas: {resultado['camino']}")
        print(f"Nodos explorados: {resultado['explorados']}")
        print(f"Tamaño máximo de la frontera: {resultado['max_frontera']}")
        print(f"Tiempo de ejecución: {resultado['tiempo_ms']:.4f} ms")
    else:
        print("No se encontró una ruta posible en este laberinto.")
