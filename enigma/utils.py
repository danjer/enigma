import string
from dataclasses import dataclass, field


def read_mapping(mapping_string):
    return {k: string.ascii_uppercase.index(v) for k, v in enumerate(mapping_string)}


@dataclass
class RotorType:
    name: string
    mapping_string: string
    notch_position: string


@dataclass
class ReflectorType:
    name: string
    mapping_string: string


I = RotorType("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
Beta = ReflectorType("Beta", "LEYJVCNIXWPBQMDRTAKZGFUHOS")


@dataclass
class Rotor:
    rotor_type: RotorType = field(default=I)
    ring_setting: string = field(default="A")
    start_position: string = field(default="A")
    forward: dict = field(init=False)
    reverse: dict = field(init=False)

    def __post_init__(self):
        ring_offset = string.ascii_uppercase.index(self.ring_setting)
        rotor_offset = string.ascii_uppercase.index(self.start_position)
        self.forward = {(k + rotor_offset) % 26: (v + rotor_offset + ring_offset) % 26 for k, v in
                        read_mapping(self.rotor_type.mapping_string).items()}
        self.reverse = {v: k for k, v in self.forward.items()}

    def feed_index(self, index: int, backward=False):
        mapping = self.forward if not backward else self.reverse
        return mapping[index]

    def feed_letter(self, letter: str):
        return string.ascii_uppercase[self.feed_index(string.ascii_uppercase.index(letter))]


@dataclass
class Reflector:
    reflector_type: ReflectorType = field(default=Beta)
    forward: dict = field(init=False)

    def __post_init__(self):
        self.forward = read_mapping(self.reflector_type.mapping_string)

    def feed_index(self, letter: int):
        return self.forward[letter]

    def feed_letter(self, letter: str):
        return string.ascii_uppercase[self.feed_index(string.ascii_uppercase.index(letter))]


@dataclass
class EnigmaBox:
    first_rotor: Rotor = field(default_factory=Rotor)
    second_rotor: Rotor = field(default_factory=Rotor)
    third_rotor: Rotor = field(default_factory=Rotor)
    reflector: Reflector = field(default_factory=Reflector)

    def forward_pass(self, letter: int):
        for rotor in (self.first_rotor, self.second_rotor, self.third_rotor):
            letter = rotor.feed_index(letter)
        return letter

    def back_pass(self, letter: int):
        for rotor in (self.third_rotor, self.second_rotor, self.first_rotor):
            letter = rotor.feed_index(letter, backward=True)
        return letter

    def encrypt_letter(self, letter):
        index = string.ascii_uppercase.index(letter)
        return string.ascii_uppercase[self.back_pass(self.reflector.feed_index(self.forward_pass(index)))]

    def encrypt(self, text):
        return "".join([self.encrypt_letter(letter) for letter in text])
