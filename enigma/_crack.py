import string
import random
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import deque


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


class PlugBoardCracker:

    def __init__(self, text, cypher_text):
        self.text = text
        self.cypher_text = cypher_text
        self.plugboard_pairs = {l: [l2 for l2 in string.ascii_uppercase] for l in string.ascii_uppercase}
        self.loops = self.get_loops()

    def get_loops(self):
        g = self.build_loop_graph()
        cycles = nx.cycle_basis(g)
        nw_cycles = []
        for cycle in cycles:
            shifted_cycle = deque(cycle)
            shifted_cycle.rotate(1)
            shifted_cycle = list(shifted_cycle)
            nw_cycles.append([(n1, g.get_edge_data(n1, n2)['weight'], n2) for n1, n2 in zip(shifted_cycle, cycle)])
        return nw_cycles

    def build_loop_graph(self):
        g = nx.Graph()
        weighted_edges = [(n1, n2, w) for w, (n1, n2) in enumerate(zip(self.cypher_text, self.text))]
        g.add_weighted_edges_from(weighted_edges)
        return g

    def eliminate_pairs(self):
        loop = self.loops[0]
        for possible_


if __name__ == "__main__":
    e = Enigma(plugboard_pairs="AB,OM,CD,HQ,XZ,NK,EP,WT")
    text = "watmoetiktocheensschrijvenhierhetmoetwellanggenoegzijn".upper()
    cypher_text = e.encrypt(text)
    pbc = PlugBoardCracker(text, cypher_text)
    pbc.eliminate_pairs()
