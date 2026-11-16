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
        print("Error: el laberinto debe tener una I (inicio) y una S (salida). Registra el laberinto correctamente.")
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

    case 2:
        print("================================================")
        print("Resolviendo el laberinto con DFS...")
        print("================================================")

    case 3:
        print("================================================")
        print("Resolviendo el laberinto con A*...")
        print("================================================")

    case 4:
        print("================================================")
        print("Resolviendo el laberinto con Backtracking...")
        print("================================================")