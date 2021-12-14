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
from translator_controller import initialize_axes, close_axes
from pyximc_wrapper.pyximc import *


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
            self.tcp_socket.close()
        except timeout:
            self.show_info("Не удалось подключиться к измерителю мощности :(")
    def connect_translator(self):
        try:
            self.device_x, self.device_y = initialize_axes()
        except NameError:
            self.show_info("Не удалось подключиться к подвижке")
            return
        self.user_unit = self.user_calibration()
        close_axes(self.device_x, self.device_y)
    
    def initialize_axes(self):
        # This is device search and enumeration with probing. It gives more information about devices.
        probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
        enum_hints = b"addr="
        # enum_hints = b"addr=" # Use this hint string for broadcast enumerate
        devenum = lib.enumerate_devices(probe_flags, enum_hints)
        print("Device enum handle: " + repr(devenum))
        print("Device enum handle type: " + repr(type(devenum)))
        
        dev_count = lib.get_device_count(devenum)
        if dev_count < 2:
            raise NameError("Обнаружено {} устройств".format(dev_count))
        
        print("Device count: " + repr(dev_count))
        
        
        controller_name = controller_name_t()
        for dev_ind in range(0, dev_count):
            enum_name = lib.get_device_name(devenum, dev_ind)
            result = lib.get_enumerate_device_controller_name(devenum, dev_ind, byref(controller_name))
            if result == Result.Ok:
                print("Enumerated device #{} name (port name): ".format(dev_ind) + repr(enum_name) + ". Friendly name: " + repr(controller_name.ControllerName) + ".")
        
        flag_virtual = 0
        
        open_name_x = None
        open_name_y = None
        if len(sys.argv) > 1:
            open_name = sys.argv[1]
        elif dev_count == 2:
            open_name_x = lib.get_device_name(devenum, 0)
            open_name_y = lib.get_device_name(devenum, 1)
        elif sys.version_info >= (3,0):
            # use URI for virtual device when there is new urllib python3 API
            tempdir = tempfile.gettempdir() + "/testdevice.bin"
            if os.altsep:
                tempdir = tempdir.replace(os.sep, os.altsep)
            # urlparse build wrong path if scheme is not file
            uri = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme="file", \
                    netloc=None, path=tempdir, params=None, query=None, fragment=None))
            open_name = re.sub(r'^file', 'xi-emu', uri).encode()
            flag_virtual = 1
            print("The real controller is not found or busy with another app.")
            print("The virtual controller is opened to check the operation of the library.")
            print("If you want to open a real controller, connect it or close the application that uses it.")
        
        if not open_name_x and not open_name_y:
            exit(1)
        
        if type(open_name_x) is str:
            open_name_x = open_name_x.encode()
        if type(open_name_y) is str:
            open_name_y = open_name_y.encode()
        
        print("\nOpen device x" + repr(open_name_x))
        print("\nOpen device y" + repr(open_name_y))
        device_id_x = lib.open_device(open_name_x)
        device_id_y = lib.open_device(open_name_y)
        print("Device id x: " + repr(device_id_x))
        print("Device id y: " + repr(device_id_y))
        
        return (device_id_x, device_id_y)
    
    def user_calibration(self):
        user_unit = calibration_t()
        user_unit.A = 0.0025
        user_unit.MicrostepMode = True
        return user_unit
        
    def params_setter(self):
        self.step_across_value = float(self.step_across_beam.text())
        self.step_along_value = float(self.step_along_beam.text())
        self.info_field.appendPlainText(str(self.step_across_value))
        self.info_field.appendPlainText(str(self.step_along_value))
    def execute_measurment(self):
        self.info_field.appendPlainText("Начинаем измерения")
        
    def show_info(self, message):
        self.info_field.appendPlainText(message)
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = BeamWidthMeterApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()