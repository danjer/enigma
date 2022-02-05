import string
from PyQt5 import QtWidgets
from _enigma import Enigma
from _rotors import ROTORS
from gui import Ui_MainWindow

class WrappedUi(Ui_MainWindow):

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

    def setup_logic(self):
        self.encrypt_button.clicked.connect(self.encrypt)

    def encrypt(self):
        rotors = ",".join([self.rotor_1.currentText(), self.rotor_2.currentText(), self.rotor_3.currentText()])
        ring_settings = ",".join([self.ring_1.currentText(), self.ring_2.currentText(), self.ring_3.currentText()])
        ring_positions = ",".join([self.position_1.currentText(), self.position_2.currentText(), self.position_3.currentText()])
        self.enigma = Enigma(rotors, "B", ring_settings, ring_positions)
        self.output_field.setPlainText(self.enigma.encrypt(self.input_field.toPlainText()))
        self.update_gui_state()

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