# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/skeleton.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Enigma(object):
    def setupUi(self, Enigma):
        Enigma.setObjectName("Enigma")
        Enigma.resize(972, 805)
        self.centralwidget = QtWidgets.QWidget(Enigma)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.reflector = QtWidgets.QComboBox(self.frame_2)
        self.reflector.setObjectName("reflector")
        self.verticalLayout_6.addWidget(self.reflector)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_6.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setMaximumSize(QtCore.QSize(297, 20))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.rotor_1 = QtWidgets.QComboBox(self.frame_2)
        self.rotor_1.setObjectName("rotor_1")
        self.verticalLayout_10.addWidget(self.rotor_1)
        self.rotor_2 = QtWidgets.QComboBox(self.frame_2)
        self.rotor_2.setObjectName("rotor_2")
        self.verticalLayout_10.addWidget(self.rotor_2)
        self.rotor_3 = QtWidgets.QComboBox(self.frame_2)
        self.rotor_3.setObjectName("rotor_3")
        self.verticalLayout_10.addWidget(self.rotor_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_11.addWidget(self.label_5)
        self.ring_1 = QtWidgets.QComboBox(self.frame_2)
        self.ring_1.setObjectName("ring_1")
        self.verticalLayout_11.addWidget(self.ring_1)
        self.ring_2 = QtWidgets.QComboBox(self.frame_2)
        self.ring_2.setObjectName("ring_2")
        self.verticalLayout_11.addWidget(self.ring_2)
        self.ring_3 = QtWidgets.QComboBox(self.frame_2)
        self.ring_3.setObjectName("ring_3")
        self.verticalLayout_11.addWidget(self.ring_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_11)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName("label_6")
        self.verticalLayout_12.addWidget(self.label_6)
        self.position_1 = QtWidgets.QComboBox(self.frame_2)
        self.position_1.setObjectName("position_1")
        self.verticalLayout_12.addWidget(self.position_1)
        self.position_2 = QtWidgets.QComboBox(self.frame_2)
        self.position_2.setObjectName("position_2")
        self.verticalLayout_12.addWidget(self.position_2)
        self.position_3 = QtWidgets.QComboBox(self.frame_2)
        self.position_3.setObjectName("position_3")
        self.verticalLayout_12.addWidget(self.position_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_12)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.plugboard = QtWidgets.QPlainTextEdit(self.frame_3)
        self.plugboard.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plugboard.setObjectName("plugboard")
        self.verticalLayout_8.addWidget(self.plugboard)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.verticalLayout_2.addWidget(self.frame_2)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.encrypt_button = QtWidgets.QPushButton(self.frame)
        self.encrypt_button.setObjectName("encrypt_button")
        self.verticalLayout_2.addWidget(self.encrypt_button)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.verticalLayout_2.addItem(spacerItem2)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.input_field = QtWidgets.QPlainTextEdit(self.frame)
        self.input_field.setObjectName("input_field")
        self.verticalLayout_2.addWidget(self.input_field)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.output_field = QtWidgets.QPlainTextEdit(self.frame)
        self.output_field.setObjectName("output_field")
        self.verticalLayout_2.addWidget(self.output_field)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.frame)
        Enigma.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Enigma)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 22))
        self.menubar.setObjectName("menubar")
        Enigma.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Enigma)
        self.statusbar.setObjectName("statusbar")
        Enigma.setStatusBar(self.statusbar)

        self.retranslateUi(Enigma)
        QtCore.QMetaObject.connectSlotsByName(Enigma)

    def retranslateUi(self, Enigma):
        _translate = QtCore.QCoreApplication.translate
        Enigma.setWindowTitle(_translate("Enigma", "MainWindow"))
        self.label_3.setText(_translate("Enigma", "Enigma settings"))
        self.label_8.setText(_translate("Enigma", "Reflector"))
        self.label_4.setText(_translate("Enigma", "Rotors"))
        self.label_5.setText(_translate("Enigma", "Rings"))
        self.label_6.setText(_translate("Enigma", "Positions"))
        self.label_7.setText(_translate("Enigma", "Plugboard"))
        self.encrypt_button.setText(_translate("Enigma", "ENCRYPT"))
        self.label.setText(_translate("Enigma", "Input text"))
        self.label_2.setText(_translate("Enigma", "Encrypted text"))
