import numpy as np
from h2lib.dll_wrapper import DLLWrapper
import os

from h2lib.h2lib_signatures import H2LibSignatures
in_use = None


class H2Lib(H2LibSignatures, DLLWrapper):
    def __init__(self, filename=None):
        if filename is None:
            if os.name == 'nt':
                filename = os.path.dirname(__file__) + '/HAWC2Lib.dll'
            else:
                filename = os.path.dirname(__file__) + '/HAWC2Lib.so'

        DLLWrapper.__init__(self, filename, cdecl=True)

    def getState(self):
        return H2LibSignatures.getState(self, restype=np.int32)


if __name__ == '__main__':
    h2lib = H2Lib()
    h2lib.echo_version()
    (s,), res = h2lib.get_version("")
    print("#" + s + "#")
    print(h2lib.getSquare(3., restype=np.float64))
