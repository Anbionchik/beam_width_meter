# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:36:37 2021

@author: Anbion
"""
import sys
import os
from PyQt5 import QtWidgets, QtCore
import main_window
from socket import socket, AF_INET, SOCK_STREAM, timeout
import time
from translator_controller import (initialize_axes, 
                                   close_axes, 
                                   user_calibration,
                                   movement_setter,
                                   reverse_engine,
                                   shift_move,
                                   set_zero,
                                   test_run,
                                   get_position,
                                   move_to_coords)
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
        self.step_along_value = 1        
        self.step_across_beam.setText(str(self.step_across_value))
        self.step_along_beam.setText(str(self.step_along_value))
        self.step_across_beam.textChanged.connect(self.params_setter)
        self.step_along_beam.textChanged.connect(self.params_setter)
        self.disconnect_powermeter_btn.clicked.connect(self.disconnect_powermeter)
        self.disconnect_translator_btn.clicked.connect(self.disconnect_translator)
        self.reverse_x_btn.clicked.connect(lambda: self.reverse("X"))
        self.reverse_y_btn.clicked.connect(lambda: self.reverse("Y"))
        self.x_test_run_btn.clicked.connect(lambda: self.test_run("X"))
        self.y_test_run_btn.clicked.connect(lambda: self.test_run("Y"))
        self.xy_change_btn.clicked.connect(self.change_axes)

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
        self.reverse_x_btn.setEnabled(True)
        self.reverse_y_btn.setEnabled(True)
        self.x_test_run_btn.setEnabled(True)
        self.y_test_run_btn.setEnabled(True)
        self.xy_change_btn.setEnabled(True)
        
    
    def disconnect_powermeter(self):
        self.tcp_socket.close()
        self.show_info("Измеритель мощности отключён")
        self.disconnect_powermeter_btn.setEnabled(False)
    
    def disconnect_translator(self):
        close_axes(self.device_x, self.device_y)
        self.show_info("Подвижка отключена")
        self.disconnect_translator_btn.setEnabled(False)
        self.reverse_x_btn.setEnabled(False)
        self.reverse_y_btn.setEnabled(False)
        self.x_test_run_btn.setEnabled(False)
        self.y_test_run_btn.setEnabled(False)
        self.xy_change_btn.setEnabled(False)
    
    def params_setter(self):
        self.step_across_value = float(self.step_across_beam.text())
        self.step_along_value = float(self.step_along_beam.text())
    
    def reverse(self, axis):
        if axis == "X":
            result = reverse_engine(self.device_x)
            self.show_info("Двигатель X: " + result)
        elif axis == "Y":
            result = reverse_engine(self.device_y)
            self.show_info("Двигатель Y: " + result)
    
    def test_run(self, axis):
        if axis == "X":
            test_run(self.device_x, self.user_unit)
        elif axis == "Y":
            test_run(self.device_y, self.user_unit)
    
    def change_axes(self):
        self.device_x, self.device_y = self.device_y, self.device_x
        self.show_info("Ось X -> Ось Y\nОсь Y -> Ось X")
    
    
    def execute_measurment(self):
        self.show_info("Начинаем измерение.")
        point_number = 1
        with open("../" + time.strftime("%d.%m.%y %H_%M_%S", time.localtime()) + " Results.csv", "w") as file:
            file.write("N,Time,X_pos,Y_pos,Value\r")
            set_zero(self.device_x, self.device_y)
            for j in range(2):
                for i in range(3):
                    self.update()
                    QtWidgets.QApplication.processEvents()
                    shift_move(self.device_y, self.step_across_value, 
                               self.user_unit)
                    QtCore.QThread.msleep(5000) 
                    power_value = self.get_point()
                    x_pos, y_pos = map(round, get_position(self.device_x, 
                                                self.device_y, 
                                                self.user_unit), [2,2])
                    time_now = time.strftime("%M:%S", time.localtime())
                    line = (str(point_number) + "," + time_now + "," + 
                            str(x_pos) + "," + str(y_pos) + 
                            "," + str(power_value)).replace("\r\n", "")
                    print(repr(line))
                    file.write(line)
                    self.show_info(line.replace(",", " "))
                    point_number += 1
                move_to_coords(self.device_x, self.device_y, 
                               (0,0), self.user_unit)
                
                shift_move(self.device_x, -(self.step_along_value) * (j + 1), 
                           self.user_unit)
            
    
        

        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()