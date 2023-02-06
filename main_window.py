# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1314, 695)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow{\n"
"background-color:#293133\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.main_graph = PlotWidget(self.centralwidget)
        self.main_graph.setMinimumSize(QtCore.QSize(590, 550))
        self.main_graph.setObjectName("main_graph")
        self.verticalLayout_4.addWidget(self.main_graph)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.info_field = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.info_field.setEnabled(False)
        self.info_field.setMaximumSize(QtCore.QSize(16777215, 94))
        self.info_field.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.info_field.setReadOnly(True)
        self.info_field.setObjectName("info_field")
        self.verticalLayout.addWidget(self.info_field)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.translator_coords_graph = PlotWidget(self.centralwidget)
        self.translator_coords_graph.setEnabled(False)
        self.translator_coords_graph.setMinimumSize(QtCore.QSize(340, 300))
        self.translator_coords_graph.setObjectName("translator_coords_graph")
        self.horizontalLayout_3.addWidget(self.translator_coords_graph)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.connect_translator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_translator_btn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_translator_btn.sizePolicy().hasHeightForWidth())
        self.connect_translator_btn.setSizePolicy(sizePolicy)
        self.connect_translator_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.connect_translator_btn.setStyleSheet("QPushButton{\n"
"box-shadow:inset 0px 1px 0px 0px #fff6af;\n"
"    background:linear-gradient(to bottom, #ffec64 5%, #ffab23 100%);\n"
"    background-color:#ffec64;\n"
"    border-radius:6px;\n"
"    border:1px solid #ffaa22;\n"
"}\n"
"QPushButton:disabled{\n"
"background-color:#fff3a1;\n"
"color:#757d6f;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#ffe52b;\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #ffaa22;\n"
"}")
        self.connect_translator_btn.setObjectName("connect_translator_btn")
        self.gridLayout.addWidget(self.connect_translator_btn, 0, 0, 1, 2)
        self.disconnect_translator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_translator_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disconnect_translator_btn.sizePolicy().hasHeightForWidth())
        self.disconnect_translator_btn.setSizePolicy(sizePolicy)
        self.disconnect_translator_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.disconnect_translator_btn.setStyleSheet("QPushButton{\n"
"box-shadow: 0px 10px 14px -7px #276873;\n"
"    background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);\n"
"    background-color:#599bb3;\n"
"    border:1px solid #305f70;\n"
"border-radius:6px;\n"
"color:#ffffff;\n"
"}\n"
"QPushButton:disabled{\n"
"background-color:#92aab3;\n"
"color:#757d6f;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#2694bd;\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #305f70;\n"
"}")
        self.disconnect_translator_btn.setObjectName("disconnect_translator_btn")
        self.gridLayout.addWidget(self.disconnect_translator_btn, 0, 2, 1, 3)
        self.reverse_x_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reverse_x_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverse_x_btn.sizePolicy().hasHeightForWidth())
        self.reverse_x_btn.setSizePolicy(sizePolicy)
        self.reverse_x_btn.setObjectName("reverse_x_btn")
        self.gridLayout.addWidget(self.reverse_x_btn, 1, 0, 1, 1)
        self.xy_change_btn = QtWidgets.QPushButton(self.centralwidget)
        self.xy_change_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xy_change_btn.sizePolicy().hasHeightForWidth())
        self.xy_change_btn.setSizePolicy(sizePolicy)
        self.xy_change_btn.setObjectName("xy_change_btn")
        self.gridLayout.addWidget(self.xy_change_btn, 1, 1, 1, 2)
        self.reverse_y_btn = QtWidgets.QPushButton(self.centralwidget)
        self.reverse_y_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverse_y_btn.sizePolicy().hasHeightForWidth())
        self.reverse_y_btn.setSizePolicy(sizePolicy)
        self.reverse_y_btn.setObjectName("reverse_y_btn")
        self.gridLayout.addWidget(self.reverse_y_btn, 1, 3, 1, 2)
        self.shift_x_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shift_x_line.sizePolicy().hasHeightForWidth())
        self.shift_x_line.setSizePolicy(sizePolicy)
        self.shift_x_line.setObjectName("shift_x_line")
        self.gridLayout.addWidget(self.shift_x_line, 2, 0, 1, 1)
        self.move_x_btn = QtWidgets.QPushButton(self.centralwidget)
        self.move_x_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_x_btn.sizePolicy().hasHeightForWidth())
        self.move_x_btn.setSizePolicy(sizePolicy)
        self.move_x_btn.setObjectName("move_x_btn")
        self.gridLayout.addWidget(self.move_x_btn, 2, 1, 1, 1)
        self.shift_y_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shift_y_line.sizePolicy().hasHeightForWidth())
        self.shift_y_line.setSizePolicy(sizePolicy)
        self.shift_y_line.setObjectName("shift_y_line")
        self.gridLayout.addWidget(self.shift_y_line, 2, 2, 1, 2)
        self.move_y_btn = QtWidgets.QPushButton(self.centralwidget)
        self.move_y_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.move_y_btn.sizePolicy().hasHeightForWidth())
        self.move_y_btn.setSizePolicy(sizePolicy)
        self.move_y_btn.setObjectName("move_y_btn")
        self.gridLayout.addWidget(self.move_y_btn, 2, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.step_along_beam_n = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_along_beam_n.sizePolicy().hasHeightForWidth())
        self.step_along_beam_n.setSizePolicy(sizePolicy)
        self.step_along_beam_n.setObjectName("step_along_beam_n")
        self.gridLayout_2.addWidget(self.step_along_beam_n, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("color:#dedede")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.disconnect_powermeter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_powermeter_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disconnect_powermeter_btn.sizePolicy().hasHeightForWidth())
        self.disconnect_powermeter_btn.setSizePolicy(sizePolicy)
        self.disconnect_powermeter_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.disconnect_powermeter_btn.setStyleSheet("QPushButton{\n"
"box-shadow: 0px 10px 14px -7px #276873;\n"
"    background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);\n"
"    background-color:#599bb3;\n"
"    border:1px solid #305f70;\n"
"border-radius:6px;\n"
"color:#ffffff;\n"
"}\n"
"QPushButton:disabled{\n"
"background-color:#92aab3;\n"
"color:#757d6f;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#2694bd;\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #305f70;\n"
"}")
        self.disconnect_powermeter_btn.setObjectName("disconnect_powermeter_btn")
        self.gridLayout_2.addWidget(self.disconnect_powermeter_btn, 0, 1, 1, 1)
        self.step_along_beam = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_along_beam.sizePolicy().hasHeightForWidth())
        self.step_along_beam.setSizePolicy(sizePolicy)
        self.step_along_beam.setObjectName("step_along_beam")
        self.gridLayout_2.addWidget(self.step_along_beam, 2, 1, 1, 1)
        self.label_n_along = QtWidgets.QLabel(self.centralwidget)
        self.label_n_along.setStyleSheet("color: #dedede")
        self.label_n_along.setText("")
        self.label_n_along.setObjectName("label_n_along")
        self.gridLayout_2.addWidget(self.label_n_along, 5, 1, 1, 1)
        self.step_across_beam = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_across_beam.sizePolicy().hasHeightForWidth())
        self.step_across_beam.setSizePolicy(sizePolicy)
        self.step_across_beam.setObjectName("step_across_beam")
        self.gridLayout_2.addWidget(self.step_across_beam, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("color:#dedede")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("color:#dedede")
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_n_across = QtWidgets.QLabel(self.centralwidget)
        self.label_n_across.setStyleSheet("color: #dedede")
        self.label_n_across.setText("")
        self.label_n_across.setObjectName("label_n_across")
        self.gridLayout_2.addWidget(self.label_n_across, 5, 0, 1, 1)
        self.connect_powermeter_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_powermeter_btn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_powermeter_btn.sizePolicy().hasHeightForWidth())
        self.connect_powermeter_btn.setSizePolicy(sizePolicy)
        self.connect_powermeter_btn.setMinimumSize(QtCore.QSize(0, 24))
        self.connect_powermeter_btn.setStyleSheet("QPushButton{\n"
"box-shadow:inset 0px 1px 0px 0px #fff6af;\n"
"    background:linear-gradient(to bottom, #ffec64 5%, #ffab23 100%);\n"
"    background-color:#ffec64;\n"
"    border-radius:6px;\n"
"    border:1px solid #ffaa22;\n"
"}\n"
"QPushButton:disabled{\n"
"background-color:#fff3a1;\n"
"color:#757d6f;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#ffe52b;\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #ffaa22;\n"
"}")
        self.connect_powermeter_btn.setObjectName("connect_powermeter_btn")
        self.gridLayout_2.addWidget(self.connect_powermeter_btn, 0, 0, 1, 1)
        self.step_across_beam_n = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_across_beam_n.sizePolicy().hasHeightForWidth())
        self.step_across_beam_n.setSizePolicy(sizePolicy)
        self.step_across_beam_n.setObjectName("step_across_beam_n")
        self.gridLayout_2.addWidget(self.step_across_beam_n, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setStyleSheet("color:#dedede")
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setStyleSheet("color:#dedede")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.threshold_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.threshold_line.sizePolicy().hasHeightForWidth())
        self.threshold_line.setSizePolicy(sizePolicy)
        self.threshold_line.setObjectName("threshold_line")
        self.gridLayout_3.addWidget(self.threshold_line, 2, 0, 1, 1)
        self.diameter_line = QtWidgets.QLineEdit(self.centralwidget)
        self.diameter_line.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diameter_line.sizePolicy().hasHeightForWidth())
        self.diameter_line.setSizePolicy(sizePolicy)
        self.diameter_line.setObjectName("diameter_line")
        self.gridLayout_3.addWidget(self.diameter_line, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet("color:#dedede")
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setStyleSheet("color:#dedede")
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setStyleSheet("color:#dedede")
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 3, 1, 1)
        self.wave_length_line = QtWidgets.QLineEdit(self.centralwidget)
        self.wave_length_line.setObjectName("wave_length_line")
        self.gridLayout_3.addWidget(self.wave_length_line, 2, 1, 1, 1)
        self.M2_line = QtWidgets.QLineEdit(self.centralwidget)
        self.M2_line.setEnabled(False)
        self.M2_line.setObjectName("M2_line")
        self.gridLayout_3.addWidget(self.M2_line, 2, 3, 1, 1)
        self.begin_measurment_btn = QtWidgets.QPushButton(self.centralwidget)
        self.begin_measurment_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.begin_measurment_btn.sizePolicy().hasHeightForWidth())
        self.begin_measurment_btn.setSizePolicy(sizePolicy)
        self.begin_measurment_btn.setStyleSheet("QPushButton{\n"
"box-shadow:inset 0px 1px 0px 0px #d9fbbe;\n"
"background:linear-gradient(to bottom, #b8e356 5%, #a5cc52 100%);\n"
"background-color:#b8e356;\n"
"border-radius:6px;\n"
"border:1px solid #83c41a;\n"
"display:inline-block;\n"
"cursor:pointer;\n"
"color:#000000;\n"
"font-family:Arial;\n"
"font-weight:bold;\n"
"text-decoration:none;\n"
"text-shadow:0px 1px 0px #86ae47;\n"
"}\n"
"QPushButton:disabled {\n"
"box-shadow:inset 0px 0px 14px -3px #f2fadc;\n"
"    background:linear-gradient(to bottom, #dbe6c4 5%, #9ba892 100%);\n"
"    background-color:#dbe6c4;\n"
"    border-radius:6px;\n"
"    border:1px solid #b2b8ad;\n"
"    display:inline-block;\n"
"    cursor:pointer;\n"
"    color:#757d6f;\n"
"    font-family:Arial;\n"
"    font-weight:bold;\n"
"    text-decoration:none;\n"
"    text-shadow:0px 1px 0px #ced9bf;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#9ede16\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #83c41a;\n"
"}")
        self.begin_measurment_btn.setObjectName("begin_measurment_btn")
        self.gridLayout_3.addWidget(self.begin_measurment_btn, 0, 0, 1, 2)
        self.interrupt_btn = QtWidgets.QPushButton(self.centralwidget)
        self.interrupt_btn.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interrupt_btn.sizePolicy().hasHeightForWidth())
        self.interrupt_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.interrupt_btn.setFont(font)
        self.interrupt_btn.setStyleSheet("QPushButton#interrupt_btn{\n"
"    box-shadow:inset 0px 1px 0px 0px #f29c93;\n"
"    background:linear-gradient(to bottom, #fe1a00 5%, #ce0100 100%);\n"
"    background-color:#fe1a00;\n"
"    border-radius:6px;\n"
"    border:1px solid #d83526;\n"
"    display:inline-block;\n"
"    cursor:pointer;\n"
"    color:#ffffff;\n"
"    font-family:Arial;\n"
"    font-weight:bold;\n"
"    text-decoration:none;\n"
"    text-shadow:0px 1px 0px #b23e35;\n"
"}\n"
"\n"
"QPushButton#interrupt_btn:disabled {\n"
"    box-shadow:inset 0px 1px 0px 0px #f29c93;\n"
"    background:linear-gradient(to bottom, #fe1a00 5%, #ce0100 100%);\n"
"    background-color:#ffa196;\n"
"    border-radius:6px;\n"
"    border:1px solid #ab6b63;\n"
"    display:inline-block;\n"
"    cursor:pointer;\n"
"    color:#ffffff;\n"
"    font-family:Arial;\n"
"    font-weight:bold;\n"
"    text-decoration:none;\n"
"    text-shadow:0px 1px 0px #b23e35;\n"
"}\n"
"\n"
"QPushButton#interrupt_btn:pressed{\n"
"background-color: #c21400\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid #d83526;\n"
"}")
        self.interrupt_btn.setObjectName("interrupt_btn")
        self.gridLayout_3.addWidget(self.interrupt_btn, 0, 2, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_graph = PlotWidget(self.centralwidget)
        self.line_graph.setMinimumSize(QtCore.QSize(0, 300))
        self.line_graph.setObjectName("line_graph")
        self.horizontalLayout.addWidget(self.line_graph)
        self.gauss_graph = PlotWidget(self.centralwidget)
        self.gauss_graph.setMinimumSize(QtCore.QSize(0, 300))
        self.gauss_graph.setObjectName("gauss_graph")
        self.horizontalLayout.addWidget(self.gauss_graph)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1314, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.powermeter_action = QtWidgets.QAction(MainWindow)
        self.powermeter_action.setObjectName("powermeter_action")
        self.act_save = QtWidgets.QAction(MainWindow)
        self.act_save.setObjectName("act_save")
        self.act_saveas = QtWidgets.QAction(MainWindow)
        self.act_saveas.setObjectName("act_saveas")
        self.act_open = QtWidgets.QAction(MainWindow)
        self.act_open.setObjectName("act_open")
        self.menu.addAction(self.powermeter_action)
        self.menu_2.addAction(self.act_save)
        self.menu_2.addAction(self.act_open)
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Beam Width Meter"))
        self.connect_translator_btn.setText(_translate("MainWindow", "Подключить подвижку"))
        self.disconnect_translator_btn.setText(_translate("MainWindow", "Отключить подвижку"))
        self.reverse_x_btn.setText(_translate("MainWindow", "Реверс X"))
        self.xy_change_btn.setText(_translate("MainWindow", "X <-> Y"))
        self.reverse_y_btn.setText(_translate("MainWindow", "Реверс Y"))
        self.move_x_btn.setText(_translate("MainWindow", "Move X"))
        self.move_y_btn.setText(_translate("MainWindow", "Move  Y"))
        self.label.setText(_translate("MainWindow", "Шаг поперёк пучка, мм"))
        self.disconnect_powermeter_btn.setText(_translate("MainWindow", "Отключить измеритель"))
        self.label_2.setText(_translate("MainWindow", "Шаг вдоль пучка, мм"))
        self.label_6.setText(_translate("MainWindow", "Макс. шагов поперёк"))
        self.connect_powermeter_btn.setText(_translate("MainWindow", "Подключить измеритель"))
        self.label_7.setText(_translate("MainWindow", "Макс. шагов вдоль"))
        self.label_4.setText(_translate("MainWindow", "Уровень"))
        self.label_5.setText(_translate("MainWindow", "Диаметр"))
        self.label_8.setText(_translate("MainWindow", "Длина волны"))
        self.label_9.setText(_translate("MainWindow", "M2"))
        self.begin_measurment_btn.setText(_translate("MainWindow", "Начать измерение"))
        self.interrupt_btn.setText(_translate("MainWindow", "Прервать измерение"))
        self.menu.setTitle(_translate("MainWindow", "Подключение"))
        self.menu_2.setTitle(_translate("MainWindow", "Файл"))
        self.powermeter_action.setText(_translate("MainWindow", "Подключение измерителя"))
        self.act_save.setText(_translate("MainWindow", "Сохранять в..."))
        self.act_saveas.setText(_translate("MainWindow", "Сохранить как..."))
        self.act_open.setText(_translate("MainWindow", "Открыть"))

from pyqtgraph import PlotWidget
