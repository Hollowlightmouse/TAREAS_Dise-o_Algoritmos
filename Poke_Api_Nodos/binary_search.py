class BinarySearch:
    @staticmethod
    def search(sorted_list, target, left=0, right=None):
        # Implementa el algoritmo de búsqueda binaria de forma recursiva dividiendo el espacio de búsqueda a la mitad en cada llamada hasta encontrar el elemento o determinar que no existe
        if right is None:
            right = len(sorted_list) - 1
        
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            return BinarySearch.search(sorted_list, target, mid + 1, right)
        else:
            return BinarySearch.search(sorted_list, target, left, mid - 1)