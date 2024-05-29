import json
from delivery_algorithms import greedy_algorithm, knapsack_algorithm, dijkstra_algorithm
from utils import load_data


def main():
    # Lectura de dades
    with open("restaurants.json", "r") as file:
        restaurants = json.load(file)
    with open("comandes.json", "r") as file:
        comandes = json.load(file)

    # Aplicar algoritme Greedy
    selected_comandes_greedy = greedy_algorithm(comandes)
    print("Comandes seleccionades (Greedy):")
    for comanda in selected_comandes_greedy:
        print(comanda)

    # Aplicar problema de la motxilla
    selected_comandes_knapsack = knapsack_algorithm(comandes)
    print("Comandes seleccionades (Knapsack):")
    for comanda in selected_comandes_knapsack:
        print(comanda)

    # Definir el graf de distàncies entre restaurants (aquest graf ha de ser creat prèviament)
    graph = {
        # Exemple de graf amb distàncies entre nodes (restaurants)
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "C": 2, "D": 5},
        "C": {"A": 4, "B": 2, "D": 1},
        "D": {"B": 5, "C": 1},
    }

    # Aplicar algoritme de Dijkstra
    distances, shortest_path = dijkstra(graph, "A")
    print("Distàncies més curtes des de 'A':")
    print(distances)


if __name__ == "__main__":
    main()
