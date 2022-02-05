from PyQt5 import QtWidgets
from _enigma import Enigma
from gui import Ui_MainWindow

class WrappedUi(Ui_MainWindow):

    def setup_logic(self):
        self.encrypt_button.clicked.connect(self.encrypt)
        self.reset_button.clicked.connect(self.reset)

    def encrypt(self):
        self.output_field.setPlainText(self.enigma.encrypt(self.input_field.toPlainText()))
        self.update_enigma_state()

    def update_enigma_state(self):
        self.position_label.setText("-".join(self.enigma.current_state))

    def reset(self):
        self.enigma = Enigma()
        self.update_enigma_state()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = WrappedUi()
    ui.setupUi(MainWindow)
    ui.setup_logic()
    MainWindow.show()
    sys.exit(app.exec_())