# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powermeter_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 247)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(20, 10, 82, 17))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 90, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 191, 48))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ip_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.ip_line.setMinimumSize(QtCore.QSize(140, 0))
        self.ip_line.setObjectName("ip_line")
        self.gridLayout.addWidget(self.ip_line, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.port_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.port_line.setMinimumSize(QtCore.QSize(140, 0))
        self.port_line.setObjectName("port_line")
        self.gridLayout.addWidget(self.port_line, 1, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 110, 193, 79))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.com_port_box = QtWidgets.QComboBox(self.layoutWidget1)
        self.com_port_box.setObjectName("com_port_box")
        self.verticalLayout.addWidget(self.com_port_box)
        self.rescan_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.rescan_btn.setMaximumSize(QtCore.QSize(75, 23))
        self.rescan_btn.setObjectName("rescan_btn")
        self.verticalLayout.addWidget(self.rescan_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.baud_rate_line = QtWidgets.QLineEdit(self.layoutWidget1)
        self.baud_rate_line.setObjectName("baud_rate_line")
        self.horizontalLayout.addWidget(self.baud_rate_line)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setGeometry(QtCore.QRect(230, 10, 75, 23))
        self.ok_btn.setObjectName("ok_btn")
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setGeometry(QtCore.QRect(230, 40, 75, 23))
        self.cancel_btn.setObjectName("cancel_btn")

        self.retranslateUi(Dialog)
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
        self.ok_btn.setText(_translate("Dialog", "OK"))
        self.cancel_btn.setText(_translate("Dialog", "????????????"))
