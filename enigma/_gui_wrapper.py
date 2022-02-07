"""wraps the gui class defined in _gui and adds the event logic"""

import string
from PyQt5 import QtWidgets
from _enigma import Enigma
from _rotors import ROTORS, REFLECTORS
from _gui import Ui_Enigma


class WrappedUi(Ui_Enigma):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enigma = Enigma()

    def retranslateUi(self, *args, **kwargs):
        super().retranslateUi(*args, **kwargs)

        self.rotor_1.addItems([r.name for r in ROTORS])
        self.rotor_2.addItems([r.name for r in ROTORS])
        self.rotor_3.addItems([r.name for r in ROTORS])

        self.ring_1.addItems([c for c in string.ascii_uppercase])
        self.ring_2.addItems([c for c in string.ascii_uppercase])
        self.ring_3.addItems([c for c in string.ascii_uppercase])

        self.position_1.addItems([c for c in string.ascii_uppercase])
        self.position_2.addItems([c for c in string.ascii_uppercase])
        self.position_3.addItems([c for c in string.ascii_uppercase])

        self.reflector.addItems([rf.name for rf in REFLECTORS])

    def setup_logic(self):
        self.encrypt_button.clicked.connect(self.encrypt)

    def encrypt(self):
        rotors = ",".join(
            [
                self.rotor_1.currentText(),
                self.rotor_2.currentText(),
                self.rotor_3.currentText(),
            ]
        )
        reflector = self.reflector.currentText()
        ring_settings = ",".join(
            [
                self.ring_1.currentText(),
                self.ring_2.currentText(),
                self.ring_3.currentText(),
            ]
        )
        ring_positions = ",".join(
            [
                self.position_1.currentText(),
                self.position_2.currentText(),
                self.position_3.currentText(),
            ]
        )
        plugboard_pairs = self.read_plugboard()
        self.enigma = Enigma(
            rotors, reflector, ring_settings, ring_positions, plugboard_pairs
        )
        input_text = [
            l
            for l in self.input_field.toPlainText().upper()
            if l in string.ascii_uppercase
        ]
        self.output_field.setPlainText(self.enigma.encrypt(input_text))

    def read_plugboard(self):
        plugboard_pairs = self.plugboard.toPlainText().upper()
        if all([p in string.ascii_uppercase + " " for p in plugboard_pairs]) and all(
            [len(p) == 2 for p in plugboard_pairs.split(" ")]
        ):
            return plugboard_pairs
        else:
            self.plugboard.setPlainText("")
            return ""

    def update_gui_state(self):
        first, second, third = self.enigma.current_state
        self.position_1.setCurrentText(first)
        self.position_2.setCurrentText(second)
        self.position_3.setCurrentText(third)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = WrappedUi()
    ui.setupUi(MainWindow)
    ui.setup_logic()
    MainWindow.show()
    sys.exit(app.exec_())
