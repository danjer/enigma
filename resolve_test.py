from enigma._crack import PlugBoardResolver

pairs = {"A": {"B", "A", "D"}, "B": {"A", "B"}, "C": {"C", "D"}, "D": {"D", "C", "A"}, "E": {"E"}, "F": {"F"},
         "G": {"G"},
         "H": {"H"},
         "I": {"I"}, "J": {"J"}, "K": {"K"}, "L": {"L"}, "M": {"M"}}

p = PlugBoardResolver("", "", "")
p.plugboard_pairs = pairs
print(p.get_remaining_pairs())
