import string
import random
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import deque, defaultdict
from copy import deepcopy

class InvalidSettings(Exception):
    pass

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


class RotorOrder:

    def __init__(self, text, cypher_text):
        self._text = text
        self._cypher_text = cypher_text
        self.best_setting = None
        self.best_settings = []
        self.best_score = -1

    def get_rotor_order(self):
        for count, setting in enumerate(get_possible_settings()):
            score = self.score_setting(setting)
            print(f"attempt number {count}")
            self.best_settings.append((setting, score))
        self.best_settings.sort(key=lambda x: x[-1])

    def score_setting(self, setting):
        e = Enigma(*setting)
        return len([m for i, m in enumerate(e.encrypt(self._cypher_text)) if m == self._text[i]])


class PlugBoardCracker:

    def __init__(self, text, cypher_text, settings):
        self.text = text
        self.cypher_text = cypher_text
        self.settings = settings
        self.plugboard_pairs = {l: set((l2 for l2 in string.ascii_uppercase)) for l in string.ascii_uppercase}
        self.loops = self.get_loops()

    def get_remaining(self):
        i = 1
        for v in list(self.plugboard_pairs.values())[:13]:
            i *= len(v)
        return i

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

    def eliminate_pairs_from_loop(self, loop):
        valid_guesses = defaultdict(set)
        loop_start = loop[0][0]
        for pstart in self.plugboard_pairs[loop_start]:
            current_guesses = defaultdict(set)
            recent_guess = pstart
            current_guesses[loop_start].add(recent_guess)
            for _, weight, next_in_loop in loop:
                enigma = Enigma(*self.settings)
                recent_guess = enigma.encrypt("".join([recent_guess for _ in range(weight + 1)]))[-1]
                current_guesses[next_in_loop].add(recent_guess)
            if pstart == recent_guess:
                for k, v in current_guesses.items():
                    valid_guesses[k].update(v)
        for k, v in valid_guesses.items():
            self.plugboard_pairs[k].intersection_update(v)

    def check_consistency(self):
        for l, ps in self.plugboard_pairs.items():
            for to_update in set(string.ascii_uppercase) - ps:
                self.plugboard_pairs[to_update].discard(l)
        for l, ps in self.plugboard_pairs.items():
            if len(ps) == 1:
                for to_update in string.ascii_uppercase.replace(l, ""):
                    self.plugboard_pairs[to_update].discard(list(ps)[0])
        if any([len(v)==0 for v in self.plugboard_pairs.values()]):
            raise InvalidSettings

    def eliminate_pairs(self):
        for loop in self.loops:
            self.eliminate_pairs_from_loop(loop)
            self.check_consistency()




if __name__ == "__main__":
    e = Enigma(rotor_offsets="A,A,A", plugboard_pairs="OM,CU,HQ,XZ,NK,EP,WT,DL")
    text = "WettervorhersageXfurxdiexRegionxMoskau".upper()
    ct = e.encrypt(text)
    print("finding best candidates for rotor settings...")
    ro = RotorOrder(text, ct)
    ro.get_rotor_order()
    best = ro.best_settings[-1000:]
    for setting,score in best:
        pbc = PlugBoardCracker(text, ct, setting)
        try:
            pbc.eliminate_pairs()
            if pbc.get_remaining() < 100:
                print(pbc.plugboard_pairs)
                print(setting)
        except InvalidSettings:
            pass



    # cypher_text = e.encrypt(text)
    # settings = list(get_possible_settings())[:1000]
    # for i in range(1000):
    #     print(f"{i} cracking....")
    #     pbc = PlugBoardCracker(text, cypher_text, settings[i])
    #     try:
    #         j = 1
    #         pbc.eliminate_pairs()
    #         print(pbc.plugboard_pairs)
    #         # for v in list(pbc.plugboard_pairs.values())[:13]:
    #         #     j *= len(v)
    #         # print(j)
    #         print(f"n loops = {len(pbc.loops)}")
    #     except InvalidSettings:
    #         pass
    # i = 1
    #
    # print(i)
    # print(pbc.plugboard_pairs)
