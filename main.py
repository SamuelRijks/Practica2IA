import json
from algorithm import (
    greedy_algorithm,
    knapsack_algorithm,
    dijkstra_algorithm,
    haversine,
)


def parse_coordinates(coord_str):
    lat, lon = map(float, coord_str.split(","))
    return (lat, lon)


def build_graph(restaurants, orders, start_coordinates):
    graph = {start_coordinates: {"start"}}

    # Add restaurants of the same specialty to graph
    for restaurant in restaurants:
        if restaurant["especialidad"] == orders[0]["especialitat"]:
            graph[restaurant["coordenadas"]] = {"restaurant"}

    # Add each order's coordinates to graph
    for order in orders:
        graph[order["coordenades"]] = {"entrega"}

    return graph


def build_graph_with_distances(graph):
    graph_with_distances = {}
    for node1 in graph:
        if len(node1) != 2:
            raise ValueError(f"Node {node1} does not have exactly two coordinates")
        graph_with_distances[node1] = {}
        for node2 in graph:
            if len(node2) != 2:
                raise ValueError(f"Node {node2} does not have exactly two coordinates")
            if node1 != node2:
                graph_with_distances[node1][node2] = haversine(node1, node2)
    return graph_with_distances


pes_mitja_menu = {
    "Africana": {"pes": 400, "temps_lliurament": 35},
    "Alemanya": {"pes": 380, "temps_lliurament": 38},
    "Americana": {"pes": 425, "temps_lliurament": 25},
    "Argentina": {"pes": 450, "temps_lliurament": 24},
    "Catalana": {"pes": 400, "temps_lliurament": 15},
    "Francesa": {"pes": 395, "temps_lliurament": 17},
    "Hindú": {"pes": 410, "temps_lliurament": 12},
    "Italiana": {"pes": 440, "temps_lliurament": 20},
    "Japonesa": {"pes": 300, "temps_lliurament": 30},
    "Mexicana": {"pes": 370, "temps_lliurament": 18},
    "Peruana": {"pes": 405, "temps_lliurament": 16},
    "Tailandesa": {"pes": 385, "temps_lliurament": 19},
    "Veneçolana": {"pes": 395, "temps_lliurament": 28},
    "Xinesa": {"pes": 350, "temps_lliurament": 32},
}


def main():

    with open("restaurants.json", "r", encoding="utf-8") as file:
        restaurants = json.load(file)
    with open("comandes.json", "r", encoding="utf-8") as file:
        comandes = json.load(file)

    max_weight = 12000

    # Group orders by specialty
    comandes_by_especialitat = {}
    for comanda in comandes:
        especialitat = comanda["especialitat"]
        if especialitat not in comandes_by_especialitat:
            comandes_by_especialitat[especialitat] = []
        comandes_by_especialitat[especialitat].append(comanda)

    # Process each group of orders
    for especialitat in list(
        comandes_by_especialitat.keys()
    ):  # Create a copy of the keys
        comandes_group = comandes_by_especialitat[especialitat]
        print(f"Processing orders for {especialitat}...")

        # Assign the average menu weight to each order
        for comanda in comandes_group:
            comanda["weight"] = pes_mitja_menu[especialitat]["pes"]
            comanda["temps_lliurament"] = pes_mitja_menu[especialitat][
                "temps_lliurament"
            ]

        # Apply Greedy algorithm to select orders with the smallest delivery commitment time
        selected_comandes_greedy = greedy_algorithm(comandes_group)
        print("Selected orders (Greedy):")
        for comanda in selected_comandes_greedy:
            print(comanda)

        # Remove selected orders from the group
        for comanda in selected_comandes_greedy:
            comandes_group.remove(comanda)

        # If all orders in the group have been delivered, remove the group
        if not comandes_group:
            del comandes_by_especialitat[especialitat]

        # Apply Knapsack problem with the orders selected by the Greedy algorithm
        selected_comandes_knapsack, total_weight = knapsack_algorithm(
            selected_comandes_greedy, max_weight
        )
        print(total_weight)
        print("Selected orders (Knapsack):")
        for comanda in selected_comandes_knapsack:
            print(comanda)

        # Build the graph of distances between restaurants using the coordinates
        start_coordinates = "41.528154350078815,2.4346229558256196"
        graph = build_graph(restaurants, selected_comandes_knapsack, start_coordinates)

        # Convert the nodes to tuples
        def convert_to_tuple(coord_str):
            return tuple(map(float, coord_str.split(",")))

        graph = {convert_to_tuple(node): neighbors for node, neighbors in graph.items()}

        graph_with_distances = build_graph_with_distances(graph)
        distances = dijkstra_algorithm(graph_with_distances)

        # Print only the restaurant and the delivery points of the orders
        print("Shortest route:")
        for comanda in selected_comandes_knapsack:
            delivery_point = convert_to_tuple(comanda["coordenades"])
            print(
                f"Delivery point: {comanda['coordenades']}, Distance: {distances[delivery_point]}"
            )


if __name__ == "__main__":
    main()
