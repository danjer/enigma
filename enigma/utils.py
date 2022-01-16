import string
import random
from dataclasses import dataclass, field


def create_random_wiring():
    available = [i for i in string.ascii_uppercase]
    wiring = {}
    for letter in string.ascii_uppercase:
        # letters can't map to their own position
        while True:
            candidate = available.pop(random.randrange(0, len(available)))
            if candidate != letter:
                wiring[letter] = candidate
                break
            else:
                available.append(candidate)
    return wiring


@dataclass
class Reflector:
    wiring: dict = field(default_factory=create_random_wiring)


@dataclass
class Rotor:
    wiring: dict = field(default_factory=create_random_wiring)

    @property
    def forward(self):
        return self.wiring


@dataclass
class EnigmaBox:
    first_rotor: Rotor = field(default_factory=Rotor)
    second_rotor: Rotor = field(default_factory=Rotor)
    third_rotor: Rotor = field(default_factory=Rotor)
    reflector: Reflector = field(default_factory=Reflector)

    def feed_forward(self, letter):
        return self.third_rotor.forward[self.second_rotor.forward[self.first_rotor.forward[letter]]]
