# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:36:37 2021

@author: Anbion
"""

import sys
import os
from PyQt5 import QtWidgets, QtCore
import main_window
import warn_dialog
from socket import socket, AF_INET, SOCK_STREAM, timeout
import time
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import pandas as pd
from zipfile import ZipFile

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
        os.add_dll_directory(os.path.abspath('c:/windows/system32'))
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
                                   get_coords,
                                   move_to_coords,
                                   shift_move,
                                   check_edges)
from pyximc_wrapper.pyximc import *
from graph_fit import get_gauss_fit, find_intersection, calculator_M2
import numpy as np
from statistics import stdev


pg.setConfigOptions(antialias=True)
# Static
powermeter_ip_address = "172.16.16.84"
# Dynamic
# powermeter_ip_address = "172.16.16.84"
powermeter_port = 5000

powermeter_baud_rate = 115200

powermeter_com_port = ''

connection_type = 'Ethernet'

commands_dict = {'thorlabs': ('*IDN?', 'MEAS:POW?', 'SENS:CORR:WAV?', 'SENS:CORR:WAV'), 
                 'maestro':('*VER?', '*CVU', '*GWL', '*PWC')}





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
        self.value_M2 = None
        self.default_sigma = 0.3
        self.faster_flag = True  
        self.results_saved = True
        
        self.threshold_line.setText('0.137')
        self.step_across_beam.setText(str(self.step_across_value))
        self.step_along_beam.setText(str(self.step_along_value))
        self.step_across_beam_n.setText(str(self.steps_across))
        self.step_along_beam_n.setText(str(self.steps_along))
        self.params_calculator()
        
        self.step_across_beam.editingFinished.connect(self.allow_to_measure)
        self.step_along_beam.editingFinished.connect(self.allow_to_measure)
        self.step_across_beam_n.editingFinished.connect(self.allow_to_measure)
        self.step_along_beam_n.editingFinished.connect(self.allow_to_measure)
        
        self.disconnect_powermeter_btn.clicked.connect(self.disconnect_powermeter)
        self.disconnect_translator_btn.clicked.connect(self.disconnect_translator)
        self.reverse_x_btn.clicked.connect(lambda: self.reverse("X"))
        self.reverse_y_btn.clicked.connect(lambda: self.reverse("Y"))
        self.move_x_btn.clicked.connect(lambda: self.move_axis("X"))
        self.move_y_btn.clicked.connect(lambda: self.move_axis("Y"))
        self.xy_change_btn.clicked.connect(self.change_axes)
        self.act_save.triggered.connect(self.save_file)
        # TODO поменятЬ!
        self.act_open.triggered.connect(self.open_record)
        self.wave_length_line.editingFinished.connect(self.set_wave_length) 

        self.folder_name = "../"
        self.file_name = None
        self.info_field.setEnabled(True)
        
        # Ручки для оформления графиков
        self.main_graph_pen = pg.mkPen(color=(229,43,80), width=2)
        self.yellow_pen = pg.mkPen(color=(255,220,51), width=2)
        self.green_pen = pg.mkPen(color=(68,148,74), width=2)
        self.purple_pen = pg.mkPen(color=(222,76,138), width = 2)
        
        self.main_graph.setBackground("#293133")
        self.main_graph.setTitle("Основной график")
        self.main_graph.setLabel('left', 'Ширина пучка, мм')
        self.main_graph.setLabel('bottom', 'Смещение вдоль пучка, мм')
        self.main_graph.addLegend()
        self.main_points = self.main_graph.plot([], [], 
                             pen=self.main_graph_pen, symbol="o", 
                             symbolBrush="#44944A", symbolSize=7)
        self.main_points.sigPointsClicked.connect(self.print_points_clicked)
        self.main_curve = self.main_graph.plot([],[])
         
        self.translator_coords_graph.setBackground("#293133")
        self.translator_coords_graph.setTitle("Положение подвижки")
        self.translator_coords_graph.setLabel('left', 'Y, мм')
        self.translator_coords_graph.setLabel('bottom', 'X, мм')
        self.coords_line = self.translator_coords_graph.plot([], 
                                          [],
                                          pen=self.green_pen,
                                          symbol="o", symbolBrush="#6A5ACD", 
                                          symbolSize=3)
        
        self.line_graph.setBackground("#293133")
        self.line_graph.setTitle("Значение мощности")
        self.line_graph.setLabel('left', 'P, W')
        self.line_graph.setLabel('bottom', 'X, мм')
        self.power_line = self.line_graph.plot([], [], 
                             pen=self.yellow_pen,
                             symbol="t", symbolBrush="#6A5ACD", 
                             symbolSize=2)
        
        self.gauss_graph.setBackground("#293133")
        self.gauss_graph.setTitle("Производная мощности")
        self.gauss_graph.setLabel('left', "P', мм")
        self.gauss_graph.setLabel('bottom', 'X, мм')
        self.gauss_points = self.gauss_graph.plot([], [], pen=None, 
                             symbol="o", symbolBrush="#0000AA", 
                             symbolSize=4)
        self.gauss_curve = self.gauss_graph.plot([], [], 
                             pen=self.purple_pen,
                             symbol="t", symbolBrush="#0000AA", 
                             symbolSize=2)
        self.intersection_points = self.gauss_graph.plot([], pen=None,
                              symbol='x', symbolBrush="7CFC00",
                              symbolSize=8)
        
        #Добавление графиков
        self.power_list = []
        self.powermeter_action.triggered.connect(self.open_dialog)
        self.raw_res = None
        
        
    def open_dialog(self):
        dlg = DialogPowermeter(powermeter_ip_address,
                               powermeter_port,
                               powermeter_baud_rate)
        result_code = dlg.exec_() 
        print(result_code) 
    
        
        
    def connect_powermeter(self):
        if connection_type == 'USB':
            self.device = ''
            rm = pyvisa.ResourceManager()
            rm.list_resources()
            self.my_instrument = rm.open_resource(powermeter_com_port)
            self.my_instrument.baud_rate = powermeter_baud_rate
            
            for k, j in commands_dict.items():
                try:
                    in_data = self.my_instrument.query(j[0]).strip('\n')
                    if in_data == "Command not found\r":
                        continue
                except Exception as e:
                    self.show_info(str(e))
                else:
                    self.device = k
                    break
            if self.device:
                self.show_info("Измеритель мощности подключён: " + in_data)
                wavelength = self.get_wave_length()
                self.wave_length_line.setText(wavelength)
                self.wave_length = int(wavelength)
            else:
                self.show_info("Ошибка запроса на подключённое устройство")
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
                self.show_info("Измеритель мощности подключён: " + in_data)
                wavelength = self.get_wave_length()
                self.wave_length_line.setText(wavelength)
                self.wave_length = int(wavelength)
            except timeout:
                self.show_info("Не удалось подключиться к измерителю мощности :(")
                return
        
        self.disconnect_powermeter_btn.setEnabled(True)
        self.connect_powermeter_btn.setEnabled(False)
        self.allow_to_measure()
    
    def get_wave_length(self):
        if connection_type == 'USB':
            if self.device == 'maestro':
                
                wavelength = self.my_instrument.query(
                    commands_dict[self.device][2]).rstrip('\r\n').split()[1]
            else:
                wavelength = self.my_instrument.query(
                    commands_dict[self.device][2]).rstrip('\r\n')
            return wavelength           
        else:
            self.tcp_socket.send(str.encode("*GWL"))
            wavelength = bytes.decode(self.tcp_socket.recv(1024))
            wavelength = wavelength.rstrip('\r\n').split()[1]
            return wavelength
    
    def set_wave_length(self):
        wavelength = self.wave_length_line.text()
        if connection_type == 'USB':
            if self.device == "maestro":
                self.my_instrument.write(commands_dict[self.device][3] +
                                         f'{int(wavelength):05}')
            else:
                self.my_instrument.write(commands_dict[self.device][3] + " " +
                                         wavelength)
            
        else:
            self.tcp_socket.send(str.encode("*PWC" + f'{int(wavelength):05}'))
        
        #Проверка успешности установки длины волны
        recieved_wavelength = self.get_wave_length()
        if recieved_wavelength == wavelength:
            self.show_info(f"Длина волны {wavelength} нм установлена успешно.")
        else:
            self.show_info(f"Не удалось установить длину волны {wavelength} нм. Возврат к значению {recieved_wavelength}.")
            self.wave_length_line.setText(recieved_wavelength)
    
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
                answer = self.my_instrument.query(commands_dict[self.device][1])
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
                if not shift_move(self.device_x, shift_val, self.user_unit):
                    dlg = WarnDialog(warn_message="""ОШИБКА! Заданы координаты перемещения,
                                     выходящие за границы разрешённых, перемещение не будет выполнено.""")
                    dlg.exec_()
            elif axis == "Y":
                shift_val = float(self.shift_y_line.text())
                if not shift_move(self.device_y, shift_val, self.user_unit):
                    dlg = WarnDialog(warn_message="""ОШИБКА! Заданы координаты перемещения,
                                     выходящие за границы разрешённых, перемещение не будет выполнено.""")
                    dlg.exec_()
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
            if self.params_calculator():
                self.begin_measurment_btn.setEnabled(True)
            else:
                self.begin_measurment_btn.setEnabled(False)
        else:
            self.begin_measurment_btn.setEnabled(False)
            
        
    
    def disconnect_powermeter(self):
        if connection_type == 'USB' and self.disconnect_powermeter_btn.isEnabled:
            self.my_instrument.close()
        elif self.disconnect_powermeter_btn.isEnabled:
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
        raise_error = False
        try:
            lab_across = round(int(self.step_across_beam_n.text()) * 
                               float(self.step_across_beam.text()), 2)
            lab_along = round(int(self.step_along_beam_n.text()) * 
                              float(self.step_along_beam.text()) , 2)            
            
            self.label_n_across.setText("Всего {} мм".format(lab_across))
            self.label_n_along.setText("Всего {} мм".format(lab_along))
            
            if not check_edges(self.device_x, self.user_unit, lab_along):
                self.label_n_along.setStyleSheet("color: red;")
                raise_error = True
            else:
                self.label_n_along.setStyleSheet("color: #dedede")
            if not check_edges(self.device_y, self.user_unit, lab_across):
                self.label_n_across.setStyleSheet("color: red;")
                raise_error = True
            else:
                self.label_n_across.setStyleSheet("color: #dedede")
            
            if raise_error:
                raise ValueError
            return True
        except (ValueError, AttributeError):
            return False
        
    
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
    
    def draw_main(self):
        
        self.main_points.setData(self.x_coords_list, self.diameters_list)
        
        try:
            self.main_graph.setYRange(0, max(self.diameters_list) * 1.2)
        except ValueError:
            pass
        
        
        if len(self.diameters_list) >= 4:
            
            if not self.wave_length is None:
                (self.value_M2, 
                 x_coords_list_teor, 
                 diameters_list_teor) = calculator_M2(self.x_coords_list,
                                                      self.diameters_list, 
                                                      (self.wave_length * 10**-9))
                self.main_curve.setData(x_coords_list_teor, diameters_list_teor)
                self.M2_line.setText(str(self.value_M2))
            else:
                self.show_info("Длина волны неизвестна, подсчёт M2 невозможен.")
    
    def draw_coords(self, coords=None):
        if coords is None:
            x_pos, y_pos = map(round, get_coords(self.device_x, 
                                        self.device_y, 
                                        self.user_unit), [4,4])
            self.translator_move_history[0].append(x_pos)
            self.translator_move_history[1].append(y_pos)
        elif coords == "demo":
            self.coords_line.setData(self.translator_move_history[0], 
                                     self.translator_move_history[1])
        else:
            self.translator_move_history[0].append(coords[0])
            self.translator_move_history[1].append(coords[1])
            self.coords_line.setData(self.translator_move_history[0], 
                                     self.translator_move_history[1])
    
    def draw_power(self, start_point, end_point, faster_flag):
        if not faster_flag and not start_point is None and start_point[0] > 10:
            crds_list = self.local_coords_list[start_point[0] - 10:]
            pwr_list = self.power_list[start_point[0] - 10:]
            self.power_line.setData(crds_list, pwr_list)
        else:
            self.power_line.setData(self.local_coords_list, self.power_list)
        
            
    
    
    def draw_gauss(self, start_point, end_point, faster_flag):
        if not end_point is None and not start_point is None:
            if self.default_sigma:
                sigma = self.default_sigma
            else:
                sigma = end_point[1] - start_point[1]
            
            gauss_fit, y = get_gauss_fit(self.local_coords_list, self.power_list, sigma)
        else:
            gauss_fit, y = get_gauss_fit(self.local_coords_list, self.power_list)
        
        if not faster_flag and not start_point is None and start_point[0] > 7:
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
            self.gauss_points.setData(crds_list[:-1], y_list[:-1])
        else:
            self.gauss_curve.setData(crds_list, gauss_list)
            self.gauss_points.setData(crds_list[:-1], y_list[:-1])
        if not end_point is None:
            self.find_diameter(self.local_coords_list, gauss_fit)
        
    def find_diameter(self, x, gauss_fit):
        threshold = float(self.threshold_line.text())
        if not gauss_fit is None: 
            gauss_max = gauss_fit.max()
            threshold_curve = np.full(len(x), gauss_max * threshold)
            
            intersection_list = find_intersection(x, gauss_fit, threshold_curve)        
            if not intersection_list is None:            
                self.intersection_points.setData(*intersection_list)
                if len(intersection_list[0]) == 2:
                    diameter = round(abs(intersection_list[0][1] - intersection_list[0][0]), 4)
                    self.diameter_line.setText(str(diameter))
                    #Проверка на то, что значение диаметра не отличается от предыдущего более чем на 50%
                    if self.diameters_list:
                        if abs(self.diameters_list[-1] - diameter < self.diameters_list[-1] * 0.5):
                            try:
                                self.inner_diameters_list.append(diameter)
                            except AttributeError:
                                print("Нет списка диаметров")
                            self.diameter_edge_array = intersection_list[0]
                    else:
                        self.diameter_edge_array = intersection_list[0]
    
    def change_axes(self):
        self.device_x, self.device_y = self.device_y, self.device_x
        self.show_info("Ось X -> Ось Y\nОсь Y -> Ось X")
    
    
    def execute_measurment(self):
        if not self.results_saved:
            self.save_results()
        
        self.results_saved = False    
        self.raw_res = []        
        self.interrupt_measurment_flag = False
        self.interrupt_btn.setEnabled(True)
        self.begin_measurment_btn.setEnabled(False)
        self.params_setter()
        self.main_points.setData(symbolBrush="#44944A")
        self.clear_graphs()
        self.diameters_list = []
        self.x_coords_list = []
        self.diameter_line.clear()
        self.diameter_edge_array = None
        self.show_info("Начинаем измерение.")
        self.time_file_name = time.strftime("%d.%m.%y %H_%M_%S", time.localtime())
        coords = {"x" : 0, "y" : 0}
        point_number = 1
        set_zero(self.device_x, self.device_y)
                    
        for j in range(self.steps_along):
            self.inner_diameters_list = []
            self.power_list = []
            #Здесь выбор диапазона для range поперёк пучка на основании предыдущего цикла
            if self.faster_flag and j > 0 and self.diameter_edge_array is not None:
                diameter_start_point = self.diameter_edge_array[0] // self.step_across_value
                diameter_end_point = self.diameter_edge_array[1] // self.step_across_value
                range_start_value =  diameter_start_point - 25 if diameter_start_point > 25 else 0
                range_end_value = diameter_end_point + 25 if diameter_end_point + 25 < self.steps_across else self.steps_across
                across_range = range(int(range_start_value), int(range_end_value))
            else:
                range_start_value = None
                across_range = range(self.steps_across)
            
            beam_start_point = None
            beam_end_point = None
            self.local_coords_list = []
            
            for i in across_range:
                
                if self.interrupt_measurment_flag:
                    self.show_info("Измерение прервано")
                    move_to_coords(self.device_x, self.device_y, (0,0), self.user_unit)
                    self.begin_measurment_btn.setEnabled(True)
                    self.interrupt_btn.setEnabled(False)  
                    return
                #Преждевременный выход первые три цикла только после 65% точек
                if not self.faster_flag:                        
                    if not beam_end_point is None and self.diameter_line.text() != "":
                        if i - beam_end_point[0] > 20 and j < 3 and i > (self.steps_across * 0.65):
                            break
                
                self.update()
                QtWidgets.QApplication.processEvents()
                coords["x"] = self.step_along_value * j
                coords["y"] = self.step_across_value * i
                
                move_to_coords(self.device_x, self.device_y, 
                               (coords["x"],coords["y"]), self.user_unit)
                QtCore.QThread.msleep(self.wait_time) 
                
                power_value = None
                while power_value is None:                        
                    power_value = self.get_point()                    
                    if power_value is None:
                        self.show_info("Повторный запрос значения мощности")
                
                self.power_list.append(power_value)
                
                x_pos, y_pos = map(round, get_coords(self.device_x, 
                                            self.device_y, 
                                            self.user_unit), [4,4])
                
                self.local_coords_list.append(y_pos)
                
                if beam_start_point is None and len(self.power_list) > 6:
                    if ((mean(self.power_list[-2:-1]) - mean(self.power_list[-6:-3])) / 
                        mean(self.power_list[-6:-3]) > self.beam_threshold):
                        
                        beam_start_point = (i, y_pos)
                        print(beam_start_point)
                
                elif not beam_start_point is None and beam_end_point is None:
                    if ((mean(self.power_list[-2:-1]) - mean(self.power_list[-6:-3])) / 
                        mean(self.power_list[-6:-3]) < self.beam_threshold 
                        or (self.steps_across - i < 10)):
                        
                        beam_end_point = (i, y_pos)
                        print(beam_end_point)
                
                
                if self.faster_flag and j > 0 and range_start_value is not None:
                    if i > int(range_start_value) + 1:
                        self.draw_gauss(beam_start_point, beam_end_point, self.faster_flag)
                elif i > 3:
                    self.draw_gauss(beam_start_point, beam_end_point, self.faster_flag)
                    
                self.draw_power(beam_start_point, beam_end_point, self.faster_flag)
                self.draw_coords((x_pos, y_pos))
                time_now = time.strftime("%M:%S", time.localtime())
                line = (str(point_number) + "," + time_now + "," + 
                        str(x_pos) + "," + str(y_pos) + 
                        "," + str(power_value)).replace("\r\n", "")
                shw_line = "{:^4}|{:^8}|{:^8.4f}|{:^8.4f}|{:^8.4f}".format(point_number, 
                                                                              time_now, x_pos, 
                                                                              y_pos,float(power_value))
                print(repr(line))
                self.raw_res.append(line + '\r')
                self.show_info(shw_line)
                point_number += 1
            
            if self.diameter_line.text() != "":                    
                if self.inner_diameters_list:
                    self.diameters_list.append(float(self.inner_diameters_list[-1]))
                else:
                    self.diameters_list.append(float(self.diameter_line.text()))
                self.x_coords_list.append(x_pos)
                self.show_info("В точке {:.2f} диаметр пучка составляет {:.4f}".format(x_pos, float(self.diameter_line.text())))
            
            self.diameter_line.clear()
            self.draw_main()
            
            move_to_coords(self.device_x, self.device_y, 
                           ((self.step_along_value) * (j + 1),0), 
                           self.user_unit)
            if j < self.steps_along -1:
                QtCore.QThread.msleep(10000) 
        
        move_to_coords(self.device_x, self.device_y, (0,0), self.user_unit)
        self.begin_measurment_btn.setEnabled(True)
        self.interrupt_btn.setEnabled(False)
        self.show_info("Измерение завершено.")
                
       
    def interrupt_measurment(self):
        self.interrupt_btn.setEnabled(False)
        self.interrupt_measurment_flag = True
        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
    
    def open_record(self):
        user_record = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Results file", '',  
                                                                 'Results files (*.zip);;Any zip files (*.zip)'
                                                                 )
        if user_record[0]:            
            self.show_info(f'Выбран файл {user_record[0]}')            
            self.process_record(user_record)
        else:
            self.show_info("Файл не выбран")
    
    def clear_graphs(self):
        self.main_points.setData([],[])
        self.main_curve.setData([],[])
        self.power_line.setData([],[])
        self.intersection_points.setData([],[])
        self.gauss_curve.setData([],[])
        self.gauss_points.setData([],[])
        self.translator_move_history = [[],[]]
            
    def process_record(self, user_record):
        self.main_points.setData(symbolBrush="#44944A")
        self.clear_graphs()
        self.diameters_list = []
        self.x_coords_list = []
        self.diameter_line.clear()
        self.diameter_edge_array = None
        
        zipObj = ZipFile(user_record[0], 'r')
        self.raw_df, self.main_df = None, None
        for file in zipObj.namelist():
            if 'raw_results' in file.lower():
                self.raw_df = pd.read_csv(zipObj.open(file))
            elif 'results' in file.lower():
                self.main_df = pd.read_csv(zipObj.open(file))
        if self.main_df is None or self.raw_df is None:
            self.show_info(f'Архив {user_record[0]} не содержит файлов результатов')
            return
        
        self.x_coords_list = list(self.main_df['X_pos'][self.main_df['X_pos'].notna()])
        self.diameters_list = list(self.main_df['Diameter'][self.main_df['Diameter'].notna()])
        self.translator_move_history = [self.raw_df['X_pos'],self.raw_df['Y_pos']]
        try:
            self.wave_length = int(self.main_df.iloc[-1]['N'].split('=')[1])
            self.wave_length_line.setText(str(self.wave_length))
        except (ValueError, AttributeError):
            self.wave_length = None
        self.draw_main()
        self.draw_coords('demo')
        
    def print_points_clicked(self, item, points):
        data_list = list(item.getData()[0])
        mypoint = points[0].pos()[0]
        mypoint_index = data_list.index(mypoint)

        symbolBrushs = [None] * len(data_list)
        symbolBrushs[mypoint_index] = pg.mkBrush(color=(255, 0, 0))
        self.main_points.setData(symbolBrush=symbolBrushs)
        
        self.local_coords_list = list(self.raw_df.loc[self.raw_df['X_pos'] == mypoint]['Y_pos'])
        self.power_list = list(self.raw_df.loc[self.raw_df['X_pos'] == mypoint]['Value'])
        
        self.draw_power(None, None, True)
        self.draw_gauss(None, True, True)
        print(points[0].pos())
        self.show_info(str(points[0].pos()))        
        
    
    def save_file(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("zip-files (*.zip)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if dialog.exec_():
            self.file_name = dialog.selectedFiles()[0]
            if not self.results_saved:
                self.show_info(f"Файл для сохранения: {self.file_name}")
                self.save_results()
            else:
                self.show_info(f"Результаты будут сохранены в: {self.file_name}")
            return True
        else:
            self.file_name = None
        
        
    def closeEvent(self, event):
        if self.disconnect_powermeter_btn.isEnabled():
            self.disconnect_powermeter()
        if self.disconnect_translator_btn.isEnabled():
            self.disconnect_translator()
        if not self.results_saved:
            self.save_results()
        event.accept() # let the window close
    
    def test_func(self):
        pass
        
    
    def save_results(self):        
        
        raw_res_file = open(self.folder_name + "/" + self.time_file_name + " raw_results.csv", "w")
        raw_res_file.write("N,Time,X_pos,Y_pos,Value\r")
        
        main_res_file = open(self.folder_name + "/" + self.time_file_name + " results.csv", "w")
        main_res_file.write("N,X_pos,Diameter\r")
        
        for rec in self.raw_res:
            raw_res_file.write(rec)
        
        for rec in range(len(self.diameters_list)):
            main_res_file.write("{},{},{}\r".format(str(rec), 
                                           str(self.x_coords_list[rec]),
                                           str(self.diameters_list[rec])))
        main_res_file.write(f"M_square = {self.value_M2}\r")
        main_res_file.write(f'Wave_length = {self.wave_length}\r')
        
        result_code = 0
        while self.file_name is None and result_code == 0:
            if self.save_file():
                break
            dlg = WarnDialog(warn_message="Результаты не будут сохранены, продолжить?")
            result_code = dlg.exec_()
        if self.file_name is None:
            raw_res_file.close()
            os.remove(raw_res_file.name)
            main_res_file.close()
            os.remove(main_res_file.name)
            self.results_saved = True
            return
        else:
            # create a ZipFile object
            if not self.file_name.endswith('.zip'):
                self.file_name += '.zip'
            zipObj = ZipFile(self.file_name, "w")
            # Add multiple files to the zip
            raw_res_file.close()
            main_res_file.close()
            zipObj.write(raw_res_file.name, arcname=os.path.basename(raw_res_file.name))
            zipObj.write(main_res_file.name,arcname=os.path.basename(main_res_file.name))
            os.remove(raw_res_file.name)
            os.remove(main_res_file.name)
            # close the Zip File
            zipObj.close()
            self.show_info(f"Результаты сохранены в: {self.file_name}")
            self.file_name = None
            self.results_saved = True
        

class WarnDialog(QtWidgets.QDialog, warn_dialog.Ui_Dialog):
    def __init__(self, warn_message):
        super().__init__()
        self.setupUi(self)
        self.label.setText(warn_message)

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