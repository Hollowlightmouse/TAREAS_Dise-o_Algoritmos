# Lib.py

def inicializar_torres():
    # Inicializa las torres
    return [[5, 4, 3, 2, 1], [], []]


def mostrar_torres(torres):
    # Muestra el estado actual
    print(f"Torre 1: {torres[0]}")
    print(f"Torre 2: {torres[1]}")
    print(f"Torre 3: {torres[2]}")
    print("-" * 40)


def mover_pieza(torres, origen, destino):
    # Mueve una pieza validando reglas
    if not torres[origen]:
        return False  # no hay nada que mover
    if torres[destino] and torres[destino][-1] < torres[origen][-1]:
        return False  # no se puede poner grande sobre pequeño
    
    pieza = torres[origen].pop()
    torres[destino].append(pieza)
    print(f"Moviendo pieza {pieza} de Torre {origen+1} a Torre {destino+1}")
    mostrar_torres(torres)
    return True


def resolver_hanoi_simple(torres):
    # Resuelve Hanoi iterativamente
    objetivo = [5, 4, 3, 2, 1]
    movimientos = 0
    
    while torres[2] != objetivo:
        if mover_pieza(torres, 0, 1) or mover_pieza(torres, 1, 0):
            movimientos += 1
        if torres[2] == objetivo: break

        if mover_pieza(torres, 0, 2) or mover_pieza(torres, 2, 0):
            movimientos += 1
        if torres[2] == objetivo: break

        if mover_pieza(torres, 1, 2) or mover_pieza(torres, 2, 1):
            movimientos += 1
    
    print(f"Total de movimientos realizados: {movimientos}")
