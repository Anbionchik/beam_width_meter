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
        MainWindow.resize(1300, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connect_translator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_translator_btn.setGeometry(QtCore.QRect(1010, 10, 141, 41))
        self.connect_translator_btn.setObjectName("connect_translator_btn")
        self.connect_powermeter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_powermeter_btn.setGeometry(QtCore.QRect(1010, 80, 141, 41))
        self.connect_powermeter_btn.setObjectName("connect_powermeter_btn")
        self.begin_measurment_btn = QtWidgets.QPushButton(self.centralwidget)
        self.begin_measurment_btn.setEnabled(False)
        self.begin_measurment_btn.setGeometry(QtCore.QRect(1020, 180, 251, 41))
        self.begin_measurment_btn.setObjectName("begin_measurment_btn")
        self.step_across_beam = QtWidgets.QLineEdit(self.centralwidget)
        self.step_across_beam.setGeometry(QtCore.QRect(1020, 150, 121, 20))
        self.step_across_beam.setObjectName("step_across_beam")
        self.step_along_beam = QtWidgets.QLineEdit(self.centralwidget)
        self.step_along_beam.setGeometry(QtCore.QRect(1152, 150, 121, 20))
        self.step_along_beam.setObjectName("step_along_beam")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1020, 130, 121, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1150, 130, 131, 21))
        self.label_2.setObjectName("label_2")
        self.disconnect_powermeter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_powermeter_btn.setEnabled(False)
        self.disconnect_powermeter_btn.setGeometry(QtCore.QRect(1150, 80, 141, 41))
        self.disconnect_powermeter_btn.setObjectName("disconnect_powermeter_btn")
        self.disconnect_translator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_translator_btn.setEnabled(False)
        self.disconnect_translator_btn.setGeometry(QtCore.QRect(1150, 10, 141, 41))
        self.disconnect_translator_btn.setObjectName("disconnect_translator_btn")
        self.reverse_x_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reverse_x_btn.setEnabled(False)
        self.reverse_x_btn.setGeometry(QtCore.QRect(1010, 50, 55, 23))
        self.reverse_x_btn.setObjectName("reverse_x_btn")
        self.x_test_run_btn = QtWidgets.QPushButton(self.centralwidget)
        self.x_test_run_btn.setEnabled(False)
        self.x_test_run_btn.setGeometry(QtCore.QRect(1070, 50, 55, 23))
        self.x_test_run_btn.setObjectName("x_test_run_btn")
        self.reverse_y_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reverse_y_btn.setEnabled(False)
        self.reverse_y_btn.setGeometry(QtCore.QRect(1190, 50, 55, 23))
        self.reverse_y_btn.setObjectName("reverse_y_btn")
        self.y_test_run_btn = QtWidgets.QPushButton(self.centralwidget)
        self.y_test_run_btn.setEnabled(False)
        self.y_test_run_btn.setGeometry(QtCore.QRect(1240, 50, 55, 23))
        self.y_test_run_btn.setObjectName("y_test_run_btn")
        self.xy_change_btn = QtWidgets.QPushButton(self.centralwidget)
        self.xy_change_btn.setEnabled(False)
        self.xy_change_btn.setGeometry(QtCore.QRect(1130, 50, 57, 23))
        self.xy_change_btn.setObjectName("xy_change_btn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 0, 291, 31))
        self.label_3.setObjectName("label_3")
        self.results_folder_path = QtWidgets.QLineEdit(self.centralwidget)
        self.results_folder_path.setEnabled(False)
        self.results_folder_path.setGeometry(QtCore.QRect(10, 30, 441, 21))
        self.results_folder_path.setObjectName("results_folder_path")
        self.choose_folder_btn = QtWidgets.QPushButton(self.centralwidget)
        self.choose_folder_btn.setGeometry(QtCore.QRect(460, 32, 61, 21))
        self.choose_folder_btn.setText("")
        self.choose_folder_btn.setObjectName("choose_folder_btn")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 570, 1291, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.info_field = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.info_field.setEnabled(False)
        self.info_field.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.info_field.setReadOnly(True)
        self.info_field.setObjectName("info_field")
        self.verticalLayout.addWidget(self.info_field)
        self.main_graph = PlotWidget(self.centralwidget)
        self.main_graph.setGeometry(QtCore.QRect(10, 70, 591, 491))
        self.main_graph.setObjectName("main_graph")
        self.line_graph = PlotWidget(self.centralwidget)
        self.line_graph.setGeometry(QtCore.QRect(610, 270, 321, 291))
        self.line_graph.setObjectName("line_graph")
        self.gauss_graph = PlotWidget(self.centralwidget)
        self.gauss_graph.setGeometry(QtCore.QRect(950, 270, 341, 291))
        self.gauss_graph.setObjectName("gauss_graph")
        self.translator_coords_graph = PlotWidget(self.centralwidget)
        self.translator_coords_graph.setGeometry(QtCore.QRect(610, 20, 391, 241))
        self.translator_coords_graph.setObjectName("translator_coords_graph")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1020, 220, 47, 13))
        self.label_4.setObjectName("label_4")
        self.threshold_line = QtWidgets.QLineEdit(self.centralwidget)
        self.threshold_line.setGeometry(QtCore.QRect(1020, 240, 113, 20))
        self.threshold_line.setObjectName("threshold_line")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1140, 220, 47, 13))
        self.label_5.setObjectName("label_5")
        self.diameter_line = QtWidgets.QLineEdit(self.centralwidget)
        self.diameter_line.setEnabled(False)
        self.diameter_line.setGeometry(QtCore.QRect(1140, 240, 113, 20))
        self.diameter_line.setObjectName("diameter_line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Beam Width Meter"))
        self.connect_translator_btn.setText(_translate("MainWindow", "Подключить подвижку"))
        self.connect_powermeter_btn.setText(_translate("MainWindow", "Подключить измеритель"))
        self.begin_measurment_btn.setText(_translate("MainWindow", "Начать измерение"))
        self.label.setText(_translate("MainWindow", "Шаг поперёк пучка, мм"))
        self.label_2.setText(_translate("MainWindow", "Шаг вдоль пучка, мм"))
        self.disconnect_powermeter_btn.setText(_translate("MainWindow", "Отключить измеритель"))
        self.disconnect_translator_btn.setText(_translate("MainWindow", "Отключить подвижку"))
        self.reverse_x_btn.setText(_translate("MainWindow", "Реверс X"))
        self.x_test_run_btn.setText(_translate("MainWindow", "Тест X"))
        self.reverse_y_btn.setText(_translate("MainWindow", "Реверс Y"))
        self.y_test_run_btn.setText(_translate("MainWindow", "Тест Y"))
        self.xy_change_btn.setText(_translate("MainWindow", "X <-> Y"))
        self.label_3.setText(_translate("MainWindow", "Путь сохранения"))
        self.label_4.setText(_translate("MainWindow", "Уровень"))
        self.label_5.setText(_translate("MainWindow", "Диаметр"))
from pyqtgraph import PlotWidget
