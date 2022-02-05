import string
from dataclasses import dataclass, field

ROTOR_SIZE = 26  # 26 letters and positons on each rotor


@dataclass(frozen=True)
class RotorType:
    name: string
    mapping_string: string
    notch_position: string


@dataclass(frozen=True)
class ReflectorType:
    name: string
    mapping_string: string


ROTORS = [
    RotorType("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    RotorType("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    RotorType("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    RotorType("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
]

REFLECTORS = [
    ReflectorType("B", "YRUHQSLDPXNGOKMIEBFZCWVJAT"),
]


@dataclass
class Rotor:
    rotor_type: RotorType
    ring_setting: string = field(default="A")
    start_position: string = field(default="A")
    notch_position: int = field(init=False, default=0)
    current_position: int = field(init=False, default=0)
    forward: dict = field(init=False, default_factory=dict)
    reverse: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        ring_offset = string.ascii_uppercase.index(self.ring_setting)
        rotor_offset = string.ascii_uppercase.index(self.start_position)
        self.notch_position = (
                                      string.ascii_uppercase.index(self.rotor_type.notch_position) + rotor_offset
                              ) % ROTOR_SIZE
        #self.current_position = ring_offset
        self.current_position = rotor_offset
        self.forward = {
            (k + rotor_offset)
            % ROTOR_SIZE: (v + rotor_offset + ring_offset)
                          % ROTOR_SIZE
            for k, v in read_mapping(self.rotor_type.mapping_string).items()
        }
        self.reverse = {v: k for k, v in self.forward.items()}

    @property
    def in_notch_position(self):
        return self.current_position == self.notch_position

    def rotate(self):
        self.current_position = (self.current_position + 1) % ROTOR_SIZE
        self.forward = {
            (k + 1) % ROTOR_SIZE: (v + 1) % ROTOR_SIZE for k, v in self.forward.items()
        }
        self.reverse = {v: k for k, v in self.forward.items()}

    def feed_index(self, index: int, backward=False):
        mapping = self.forward if not backward else self.reverse
        return mapping[index]

    def feed_letter(self, letter: str):
        return string.ascii_uppercase[
            self.feed_index(string.ascii_uppercase.index(letter))
        ]


@dataclass
class Reflector:
    reflector_type: ReflectorType
    forward: dict = field(init=False)

    def __post_init__(self):
        self.forward = read_mapping(self.reflector_type.mapping_string)

    def feed_index(self, letter: int):
        return self.forward[letter]

    def feed_letter(self, letter: str):
        return string.ascii_uppercase[
            self.feed_index(string.ascii_uppercase.index(letter))
        ]


def read_mapping(mapping_string):
    return {k: string.ascii_uppercase.index(v) for k, v in enumerate(mapping_string)}


def rotor_factory(name, ring_setting, rotor_offset):
    try:
        rtype = [r for r in ROTORS if r.name == name][0]
    except IndexError:
        raise ValueError("Unkown rotortype")
    return Rotor(rtype, ring_setting, rotor_offset)


def reflector_factory(name):
    try:
        rtype = [r for r in REFLECTORS if r.name == name][0]
    except IndexError:
        raise ValueError("Unkown reflector type")
    return Reflector(rtype)
