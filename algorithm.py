import heapq


def dijkstra_algorithm(graph, start):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float("infinity") for node in graph}
    distances[start] = 0
    shortest_path = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    return distances, shortest_path


def greedy_algorithm(comandes, max_weight=12):
    comandes.sort(
        key=lambda x: x["temps_lliurament"]
    )  # Ordenar per temps de lliurament més curt
    selected_comandes = []
    total_weight = 0

    for comanda in comandes:
        if total_weight + comanda["pes"] <= max_weight:
            selected_comandes.append(comanda)
            total_weight += comanda["pes"]

    return selected_comandes


def knapsack_algorithm(comandes, max_weight=12):
    n = len(comandes)
    K = [[0 for x in range(max_weight + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(max_weight + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif comandes[i - 1]["pes"] <= w:
                K[i][w] = max(
                    comandes[i - 1]["pes"] + K[i - 1][w - comandes[i - 1]["pes"]],
                    K[i - 1][w],
                )
            else:
                K[i][w] = K[i - 1][w]

    res = K[n][max_weight]
    w = max_weight
    selected_comandes = []

    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            selected_comandes.append(comandes[i - 1])
            res = res - comandes[i - 1]["pes"]
            w = w - comandes[i - 1]["pes"]

    return selected_comandes
