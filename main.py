# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:36:37 2021

@author: Anbion
"""
import sys
import os
from PyQt5 import QtWidgets
import main_window
from socket import socket, AF_INET, SOCK_STREAM, timeout
import time
from translator_controller import (initialize_axes, 
                                   close_axes, 
                                   user_calibration,
                                   movement_setter,
                                   reverse_engine,
                                   shift_move,
                                   set_zero)
from pyximc_wrapper.pyximc import *
from multiprocessing.pool import ThreadPool

threadPool = ThreadPool(2)


dll_path = "d:\\XIlab\\beam_width_meter\\pyximc_wrapper\\"
if not "d:\\XIlab\\beam_width_meter\\pyximc_wrapper\\" in os.environ["Path"]:
    os.environ["Path"] = dll_path + ";" + os.environ["Path"]

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
        self.disconnect_powermeter_btn.clicked.connect(self.disconnect_powermeter)
        self.disconnect_translator_btn.clicked.connect(self.disconnect_translator)
        
        self.maestro_address = "192.168.77.77"
        self.maestro_port = 5000
        
    def connect_powermeter(self):
        
        addr = (self.maestro_address, self.maestro_port)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.settimeout(4.0)
        self.tcp_socket.connect(addr)
        try:
            out_data = str.encode("*VER")
            self.tcp_socket.send(out_data)
            in_data = self.tcp_socket.recv(1024)
            in_data = bytes.decode(in_data)
            self.show_info("Измеритель мощности подключён: " + in_data)
            self.disconnect_powermeter_btn.setEnabled(True)
        except timeout:
            self.show_info("Не удалось подключиться к измерителю мощности :(")
        
    def get_point(self):
        self.tcp_socket.send(str.encode("*CVU"))
        return bytes.decode(self.tcp_socket.recv(1024))
    
    def move_to(self, device_x, device_y, position):
        pass
    
    def connect_translator(self):
        try:
            self.device_x, self.device_y = initialize_axes()            
        except NameError:
            self.show_info("Не удалось подключиться к подвижке")
            return
        movement_setter(self.device_x, self.device_y, 4000, 2000, 2000)
        self.user_unit = user_calibration()
        set_zero(self.device_x, self.device_y)
        self.show_info("Подвижка подключена")
        self.disconnect_translator_btn.setEnabled(True)
        
    
    def disconnect_powermeter(self):
        self.tcp_socket.close()
        self.show_info("Измеритель мощности отключён")
        self.disconnect_powermeter_btn.setEnabled(False)
    
    def disconnect_translator(self):
        close_axes(self.device_x, self.device_y)
        self.show_info("Подвижка отключена")
        self.disconnect_translator_btn.setEnabled(False)
    
    def params_setter(self):
        self.step_across_value = float(self.step_across_beam.text())
        self.step_along_value = float(self.step_along_beam.text())
        self.info_field.appendPlainText(str(self.step_across_value))
        self.info_field.appendPlainText(str(self.step_along_value))
    def execute_measurment(self):
        for i in range(10):
             shift_move(self.device_x, 0.5, self.user_unit)
             self.info_field.appendPlainText(self.get_point())
             time.sleep(2)
    
        

        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()