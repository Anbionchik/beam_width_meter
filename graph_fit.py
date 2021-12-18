# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:52:07 2021

@author: Anbion
"""
from scipy.optimize import curve_fit
import numpy as np

def gauss_func(x, a, x0, sigma):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))

def get_diff(x, y):
    
    diff_array = np.zeros(len(y))
    for i in range(len(y)):
        if i == 0:
            diff_array[i] = y[i+1] - y[i] / x[i+1] - x[i]
        elif i == len(y) - 1:
            diff_array[i] = y[i] - y[i-1] / x[i] - x[i-1]
        else:
            diff_array[i] = y[i+1] - y[i-1] / x[i+1] - x[i-1]
    
    return diff_array

def get_gauss_fit(x, y):
    sigma = 1
    y = get_diff(x,y)
    y_max = y.max()
    x_max = x[np.argmax(y)]
    try:
        popt, pcov = curve_fit(gauss_func, x, y, [y_max, x_max, sigma])
    except RuntimeError:
        return None
    
    gauss_fit = gauss_func(x, popt[0], popt[1], popt[2])
    
    return gauss_fit