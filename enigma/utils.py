import string
import random
from dataclasses import dataclass, field


def create_random_rotor_wiring():
    available = list(range(len(string.ascii_uppercase)))
    return {i: available.pop(random.randrange(0, len(available))) for i in range(len(string.ascii_uppercase))}

def create_random_reflector_wiring():
    wiring = {}
    available = list(range(len(string.ascii_uppercase)))
    while available:
        first, second = available.pop(random.randrange(0, len(available))), available.pop(random.randrange(0, len(available)))
        wiring[first] = second
        wiring[second] = first
    return wiring


@dataclass
class Rotor:
    wiring: dict = field(default_factory=create_random_rotor_wiring)

    def feed(self, letter, backward=False):
        wire_map = self.wiring if not backward else {v: k for k, v in self.wiring.items()}
        return string.ascii_uppercase[wire_map[string.ascii_uppercase.index(letter)]]



@dataclass
class Reflector:
    wiring: dict = field(default_factory=create_random_reflector_wiring)

    def feed(self, letter):
        index = string.ascii_uppercase.index(letter)
        return string.ascii_uppercase[self.wiring[index]]


@dataclass
class EnigmaBox:
    first_rotor: Rotor = field(default_factory=Rotor)
    second_rotor: Rotor = field(default_factory=Rotor)
    third_rotor: Rotor = field(default_factory=Rotor)
    reflector: Reflector = field(default_factory=Reflector)
    first_offset: int = field(default=0)
    second_offset: int = field(default=0)
    third_offset: int = field(default=0)
    ticks: int = field(default=1)

    @property
    def offsets(self):
        return (self.third_offset, self.second_offset, self.first_offset)

    def forward_pass(self, letter):
        for rotor in (self.first_rotor, self.second_rotor, self.third_rotor):
            letter = rotor.feed(letter)
        return letter

    def back_pass(self, letter):
        for rotor in (self.third_rotor, self.second_rotor, self.first_rotor):
            letter = rotor.feed(letter, backward=True)
        return letter

    def rotate_rotor(self, rotor, amount=1):
        updated_wiring = {(k + amount)%len(string.ascii_uppercase): (v + amount)%len(string.ascii_uppercase) for k, v in rotor.wiring.items()}
        rotor.wiring = updated_wiring

    def rotate_rotors(self):
        if self.ticks % 1 == 0:
            self.rotate_rotor(self.first_rotor)
            self.first_offset = (self.first_offset + 1) % len(string.ascii_uppercase)
        if self.ticks % (1 * 26) == 0:
            self.rotate_rotor(self.second_rotor)
            self.second_offset = (self.second_offset + 1) % len(string.ascii_uppercase)
        if self.ticks % (1 * 26 * 26) == 0:
            self.rotate_rotor(self.third_rotor)
            self.third_offset = (self.third_offset + 1) % len(string.ascii_uppercase)

    def reset(self):
        offsets_rotors = zip(self.offsets, (self.third_rotor, self.second_rotor, self.first_rotor))
        for offset, rotor in offsets_rotors:
            self.rotate_rotor(rotor, -1 * offset)
        self.first_offset, self.second_offset, self.third_offset = 0, 0, 0
        self.ticks = 0


    def encrypt_letter(self, letter):
        self.ticks += 1
        self.rotate_rotors()
        return self.back_pass(self.reflector.feed(self.forward_pass(letter)))


    def encrypt(self, text):
        return "".join([self.encrypt_letter(letter) for letter in text])

