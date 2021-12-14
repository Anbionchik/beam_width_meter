# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:36:37 2021

@author: Anbion
"""
import sys
from PyQt5 import QtWidgets
import main_window


class BeamWidthMeterApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connect_powermeter_btn.clicked.connect(self.connect_powermeter)
        self.connect_translator_btn.clicked.connect(self.connect_translator)
        self.begin_measurment_btn.clicked.connect(self.execute_measurment)
        self.step_across_value = 0.01
        self.step_along_value = 10        
        self.step_across_beam.setText(str(self.step_across_value))
        self.step_along_beam.setText(str(self.step_along_value))
        self.step_across_beam.textChanged.connect(self.params_setter)
        self.step_along_beam.textChanged.connect(self.params_setter)
        
    def connect_powermeter(self):
        self.info_field.appendPlainText("Подключен поверметр")
    def connect_translator(self):
        self.info_field.appendPlainText("Подключен транслатор")
    def params_setter(self):
        self.step_across_value = float(self.step_across_beam.text())
        self.step_along_value = float(self.step_along_beam.text())
        self.info_field.appendPlainText(str(self.step_across_value))
        self.info_field.appendPlainText(str(self.step_along_value))
    def execute_measurment(self):
        self.info_field.appendPlainText("Начинаем измерения")
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()