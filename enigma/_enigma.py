import string
from dataclasses import dataclass, field
from enigma._rotors import rotor_factory, reflector_factory, Rotor, Reflector


@dataclass
class Enigma:
    rotor_types: string = field(default="I,II,III")
    reflector_type: string = field(default="B")
    ring_settings: string = field(default="AAA")
    rotor_offsets: string = field(default="AAA")

    first_rotor: Rotor = field(init=False)
    second_rotor: Rotor = field(init=False)
    third_rotor: Rotor = field(init=False)
    reflector: Reflector = field(init=False)

    def __post_init__(self):
        third_rotor, second_rotor, first_rotor = self.rotor_types.split(",")
        third_ring_s, second_ring_s, first_ring_s = self.ring_settings
        third_offset, second_offset, first_offset = self.rotor_offsets

        self.first_rotor = rotor_factory(first_rotor, first_ring_s, first_offset)
        self.second_rotor = rotor_factory(second_rotor, second_ring_s, second_offset)
        self.third_rotor = rotor_factory(third_rotor, third_ring_s, third_offset)

        self.reflector = reflector_factory(self.reflector_type)

    def forward_pass(self, letter: int):
        for rotor in (self.first_rotor, self.second_rotor, self.third_rotor):
            letter = rotor.feed_index(letter)
        return letter

    @property
    def current_state(self):
        return "".join(
            [string.ascii_uppercase[i.current_position] for i in self.rotors]
        )

    @property
    def rotors(self):
        return [self.third_rotor, self.second_rotor, self.first_rotor]

    def back_pass(self, letter: int):
        for rotor in (self.third_rotor, self.second_rotor, self.first_rotor):
            letter = rotor.feed_index(letter, backward=True)
        return letter

    def rotate_rotors(self):
        rotate_second_rotor = self.first_rotor.in_notch_position
        rotate_third_rotor = self.second_rotor.in_notch_position
        self.first_rotor.rotate()  # always rotate the first rotor.
        if (
            rotate_second_rotor or rotate_third_rotor
        ):  # rotate second rotor if third rotor rotates, known as double stepping
            self.second_rotor.rotate()
        if rotate_third_rotor:
            self.third_rotor.rotate()

    def encrypt_letter(self, letter):
        letter = letter.upper()
        self.rotate_rotors()
        index = string.ascii_uppercase.index(letter)
        return string.ascii_uppercase[
            self.back_pass(self.reflector.feed_index(self.forward_pass(index)))
        ]

    def encrypt(self, text):
        return "".join([self.encrypt_letter(letter) for letter in text])
