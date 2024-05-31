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
    graph = {start_coordinates: {}}

    # Add restaurants of the same specialty to graph
    for restaurant in restaurants:
        if restaurant["especialidad"] == orders[0]["especialitat"]:
            graph[restaurant["coordenadas"]] = {}

    # Add each order's coordinates to graph
    for order in orders:
        graph[order["coordenades"]] = {}

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
# el repartidor ha d'omplir la motxilla (12kg) recolling el menjar dels restaurants més propers segons les especialitats especificades
# a dins de les comandes i es fa el repartimemt utilitzant dijkstra per trobar el camí més curt entre els restaurants. Quan
# es buidi la motxilla, es repatirà aquest procés fins haver complert totes les comandes


def main():

    # Lectura de dades
    with open("restaurants.json", "r", encoding="utf-8") as file:
        restaurants = json.load(file)
    with open("comandes.json", "r", encoding="utf-8") as file:
        comandes = json.load(file)

    # Define the maximum weight the backpack can carry
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

        # Apply Dijkstra's algorithm
        distances = dijkstra_algorithm(graph)  # We start from the restaurant with id 0

        # Print only the restaurant and the delivery points of the orders
        print("Shortest distances from restaurant 0:")
        for comanda in selected_comandes_knapsack:
            print(
                f"Delivery point: {comanda['coordenades']}, Distance: {distances[comanda['coordenades']]}"
            )


if __name__ == "__main__":
    main()
