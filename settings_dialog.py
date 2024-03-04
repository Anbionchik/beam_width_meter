# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(447, 555)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 510, 411, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(SettingsDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 411, 361))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.default_sigma_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.default_sigma_line.setObjectName("default_sigma_line")
        self.gridLayout.addWidget(self.default_sigma_line, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.faster_flag_points_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.faster_flag_points_line.setObjectName("faster_flag_points_line")
        self.gridLayout.addWidget(self.faster_flag_points_line, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.wait_time_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.wait_time_line.setObjectName("wait_time_line")
        self.gridLayout.addWidget(self.wait_time_line, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.beam_threshold_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.beam_threshold_line.setObjectName("beam_threshold_line")
        self.gridLayout.addWidget(self.beam_threshold_line, 2, 1, 1, 1)
        self.relax_pause_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.relax_pause_line.setObjectName("relax_pause_line")
        self.gridLayout.addWidget(self.relax_pause_line, 1, 1, 1, 1)
        self.faster_flag_check = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.faster_flag_check.setObjectName("faster_flag_check")
        self.gridLayout.addWidget(self.faster_flag_check, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 6, 0, 1, 1)
        self.calb_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.calb_line.setText("")
        self.calb_line.setObjectName("calb_line")
        self.gridLayout.addWidget(self.calb_line, 5, 1, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Параметры"))
        self.label.setText(_translate("SettingsDialog", "<html><head/><body><p>Пауза перед имзерением каждой точки</p></body></html>"))
        self.label_2.setText(_translate("SettingsDialog", "Пацза перед началом нового цикла"))
        self.label_3.setText(_translate("SettingsDialog", "Пороговое значение начала пучка"))
        self.label_5.setText(_translate("SettingsDialog", "Минимальное количество точек в ускоренном режиме "))
        self.label_4.setText(_translate("SettingsDialog", "Ускоренное измерение"))
        self.faster_flag_check.setText(_translate("SettingsDialog", "Активно"))
        self.label_6.setText(_translate("SettingsDialog", "Калибровочное соотношение"))
        self.label_11.setText(_translate("SettingsDialog", "Sigma (по умолчанию)"))

