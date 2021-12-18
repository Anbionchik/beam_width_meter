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
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from statistics import mean
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

test_val_list = [-0.0003,
0.002,
0.0019,
0.0001,
0.0006,
0.0013,
0.0008,
0.0046,
0.0101,
0.0216,
0.0351,
0.0539,
0.0737,
0.0916,
0.1033,
0.111,
0.1117,
0.1126,
0.1141,
0.1135,
0.11136,
0.1135,
0.11136,
0.1135,
0.11136,
0.1135,
0.11136,
0.1135,
0.11136,
0.1135,
0.11136,
]

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
        self.choose_folder_btn.clicked.connect(self.open_folder)
        
        
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon)
        self.choose_folder_btn.setIcon(icon)
        self.folder_name = "../"
        self.info_field.setEnabled(True)

        self.maestro_address = "192.168.77.77"
        self.maestro_port = 5000
        
        
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.main_graph_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.main_graph.plot(hour, temperature, name="Сенсор 1", pen=self.main_graph_pen,
                             symbol="o", symbolBrush="#00AA00", symbolSize=10)
        self.main_graph.setBackground("#FFFFFF")
        self.main_graph.setTitle("Основной график")
        self.main_graph.setLabel('left', 'Ширина пучка, мкм')
        self.main_graph.setLabel('bottom', 'Смещение вдоль пучка, мм')
        self.main_graph.addLegend()
        
        
        self.translator_coords_graph.setBackground("#FFFFFF")
        self.translator_coords_graph.setTitle("Положение подвижки")
        self.translator_coords_graph.setLabel('left', 'Y, мм')
        self.translator_coords_graph.setLabel('bottom', 'X, мм')
        
        self.line_graph.setBackground("#FFFFFF")
        self.line_graph.setTitle("Значение мощности")
        self.line_graph.setLabel('left', 'P, W')
        self.line_graph.setLabel('bottom', 'X, мм')
        
        self.gauss_graph.setBackground("#FFFFFF")
        self.gauss_graph.setTitle("Производная мощности")
        self.gauss_graph.setLabel('left', "P', мм")
        self.gauss_graph.setLabel('bottom', 'X, мм')
        
        self.translator_move_history = [[],[]]    
        self.power_list = []
        
        
            
        
        
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
            self.connect_powermeter_btn.setEnabled(False)
            self.allow_to_measure()
        except timeout:
            self.show_info("Не удалось подключиться к измерителю мощности :(")
        
    def get_point(self):
                
        average_list = []
        
        for _ in range(5):
            self.tcp_socket.send(str.encode("*CVU"))
            answer = bytes.decode(self.tcp_socket.recv(1024))
            average_list.append(float(answer))
            QtCore.QThread.msleep(150)
        
        power_value = mean(average_list)
        
        return power_value
    
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
        self.connect_translator_btn.setEnabled(False)
        self.allow_to_measure()
    
    def allow_to_measure(self):
        if (not self.connect_powermeter_btn.isEnabled() and
            not self.connect_translator_btn.isEnabled()):
            self.begin_measurment_btn.setEnabled(True)
        else:
            self.begin_measurment_btn.setEnabled(False)
            
        
    
    def disconnect_powermeter(self):
        self.tcp_socket.close()
        self.show_info("Измеритель мощности отключён")
        self.disconnect_powermeter_btn.setEnabled(False)
        self.connect_powermeter_btn.setEnabled(True)
        self.allow_to_measure()
    
    def disconnect_translator(self):
        close_axes(self.device_x, self.device_y)
        self.show_info("Подвижка отключена")
        self.disconnect_translator_btn.setEnabled(False)
        self.reverse_x_btn.setEnabled(False)
        self.reverse_y_btn.setEnabled(False)
        self.x_test_run_btn.setEnabled(False)
        self.y_test_run_btn.setEnabled(False)
        self.xy_change_btn.setEnabled(False)
        self.connect_translator_btn.setEnabled(True)
        self.allow_to_measure()
    
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
            self.draw_coords()
        elif axis == "Y":
            test_run(self.device_y, self.user_unit)
            self.draw_coords()
    
    def draw_coords(self, coords=None):
        if coords is None:
            x_pos, y_pos = map(round, get_position(self.device_x, 
                                        self.device_y, 
                                        self.user_unit), [4,4])
            self.translator_move_history[0].append(x_pos)
            self.translator_move_history[1].append(y_pos)
        else:
            self.translator_move_history[0].append(coords[0])
            self.translator_move_history[1].append(coords[1])
        self.translator_coords_graph.plot(self.translator_move_history[0], 
                                          self.translator_move_history[1],
                                          pen=self.main_graph_pen,
                                          symbol="o", symbolBrush="#00AA00", 
                                          symbolSize=4)
    
    def draw_power(self):
        self.line_graph.plot(self.local_coords_list, self.power_list, 
                             pen=self.main_graph_pen,
                             symbol="t", symbolBrush="#0000AA", symbolSize=2)
    
    def change_axes(self):
        self.device_x, self.device_y = self.device_y, self.device_x
        self.show_info("Ось X -> Ось Y\nОсь Y -> Ось X")
    
    
    def execute_measurment(self):
        wait_time = 3000 # в мс
        steps_across = 10
        steps_along = 5
        threshold = 0.2
        self.show_info("Начинаем измерение.")
        coords = {"x" : 0, "y" : 0}
        point_number = 1
        with open(self.folder_name + time.strftime("%d.%m.%y %H_%M_%S", time.localtime()) + " Results.csv", "w") as file:
            file.write("N,Time,X_pos,Y_pos,Value\r")
            set_zero(self.device_x, self.device_y)
            for j in range(steps_along):
                
                self.power_list = []
                beam_start_point = None
                beam_end_point = None
                self.local_coords_list = []
                
                for i in range(steps_across):
                    
                    if not beam_end_point is None:
                        if i - beam_end_point[0] > 5:
                            break
                    
                    self.update()
                    QtWidgets.QApplication.processEvents()
                    # shift_move(self.device_y, self.step_across_value, 
                    #            self.user_unit)
                    
                    coords["x"] = -(self.step_along_value) * j
                    coords["y"] = self.step_across_value * i
                    
                    move_to_coords(self.device_x, self.device_y, 
                                   (coords["x"],coords["y"]), self.user_unit)
                    QtCore.QThread.msleep(wait_time) 
                    
                    power_value = self.get_point()                    
                    self.power_list.append(power_value)
                    
                    x_pos, y_pos = map(round, get_position(self.device_x, 
                                                self.device_y, 
                                                self.user_unit), [4,4])
                    
                    self.local_coords_list.append(y_pos)
                    
                    if beam_start_point is None and len(self.power_list) > 1:
                        if (self.power_list[-1] - self.power_list[-2]) / self.step_across_value > threshold:
                            beam_start_point = (i, x_pos)
                    elif not beam_start_point is None:
                        if (self.power_list[-1] - self.power_list[-2]) / self.step_across_value < threshold:
                            beam_end_point = (i, x_pos)
                    
                        
                    self.draw_power()
                    self.draw_coords((x_pos, y_pos))
                    time_now = time.strftime("%M:%S", time.localtime())
                    line = (str(point_number) + "," + time_now + "," + 
                            str(x_pos) + "," + str(y_pos) + 
                            "," + str(power_value)).replace("\n", "")
                    print(repr(line))
                    file.write(line)
                    self.show_info(line.replace(",", " ").replace("\r", ""))
                    point_number += 1
                
                move_to_coords(self.device_x, self.device_y, 
                               (-(self.step_along_value) * (j + 1),0), 
                               self.user_unit)
        self.show_info("Измерение завершено.")
                
            
    
        

        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
        
    def open_folder(self):
        
        self.folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                                 "Choose folder for results files",
                                                                 options=QtWidgets.QFileDialog.ShowDirsOnly)
        self.results_folder_path.setText(self.folder_name)
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()