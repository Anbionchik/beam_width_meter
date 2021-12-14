# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect_translator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_translator_btn.setGeometry(QtCore.QRect(584, 60, 141, 41))
        self.connect_translator_btn.setObjectName("connect_translator_btn")
        self.connect_powermeter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_powermeter_btn.setGeometry(QtCore.QRect(584, 100, 141, 41))
        self.connect_powermeter_btn.setObjectName("connect_powermeter_btn")
        self.begin_measurment_btn = QtWidgets.QPushButton(self.centralwidget)
        self.begin_measurment_btn.setGeometry(QtCore.QRect(500, 220, 251, 41))
        self.begin_measurment_btn.setObjectName("begin_measurment_btn")
        self.step_across_line = QtWidgets.QLineEdit(self.centralwidget)
        self.step_across_line.setGeometry(QtCore.QRect(500, 190, 121, 20))
        self.step_across_line.setObjectName("step_across_line")
        self.step_along_line = QtWidgets.QLineEdit(self.centralwidget)
        self.step_along_line.setGeometry(QtCore.QRect(632, 190, 121, 20))
        self.step_along_line.setObjectName("step_along_line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 170, 121, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 170, 131, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_translator_btn.setText(_translate("MainWindow", "Подключить подвижку"))
        self.connect_powermeter_btn.setText(_translate("MainWindow", "Подключить измеритель"))
        self.begin_measurment_btn.setText(_translate("MainWindow", "Начать измерение"))
        self.label.setText(_translate("MainWindow", "Шаг поперёк пучка, мм"))
        self.label_2.setText(_translate("MainWindow", "Шаг вдоль пучка, мм"))
