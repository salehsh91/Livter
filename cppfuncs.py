import ctypes
import threading
lib = ctypes.CDLL("./cppmain.dll")
def loadFunction(name,one = [],two = None):
    f = getattr(lib,name)
    f.argtypes = one
    f.restype = two
    
    return f


class draw:

    @classmethod
    def draw(cls,array):
        pass

Init = loadFunction("Init",two = ctypes.c_int)
Quit = loadFunction("Quit",two = ctypes.c_int)
LoadTexture = loadFunction("LoadTexture",one=[ctypes.c_void_p,ctypes.c_uint8,ctypes.c_uint8,ctypes.c_uint8,ctypes.c_uint8,ctypes.c_int])
Render = loadFunction("render",one = [],two = ctypes.c_int)
GetRenderer = loadFunction("GetRENDERER")
GetWindow = loadFunction("GetWINDOW")
DrawObj = loadFunction("drawobj",one=[ctypes.c_void_p,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_int])
pr = loadFunction("pr",one = [ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,],two=None)
GetWinSize = loadFunction("GetWindowsize",one=[ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)])
present = loadFunction("present")
LoadImageTexture = loadFunction("LoadImageTexture",one=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int],two=ctypes.c_bool)
def Pr(arr):
    Arrtype = ctypes.c_int * len(arr)
    arr2 = Arrtype(*arr)

    pr(arr2,len(arr))

def getWinSize():
    width = ctypes.c_int()
    height = ctypes.c_int()

    GetWinSize(
        ctypes.byref(width),
        ctypes.byref(height)
    )

    return width.value, height.value