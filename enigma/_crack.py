import string
import random
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import deque, defaultdict


class InvalidSettings(Exception):
    pass


def get_possible_settings():
    rotor_options = [",".join(c) for c in permutations(["I", "II", "III"], 3)]
    positions = [",".join(c) for c in product(string.ascii_uppercase, string.ascii_uppercase, string.ascii_uppercase)]
    return product(rotor_options, "B", positions)


def get_random_plugboard_pair():
    available = list(string.ascii_uppercase)
    pairs = []
    for _ in range(26):
        left, right = random.choice(available), random.choice(available)
        try:
            available.remove(left)
            available.remove(right)
            pairs.append(f"{left}{right}")
        # in case left and right are the same
        except ValueError:
            pass
    return ",".join(pairs)


def get_random_enigma():
    settings = random.choice(list(get_possible_settings()))
    return Enigma(*settings)


class RotorOrderResolver:

    def __init__(self, text, cypher_text):
        self._text = text
        self._cypher_text = cypher_text
        self.best_setting = None
        self.best_settings = []
        self.best_score = -1

    def asses_rotor_orders(self):
        for rotor_setting in get_possible_settings():
            current_score = self.score_setting(rotor_setting)
            self.best_settings.append((rotor_setting, current_score))
        self.best_settings.sort(key=lambda x: x[-1])

    def score_setting(self, rotor_setting):
        e = Enigma(*rotor_setting)
        return len([m for i, m in enumerate(e.encrypt(self._cypher_text)) if m == self._text[i]])


class PlugBoardCracker:

    def __init__(self, crib, cypher_text, rotor_settings):
        self.crib = crib
        self.cypher_text = cypher_text
        self.rotor_settings = rotor_settings
        self.plugboard_pairs = {left_end: set((l2 for l2 in string.ascii_uppercase)) for left_end in
                                string.ascii_uppercase}
        self.loops = self.get_loops()

    def get_remaining(self):
        i = 1
        for v in list(self.plugboard_pairs.values())[:13]:
            i *= len(v)
        return i

    def build_loop_graph(self):
        g = nx.Graph()
        weighted_edges = [(n1, n2, w) for w, (n1, n2) in enumerate(zip(self.cypher_text, self.crib))]
        g.add_weighted_edges_from(weighted_edges)
        return g

    def get_loops(self):
        g = self.build_loop_graph()
        cycles = nx.cycle_basis(g)
        nw_cycles = []  # nw_cycles holds the nodes and weights in an easier format
        for cycle in cycles:
            shifted_cycle = deque(cycle)
            shifted_cycle.rotate(1)
            shifted_cycle = list(shifted_cycle)
            nw_cycles.append([(n1, g.get_edge_data(n1, n2)['weight'], n2) for n1, n2 in zip(shifted_cycle, cycle)])
        return nw_cycles

    def eliminate_pairs_from_loop(self, loop):
        valid_guesses = defaultdict(set)
        loop_start = loop[0][0]
        for pstart in self.plugboard_pairs[loop_start]:
            current_guesses = defaultdict(set)
            recent_guess = pstart
            current_guesses[loop_start].add(recent_guess)
            for _, weight, next_in_loop in loop:
                enigma = Enigma(*self.rotor_settings)
                recent_guess = enigma.encrypt("".join([recent_guess for _ in range(weight + 1)]))[-1]
                # means that next_in_loop requires a value that was previously discarded, break and asses next loop
                if recent_guess not in self.plugboard_pairs[next_in_loop]:
                    break
                current_guesses[next_in_loop].add(recent_guess)
            if pstart == recent_guess:
                for k, v in current_guesses.items():
                    valid_guesses[k].update(v)

        # the loop is valid, so update the plugboard pais
        # for k, v in valid_guesses.items():
        #     self.plugboard_pairs[k].intersection_update(v)

    def check_consistency(self):
        # if right end of plug can't be attached to left end, left and can't be connected to the right end
        for left_end, potential_right_end in self.plugboard_pairs.items():
            for to_update in set(string.ascii_uppercase) - potential_right_end:
                self.plugboard_pairs[to_update].discard(left_end)
        for left_end, potential_right_end in self.plugboard_pairs.items():
            if len(potential_right_end) == 1:
                for to_update in string.ascii_uppercase.replace(left_end, ""):
                    self.plugboard_pairs[to_update].discard(list(potential_right_end)[0])
        if any([len(v) == 0 for v in self.plugboard_pairs.values()]):
            raise InvalidSettings

    def eliminate_pairs(self):
        for loop in self.loops:
            self.eliminate_pairs_from_loop(loop)
            self.check_consistency()


if __name__ == "__main__":
    e = Enigma(ring_settings="I,B,Z", plugboard_pairs="OM,CU,HQ,XZ,NK,EP,WT,DL")
    text = "WettervorhersageXfurxdiexRegionxMoskau".upper()
    ct = e.encrypt(text)
    print("finding best candidates for rotor settings...")
    ro = RotorOrder(text, ct)
    ro.get_rotor_order()
    best = ro.best_settings[-100:]
    for setting, score in best:
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
