import numpy as np
from scipy.signal import firwin, butter, lfilter

def design_fir(cutoff, rate, numtaps=101):
    nyq = 0.5 * rate
    fir_coeff = firwin(numtaps, cutoff / nyq)
    return fir_coeff

def apply_fir(data, coeffs):
    return lfilter(coeffs, 1.0, data)

def design_iir(cutoff, rate, order=10):
    nyq = 0.5 * rate
    b, a = butter(order, cutoff / nyq, btype='low')
    return b, a

def apply_iir(data, b, a):
    return lfilter(b, a, data)
