# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powermeter_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 247)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(230, 10, 81, 221))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(20, 10, 82, 17))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 90, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 30, 191, 48))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ip_line = QtWidgets.QLineEdit(self.widget)
        self.ip_line.setMinimumSize(QtCore.QSize(140, 0))
        self.ip_line.setObjectName("ip_line")
        self.gridLayout.addWidget(self.ip_line, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.port_line = QtWidgets.QLineEdit(self.widget)
        self.port_line.setMinimumSize(QtCore.QSize(140, 0))
        self.port_line.setObjectName("port_line")
        self.gridLayout.addWidget(self.port_line, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(20, 110, 193, 79))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.com_port_box = QtWidgets.QComboBox(self.widget1)
        self.com_port_box.setObjectName("com_port_box")
        self.verticalLayout.addWidget(self.com_port_box)
        self.rescan_btn = QtWidgets.QPushButton(self.widget1)
        self.rescan_btn.setMaximumSize(QtCore.QSize(75, 23))
        self.rescan_btn.setObjectName("rescan_btn")
        self.verticalLayout.addWidget(self.rescan_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.baud_rate_line = QtWidgets.QLineEdit(self.widget1)
        self.baud_rate_line.setObjectName("baud_rate_line")
        self.horizontalLayout.addWidget(self.baud_rate_line)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radioButton.setText(_translate("Dialog", "Ethernet"))
        self.radioButton_2.setText(_translate("Dialog", "USB"))
        self.label.setText(_translate("Dialog", "IP"))
        self.label_2.setText(_translate("Dialog", "Port"))
        self.rescan_btn.setText(_translate("Dialog", "Rescan"))
        self.label_3.setText(_translate("Dialog", "Baud_rate"))

