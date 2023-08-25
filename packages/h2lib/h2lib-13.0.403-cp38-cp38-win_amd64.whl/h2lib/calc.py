import ctypes
from ctypes import CDLL, cdll, c_double
import os
from h2lib.dll_wrapper import DLLWrapper, c_double_p
import numpy as np


def add(a, b):
    return a + b


def square(a):
    print(os.getcwd())
    f = os.path.abspath('../../../build/TestLib_64.dll')
    dll = DLLWrapper(filename=f, cdecl=True)
    print(dll.sqr2(3))
    print(dll.getSquare(3., restype=np.float64))


if __name__ == '__main__':
    square(3)
