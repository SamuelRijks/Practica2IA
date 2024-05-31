import heapq
import math


import heapq

import heapq


def dijkstra_algorithm(graph, start):
    distances = {node: float("infinity") for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

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
    )  # Return both the orders and the total weight


def haversine(coord1, coord2):
    # Converteix de graus a radians
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    # Diferències de les coordenades
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Radi de la Terra en quilòmetres (6371)
    km = 6371 * c
    return km
