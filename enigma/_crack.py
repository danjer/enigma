import string
import random
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import deque, defaultdict
from copy import deepcopy


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
        self.plugboard_pairs = {l: set((l2 for l2 in string.ascii_uppercase)) for l in string.ascii_uppercase}
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
        for loop in self.loops:
            invalid_guesses = defaultdict(set)
            for pstart in self.plugboard_pairs[loop[0][0]]:
                print(f"testing with initial pair {loop[0][0]} --> {pstart}")
                current_guesses = defaultdict(set)
                last_guess = pstart
                current_guesses[loop[0][0]].add(last_guess)
                for _, w, next_guess in loop:
                    enigma = Enigma()
                    last_guess = enigma.encrypt("".join([last_guess for _ in range(w + 1)]))[-1]
                    current_guesses[next_guess].add(last_guess)
                if pstart != last_guess:
                    print(f"{loop[0][0]} --> {pstart} cant be true")
                    for k, v in current_guesses.items():
                        invalid_guesses[k].update(v)
                    print(current_guesses)
                else:
                    print(f"{loop[0][0]} --> {pstart} is a possible setting...")
            for k, v in invalid_guesses.items():
                self.plugboard_pairs[k] -= v
                for cv in v:
                    self.plugboard_pairs[cv].discard(k)
            print(self.plugboard_pairs)
            for i in self.plugboard_pairs.values():
                print(len(i))
            print(f"number ofloops {len(self.loops)}")



if __name__ == "__main__":
    e = Enigma(plugboard_pairs="AB,OM,CD,HQ,XZ,NK,EP,WT")
    e = Enigma()
    text = "watmaakthetuitalsikhiereenminderlangverhaaltypowheeftdatweleffect".upper()
    cypher_text = e.encrypt(text)
    pbc = PlugBoardCracker(text, cypher_text)
    pbc.eliminate_pairs()
    i = 1
    for v in list(pbc.plugboard_pairs.values())[:13]:
        i *= len(v)
    print(i)
