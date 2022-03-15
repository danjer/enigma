import string
import random
import networkx as nx
from itertools import permutations, product
from enigma._enigma import Enigma
from collections import deque, defaultdict
from tqdm import tqdm


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
        self.best_settings = defaultdict(list)
        self.best_score = -1

    def get_n_best_rotor_settings(self, n):
        print('Resolving rotor settings...')
        for rotor_setting in tqdm(list(get_possible_settings())):
            current_score = self.score_setting(rotor_setting)
            rotor_order = rotor_setting[0]
            self.best_settings[rotor_order].append((rotor_setting, current_score))
        best_lists = []
        print(len(self.best_settings))
        for order in self.best_settings.values():
            #best_lists += self.best_settings.sort(key=lambda x: x[-1])
            best_lists += sorted(order, key=lambda x: x[-1])[-n:] #.best_settings.sort(key=lambda x: x[-1])
        print(len(best_lists))
        return best_lists

    def score_setting(self, rotor_setting):
        e = Enigma(*rotor_setting)
        return len([m for i, m in enumerate(e.encrypt(self._cypher_text)) if m == self._text[i]])


class PlugBoardResolver:

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
            # the loop is satisfied, so we can add the assumptions as (potential) valid_guesses
            if pstart == recent_guess:
                for k, v in current_guesses.items():
                    valid_guesses[k].update(v)
        # update the plugboard_pairs from which to choose from for next loop
        for k, v in valid_guesses.items():
            self.plugboard_pairs[k].intersection_update(v)

    def check_consistency(self):
        # if right end of plug can't be attached to left end, the left end can't be connected to the right end...
        for left_end, potential_right_end in self.plugboard_pairs.items():
            for to_update in set(string.ascii_uppercase) - potential_right_end:
                self.plugboard_pairs[to_update].discard(left_end)
        for left_end, potential_right_end in self.plugboard_pairs.items():
            if len(potential_right_end) == 1:
                for to_update in string.ascii_uppercase.replace(left_end, ""):
                    self.plugboard_pairs[to_update].discard(list(potential_right_end)[0])
        if any([len(v) == 0 for v in self.plugboard_pairs.values()]):
            raise InvalidSettings("There is noway to setup the plugboard to produce the crib under these settings...")

    def eliminate_pairs(self):
        for loop in self.loops:
            self.eliminate_pairs_from_loop(loop)
            self.check_consistency()


class EnigmaResolver:

    def __init__(self, crib, cypher_text):
        self.crib = crib
        self.cypher_text = cypher_text
        self.rsr = RotorOrderResolver(crib, cypher_text)

    def resovle(self, n=1000):
        best_rotor_settings = self.rsr.get_n_best_rotor_settings(n)
        for rotor_settings, score in tqdm(best_rotor_settings):
            pbr = PlugBoardResolver(self.crib, self.cypher_text, rotor_settings)
            try:
                pbr.eliminate_pairs()
                if pbr.get_remaining() < 100:
                    print(pbr.plugboard_pairs)
                    print(rotor_settings)
            except InvalidSettings:
                pass


if __name__ == "__main__":
    e = Enigma(rotor_types="II,III,I", ring_settings="I,A,A", plugboard_pairs="OM,CU,HQ,XZ,NK,EP,WT,DL")
    # e = Enigma(rotor_types="I,III,II", ring_settings="I,A,A", plugboard_pairs="AB,OM,CU,HQ,XZ,NK,EP,WT,DL,FI")
    crib = "WettervorhersageXfurxdiexRegionxMoskau".upper()
    cypher_text = e.encrypt(crib)
    er = EnigmaResolver(crib, cypher_text)
    er.resovle()
