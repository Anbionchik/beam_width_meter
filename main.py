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
import platform
import powermeter_dialog

without_USB = False
try:
    import pyvisa
except ModuleNotFoundError:
    without_USB = True
    

# Dependences
    
# For correct usage of the library libximc,
# you need to add the file pyximc.py wrapper with the structures of the library to python path.
cur_dir = os.path.abspath(os.path.dirname(__file__)) # Specifies the current directory.
ximc_package_dir = os.path.join(cur_dir, "pyximc_wrapper") # Formation of the directory name with python dependencies.
sys.path.append(ximc_package_dir)  # add pyximc.py wrapper to python path

# Depending on your version of Windows, add the path to the required DLLs to the environment variable
# bindy.dll
# libximc.dll
# xiwrapper.dll
if platform.system() == "Windows":
    # Determining the directory with dependencies for windows depending on the bit depth.
    
    if sys.version_info >= (3,8):
        os.add_dll_directory(ximc_package_dir)
    if not ximc_package_dir in os.environ["Path"]:
        os.environ["Path"] = ximc_package_dir + ";" + os.environ["Path"] # add dll path into an environment variable

try: 
    import pyximc
except ImportError:
    print ("Can't import pyximc module. The most probable reason is that you changed the relative location of the test_Python.py and pyximc.py files. See developers' documentation for details.")
    exit()

from translator_controller import (initialize_axes, 
                                   close_axes, 
                                   user_calibration,
                                   movement_setter,
                                   reverse_engine,                                   
                                   set_zero,
                                   test_run,
                                   get_position,
                                   move_to_coords,
                                   shift_move)
from pyximc_wrapper.pyximc import *
from graph_fit import get_gauss_fit, find_intersection
import numpy as np
from statistics import stdev


# Static
powermeter_ip_address = "192.168.77.78"
# Dynamic
# powermeter_ip_address = "172.16.16.84"
powermeter_port = 5000

powermeter_baud_rate = 115200

powermeter_com_port = ''

connection_type = 'Ethernet'





class BeamWidthMeterApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.connect_powermeter_btn.clicked.connect(self.connect_powermeter)
        self.connect_translator_btn.clicked.connect(self.connect_translator)
        self.begin_measurment_btn.clicked.connect(self.execute_measurment)
        self.interrupt_btn.clicked.connect(self.interrupt_measurment)
        self.step_across_value = 0.01
        self.step_along_value = 1  
        self.wait_time = 1000 # в мс
        self.beam_threshold = 0.3
        self.steps_across = 38
        self.steps_along = 1
        self.diameters_list = []
        self.x_coords_list = []
        
        
        self.threshold_line.setText('0.137')
        self.step_across_beam.setText(str(self.step_across_value))
        self.step_along_beam.setText(str(self.step_along_value))
        self.step_across_beam_n.setText(str(self.steps_across))
        self.step_along_beam_n.setText(str(self.steps_along))
        self.params_calculator()
        
        self.step_across_beam.textChanged.connect(self.params_calculator)
        self.step_along_beam.textChanged.connect(self.params_calculator)
        self.step_across_beam_n.textChanged.connect(self.params_calculator)
        self.step_along_beam_n.textChanged.connect(self.params_calculator)
        
        
        
        self.disconnect_powermeter_btn.clicked.connect(self.disconnect_powermeter)
        self.disconnect_translator_btn.clicked.connect(self.disconnect_translator)
        self.reverse_x_btn.clicked.connect(lambda: self.reverse("X"))
        self.reverse_y_btn.clicked.connect(lambda: self.reverse("Y"))
        self.move_x_btn.clicked.connect(lambda: self.move_axis("X"))
        self.move_y_btn.clicked.connect(lambda: self.move_axis("Y"))
        self.xy_change_btn.clicked.connect(self.change_axes)
        self.choose_folder_btn.clicked.connect(self.open_folder)
        
        
        
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon)
        self.choose_folder_btn.setIcon(icon)
        self.folder_name = "../"
        self.results_folder_path.setText(self.folder_name)
        self.info_field.setEnabled(True)
        
        # Ручки для оформления графиков
        self.main_graph_pen = pg.mkPen(color=(229,43,80), width=2)
        self.yellow_pen = pg.mkPen(color=(255,220,51), width=2)
        self.green_pen = pg.mkPen(color=(68,148,74), width=2)
        self.purple_pen = pg.mkPen(color=(222,76,138), width = 2)
        
        
        
        self.main_graph.setBackground("#293133")
        self.main_graph.setTitle("Основной график")
        self.main_graph.setLabel('left', 'Ширина пучка, мкм')
        self.main_graph.setLabel('bottom', 'Смещение вдоль пучка, мм')
        self.main_graph.addLegend()
        
        
        self.translator_coords_graph.setBackground("#293133")
        self.translator_coords_graph.setTitle("Положение подвижки")
        self.translator_coords_graph.setLabel('left', 'Y, мм')
        self.translator_coords_graph.setLabel('bottom', 'X, мм')
        
        self.line_graph.setBackground("#293133")
        self.line_graph.setTitle("Значение мощности")
        self.line_graph.setLabel('left', 'P, W')
        self.line_graph.setLabel('bottom', 'X, мм')
        
        self.gauss_graph.setBackground("#293133")
        self.gauss_graph.setTitle("Производная мощности")
        self.gauss_graph.setLabel('left', "P', мм")
        self.gauss_graph.setLabel('bottom', 'X, мм')
        
            
        self.power_list = []

        self.powermeter_action.triggered.connect(self.open_dialog)
        
        
    def open_dialog(self):
        dlg = DialogPowermeter(powermeter_ip_address,
                               powermeter_port,
                               powermeter_baud_rate)
        result_code = dlg.exec_() 
        print(result_code)        
        
        
    def connect_powermeter(self):
        if connection_type == 'USB':
            try:
                rm = pyvisa.ResourceManager()
                rm.list_resources()
                self.my_instrument = rm.open_resource(powermeter_com_port)
                self.my_instrument.baud_rate = powermeter_baud_rate
                in_data = self.my_instrument.query('*VER?').strip('\n')
                self.show_info("Измеритель мощности подключён: " + in_data)
            except IndexError:
                self.show_info("Подключённых устройств не обнаружено")
                return
            except Exception as e:
                self.show_info("Ошибка запроса на подключённое устройство:" + str(e))
                return
        else:
            addr = (powermeter_ip_address, powermeter_port)
            self.tcp_socket = socket(AF_INET, SOCK_STREAM)
            self.tcp_socket.settimeout(4.0)
            try:
                self.tcp_socket.connect(addr)
                out_data = str.encode("*VER")
                self.tcp_socket.send(out_data)
                in_data = self.tcp_socket.recv(1024)
                in_data = bytes.decode(in_data)
                # in_data = "Фантомный маэстро"
                self.show_info("Измеритель мощности подключён: " + in_data)
            except timeout:
                self.show_info("Не удалось подключиться к измерителю мощности :(")
                return
        
        self.disconnect_powermeter_btn.setEnabled(True)
        self.connect_powermeter_btn.setEnabled(False)
        self.allow_to_measure()
    
    
    
    def get_point(self):
        
        """
        Делается запрос 5 точек от измерителя с паузой в 150 мс, затем 
        высчитывается станадартное отклонение и среднее. Если 
        ст.откл/среднее > threshold_value. То возвращается None, в противном 
        случае среднее.

        Returns
        -------
        power_value : float.

        """
        threshold_value = 0.5        
        
        average_list = []
        
        for _ in range(5):
            if connection_type == 'USB':
                answer = self.my_instrument.query("*CVU?")
            else:
                self.tcp_socket.send(str.encode("*CVU"))
                answer = bytes.decode(self.tcp_socket.recv(1024))
            average_list.append(float(answer))
            QtCore.QThread.msleep(150)
            
        
        power_value = mean(average_list)
        
        st_otkl = stdev(average_list)
        
        if st_otkl / power_value > threshold_value:
            return None
        else:
            return power_value
    
    def move_axis(self, axis):
        try:
            if axis == "X":
                shift_val = float(self.shift_x_line.text())
                shift_move(self.device_x, shift_val, self.user_unit)
            elif axis == "Y":
                shift_val = float(self.shift_y_line.text())
                shift_move(self.device_y, shift_val, self.user_unit)
        except ValueError:
            pass
    
    def connect_translator(self):
        try:
            self.device_x, self.device_y = initialize_axes()            
        except NameError:
            self.show_info("Не удалось подключиться к подвижке")
            return
        movement_setter(self.device_x, self.device_y, 4000, 2000, 4000)
        self.user_unit = user_calibration()
        set_zero(self.device_x, self.device_y)
        self.show_info("Подвижка подключена")
        self.disconnect_translator_btn.setEnabled(True)
        self.reverse_x_btn.setEnabled(True)
        self.reverse_y_btn.setEnabled(True)
        self.xy_change_btn.setEnabled(True)
        self.move_x_btn.setEnabled(True)
        self.move_y_btn.setEnabled(True)
        self.connect_translator_btn.setEnabled(False)
        self.allow_to_measure()
    
    def allow_to_measure(self):
        if (not self.connect_powermeter_btn.isEnabled() and
            not self.connect_translator_btn.isEnabled()):
            self.begin_measurment_btn.setEnabled(True)
        else:
            self.begin_measurment_btn.setEnabled(False)
            
        
    
    def disconnect_powermeter(self):
        if connection_type == 'USB':
            self.my_instrument.close()
        else:
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
        self.xy_change_btn.setEnabled(False)
        self.move_x_btn.setEnabled(False)
        self.move_y_btn.setEnabled(False)
        self.connect_translator_btn.setEnabled(True)
        self.allow_to_measure()
    
    def params_setter(self):
        self.step_across_value = float(self.step_across_beam.text())
        self.step_along_value = float(self.step_along_beam.text())
        self.steps_across = int(self.step_across_beam_n.text())
        self.steps_along = int(self.step_along_beam_n.text())
        
    def params_calculator(self):
        try:
            lab_across = round(int(self.step_across_beam_n.text()) * 
                               float(self.step_across_beam.text()), 2)
            lab_along = round(int(self.step_along_beam_n.text()) * 
                              float(self.step_along_beam.text()) , 2)
            self.label_n_across.setText("Всего {} мм".format(lab_across))
            self.label_n_along.setText("Всего {} мм".format(lab_along))
        except ValueError:
            pass
        
    
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
                                          pen=self.green_pen,
                                          symbol="o", symbolBrush="#6A5ACD", 
                                          symbolSize=3)
    
    def draw_power(self, start_point, end_point):
        if not start_point is None and start_point[0] > 7:
            crds_list = self.local_coords_list[start_point[0] - 7:]
            pwr_list = self.power_list[start_point[0] - 7:]
            self.line_graph.clear()
            self.line_graph.plot(crds_list, pwr_list, 
                                 pen=self.yellow_pen,
                                 symbol="t", symbolBrush="#6A5ACD", 
                                 symbolSize=2)
        else:
            self.line_graph.clear()
            self.line_graph.plot(self.local_coords_list, self.power_list, 
                                 pen=self.yellow_pen,
                                 symbol="t", symbolBrush="#6A5ACD", 
                                 symbolSize=2)
    
    
    def draw_gauss(self, start_point, end_point):
        gauss_fit, y = get_gauss_fit(self.local_coords_list, self.power_list)
        
        if not start_point is None and start_point[0] > 7:
            crds_list = self.local_coords_list[start_point[0] - 7:]
            y_list = y[start_point[0] - 7:]
            if gauss_fit is not None:
                gauss_list = gauss_fit[start_point[0] - 7:]
        else:
            crds_list = self.local_coords_list[:]            
            y_list = y[:]
            if gauss_fit is not None:
                gauss_list = gauss_fit[:]
        
        if gauss_fit is None:
            self.gauss_graph.clear()
            self.gauss_graph.plot(crds_list, y_list, pen=None, 
                                 symbol="o", symbolBrush="#0000AA", 
                                 symbolSize=4)
        else:
            self.gauss_graph.clear()
            self.gauss_graph.plot(crds_list, gauss_list, 
                                 pen=self.purple_pen,
                                 symbol="t", symbolBrush="#0000AA", 
                                 symbolSize=2)
            self.gauss_graph.plot(crds_list, y_list, pen=None, 
                                 symbol="o", symbolBrush="#0000AA", 
                                 symbolSize=4)
        if not end_point is None:
            self.find_diameter(self.local_coords_list, gauss_fit)
        
    def find_diameter(self, x, gauss_fit):
        threshold = float(self.threshold_line.text())
        if not gauss_fit is None: 
            gauss_max = gauss_fit.max()
            threshold_curve = np.full(len(x), gauss_max * threshold)
            
            intersection_list = find_intersection(x, gauss_fit, threshold_curve)        
            if not intersection_list is None:            
                self.gauss_graph.plot(*intersection_list, pen=None,
                                      symbol='x', symbolBrush="7CFC00",
                                      symbolSize=8)
                if len(intersection_list[0]) == 2:
                    diameter = round(abs(intersection_list[0][1] - intersection_list[0][0]) * 2, 4)
                    self.diameter_line.setText(str(diameter))
    
    def change_axes(self):
        self.device_x, self.device_y = self.device_y, self.device_x
        self.show_info("Ось X -> Ось Y\nОсь Y -> Ось X")
    
    
    def execute_measurment(self):
        
        self.interrupt_measurment_flag = False
        self.interrupt_btn.setEnabled(True)
        self.begin_measurment_btn.setEnabled(False)
        self.params_setter()
        self.main_graph.clear()
        self.translator_coords_graph.clear()
        self.translator_move_history = [[],[]]
        self.diameter_line.clear()
        self.show_info("Начинаем измерение.")
        time_file_name = time.strftime("%d.%m.%y %H_%M_%S", time.localtime())
        coords = {"x" : 0, "y" : 0}
        point_number = 1
        with open(self.folder_name + time_file_name + " raw_results.csv", "w") as file:
            
            file.write("N,Time,X_pos,Y_pos,Value\r")
            set_zero(self.device_x, self.device_y)
                        
            for j in range(self.steps_along):
                
                self.power_list = []
                beam_start_point = None
                beam_end_point = None
                self.local_coords_list = []
                self.gauss_graph.clear()
                
                for i in range(self.steps_across):
                    
                    if self.interrupt_measurment_flag:
                        
                        self.show_info("Измерение прервано")
                        move_to_coords(self.device_x, self.device_y, (0,0), self.user_unit)
                        self.begin_measurment_btn.setEnabled(True)
                        return
                    
                    if not beam_end_point is None:
                        if i - beam_end_point[0] > 10:
                            break
                    
                    self.update()
                    QtWidgets.QApplication.processEvents()
                    # shift_move(self.device_y, self.step_across_value, 
                    #            self.user_unit)
                    
                    coords["x"] = -(self.step_along_value) * j
                    coords["y"] = self.step_across_value * i
                    
                    move_to_coords(self.device_x, self.device_y, 
                                   (coords["x"],coords["y"]), self.user_unit)
                    QtCore.QThread.msleep(self.wait_time) 
                    
                    power_value = None
                    while power_value is None:                        
                        power_value = self.get_point()                    
                        # power_value = test_val_list[i]
                        if power_value is None:
                            self.show_info("Повторный запрос значения мощности")
                    
                    self.power_list.append(power_value)
                    
                    x_pos, y_pos = map(round, get_position(self.device_x, 
                                                self.device_y, 
                                                self.user_unit), [4,4])
                    
                    self.local_coords_list.append(y_pos)
                    
                    if beam_start_point is None and len(self.power_list) > 2:
                        if (self.power_list[-1] - self.power_list[-2]) / self.step_across_value > self.beam_threshold:
                            beam_start_point = (i, y_pos)
                            print(beam_start_point)
                    elif not beam_start_point is None and beam_end_point is None:
                        if (((self.power_list[-1] - self.power_list[-2]) / 
                            self.step_across_value < self.beam_threshold) or
                        (self.steps_across - i < 10)):
                            
                            beam_end_point = (i, y_pos)
                            print(beam_end_point)
                    
                    if i > 1:
                        self.draw_gauss(beam_start_point, beam_end_point)
                        
                    self.draw_power(beam_start_point, beam_end_point)
                    self.draw_coords((x_pos, y_pos))
                    time_now = time.strftime("%M:%S", time.localtime())
                    line = (str(point_number) + "," + time_now + "," + 
                            str(x_pos) + "," + str(y_pos) + 
                            "," + str(power_value)).replace("\r\n", "")
                    shw_line = "{:^4}|{:^8}|{:^8.4f}|{:^8.4f}|{:^8.4f}".format(point_number, 
                                                                                  time_now, x_pos, 
                                                                                  y_pos,float(power_value))
                    print(repr(line))
                    file.write(line + '\r')
                    self.show_info(shw_line)
                    point_number += 1
                
                if self.diameter_line.text() != "":
                    self.diameters_list.append(float(self.diameter_line.text()))
                    self.x_coords_list.append(x_pos)
                    self.show_info("В точке {:.2f} диаметр пучка составляет {:.4f}".format(x_pos, float(self.diameter_line.text())))
                
                self.main_graph.plot(self.x_coords_list, self.diameters_list, 
                                     pen=self.main_graph_pen, symbol="o", 
                                     symbolBrush="#44944A", symbolSize=7)
                try:
                    self.main_graph.setYRange(0, max(self.diameters_list) * 1.2)
                except ValueError:
                    pass
                self.diameter_line.clear()
                
                move_to_coords(self.device_x, self.device_y, 
                               (-(self.step_along_value) * (j + 1),0), 
                               self.user_unit)
                QtCore.QThread.msleep(10000) 
        move_to_coords(self.device_x, self.device_y, (0,0), self.user_unit)
        with open(self.folder_name + time_file_name + " Results.csv", "w") as file:
            file.write("N,X_pos,Diameter\r")
            for rec in range(len(self.diameters_list)):
                file.write("{},{},{}\r".format(str(rec), 
                                               str(self.x_coords_list[rec]),
                                               str(self.diameters_list[rec])))
        self.begin_measurment_btn.setEnabled(True)
        self.interrupt_btn.setEnabled(False)
        self.show_info("Измерение завершено.")
                
            
    
        
    def interrupt_measurment(self):
        self.interrupt_btn.setEnabled(False)
        self.interrupt_measurment_flag = True
        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
        
    def open_folder(self):
        
        self.folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                                 "Choose folder for results files",
                                                                 options=QtWidgets.QFileDialog.ShowDirsOnly)
        self.results_folder_path.setText(self.folder_name)
        
    def closeEvent(self, event):
        if self.disconnect_powermeter_btn.isEnabled():
            self.disconnect_powermeter()
        if self.disconnect_translator_btn.isEnabled():
            self.disconnect_translator()
        event.accept() # let the window close



class DialogPowermeter(QtWidgets.QDialog, powermeter_dialog.Ui_Dialog):
    def __init__(self, ip, port, baud_rate):
        super().__init__()
        self.setupUi(self)
        self.ip_line.setText(ip)
        self.port_line.setText(str(port))
        self.baud_rate_line.setText(str(baud_rate))
        if without_USB:
            self.radioButton_2.setEnabled(False)
        self.com_port_box.setEnabled(False)
        self.rescan_btn.setEnabled(False)
        self.baud_rate_line.setEnabled(False)
        
        self.radioButton.clicked.connect(self.change_connection_type)
        self.radioButton_2.clicked.connect(self.change_connection_type)
        self.rescan_btn.clicked.connect(self.rescan_com_ports)
        self.ok_btn.clicked.connect(self.save_and_exit)
        self.cancel_btn.clicked.connect(self.save_and_exit)
        
                
        
    def change_connection_type(self):
        sender = self.sender()
        if sender.text() == "Ethernet":
            if not self.ip_line.isEnabled():
                self.ip_line.setEnabled(True)
                self.port_line.setEnabled(True)
            if self.com_port_box.isEnabled():
                self.com_port_box.setEnabled(False)
                self.rescan_btn.setEnabled(False)
                self.baud_rate_line.setEnabled(False)
        else:
            if self.ip_line.isEnabled():
                self.ip_line.setEnabled(False)
                self.port_line.setEnabled(False)
            if not self.com_port_box.isEnabled():
                self.com_port_box.setEnabled(True)
                self.rescan_btn.setEnabled(True)
                self.baud_rate_line.setEnabled(True)
                
    def rescan_com_ports(self):
        self.com_port_box.clear()
        rm = pyvisa.ResourceManager()
        info = rm.list_resources_info()
        keys_list = info.keys()
        ports_list = []
        for key in keys_list:
            ports_list.append("{} -> {}".format(info[key].alias, key))
        self.com_port_box.addItems(ports_list)
    
    def save_and_exit(self):
        if self.sender().text() == "OK":
            global connection_type
            if self.radioButton.isChecked():
                global powermeter_ip_address
                global powermeter_port
                powermeter_ip_address = self.ip_line.text()
                powermeter_port = int(self.port_line.text())
                connection_type = 'Ethernet'
            else:
                global powermeter_com_port
                global powermeter_baud_rate
                powermeter_com_port = self.com_port_box.currentText()
                powermeter_com_port = powermeter_com_port.split('>')[1].lstrip(' ')
                powermeter_baud_rate = int(self.baud_rate_line.text())
                connection_type = 'USB'
            self.done(1)
        else:
            self.done(0)
        
        
        
    
    
    
class MeasurmentHandler(QtCore.QObject):
    running = False
    newTextAndColor = QtCore.pyqtSignal(str, object)  

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()