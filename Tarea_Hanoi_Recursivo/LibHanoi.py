# LibHanoi.py — Versión Recursiva

def inicializar_torres():
    # Inicializa las torres
    return [[5, 4, 3, 2, 1], [], []]


def mostrar_torres(torres):
    print(f"Torre 1: {torres[0]}")
    print(f"Torre 2: {torres[1]}")
    print(f"Torre 3: {torres[2]}")
    print("-" * 40)


def mover_pieza(torres, origen, destino):
    # Verifica que haya piezas
    if not torres[origen]:
        return False
    # No permite mover disco grande sobre uno más pequeño
    if torres[destino] and torres[destino][-1] < torres[origen][-1]:
        return False
    
    pieza = torres[origen].pop()
    torres[destino].append(pieza)
    print(f"Moviendo pieza {pieza} de Torre {origen + 1} a Torre {destino + 1}")
    mostrar_torres(torres)
    return True


def resolver_hanoi(torres, n, origen, auxiliar, destino):
    # Caso base: cuando todas las piezas están en la torre destino
    if torres[2] == [5, 4, 3, 2, 1]:
        print("Caso base alcanzado. ¡Torres completadas!")
        return

    if n == 1:
        mover_pieza(torres, origen, destino)
    else:
        # Mueve n-1 discos a la torre auxiliar
        resolver_hanoi(torres, n-1, origen, destino, auxiliar)
        # Mueve el disco más grande al destino
        mover_pieza(torres, origen, destino)
        # Mueve los n-1 discos desde auxiliar a destino
        resolver_hanoi(torres, n-1, auxiliar, origen, destino)


def resolver_hanoi_simple(torres):
    print("Estado inicial:")
    mostrar_torres(torres)
    n = len(torres[0])
    resolver_hanoi(torres, n, 0, 1, 2)
    print("¡Proceso finalizado! Estado final:")
    mostrar_torres(torres)
