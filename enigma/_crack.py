import string
import random
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import defaultdict


def get_possible_settings():
    rotor_options = [",".join(c) for c in permutations(["I", "II", "III"], 3)]
    positions = [",".join(c) for c in product(string.ascii_uppercase, string.ascii_uppercase, string.ascii_uppercase)]
    return product(rotor_options, "B", positions)


def get_random_enigma():
    settings = random.choice(list(get_possible_settings()))
    return Enigma(*settings)


def brute_force_settings(enigma, target="AAAAAAAA"):
    encrypted_target = enigma.encrypt(target)
    print(encrypted_target)
    for i, setting in enumerate(get_possible_settings()):
        if i % 100 == 0:
            print(f"tested {i} configurations...")
        potential_enigma = Enigma(*setting)
        if encrypted_target == potential_enigma.encrypt(target):
            print(encrypted_target)
            return setting


def build_loop_graph(cypher_text, crib):
    g = nx.Graph()
    weighted_edges = [(n1, n2, w) for w, (n1, n2) in enumerate(zip(cypher_text, crib))]
    g.add_weighted_edges_from(weighted_edges)
    return g

def list_paths(g):
    cycles = nx.cycle_basis(g)
    print(cycles)


class Graph:
    def __init__(self, directional=False):
        self._directional = directional
        self._graph = defaultdict(set)

    def add_edge(self, node1, node2, weight=0):
        self._graph[node1].add((weight, node2), )
        if not self._directional:
            self._graph[node2].add((weight, node1), )

    # def find_all_loops(self):
    #     starting_nodes = list(self._graph.keys())
    #     in_loop
    #     for n in

    def find_loop(self, start_node, current_node=None, visited_nodes=None, previous_node=None):
        current_node = current_node if current_node else start_node
        visited_nodes = set(visited_nodes) if visited_nodes else set()
        visited_nodes.add(current_node)
        sub_paths = []
        for weight, next_node in self._graph[current_node]:
            base_path = ((current_node, weight, next_node),)
            if next_node == start_node and next_node != previous_node:
                sub_paths.append(base_path)
                continue
            if next_node in visited_nodes:
                continue
            for sp in self.find_loop(start_node, next_node, visited_nodes, current_node):
                sub_paths.append(base_path + sp)
        return sub_paths


if __name__ == "__main__":
    ct = "IUGHLUVFAOBNEWNAGZW"
    crib = "MARKWORTHXATTACKEDX"
    g = build_loop_graph(ct, crib)
    list_paths(g)
    nx.draw_circular(g)
    plt.show()



