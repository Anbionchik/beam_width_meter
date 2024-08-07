# -*- coding: utf-8 -*-

#Скрипт для работы с подвижкой, типовые комманды в конце, 
# проводить нинициализацию несколько раз не стоит

from ctypes import *
import time
import os
import sys
import platform
import tempfile
import re
import csv
from multiprocessing.pool import ThreadPool

dll_path = "d:\\XIlab\\beam_width_meter\\pyximc_wrapper\\"
if not "d:\\XIlab\\beam_width_meter\\pyximc_wrapper\\" in os.environ["Path"]:
    os.environ["Path"] = dll_path + ";" + os.environ["Path"]

from pyximc_wrapper.pyximc import *

if sys.version_info >= (3,0):
    import urllib.parse

lib.set_bindy_key("pyximc_wrapper/keyfile.sqlite".encode("utf-8")) # Search for the key file in the current directory.

translator_move_history = [[],[]]

def initialize_axes():
    
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


def close_axes(device_id_x, device_id_y):
    lib.close_device(byref(cast(device_id_x, POINTER(c_int))))
    lib.close_device(byref(cast(device_id_y, POINTER(c_int))))
    
def user_calibration(calibration_ratio):
    user_unit = calibration_t()
    user_unit.A = 1 / calibration_ratio
    user_unit.MicrostepMode = True
    return user_unit


def movement_setter(device_id_x, device_id_y, speed, accel, decel):
    mvst = move_settings_t()
    mvst.Speed = speed
    mvst.Accel = accel
    mvst.Decel = decel
    lib.set_move_settings(device_id_x, byref(mvst))
    lib.set_move_settings(device_id_y, byref(mvst))
    
def set_zero(device_id_x, device_id_y):
    lib.command_zero(device_id_x)
    lib.command_zero(device_id_y)
    
def shift_move(device_id, shift, calibration):
    if not check_edges(device_id, calibration, shift):
        return False
    global translator_move_history
    shift = int(shift / calibration.A)
    lib.command_movr(device_id, c_int(shift))
    lib.command_wait_for_stop(device_id, 100)
    return True

def reverse_engine(device_id):
    eng = engine_settings_t()
    result = lib.get_engine_settings(device_id, byref(eng))
    if result == Result.Ok:
        if eng.EngineFlags & EngineFlags.ENGINE_REVERSE:
            eng.EngineFlags = eng.EngineFlags ^ EngineFlags.ENGINE_REVERSE
            result = lib.set_engine_settings(device_id, byref(eng))
            if result == Result.Ok:
                return "Реверс активирован"
            else:
                return 'Установка реверса не выполнена'
        else:
            eng.EngineFlags = eng.EngineFlags | EngineFlags.ENGINE_REVERSE
            result = lib.set_engine_settings(device_id, byref(eng))
            if result == Result.Ok:
                return "Реверс инактивирован"
            else:
                return 'Установка реверса не выполнена'

def test_run(device_id, calibration):
    lib.command_movr_calb(device_id, c_float(2), byref(calibration))
    lib.command_wait_for_stop(device_id, 100)
    lib.command_movr_calb(device_id, c_float(-2), byref(calibration))
    lib.command_wait_for_stop(device_id, 100)
    
def get_coords(device_id_x, device_id_y, user_unit):
    x_pos = get_position_calb_t()
    y_pos = get_position_calb_t()
    lib.get_position_calb(device_id_x, byref(x_pos), user_unit)
    lib.get_position_calb(device_id_y, byref(y_pos), user_unit)
    
    return (x_pos.Position, y_pos.Position)

def check_edges(device_id, user_unit, shift):
    pos = get_position(device_id, user_unit)
    edges = get_edges(device_id, user_unit)
    print(pos, edges[0], edges[1])
    if pos + shift <= edges[0] or pos + shift >= edges[1]:
        return False
    else:
        return True
    
def get_edges(device_id, user_unit):
    "Returns list with calibrated coords of left border and right border"
    edges = edges_settings_calb_t()
    lib.get_edges_settings_calb(device_id, byref(edges), user_unit)
    return [edges.LeftBorder, edges.RightBorder]

def get_position(device_id, user_unit):
    "Returns calibrated position"
    pos = get_position_calb_t()
    lib.get_position_calb(device_id, byref(pos), user_unit)
    return pos.Position

def move_to_coords(device_id_x, device_id_y, coords, user_unit):
    lib.command_move_calb(device_id_x, c_float(float(coords[0])), byref(user_unit))
    lib.command_move_calb(device_id_y, c_float(float(coords[1])), byref(user_unit))
    lib.command_wait_for_stop(device_id_x, 10)
    lib.command_wait_for_stop(device_id_y, 10)
