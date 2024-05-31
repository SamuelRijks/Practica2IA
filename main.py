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


def build_graph(restaurants, orders):
    graph = {}

    # Add restaurants to graph
    for restaurant in restaurants:
        graph[restaurant["coordenades"]] = {}

    # Add delivery addresses to graph
    for order in orders:
        graph[order["coordenades"]] = {}

    # Calculate distances between all pairs of nodes
    for node1 in graph:
        for node2 in graph:
            if node1 != node2:
                coord1 = parse_coordinates(node1)
                coord2 = parse_coordinates(node2)
                graph[node1][node2] = haversine(coord1, coord2)

    return graph


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
    # el repartidor ha d'omplir la motxilla (12kg) recolling el menjar dels restaurants més propers segons les especialitats especificades
    # a dins de les comandes i es fa el repartimemt utilitzant dijkstra per trobar el camí més curt entre els restaurants. Quan
    # es buidi la motxilla, es repatirà aquest procés fins haver complert totes les comandes
    # Lectura de dades
    with open("restaurants.json", "r", encoding="utf-8") as file:
        restaurants = json.load(file)
    with open("comandes.json", "r", encoding="utf-8") as file:
        comandes = json.load(file)

    # Define the maximum weight the backpack can carry
    max_weight = 12000

    # Repeat until all orders are delivered
    while comandes:
        # Assign the average menu weight to each order
        for comanda in comandes:
            especialitat = comanda["especialitat"]
            comanda["weight"] = pes_mitja_menu[especialitat]["pes"]
            comanda["temps_lliurament"] = pes_mitja_menu[especialitat][
                "temps_lliurament"
            ]

        # Apply Greedy algorithm to select orders with the smallest delivery commitment time
        selected_comandes_greedy = greedy_algorithm(comandes)
        print("Selected orders (Greedy):")
        for comanda in selected_comandes_greedy:
            print(comanda)

        # Apply Knapsack problem with the orders selected by the Greedy algorithm
        selected_comandes_knapsack = knapsack_algorithm(
            selected_comandes_greedy, max_weight
        )
        print("Selected orders (Knapsack):")
        for comanda in selected_comandes_knapsack:
            print(comanda)

        # Build the graph of distances between restaurants using the coordinates
        graph = build_graph(restaurants, selected_comandes_knapsack)

        # Apply Dijkstra's algorithm
        distances = dijkstra_algorithm(
            graph, 0
        )  # We start from the restaurant with id 0
        print("Shortest distances from restaurant 0:")
        print(distances)

        # Remove delivered orders from the list of orders
        for comanda in selected_comandes_knapsack:
            comandes.remove(comanda)


if __name__ == "__main__":
    main()
