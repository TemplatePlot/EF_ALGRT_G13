from collections import deque
import heapq
import time


SIMBOLOS = ("0", "1", "I", "S") # I = inicio, S = salida, 0 = camino, 1 = pared
I = "I"
S = "S"

def CrearLaberinto(laberintoN): # Crea un laberinto siempre y cuando no haya uno registrado, si ya hay uno registrado no hace nada.
    if len(laberintoN) != 0:
        print("El laberinto ya ha sido definido.")
        return

    print("No se ha definido un laberinto, por favor ingresa un tamaño.")
    n = int(input("Ingresa el tamaño de la matriz (N): "))
    print("====================")

    while True:
        for i in range(n):
            while True:
                entrada = input(f"Ingresa los {n} valores de la fila {i + 1} separados por espacio: ")
                fila = entrada.split()
                if len(fila) == n and all(x in SIMBOLOS for x in fila):   # solo 0, 1, I, S
                    break
                print(f"Error: la fila {i + 1} debe tener {n} valores y solo 0, 1, I o S. Registrala correctamente.")
            laberintoN.append([int(x) if x in ("0", "1") else x for x in fila])

        # Revisa que haya exactamente un inicio (I) y una salida (S)
        aplanado = [v for f in laberintoN for v in f]
        if aplanado.count("I") == 1 and aplanado.count("S") == 1:
            break
        print("Error: el laberinto debe tener un Inicio (I) y una Salida (S). Registra el laberinto correctamente.")
        laberintoN.clear()

    print("Laberinto registrado correctamente.")


# Definimos el laberinto como una matriz de 21x21, donde cada celda puede ser un camino (0) o una pared (1).
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
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,S]
]

# Los 4 movimientos posibles: abajo, derecha, arriba, izquierda
movimientos = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def buscar_posicion(laberinto, letra): # Busca la fila y columna donde está la letra (I o S).
   
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            if laberinto[fila][col] == letra:
                return (fila, col)
    return None

inicio = buscar_posicion(laberinto, I)
salida = buscar_posicion(laberinto, S)
if inicio is None or salida is None:
        print("El laberinto necesita un inicio (I) y una salida (S).")
        exit()

def bfs(laberinto, inicio, salida): # HECHO POR PAULO
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

def backtracking(laberinto, fila, col, camino, visitados): ## Hecho por Christian
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
        if backtracking(laberinto, fila + mov_fila, col + mov_col, camino, visitados):
            return True

    # 5. RETROCEDER: ningún movimiento llegó a la salida,
    #    así que quitamos esta casilla del camino y volvemos atrás
    camino.pop()
    return False

def heuristica(nodo_actual, nodo_destino): # HECHO POR YOEL
    """Calcula la distancia Manhattan entre dos puntos como heurística para A*."""
    return abs(nodo_actual[0] - nodo_destino[0]) + abs(nodo_actual[1] - nodo_destino[1])

def resolver_a_star(laberinto, inicio, salida): # HECHO POR YOEL
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
        for df, dc in movimientos:
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

def dfs(laberinto,inicio,salida): # HECHO POR FABIO
    filas = len(laberinto)
    columnas = len(laberinto[0])
    pila = [inicio] # funciona con append y pop
    visitados = set() # almacena casillas ya visitadas
    padre = {} # almacena la ruta de cada casilla para reconstruir el camino

    while pila:
        f,c = pila.pop() # saca la casilla más reciente
        if (f,c) in visitados: 
            continue
        visitados.add((f,c)) # marca la casilla como visitada
        
        if (f, c) == salida: # si llegamos a la salida, reconstruimos el camino usando la variable padre
            return reconstruir_camino(padre, inicio, (f, c))
        for df,dc in movimientos: # usa la lista de movimientos
            nf = f + df
            nc = c + dc

            if not (0 <= nf < filas and 0 <= nc < columnas): # dentro del laberinto
                continue
            if laberinto[nf][nc] !=1 and (nf,nc) not in visitados: # no es pared y no ha sido visitada
                padre[(nf,nc)] = (f,c) # guarda la casilla de donde venimos
                pila.append((nf,nc)) # agrega la casilla a la pila para explorarla después
    return None # si no se encuentra la salida, devuelve None
    
def reconstruir_camino(padre, inicio, salida): # reconstruye el camino desde la salida hasta el inicio usando la variable padre
    ruta = [salida]
    actual = salida
    while actual != inicio:
        actual = padre[actual]
        ruta.append(actual)
    return ruta[::-1] # devuelve el camino de inicio a salida


def mostrar_laberinto(laberinto, camino): # Dibuja el laberinto, el camino se marca con puntos (.)
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


print("Bienvenido al resolvedor de laberintos.")
CrearLaberinto(laberinto)
print("================================================")
print("Por favor, elija una opción:")
print("================================================")
print("1. Resolver el laberinto con BFS")
print("2. Resolver el laberinto con DFS")
print("3. Resolver el laberinto con A*")
print("4. Resolver el laberinto con Backtracking")
print("===============================================")
op = int(input())

match op:
    case 1:
        print("================================================")
        print("Resolviendo el laberinto con BFS...")
        print("================================================")
        resultado = bfs(laberinto, inicio, salida)
        
        if resultado["camino"] is None:
            print("No hay salida en este laberinto.")
        else:
            print("¡Se encontró la salida!")
            print("Pasos dados:", len(resultado["camino"]) - 1)
            print("Camino (fila, columna):")
            print(resultado["camino"])
        mostrar_laberinto(laberinto, resultado["camino"])
        print("--- Métricas BFS ---")
        print("Casillas exploradas:", resultado["explorados"])
        print("Tamaño máximo de la cola:", resultado["max_frontera"])
        print(f"Tiempo: {resultado['tiempo'] * 1000:.3f} ms")

    case 2:
        print("================================================")
        print("Resolviendo el laberinto con DFS...")
        print("================================================")
        resultado = dfs(laberinto, inicio, salida)
        if resultado is None:
            print("No hay salida en este laberinto.")
        else:
            print("¡Se encontró la salida!")
            print("Pasos dados:", len(resultado) - 1)
            print("Camino (fila, columna):")
            print(resultado)
        mostrar_laberinto(laberinto, resultado)   
    case 3:
        print("================================================")
        print("Resolviendo el laberinto con A*...")
        print("================================================")
        resultado = resolver_a_star(laberinto, inicio, salida)
        if resultado["camino"]:
                print(f"¡Camino encontrado con éxito!")
                print(f"Ruta de coordenadas: {resultado['camino']}")
                print(f"Nodos explorados: {resultado['explorados']}")
                print(f"Tamaño máximo de la frontera: {resultado['max_frontera']}")
                print(f"Tiempo de ejecución: {resultado['tiempo_ms']:.4f} ms")
        else:
            print("No se encontró una ruta posible en este laberinto.")
        mostrar_laberinto(laberinto, resultado["camino"])
        

    case 4:
        print("================================================")
        print("Resolviendo el laberinto con Backtracking...")
        print("================================================")
        camino = []
        visitados = set()
        if backtracking(laberinto, inicio[0], inicio[1], camino, visitados):
                print("¡Se encontró la salida!")
                print("Pasos dados:", len(camino) - 1)
                print("Camino (fila, columna):")
                print(camino)
                mostrar_laberinto(laberinto, camino)
        else:
            print("No hay salida en este laberinto.")

