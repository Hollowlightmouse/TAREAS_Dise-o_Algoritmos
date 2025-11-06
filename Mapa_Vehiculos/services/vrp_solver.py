# Services/vrp_solver.py
from typing import Dict, List, Tuple
from collections import namedtuple
import math
import random

Route = namedtuple("Route", ["stops", "load", "arrival_times", "distance_km", "duration_min"])

class VRPSolver:
    """
    Implementación simple de Clarke-Wright Savings con comprobación de:
     - capacidad de vehículo
     - ventanas de tiempo (feasible check con tiempos de llegada y esperas)
    """

    def __init__(self, graph, depot_id: int, vehicle_count: int, vehicle_capacity: int):
        self.graph = graph
        self.depot = depot_id
        self.V = vehicle_count
        self.capacity = vehicle_capacity

    def initial_routes(self, customer_ids: List[int]) -> Dict[int, Route]:
        """
        Ruta inicial: cada cliente en su propia ruta: depot -> customer -> depot
        """
        routes = {}
        for cid in customer_ids:
            dist = self.graph.distance(self.depot, cid) + self.graph.distance(cid, self.depot)
            dur = self.graph.travel_time(self.depot, cid) + self.graph.travel_time(cid, self.depot)
            load = self.graph.nodes[cid].demand
            arrival = [0.0,  # arrival at depot at start
                       max(self.graph.nodes[cid].tw_start, self.graph.travel_time(self.depot, cid))]  # arrival at customer
            routes[cid] = Route(stops=[self.depot, cid, self.depot],
                                load=load,
                                arrival_times=arrival,
                                distance_km=dist,
                                duration_min=dur)
        return routes

    def savings_list(self, customer_ids: List[int]) -> List[Tuple[float, int, int]]:
        """
        Calcula la lista de ahorros: s_ij = c_depot_i + c_depot_j - c_ij
        """
        savings = []
        for i in customer_ids:
            for j in customer_ids:
                if i >= j:
                    continue
                s = self.graph.distance(self.depot, i) + self.graph.distance(self.depot, j) - self.graph.distance(i, j)
                savings.append((s, i, j))
        savings.sort(reverse=True, key=lambda x: x[0])
        return savings

    def feasible_merge(self, route_a: Route, route_b: Route, i: int, j: int) -> Tuple[bool, Route]:
        """
        Comprueba si es factible fusionar route_a (... i) + route_b (j ...) en términos de capacidad y ventanas.
        Asumimos i es el último cliente de route_a antes del depot y j es el primer cliente de route_b tras depot.
        """
        # nueva carga
        new_load = route_a.load + route_b.load
        if new_load > self.capacity:
            return False, None

        # construir nuevo orden de paradas (sin repetir depots intermedios)
        new_stops = route_a.stops[:-1] + route_b.stops[1:]  # remove trailing depot of a and leading depot of b

        # calcular tiempos de llegada secuencialmente con esperas si llega antes de ventana
        arrival_times = []
        time = 0.0  # tiempo en minutos desde salida del depot
        feasible = True
        for idx, node_id in enumerate(new_stops):
            if idx == 0:
                arrival_times.append(0.0)
                continue
            prev = new_stops[idx - 1]
            travel = self.graph.travel_time(prev, node_id)
            time += travel
            if node_id != self.depot:
                node = self.graph.nodes[node_id]
                # si llega antes de tw_start, espera hasta tw_start
                if time < node.tw_start:
                    time = float(node.tw_start)
                # si llega después de tw_end -> infeasible
                if time > node.tw_end:
                    feasible = False
                    break
                # añadir tiempo de servicio
                time += node.service_time
            arrival_times.append(time)

        if not feasible:
            return False, None

        # nueva distancia y duración
        total_dist = 0.0
        total_dur = 0.0
        for k in range(len(new_stops)-1):
            a = new_stops[k]
            b = new_stops[k+1]
            total_dist += self.graph.distance(a, b)
            total_dur += self.graph.travel_time(a, b)
        new_route = Route(stops=new_stops, load=new_load, arrival_times=arrival_times,
                          distance_km=total_dist, duration_min=total_dur)
        return True, new_route

    def solve(self, customer_ids: List[int]):
        # 1) Rutas iniciales (uno por cliente)
        routes = self.initial_routes(customer_ids)  # key por cliente inicial
        # 2) Lista de ahorros
        savings = self.savings_list(customer_ids)

        # Mapear cliente -> route_key para búsquedas rápidas
        cust_to_route = {cid: cid for cid in customer_ids}

        # 3) Iterar por ahorros e intentar fusionar
        for s, i, j in savings:
            rA_key = cust_to_route.get(i)
            rB_key = cust_to_route.get(j)
            if rA_key is None or rB_key is None or rA_key == rB_key:
                continue
            rA = routes[rA_key]
            rB = routes[rB_key]

            # Chequeamos que i sea el último antes del depot en rA y j sea el primero después del depot en rB
            # i debe estar en rA.stops[1:-1] y j en rB.stops[1:-1]
            if rA.stops[-2] != i or rB.stops[1] != j:
                # no es la configuración que nos facilita la fusión básica; ignorar para simplicidad
                continue

            feasible, merged = self.feasible_merge(rA, rB, i, j)
            if feasible:
                # crear nueva ruta y actualizar estructuras
                new_key = rA_key  # reutilizamos la llave de rA
                routes[new_key] = merged
                # borrar rB
                del routes[rB_key]
                # actualizar mapping de clientes apuntando a new_key
                for c in merged.stops:
                    if c != self.depot:
                        cust_to_route[c] = new_key

        # Al terminar, routes contiene tantas rutas como agrupaciones posibles.
        # Si hay más rutas que vehículos, hacemos un simple merge por distancia/compatibilidad hasta llegar a V rutas.
        # Si hay menos, algunas vehículos quedarán sin ruta.
        final_routes = list(routes.values())

        # Si hay más rutas que vehículos: combinar por heurística greedily (fusionar rutas factibles con menor aumento de costo)
        while len(final_routes) > self.V:
            best_pair = None
            best_increase = float("inf")
            best_merged = None
            for a_idx in range(len(final_routes)):
                for b_idx in range(a_idx+1, len(final_routes)):
                    A = final_routes[a_idx]
                    B = final_routes[b_idx]
                    # intentar fusionar A + B (as A last before depot and B first after depot) en ambas direcciones
                    # para simplicidad pruebo la candidate que preserve orden A + B
                    ok, merged = self.feasible_merge(A, B, A.stops[-2], B.stops[1])
                    if ok:
                        increase = merged.distance_km - (A.distance_km + B.distance_km)
                        if increase < best_increase:
                            best_increase = increase
                            best_pair = (a_idx, b_idx)
                            best_merged = merged
            if best_pair is None:
                # no hay fusiones factibles -> rompemos (no podemos reducir más)
                break
            a_idx, b_idx = best_pair
            # reemplazar
            new_list = []
            for idx, r in enumerate(final_routes):
                if idx == a_idx:
                    new_list.append(best_merged)
                elif idx == b_idx:
                    continue
                else:
                    new_list.append(r)
            final_routes = new_list

        # Si hay menos rutas que vehículos: dejamos vehículos vacíos también es aceptable
        return final_routes
