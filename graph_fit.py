# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:52:07 2021

@author: Anbion
"""
from scipy.optimize import curve_fit
import numpy as np
from shapely.geometry import LineString

def gauss_func(x, a, x0, sigma):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))

def get_diff(x, y):
    
    diff_array = np.zeros(len(y))
    for i in range(len(y)):
        if i == 0:
            diff_array[i] = (y[i+1] - y[i]) / (x[i+1] - x[i])
        elif i == len(y) - 1:
            diff_array[i] = (y[i] - y[i-1]) / (x[i] - x[i-1])
        else:
            diff_array[i] = (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
    
    return diff_array

def get_gauss_fit(x, y, sigma=1):
    y = get_diff(x,y)
    y_max = y.max()
    x_max = x[np.argmax(y)]
    try:
        popt, pcov = curve_fit(gauss_func, x, y, [y_max, x_max, sigma])
    except RuntimeError:
        gauss_fit = None
        return gauss_fit, y
    
    gauss_fit = gauss_func(x, popt[0], popt[1], popt[2])
    
    return gauss_fit, y

def find_intersection(x, y1, y2):
    
    line1 = LineString(np.column_stack((x, y1)))
    line2 = LineString(np.column_stack((x, y2)))

    intersection = line1.intersection(line2)

    if intersection.geom_type == 'MultiPoint':
        return LineString(intersection).xy
    elif intersection.geom_type == 'Point':
        return intersection.xy
    
def quadratic_sqrt(x, a, b, c):
    return np.sqrt(a + b * x + c * x**2)

def calculator_M2(x_array, y_array, wave_length):
    popx, pcov = curve_fit(quadratic_sqrt, x_array, y_array, (1., 0.02, 0.0001), maxfev=10**6)
    a, b, c = popx
    lambdaP = wave_length * 1e3
    M2 = round(np.pi / (8 * lambdaP) * np.sqrt(4 * a * c - b**2), 2)
    
    x_teor = np.linspace(x_array[0], x_array[-1], 1000)
    y_teor = quadratic_sqrt(x_teor, a, b, c)
    
    return M2, x_teor, y_teor
    