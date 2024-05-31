import heapq
import math


def dijkstra_algorithm(graph):
    # Elige el primer nodo del grafo como el nodo de inicio
    start = next(iter(graph))
    print(f"Start node: {start}")

    distances = {node: float("infinity") for node in graph}
    distances[start] = 0

    # Crea una cola de prioridad y agrega el nodo de inicio con una distancia de 0
    queue = [(0, start)]

    while queue:
        # Extrae el nodo con la distancia más corta
        current_distance, current_node = heapq.heappop(queue)

        # Si la distancia extraída es mayor que la distancia conocida del nodo, ignora este nodo
        if current_distance > distances[current_node]:
            continue

        # Para cada vecino del nodo, calcula la distancia a través del nodo
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Si esta distancia es menor que la distancia conocida del vecino,
            # actualiza la distancia del vecino y agrega el vecino a la cola de prioridad
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    # Encuentra el restaurante con la distancia más corta
    shortest_distance = min(distances.values())
    shortest_distance_restaurant = [
        node for node, distance in distances.items() if distance == shortest_distance
    ][0]

    print(
        f"Restaurant with shortest distance: {shortest_distance_restaurant}, Distance: {shortest_distance}"
    )

    return distances


def greedy_algorithm(comandes):
    selected_comandes = sorted(
        comandes, key=lambda x: x["temps_lliurament"]
    )  # Ordenar per temps de lliurament més curt

    return selected_comandes


def knapsack_algorithm(comandes, max_weight):
    n = len(comandes)
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            if comandes[i - 1]["weight"] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - comandes[i - 1]["weight"]]
                    + comandes[i - 1]["weight"],
                )
            else:
                dp[i][w] = dp[i - 1][w]

    selected_comandes = []
    total_weight = 0
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_comandes.append(comandes[i - 1])
            w -= comandes[i - 1]["weight"]
            total_weight += comandes[i - 1]["weight"]

    return (
        selected_comandes[::-1],
        total_weight,
    )


def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
