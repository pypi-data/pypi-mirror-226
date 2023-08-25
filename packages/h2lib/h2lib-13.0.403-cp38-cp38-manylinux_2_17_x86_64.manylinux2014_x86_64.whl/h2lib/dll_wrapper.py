import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes as ct
import _ctypes

import os
import ctypes
from _ctypes import POINTER
from ctypes import c_int, c_double, c_char, c_char_p, c_long
import tempfile
import shutil
try:
    from ctypes import windll
except ImportError:
    pass
import sys
from pathlib import Path
import atexit
c_int_p = POINTER(ctypes.c_long)
c_double_p = POINTER(ctypes.c_double)
in_use = []


class DLLWrapper(object):
    def __init__(self, filename, cdecl=True):
        if filename in in_use:
            self.temp_dir = tempfile.TemporaryDirectory()
            tmp_filename = os.path.join(self.temp_dir.name, os.path.basename(filename))
            shutil.copy(filename, tmp_filename)
            filename = tmp_filename
        else:
            self.temp_dir = None
        in_use.append(filename)
        self.filename = str(filename)
        self.cdecl = cdecl
        self.open()
        atexit.register(self.close)

    @staticmethod
    def find_dll(path, name):
        p = Path(path)

#         if sys.platform == "win32":
#             prefixes = ['']
#             if sys.maxsize > 2**32:
#                 suffixes = ['.dll', '_64.dll']
#             else:
#                 suffixes = ['.dll']
#         elif sys.platform == 'linux':
#             prefixes = ['lib','']
#             suffixes = ['.so']
#         else:
#             raise NotImplementedError()

        dll_lst = []
        file_patterns = ['*%s*.dll' % name, '*%s*.so' % name]
        for fp in file_patterns:
            dll_lst.extend(list(p.glob("**/" + fp)))

        def use_first(dll_lst):
            f = str(dll_lst[0])
            print("Using ", os.path.abspath(f))
            return DLLWrapper(f)

        if len(dll_lst) == 1:
            return use_first(dll_lst)
        elif len(dll_lst) > 1:
            # check if excluding dlls in hawc2-binary, i.e. "hawc2-<platform>" results in one dll
            dll_lst2 = [d for d in dll_lst if not str(d).startswith('hawc2-')]
            if len(dll_lst2) == 1:
                return use_first(dll_lst2)
            raise FileExistsError("Multiple dlls found:\n" + "\n".join([str(p) for p in dll_lst]))
        else:
            raise FileNotFoundError("No " + " or ".join(file_patterns) +
                                    " files found in " + os.path.abspath(p.absolute()))

    def open(self):
        assert os.path.isfile(self.filename), os.path.abspath(self.filename)
        if self.cdecl:
            self.lib = ct.CDLL(self.filename, winmode=ctypes.DEFAULT_MODE)
        else:
            self.lib = windll.LoadLibrary(self.filename)

    def close(self):
        if "FreeLibrary" in dir(_ctypes):
            _ctypes.FreeLibrary(self.lib._handle)
        else:
            _ctypes.dlclose(self.lib._handle)
        atexit.unregister(self.close)
        in_use.remove(self.filename)
        if self.temp_dir:
            self.temp_dir.cleanup()

#     def __enter__(self):
#         self.open()
#         return self
#
#     def __exit__(self, type, value, traceback):
#         self.close()
#         return False

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name == 'lib':
                raise Exception("DLL not loaded. Run using: 'with dll: ...'")
            return self.get_lib_function(name)

    def get_lib_function(self, name):
        try:
            f = getattr(self.lib, name)
        except AttributeError as e:
            raise AttributeError("Attribute '%s' not found in dll ('%s')" % (name, self.filename))

        def wrap(*args, **kwargs):
            c_args = []
            for arg in args:
                if isinstance(arg, int):
                    c_args.append(c_int_p(c_int(arg)))
                elif isinstance(arg, float):
                    c_args.append(c_double_p(c_double(arg)))
                elif isinstance(arg, str):
                    c_args.append(c_char_p(arg.encode('cp1252')))
                    # c_args.append(c_int_p(c_int(len(arg))))

                elif isinstance(arg, np.ndarray):
                    if arg.dtype == int:
                        c_args.append(arg.ctypes.data_as(c_int_p))
                    elif arg.dtype == np.float64:
                        c_args.append(arg.ctypes.data_as(c_double_p))
                    else:
                        raise NotImplementedError(arg.dtype)

                else:
                    # raise NotImplementedError(arg.__class__.__name__)
                    c_args.append(arg)
            if 'restype' in kwargs:
                restype = kwargs['restype']
                if hasattr(restype, 'dtype'):
                    restype = np.ctypeslib.as_ctypes_type(restype)
                f.restype = restype

            res = f(*c_args)
            ret_args = []
            for arg in args:
                c_arg = c_args.pop(0)
                if isinstance(arg, (int, float)):
                    ret_args.append(c_arg.contents.value)
                elif isinstance(arg, (str)):
                    ret_args.append(c_arg.value.decode('cp1252'))
                    # c_args.pop(0)
                elif isinstance(arg, np.ndarray):
                    ret_args.append(arg)
                else:
                    raise NotImplementedError(arg.__class__.__name__)
            return ret_args, res
        return wrap

    def version(self, function_name='get_version'):
        try:
            f = getattr(self.lib, function_name)
            f.argtypes = [c_char_p, c_long]
            s = "".ljust(255)
            arg = c_char_p(s.encode('utf-8'))
            f(arg, len(s))
            return arg.value.decode().strip()
        except AttributeError:
            if function_name == 'get_version':
                return self.version('version')

    def getFileProperties(self):
        if sys.platform != "win32":
            raise OSError("Only supported for Windows")
        import win32api
        fname = self.filename

        # ==============================================================================
        """
        Read all properties of the given file return them as a dictionary.
        """
        propNames = ('Comments', 'InternalName', 'ProductName',
                     'CompanyName', 'LegalCopyright', 'ProductVersion',
                     'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                     'FileVersion', 'OriginalFilename', 'SpecialBuild')

        props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

        try:
            # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
            fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
            props['FixedFileInfo'] = fixedInfo
            props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                    fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                                                    fixedInfo['FileVersionLS'] % 65536)

            # \VarFileInfo\Translation returns list of available (language, codepage)
            # pairs that can be used to retreive string info. We are using only the first pair.
            lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

            # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
            # two are language/codepage pair returned from above

            strInfo = {}
            for propName in propNames:
                strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
                # print str_info
                strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

            props['StringFileInfo'] = strInfo
        except BaseException:
            pass

        return props


class Type2DllWrapper(DLLWrapper):
    def __init__(self, filename, dll_subroutine_init, dll_subroutine_update,
                 arraysizes_init, arraysizes_update,
                 init_array):
        super().__init__(filename)
        self.dll_subroutine_init = dll_subroutine_init
        self.dll_subroutine_update = dll_subroutine_update
        self.arraysizes_init = arraysizes_init
        self.arraysizes_update = arraysizes_update
        self.init_array = init_array

    def open(self):
        DLLWrapper.open(self)
        self.init()

    def call(self, name, array, n1, n2):
        f = getattr(self.lib, name)
        f.argtypes = [ndpointer(shape=n1, dtype=ct.c_double, flags='FORTRAN'),
                      ndpointer(shape=n2, dtype=ct.c_double, flags='FORTRAN')]
        f.restype = None

        pad_array = np.zeros(n1)
        pad_array[:len(array)] = array
        arg1 = np.array(pad_array, dtype=ct.c_double, order='F')
        arg2 = np.zeros(n2, dtype=ct.c_double, order='F')

        f(arg1, arg2)
        return(arg2)

    def init(self):
        n1, n2 = self.arraysizes_init
        return self.call(self.dll_subroutine_init, self.init_array, n1, n2)

    def update(self, array):
        n1, n2 = self.arraysizes_update
        return self.call(self.dll_subroutine_update, array, n1, n2)
