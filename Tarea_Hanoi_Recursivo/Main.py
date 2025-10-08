# main.py
import LibHanoi
print("=== Torres de Hanoi (Versión Simple) ===")
torres = LibHanoi.inicializar_torres()
LibHanoi.mostrar_torres(torres)

LibHanoi.resolver_hanoi_simple(torres)

print("\n¡Juego completado! La Torre 3 contiene todas las piezas en orden.")


