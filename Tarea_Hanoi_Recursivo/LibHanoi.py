# LibHanoi.py 


# Inicializa las torres con las piezas
def inicializar_torres():
    return [[5, 4, 3, 2, 1], [], []]


# Muestra el estado actual de las tres torres
def mostrar_torres(torres):
    print(f"Torre 1: {torres[0]}")
    print(f"Torre 2: {torres[1]}")
    print(f"Torre 3: {torres[2]}")
    print("-" * 40)


# Mueve una pieza entre torres si cumple las reglas del juego
def mover_pieza(torres, origen, destino):
    if not torres[origen]:
        return False
    if torres[destino] and torres[destino][-1] < torres[origen][-1]:
        return False
    pieza = torres[origen].pop()
    torres[destino].append(pieza)
    print(f"Moviendo pieza {pieza} de Torre {origen + 1} a Torre {destino + 1}")
    mostrar_torres(torres)
    return True


# Aplica recursividad para resolver el juego hasta alcanzar la torre final completa
def resolver_hanoi(torres, n, origen, auxiliar, destino):
    if torres[2] == [5, 4, 3, 2, 1]:
        print("Caso base alcanzado. ¡Torres completadas!")
        return
    if n == 1:
        mover_pieza(torres, origen, destino)
    else:
        resolver_hanoi(torres, n - 1, origen, destino, auxiliar)
        mover_pieza(torres, origen, destino)
        resolver_hanoi(torres, n - 1, auxiliar, origen, destino)


# Controla la ejecución principal del algoritmo de las torres de Hanoi
def resolver_hanoi_simple(torres):
    print("Estado inicial:")
    mostrar_torres(torres)
    n = len(torres[0])
    resolver_hanoi(torres, n, 0, 1, 2)
    print("¡Proceso finalizado! Estado final:")
    mostrar_torres(torres)
