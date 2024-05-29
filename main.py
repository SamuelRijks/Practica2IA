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


def build_graph(restaurants):
    graph = {}
    for i, rest1 in enumerate(restaurants):
        graph[i] = {}
        coord1 = parse_coordinates(rest1["coordenades"])
        for j, rest2 in enumerate(restaurants):
            if i != j:
                coord2 = parse_coordinates(rest2["coordenades"])
                distance = haversine(coord1, coord2)
                graph[i][j] = distance
    return graph


pes_mitja_menu = {
    "Africana": 400,
    "Alemanya": 380,
    "Americana": 425,
    "Argentina": 450,
    "Catalana": 400,
    "Francesa": 395,
    "Hindú": 410,
    "Italiana": 440,
    "Japonesa": 300,
    "Mexicana": 370,
    "Peruana": 405,
    "Tailandesa": 385,
    "Veneçolana": 395,
    "Xinesa": 350,
}


def main():
    # Lectura de dades
    with open("restaurants.json", "r") as file:
        restaurants = json.load(file)
    with open("comandes.json", "r") as file:
        comandes = json.load(file)

    # Assignar el pes mitjà del menú a cada comanda
    for comanda in comandes:
        restaurant_id = comanda["restaurant_id"]
        especialitat = next(
            (
                rest["especialitat"]
                for rest in restaurants
                if rest["id"] == restaurant_id
            ),
            None,
        )
        if especialitat:
            comanda["weight"] = pes_mitja_menu.get(especialitat, 0)

    # Aplicar algoritme Greedy
    selected_comandes_greedy = greedy_algorithm(comandes)
    print("Comandes seleccionades (Greedy):")
    for comanda in selected_comandes_greedy:
        print(comanda)

    # Definir el pes màxim que pot portar la motxilla (per exemple 2000 grams)
    max_weight = 2000

    # Aplicar problema de la motxilla amb les comandes seleccionades pel Greedy
    selected_comandes_knapsack = knapsack_algorithm(
        selected_comandes_greedy, max_weight
    )
    print("Comandes seleccionades (Knapsack):")
    for comanda in selected_comandes_knapsack:
        print(comanda)

    # Construir el graf de distàncies entre restaurants utilitzant les coordenades
    graph = build_graph(restaurants)

    # Aplicar algoritme de Dijkstra
    distances, shortest_path = dijkstra_algorithm(
        graph, 0
    )  # Partim del restaurant amb id 0
    print("Distàncies més curtes des del restaurant 0:")
    print(distances)


if __name__ == "__main__":
    main()
